"""
Data Models for Revenue Collection System
"""
from dataclasses import dataclass, field
from decimal import Decimal
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import uuid4


class Currency(Enum):
    """Supported currencies"""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"
    AUD = "AUD"


class TransactionStatus(Enum):
    """Transaction lifecycle status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REQUIRES_APPROVAL = "requires_approval"
    APPROVED = "approved"
    REJECTED = "rejected"


class TransferMethod(Enum):
    """Bank transfer methods"""
    ACH = "ach"  # Automated Clearing House (US)
    WIRE = "wire"  # Wire transfer
    SEPA = "sepa"  # Single Euro Payments Area (EU)
    FASTER_PAYMENTS = "faster_payments"  # UK
    SWIFT = "swift"  # International


class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class PlatformRevenue:
    """Revenue collected from a single platform"""
    transaction_id: str = field(default_factory=lambda: str(uuid4()))
    platform_name: str = ""
    amount: Decimal = Decimal('0.00')
    currency: Currency = Currency.USD
    transaction_count: int = 0
    collection_timestamp: datetime = field(default_factory=datetime.utcnow)
    status: TransactionStatus = TransactionStatus.PENDING
    platform_transaction_id: Optional[str] = None
    breakdown: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'transaction_id': self.transaction_id,
            'platform_name': self.platform_name,
            'amount': str(self.amount),
            'currency': self.currency.value,
            'transaction_count': self.transaction_count,
            'collection_timestamp': self.collection_timestamp.isoformat(),
            'status': self.status.value,
            'platform_transaction_id': self.platform_transaction_id,
            'breakdown': self.breakdown,
            'error_message': self.error_message
        }


@dataclass
class TaxCalculation:
    """Tax calculation breakdown"""
    gross_amount: Decimal
    federal_tax: Decimal
    state_tax: Decimal
    local_tax: Decimal
    self_employment_tax: Decimal
    total_tax: Decimal
    net_amount: Decimal
    jurisdiction: str
    calculation_timestamp: datetime = field(default_factory=datetime.utcnow)
    quarterly_estimated_payment: Optional[Decimal] = None

    @property
    def effective_tax_rate(self) -> Decimal:
        """Calculate effective tax rate"""
        if self.gross_amount == 0:
            return Decimal('0')
        return (self.total_tax / self.gross_amount) * 100

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'gross_amount': str(self.gross_amount),
            'federal_tax': str(self.federal_tax),
            'state_tax': str(self.state_tax),
            'local_tax': str(self.local_tax),
            'self_employment_tax': str(self.self_employment_tax),
            'total_tax': str(self.total_tax),
            'net_amount': str(self.net_amount),
            'effective_tax_rate': f"{self.effective_tax_rate:.2f}%",
            'jurisdiction': self.jurisdiction,
            'calculation_timestamp': self.calculation_timestamp.isoformat()
        }


@dataclass
class BankTransfer:
    """Bank transfer record"""
    transfer_id: str = field(default_factory=lambda: str(uuid4()))
    amount: Decimal = Decimal('0.00')
    currency: Currency = Currency.USD
    method: TransferMethod = TransferMethod.ACH
    status: TransactionStatus = TransactionStatus.PENDING
    initiated_timestamp: datetime = field(default_factory=datetime.utcnow)
    completed_timestamp: Optional[datetime] = None
    bank_transaction_id: Optional[str] = None
    recipient_account_last4: str = ""
    description: str = ""
    tax_withheld: Decimal = Decimal('0.00')
    requires_approval: bool = False
    approved_by: Optional[str] = None
    approved_timestamp: Optional[datetime] = None
    error_message: Optional[str] = None
    retry_count: int = 0

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'transfer_id': self.transfer_id,
            'amount': str(self.amount),
            'currency': self.currency.value,
            'method': self.method.value,
            'status': self.status.value,
            'initiated_timestamp': self.initiated_timestamp.isoformat(),
            'completed_timestamp': self.completed_timestamp.isoformat() if self.completed_timestamp else None,
            'bank_transaction_id': self.bank_transaction_id,
            'recipient_account_last4': self.recipient_account_last4,
            'description': self.description,
            'tax_withheld': str(self.tax_withheld),
            'requires_approval': self.requires_approval,
            'approved_by': self.approved_by,
            'approved_timestamp': self.approved_timestamp.isoformat() if self.approved_timestamp else None,
            'error_message': self.error_message,
            'retry_count': self.retry_count
        }


@dataclass
class DailyCollectionReport:
    """Daily revenue collection report"""
    report_id: str = field(default_factory=lambda: str(uuid4()))
    date: datetime = field(default_factory=lambda: datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0))
    total_gross: Decimal = Decimal('0.00')
    total_tax: Decimal = Decimal('0.00')
    total_net: Decimal = Decimal('0.00')
    platform_revenues: List[PlatformRevenue] = field(default_factory=list)
    tax_calculation: Optional[TaxCalculation] = None
    bank_transfer: Optional[BankTransfer] = None
    collection_errors: List[str] = field(default_factory=list)
    generated_timestamp: datetime = field(default_factory=datetime.utcnow)

    @property
    def total_transactions(self) -> int:
        """Total number of transactions"""
        return sum(r.transaction_count for r in self.platform_revenues)

    @property
    def successful_platforms(self) -> int:
        """Number of platforms with successful collection"""
        return sum(
            1 for r in self.platform_revenues
            if r.status == TransactionStatus.COMPLETED
        )

    @property
    def failed_platforms(self) -> int:
        """Number of platforms with failed collection"""
        return sum(
            1 for r in self.platform_revenues
            if r.status == TransactionStatus.FAILED
        )

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'report_id': self.report_id,
            'date': self.date.isoformat(),
            'total_gross': str(self.total_gross),
            'total_tax': str(self.total_tax),
            'total_net': str(self.total_net),
            'total_transactions': self.total_transactions,
            'successful_platforms': self.successful_platforms,
            'failed_platforms': self.failed_platforms,
            'platform_revenues': [r.to_dict() for r in self.platform_revenues],
            'tax_calculation': self.tax_calculation.to_dict() if self.tax_calculation else None,
            'bank_transfer': self.bank_transfer.to_dict() if self.bank_transfer else None,
            'collection_errors': self.collection_errors,
            'generated_timestamp': self.generated_timestamp.isoformat()
        }


@dataclass
class Alert:
    """System alert"""
    alert_id: str = field(default_factory=lambda: str(uuid4()))
    level: AlertLevel = AlertLevel.INFO
    title: str = ""
    message: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    source: str = ""
    resolved: bool = False
    resolved_timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'alert_id': self.alert_id,
            'level': self.level.value,
            'title': self.title,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'source': self.source,
            'resolved': self.resolved,
            'resolved_timestamp': self.resolved_timestamp.isoformat() if self.resolved_timestamp else None,
            'metadata': self.metadata
        }


@dataclass
class AuditLogEntry:
    """Audit log entry for compliance"""
    entry_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    action: str = ""
    actor: str = ""  # User or system that performed action
    resource: str = ""  # What was affected
    status: str = ""  # success/failure
    ip_address: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
    sensitive_data_accessed: bool = False

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'entry_id': self.entry_id,
            'timestamp': self.timestamp.isoformat(),
            'action': self.action,
            'actor': self.actor,
            'resource': self.resource,
            'status': self.status,
            'ip_address': self.ip_address,
            'details': self.details,
            'sensitive_data_accessed': self.sensitive_data_accessed
        }


@dataclass
class SystemHealth:
    """System health status"""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    overall_status: str = "HEALTHY"  # HEALTHY, DEGRADED, CRITICAL
    cpu_usage_percent: float = 0.0
    memory_usage_percent: float = 0.0
    disk_usage_percent: float = 0.0
    active_connections: int = 0
    failed_transactions_last_hour: int = 0
    average_response_time_ms: float = 0.0
    uptime_seconds: int = 0

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'overall_status': self.overall_status,
            'cpu_usage_percent': self.cpu_usage_percent,
            'memory_usage_percent': self.memory_usage_percent,
            'disk_usage_percent': self.disk_usage_percent,
            'active_connections': self.active_connections,
            'failed_transactions_last_hour': self.failed_transactions_last_hour,
            'average_response_time_ms': self.average_response_time_ms,
            'uptime_seconds': self.uptime_seconds
        }
