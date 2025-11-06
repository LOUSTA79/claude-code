"""
Secure Configuration Management for Revenue Collection System
Uses AWS Secrets Manager / HashiCorp Vault for production secrets
"""
import os
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class Environment(Enum):
    """Deployment environment"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class SecurityLevel(Enum):
    """Security level for operations"""
    LOW = "low"  # Read-only operations
    MEDIUM = "medium"  # Collection operations
    HIGH = "high"  # Transfer operations
    CRITICAL = "critical"  # Configuration changes


@dataclass
class PlatformConfig:
    """Configuration for a revenue platform"""
    name: str
    enabled: bool
    api_endpoint: str
    api_version: str
    timeout_seconds: int
    max_retries: int
    rate_limit_per_minute: int
    requires_mfa: bool

    # Secrets (loaded from secure vault)
    api_key_path: str  # Path in secrets manager
    account_id_path: str


@dataclass
class BankConfig:
    """Secure bank account configuration"""
    bank_name: str
    # All sensitive fields stored as paths to secrets manager
    account_number_path: str
    routing_number_path: str
    swift_code_path: str
    requires_dual_approval: bool
    max_daily_transfer: float
    max_single_transfer: float
    allowed_transfer_hours: tuple  # (start_hour, end_hour) in UTC


@dataclass
class SecurityConfig:
    """Security and compliance configuration"""
    require_mfa: bool
    require_approval_for_transfers: bool
    approval_timeout_minutes: int
    max_failed_attempts: int
    session_timeout_minutes: int
    encryption_key_path: str
    audit_log_retention_days: int
    enable_fraud_detection: bool
    anomaly_threshold_percent: float  # Alert if revenue deviates by this %


@dataclass
class TaxConfig:
    """Tax calculation configuration"""
    jurisdiction: str
    federal_tax_rate: float
    state_tax_rate: float
    local_tax_rate: float
    self_employment_tax_rate: float
    quarterly_estimated_tax: bool
    tax_advisor_email: str
    auto_withhold: bool


class Config:
    """
    Main configuration class

    SECURITY: Never hardcode credentials!
    All secrets loaded from AWS Secrets Manager or HashiCorp Vault
    """

    def __init__(self, env: Environment = None):
        self.env = env or self._detect_environment()
        self.secrets_manager = self._init_secrets_manager()

    def _detect_environment(self) -> Environment:
        """Detect current environment"""
        env_str = os.getenv('REVENUE_ENV', 'development').lower()
        return Environment(env_str)

    def _init_secrets_manager(self):
        """Initialize secrets manager based on environment"""
        if self.env == Environment.PRODUCTION:
            # Use AWS Secrets Manager in production
            try:
                import boto3
                return boto3.client('secretsmanager')
            except ImportError:
                raise RuntimeError(
                    "boto3 required for production. Install: pip install boto3"
                )
        else:
            # Use local file-based secrets for dev/staging
            from .secrets import LocalSecretsManager
            return LocalSecretsManager()

    def get_secret(self, secret_path: str) -> str:
        """Securely retrieve secret from secrets manager"""
        if self.env == Environment.PRODUCTION:
            response = self.secrets_manager.get_secret_value(SecretId=secret_path)
            return response['SecretString']
        else:
            return self.secrets_manager.get_secret(secret_path)

    @property
    def platforms(self) -> Dict[str, PlatformConfig]:
        """Platform configurations"""
        return {
            'amazon_kdp': PlatformConfig(
                name='Amazon KDP',
                enabled=True,
                api_endpoint='https://advertising-api.amazon.com',
                api_version='v3',
                timeout_seconds=30,
                max_retries=3,
                rate_limit_per_minute=10,
                requires_mfa=True,
                api_key_path='revenue/amazon_kdp/api_key',
                account_id_path='revenue/amazon_kdp/account_id'
            ),
            'google_play': PlatformConfig(
                name='Google Play Books',
                enabled=True,
                api_endpoint='https://www.googleapis.com/books/v1',
                api_version='v1',
                timeout_seconds=30,
                max_retries=3,
                rate_limit_per_minute=100,
                requires_mfa=True,
                api_key_path='revenue/google_play/api_key',
                account_id_path='revenue/google_play/publisher_id'
            ),
            'apple_books': PlatformConfig(
                name='Apple Books',
                enabled=True,
                api_endpoint='https://api.appstoreconnect.apple.com',
                api_version='v1',
                timeout_seconds=30,
                max_retries=3,
                rate_limit_per_minute=50,
                requires_mfa=True,
                api_key_path='revenue/apple_books/api_key',
                account_id_path='revenue/apple_books/vendor_id'
            ),
            'kobo': PlatformConfig(
                name='Kobo Writing Life',
                enabled=True,
                api_endpoint='https://api.kobo.com',
                api_version='v1',
                timeout_seconds=30,
                max_retries=3,
                rate_limit_per_minute=20,
                requires_mfa=False,
                api_key_path='revenue/kobo/api_key',
                account_id_path='revenue/kobo/account_id'
            ),
            'stripe': PlatformConfig(
                name='Stripe',
                enabled=True,
                api_endpoint='https://api.stripe.com',
                api_version='2023-10-16',
                timeout_seconds=30,
                max_retries=3,
                rate_limit_per_minute=100,
                requires_mfa=True,
                api_key_path='revenue/stripe/secret_key',
                account_id_path='revenue/stripe/account_id'
            ),
            'paypal': PlatformConfig(
                name='PayPal',
                enabled=True,
                api_endpoint='https://api.paypal.com',
                api_version='v2',
                timeout_seconds=30,
                max_retries=3,
                rate_limit_per_minute=50,
                requires_mfa=True,
                api_key_path='revenue/paypal/client_secret',
                account_id_path='revenue/paypal/client_id'
            )
        }

    @property
    def bank(self) -> BankConfig:
        """Bank account configuration"""
        return BankConfig(
            bank_name=os.getenv('BANK_NAME', 'Wells Fargo'),
            account_number_path='revenue/bank/account_number',
            routing_number_path='revenue/bank/routing_number',
            swift_code_path='revenue/bank/swift_code',
            requires_dual_approval=self.env == Environment.PRODUCTION,
            max_daily_transfer=50000.00,  # $50k per day max
            max_single_transfer=10000.00,  # $10k per transfer max
            allowed_transfer_hours=(9, 17)  # 9 AM - 5 PM UTC
        )

    @property
    def security(self) -> SecurityConfig:
        """Security configuration"""
        return SecurityConfig(
            require_mfa=self.env == Environment.PRODUCTION,
            require_approval_for_transfers=self.env == Environment.PRODUCTION,
            approval_timeout_minutes=30,
            max_failed_attempts=3,
            session_timeout_minutes=15,
            encryption_key_path='revenue/encryption/master_key',
            audit_log_retention_days=2555,  # 7 years for financial records
            enable_fraud_detection=True,
            anomaly_threshold_percent=50.0  # Alert if +/- 50% from average
        )

    @property
    def tax(self) -> TaxConfig:
        """Tax configuration"""
        return TaxConfig(
            jurisdiction=os.getenv('TAX_JURISDICTION', 'US-CA'),
            federal_tax_rate=0.24,  # 24% federal
            state_tax_rate=0.093,  # 9.3% CA state
            local_tax_rate=0.01,  # 1% local
            self_employment_tax_rate=0.153,  # 15.3% self-employment
            quarterly_estimated_tax=True,
            tax_advisor_email=os.getenv('TAX_ADVISOR_EMAIL', ''),
            auto_withhold=True
        )

    @property
    def monitoring(self) -> Dict[str, Any]:
        """Monitoring and alerting configuration"""
        return {
            'dashboard_update_interval_seconds': 30,
            'health_check_interval_seconds': 60,
            'alert_email': os.getenv('ALERT_EMAIL', ''),
            'alert_phone': os.getenv('ALERT_PHONE', ''),
            'slack_webhook_path': 'revenue/monitoring/slack_webhook',
            'pagerduty_key_path': 'revenue/monitoring/pagerduty_key',
            'enable_sms_alerts': self.env == Environment.PRODUCTION,
            'enable_email_alerts': True
        }

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate configuration

        Returns:
            (is_valid, list_of_errors)
        """
        errors = []

        # Validate secrets exist
        required_secrets = [
            self.bank.account_number_path,
            self.bank.routing_number_path,
            self.security.encryption_key_path
        ]

        for secret_path in required_secrets:
            try:
                self.get_secret(secret_path)
            except Exception as e:
                errors.append(f"Missing required secret: {secret_path}")

        # Validate environment variables
        if self.env == Environment.PRODUCTION:
            if not os.getenv('ALERT_EMAIL'):
                errors.append("ALERT_EMAIL required in production")
            if not os.getenv('TAX_ADVISOR_EMAIL'):
                errors.append("TAX_ADVISOR_EMAIL required in production")

        # Validate bank limits
        if self.bank.max_single_transfer > self.bank.max_daily_transfer:
            errors.append(
                "max_single_transfer cannot exceed max_daily_transfer"
            )

        # Validate tax rates
        total_tax = (
            self.tax.federal_tax_rate +
            self.tax.state_tax_rate +
            self.tax.local_tax_rate +
            self.tax.self_employment_tax_rate
        )
        if total_tax > 0.99:  # Sanity check
            errors.append(f"Total tax rate too high: {total_tax*100:.1f}%")

        return len(errors) == 0, errors


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get global config instance (singleton)"""
    global _config
    if _config is None:
        _config = Config()
    return _config


def reload_config():
    """Reload configuration (useful for testing)"""
    global _config
    _config = None
    return get_config()
