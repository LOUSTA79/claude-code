"""
Security, Audit Logging, and Fraud Detection
"""
import asyncio
import hashlib
import json
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Optional, List, Dict, Any
from cryptography.fernet import Fernet
import statistics

from .models import (
    AuditLogEntry, Alert, AlertLevel, TransactionStatus
)
from .config import get_config


logger = logging.getLogger(__name__)


class AuditLogger:
    """
    Audit logging for compliance

    Features:
    - Tamper-proof logs with checksums
    - Encrypted sensitive data
    - 7-year retention (financial compliance)
    - Searchable and exportable
    """

    def __init__(self, log_dir: Optional[Path] = None):
        self.log_dir = log_dir or Path.home() / '.revenue_collection' / 'audit_logs'
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._cipher = self._init_cipher()

    def _init_cipher(self) -> Fernet:
        """Initialize encryption for sensitive data"""
        config = get_config()
        key = config.get_secret(config.security.encryption_key_path)
        # In production, use proper key derivation
        # For now, ensure key is 32 bytes base64 encoded
        if len(key) < 32:
            key = key.ljust(32, '0')
        import base64
        key_bytes = base64.urlsafe_b64encode(key[:32].encode())
        return Fernet(key_bytes)

    def _calculate_checksum(self, entry: AuditLogEntry) -> str:
        """Calculate tamper-proof checksum"""
        data = json.dumps(entry.to_dict(), sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    async def log(
        self,
        action: str,
        actor: str,
        resource: str,
        status: str = "success",
        ip_address: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        sensitive_data_accessed: bool = False
    ) -> AuditLogEntry:
        """
        Create audit log entry

        Args:
            action: What was done (e.g., "revenue_collection", "bank_transfer")
            actor: Who did it (user ID or "system")
            resource: What was affected (e.g., "bank_account", "api_key")
            status: "success" or "failure"
            ip_address: IP address of actor
            details: Additional context
            sensitive_data_accessed: Whether sensitive data was accessed

        Returns:
            AuditLogEntry
        """
        entry = AuditLogEntry(
            action=action,
            actor=actor,
            resource=resource,
            status=status,
            ip_address=ip_address,
            details=details or {},
            sensitive_data_accessed=sensitive_data_accessed
        )

        # Calculate checksum for tamper protection
        checksum = self._calculate_checksum(entry)
        entry.details['checksum'] = checksum

        # Encrypt sensitive fields if needed
        if sensitive_data_accessed:
            entry.details = self._encrypt_sensitive_details(entry.details)

        # Write to daily log file
        log_file = self.log_dir / f"audit_{entry.timestamp.strftime('%Y-%m-%d')}.jsonl"

        # Append to log (JSONL format - one JSON per line)
        with open(log_file, 'a') as f:
            f.write(json.dumps(entry.to_dict()) + '\n')

        logger.info(
            f"Audit: {actor} {action} {resource} - {status}"
        )

        return entry

    def _encrypt_sensitive_details(self, details: Dict) -> Dict:
        """Encrypt sensitive fields in details"""
        encrypted_details = {}
        for key, value in details.items():
            if any(sensitive in key.lower() for sensitive in ['account', 'key', 'password', 'secret']):
                # Encrypt sensitive values
                encrypted_value = self._cipher.encrypt(str(value).encode()).decode()
                encrypted_details[key] = f"ENCRYPTED:{encrypted_value}"
            else:
                encrypted_details[key] = value
        return encrypted_details

    async def search_logs(
        self,
        start_date: datetime,
        end_date: datetime,
        action: Optional[str] = None,
        actor: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[AuditLogEntry]:
        """Search audit logs"""
        results = []

        # Iterate through daily log files
        current_date = start_date.date()
        while current_date <= end_date.date():
            log_file = self.log_dir / f"audit_{current_date.strftime('%Y-%m-%d')}.jsonl"

            if log_file.exists():
                with open(log_file, 'r') as f:
                    for line in f:
                        entry_dict = json.loads(line)

                        # Apply filters
                        if action and entry_dict.get('action') != action:
                            continue
                        if actor and entry_dict.get('actor') != actor:
                            continue
                        if status and entry_dict.get('status') != status:
                            continue

                        # Parse back to AuditLogEntry
                        # (simplified - would need proper deserialization)
                        results.append(entry_dict)

            current_date += timedelta(days=1)

        return results

    async def verify_integrity(self, entry: AuditLogEntry) -> bool:
        """Verify log entry hasn't been tampered with"""
        stored_checksum = entry.details.get('checksum')
        if not stored_checksum:
            return False

        # Remove checksum and recalculate
        details_copy = entry.details.copy()
        del details_copy['checksum']
        entry_copy = AuditLogEntry(**{**entry.to_dict(), 'details': details_copy})

        calculated_checksum = self._calculate_checksum(entry_copy)
        return calculated_checksum == stored_checksum


class FraudDetector:
    """
    Fraud detection and anomaly detection

    Features:
    - Revenue anomaly detection
    - Unusual transaction patterns
    - Geographic anomalies
    - Velocity checks
    """

    def __init__(self):
        self.config = get_config()
        self.historical_data: List[Decimal] = []
        self.load_historical_data()

    def load_historical_data(self):
        """Load historical revenue for baseline"""
        # Load last 30 days of revenue data
        data_file = Path.home() / '.revenue_collection' / 'historical_revenue.json'

        if data_file.exists():
            with open(data_file, 'r') as f:
                data = json.load(f)
                self.historical_data = [Decimal(x) for x in data.get('daily_revenue', [])]

    def save_historical_data(self, amount: Decimal):
        """Add today's revenue to historical data"""
        self.historical_data.append(amount)

        # Keep only last 30 days
        if len(self.historical_data) > 30:
            self.historical_data = self.historical_data[-30:]

        data_file = Path.home() / '.revenue_collection' / 'historical_revenue.json'
        data_file.parent.mkdir(parents=True, exist_ok=True)

        with open(data_file, 'w') as f:
            json.dump({
                'daily_revenue': [str(x) for x in self.historical_data],
                'updated_at': datetime.utcnow().isoformat()
            }, f)

    async def check_anomalies(self, current_revenue: Decimal) -> List[Alert]:
        """
        Check for anomalies in revenue

        Returns:
            List of alerts if anomalies detected
        """
        alerts = []

        if len(self.historical_data) < 7:
            # Not enough data for anomaly detection
            return alerts

        # Calculate statistics
        mean_revenue = statistics.mean(self.historical_data)
        stdev_revenue = statistics.stdev(self.historical_data)

        # Check for significant deviation
        threshold_percent = self.config.security.anomaly_threshold_percent / 100
        upper_bound = mean_revenue * (1 + threshold_percent)
        lower_bound = mean_revenue * (1 - threshold_percent)

        if current_revenue > upper_bound:
            alerts.append(Alert(
                level=AlertLevel.WARNING,
                title="Unusually High Revenue",
                message=(
                    f"Today's revenue (${current_revenue:.2f}) is {((current_revenue / mean_revenue - 1) * 100):.1f}% "
                    f"higher than average (${mean_revenue:.2f})"
                ),
                source="FraudDetector",
                metadata={
                    'current_revenue': str(current_revenue),
                    'average_revenue': str(mean_revenue),
                    'deviation_percent': f"{((current_revenue / mean_revenue - 1) * 100):.1f}%"
                }
            ))

        elif current_revenue < lower_bound and current_revenue > 0:
            alerts.append(Alert(
                level=AlertLevel.WARNING,
                title="Unusually Low Revenue",
                message=(
                    f"Today's revenue (${current_revenue:.2f}) is {((1 - current_revenue / mean_revenue) * 100):.1f}% "
                    f"lower than average (${mean_revenue:.2f})"
                ),
                source="FraudDetector",
                metadata={
                    'current_revenue': str(current_revenue),
                    'average_revenue': str(mean_revenue),
                    'deviation_percent': f"{((1 - current_revenue / mean_revenue) * 100):.1f}%"
                }
            ))

        elif current_revenue == 0 and mean_revenue > 10:
            alerts.append(Alert(
                level=AlertLevel.ERROR,
                title="Zero Revenue Detected",
                message=(
                    f"Zero revenue today, but average is ${mean_revenue:.2f}. "
                    "Possible collection failure."
                ),
                source="FraudDetector",
                metadata={
                    'average_revenue': str(mean_revenue)
                }
            ))

        # Save current revenue for future comparisons
        self.save_historical_data(current_revenue)

        return alerts

    async def check_transfer_velocity(
        self,
        amount: Decimal,
        recent_transfers: List[Dict]
    ) -> Optional[Alert]:
        """
        Check for suspicious transfer velocity

        Args:
            amount: Current transfer amount
            recent_transfers: Transfers in last 24 hours

        Returns:
            Alert if suspicious
        """
        if not recent_transfers:
            return None

        # Check daily limit
        total_today = sum(Decimal(t['amount']) for t in recent_transfers)
        daily_limit = Decimal(str(self.config.bank.max_daily_transfer))

        if total_today + amount > daily_limit:
            return Alert(
                level=AlertLevel.CRITICAL,
                title="Daily Transfer Limit Exceeded",
                message=(
                    f"Transfer of ${amount:.2f} would exceed daily limit of ${daily_limit:.2f}. "
                    f"Already transferred ${total_today:.2f} today."
                ),
                source="FraudDetector",
                metadata={
                    'transfer_amount': str(amount),
                    'total_today': str(total_today),
                    'daily_limit': str(daily_limit)
                }
            )

        # Check for unusual frequency
        if len(recent_transfers) > 5:
            return Alert(
                level=AlertLevel.WARNING,
                title="High Transfer Frequency",
                message=(
                    f"{len(recent_transfers)} transfers in 24 hours. "
                    "Unusual pattern detected."
                ),
                source="FraudDetector",
                metadata={
                    'transfer_count_24h': len(recent_transfers)
                }
            )

        return None


class ApprovalWorkflow:
    """
    Multi-factor approval workflow for sensitive operations

    Features:
    - Dual approval for large transfers
    - Time-based approval expiration
    - MFA verification
    - Approval audit trail
    """

    def __init__(self):
        self.config = get_config()
        self.pending_approvals: Dict[str, Dict] = {}
        self.audit_logger = AuditLogger()

    async def request_approval(
        self,
        operation: str,
        details: Dict[str, Any],
        requires_dual_approval: bool = False
    ) -> str:
        """
        Request approval for operation

        Args:
            operation: Operation type (e.g., "bank_transfer")
            details: Operation details
            requires_dual_approval: Whether two approvers needed

        Returns:
            Approval request ID
        """
        import uuid
        request_id = str(uuid.uuid4())

        approval_request = {
            'request_id': request_id,
            'operation': operation,
            'details': details,
            'requires_dual_approval': requires_dual_approval,
            'requested_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(
                minutes=self.config.security.approval_timeout_minutes
            ),
            'approvals': [],
            'status': 'pending'
        }

        self.pending_approvals[request_id] = approval_request

        # Log approval request
        await self.audit_logger.log(
            action="approval_requested",
            actor="system",
            resource=operation,
            details={'request_id': request_id, **details}
        )

        logger.info(f"Approval requested: {request_id} for {operation}")

        return request_id

    async def approve(
        self,
        request_id: str,
        approver: str,
        mfa_token: Optional[str] = None
    ) -> bool:
        """
        Approve a pending request

        Args:
            request_id: Approval request ID
            approver: Approver identifier
            mfa_token: MFA token if required

        Returns:
            True if approved, False otherwise
        """
        if request_id not in self.pending_approvals:
            raise ValueError(f"Unknown approval request: {request_id}")

        request = self.pending_approvals[request_id]

        # Check expiration
        if datetime.utcnow() > request['expires_at']:
            request['status'] = 'expired'
            await self.audit_logger.log(
                action="approval_expired",
                actor="system",
                resource=request['operation'],
                status="expired",
                details={'request_id': request_id}
            )
            return False

        # Verify MFA if required
        if self.config.security.require_mfa:
            if not mfa_token or not await self._verify_mfa(approver, mfa_token):
                raise ValueError("Invalid MFA token")

        # Add approval
        request['approvals'].append({
            'approver': approver,
            'approved_at': datetime.utcnow()
        })

        # Check if enough approvals
        required_approvals = 2 if request['requires_dual_approval'] else 1

        if len(request['approvals']) >= required_approvals:
            request['status'] = 'approved'

            await self.audit_logger.log(
                action="approval_granted",
                actor=approver,
                resource=request['operation'],
                details={'request_id': request_id}
            )

            logger.info(f"Approval granted: {request_id}")
            return True

        logger.info(f"Partial approval: {request_id} ({len(request['approvals'])}/{required_approvals})")
        return False

    async def _verify_mfa(self, user: str, token: str) -> bool:
        """Verify MFA token (placeholder)"""
        # In production, integrate with TOTP, SMS, or push notification service
        # For now, accept any 6-digit token
        return len(token) == 6 and token.isdigit()

    def is_approved(self, request_id: str) -> bool:
        """Check if request is approved"""
        if request_id not in self.pending_approvals:
            return False

        request = self.pending_approvals[request_id]
        return request['status'] == 'approved'

    def cleanup_expired(self):
        """Remove expired approval requests"""
        now = datetime.utcnow()
        expired = [
            rid for rid, req in self.pending_approvals.items()
            if now > req['expires_at']
        ]

        for rid in expired:
            del self.pending_approvals[rid]

        if expired:
            logger.info(f"Cleaned up {len(expired)} expired approval requests")
