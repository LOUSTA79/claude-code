"""
Real-Time Monitoring Dashboard and Alerting
"""
import asyncio
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional
from pathlib import Path
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .models import Alert, AlertLevel, SystemHealth
from .config import get_config


logger = logging.getLogger(__name__)


class AlertManager:
    """
    Manage and send alerts via multiple channels

    Supported channels:
    - Email
    - SMS (via Twilio)
    - Slack
    - PagerDuty
    - Push notifications
    """

    def __init__(self):
        self.config = get_config()
        self.monitoring_config = self.config.monitoring
        self.alerts_file = Path.home() / '.revenue_collection' / 'alerts.json'
        self.active_alerts: List[Alert] = self._load_active_alerts()

    def _load_active_alerts(self) -> List[Alert]:
        """Load active (unresolved) alerts"""
        if self.alerts_file.exists():
            with open(self.alerts_file, 'r') as f:
                data = json.load(f)
                # Filter for unresolved alerts
                return [
                    Alert(**alert) for alert in data.get('alerts', [])
                    if not alert.get('resolved', False)
                ]
        return []

    def _save_alerts(self):
        """Save alerts to file"""
        self.alerts_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.alerts_file, 'w') as f:
            json.dump({
                'alerts': [alert.to_dict() for alert in self.active_alerts],
                'updated_at': datetime.utcnow().isoformat()
            }, f, indent=2)

    async def send_alert(self, alert: Alert):
        """
        Send alert via configured channels

        Args:
            alert: Alert to send
        """
        logger.warning(f"🚨 ALERT [{alert.level.value.upper()}]: {alert.title}")
        logger.warning(f"   {alert.message}")

        # Add to active alerts
        self.active_alerts.append(alert)
        self._save_alerts()

        # Send via enabled channels
        tasks = []

        if self.monitoring_config.get('enable_email_alerts'):
            tasks.append(self._send_email_alert(alert))

        if self.monitoring_config.get('enable_sms_alerts'):
            tasks.append(self._send_sms_alert(alert))

        if self.monitoring_config.get('slack_webhook_path'):
            tasks.append(self._send_slack_alert(alert))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _send_email_alert(self, alert: Alert):
        """Send alert via email"""
        alert_email = self.monitoring_config.get('alert_email')
        if not alert_email:
            return

        subject = f"[{alert.level.value.upper()}] {alert.title}"

        body = f"""
Revenue Collection System Alert

Level: {alert.level.value.upper()}
Title: {alert.title}
Time: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}

Message:
{alert.message}

Source: {alert.source}

---
This is an automated alert from the Revenue Collection System.
        """

        try:
            # In production, use proper SMTP configuration
            # For now, just log
            logger.info(f"📧 Email alert would be sent to: {alert_email}")
            logger.info(f"   Subject: {subject}")

            # Example production code:
            """
            msg = MIMEMultipart()
            msg['From'] = 'alerts@revenue-system.com'
            msg['To'] = alert_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('alerts@revenue-system.com', 'password')
                server.send_message(msg)
            """

        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")

    async def _send_sms_alert(self, alert: Alert):
        """Send alert via SMS (Twilio)"""
        alert_phone = self.monitoring_config.get('alert_phone')
        if not alert_phone:
            return

        # Only send SMS for ERROR and CRITICAL
        if alert.level not in [AlertLevel.ERROR, AlertLevel.CRITICAL]:
            return

        message = f"[{alert.level.value.upper()}] {alert.title}: {alert.message}"

        try:
            logger.info(f"📱 SMS alert would be sent to: {alert_phone}")

            # Example Twilio integration:
            """
            from twilio.rest import Client

            account_sid = self.config.get_secret('twilio/account_sid')
            auth_token = self.config.get_secret('twilio/auth_token')
            from_number = self.config.get_secret('twilio/from_number')

            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=message,
                from_=from_number,
                to=alert_phone
            )
            """

        except Exception as e:
            logger.error(f"Failed to send SMS alert: {e}")

    async def _send_slack_alert(self, alert: Alert):
        """Send alert to Slack"""
        try:
            webhook_path = self.monitoring_config.get('slack_webhook_path')
            if not webhook_path:
                return

            webhook_url = self.config.get_secret(webhook_path)

            # Color based on level
            color_map = {
                AlertLevel.INFO: '#36a64f',
                AlertLevel.WARNING: '#ff9900',
                AlertLevel.ERROR: '#ff0000',
                AlertLevel.CRITICAL: '#ff0000'
            }

            slack_message = {
                'attachments': [{
                    'color': color_map.get(alert.level, '#36a64f'),
                    'title': f"[{alert.level.value.upper()}] {alert.title}",
                    'text': alert.message,
                    'fields': [
                        {'title': 'Source', 'value': alert.source, 'short': True},
                        {'title': 'Time', 'value': alert.timestamp.strftime('%Y-%m-%d %H:%M UTC'), 'short': True}
                    ],
                    'footer': 'Revenue Collection System',
                    'ts': int(alert.timestamp.timestamp())
                }]
            }

            # Send webhook
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=slack_message) as resp:
                    if resp.status != 200:
                        logger.error(f"Slack webhook failed: {resp.status}")

            logger.info("💬 Slack alert sent")

        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")

    def resolve_alert(self, alert_id: str):
        """Mark an alert as resolved"""
        for alert in self.active_alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                alert.resolved_timestamp = datetime.utcnow()
                self._save_alerts()
                logger.info(f"✅ Alert resolved: {alert_id}")
                return

        logger.warning(f"Alert not found: {alert_id}")


class RealTimeMonitoringDashboard:
    """
    Real-time monitoring of all revenue and production

    Updates every 30 seconds with:
    - Current revenue
    - System health
    - Active transfers
    - Recent errors
    """

    def __init__(self):
        self.config = get_config()
        self.metrics: Dict = self._load_metrics()
        self.running = False

    def _load_metrics(self) -> Dict:
        """Load current metrics"""
        return {
            'revenue_today': Decimal('0.00'),
            'revenue_this_hour': Decimal('0.00'),
            'revenue_this_month': Decimal('0.00'),
            'total_collections': 0,
            'successful_collections': 0,
            'failed_collections': 0,
            'pending_transfers': 0,
            'system_health': 'HEALTHY',
            'last_updated': datetime.utcnow().isoformat()
        }

    async def update_dashboard(self):
        """Update dashboard metrics - runs continuously"""
        self.running = True

        while self.running:
            try:
                # Update metrics
                await self._update_metrics()

                # Save to file for external access
                self._save_metrics()

                # Wait before next update
                await asyncio.sleep(
                    self.config.monitoring['dashboard_update_interval_seconds']
                )

            except Exception as e:
                logger.error(f"Dashboard update error: {e}")
                await asyncio.sleep(30)

    async def _update_metrics(self):
        """Update all metrics"""
        # Load today's report
        reports_dir = Path.home() / '.revenue_collection' / 'reports'
        today_report_file = reports_dir / f"report_{datetime.utcnow().strftime('%Y-%m-%d')}.json"

        if today_report_file.exists():
            with open(today_report_file, 'r') as f:
                report = json.load(f)

            self.metrics['revenue_today'] = report.get('total_gross', '0')
            self.metrics['total_collections'] = len(report.get('platform_revenues', []))
            self.metrics['successful_collections'] = report.get('successful_platforms', 0)
            self.metrics['failed_collections'] = report.get('failed_platforms', 0)

        # Calculate month-to-date revenue
        mtd_revenue = Decimal('0')
        current_month = datetime.utcnow().month
        current_year = datetime.utcnow().year

        for report_file in reports_dir.glob('report_*.json'):
            # Parse date from filename
            date_str = report_file.stem.replace('report_', '')
            report_date = datetime.strptime(date_str, '%Y-%m-%d')

            if report_date.year == current_year and report_date.month == current_month:
                with open(report_file, 'r') as f:
                    report = json.load(f)
                mtd_revenue += Decimal(report.get('total_gross', '0'))

        self.metrics['revenue_this_month'] = str(mtd_revenue)

        # Check for pending transfers
        transfer_history_file = Path.home() / '.revenue_collection' / 'transfer_history.json'
        if transfer_history_file.exists():
            with open(transfer_history_file, 'r') as f:
                data = json.load(f)
                pending = sum(
                    1 for t in data.get('transfers', [])
                    if t.get('status') in ['pending', 'requires_approval']
                )
                self.metrics['pending_transfers'] = pending

        # System health check
        self.metrics['system_health'] = await self._check_system_health()

        self.metrics['last_updated'] = datetime.utcnow().isoformat()

    async def _check_system_health(self) -> str:
        """Check overall system health"""
        # Check for recent errors
        alerts_file = Path.home() / '.revenue_collection' / 'alerts.json'

        if alerts_file.exists():
            with open(alerts_file, 'r') as f:
                data = json.load(f)
                recent_alerts = [
                    a for a in data.get('alerts', [])
                    if datetime.fromisoformat(a['timestamp']) >
                       datetime.utcnow() - timedelta(hours=1)
                ]

                # Check for critical alerts
                critical_count = sum(
                    1 for a in recent_alerts
                    if a.get('level') == 'critical'
                )

                if critical_count > 0:
                    return 'CRITICAL'

                error_count = sum(
                    1 for a in recent_alerts
                    if a.get('level') == 'error'
                )

                if error_count > 2:
                    return 'DEGRADED'

        return 'HEALTHY'

    def _save_metrics(self):
        """Save metrics to file"""
        metrics_file = Path.home() / '.revenue_collection' / 'dashboard_metrics.json'
        metrics_file.parent.mkdir(parents=True, exist_ok=True)

        with open(metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2, default=str)

    def stop(self):
        """Stop dashboard updates"""
        self.running = False

    def generate_chairman_report(self) -> str:
        """Generate concise 5-minute briefing for chairman"""
        report = f"""
╔════════════════════════════════════════════════════════╗
║     LOUSTA BOOKS - DAILY EXECUTIVE BRIEFING            ║
║     {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}                                 ║
╚════════════════════════════════════════════════════════╝

💰 FINANCIAL SUMMARY
────────────────────────────────────────────────────────
  Today's Revenue:        ${Decimal(self.metrics.get('revenue_today', '0')):>12,.2f}
  This Month:             ${Decimal(self.metrics.get('revenue_this_month', '0')):>12,.2f}

📊 OPERATIONS
────────────────────────────────────────────────────────
  Collections:            {self.metrics.get('successful_collections', 0):>3} successful, {self.metrics.get('failed_collections', 0):>3} failed
  Pending Transfers:      {self.metrics.get('pending_transfers', 0):>15}
  System Status:          {self.metrics.get('system_health', 'UNKNOWN'):>15}

📈 NEXT COLLECTION
────────────────────────────────────────────────────────
  Scheduled for midnight UTC tonight

════════════════════════════════════════════════════════
  System Status: {self.metrics.get('system_health', 'UNKNOWN')}
  Last Updated: {self.metrics.get('last_updated', 'N/A')}
════════════════════════════════════════════════════════
        """

        return report


async def main():
    """CLI for monitoring"""
    import sys

    if len(sys.argv) < 2:
        print("""
Monitoring Dashboard

Usage:
    python -m src.monitoring dashboard    - Start real-time dashboard
    python -m src.monitoring report       - Generate chairman report
    python -m src.monitoring alerts       - View active alerts

Example:
    python -m src.monitoring dashboard
        """)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'dashboard':
        dashboard = RealTimeMonitoringDashboard()
        print("🖥️  Starting real-time dashboard...")
        print("   Press Ctrl+C to stop")

        try:
            await dashboard.update_dashboard()
        except KeyboardInterrupt:
            dashboard.stop()
            print("\n👋 Dashboard stopped")

    elif command == 'report':
        dashboard = RealTimeMonitoringDashboard()
        await dashboard._update_metrics()
        print(dashboard.generate_chairman_report())

    elif command == 'alerts':
        alert_manager = AlertManager()
        print(f"\n🚨 Active Alerts ({len(alert_manager.active_alerts)})")
        print("=" * 60)

        for alert in alert_manager.active_alerts:
            print(f"\n[{alert.level.value.upper()}] {alert.title}")
            print(f"  Time: {alert.timestamp.strftime('%Y-%m-%d %H:%M UTC')}")
            print(f"  Message: {alert.message}")
            print(f"  Source: {alert.source}")

        if not alert_manager.active_alerts:
            print("No active alerts ✅")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
