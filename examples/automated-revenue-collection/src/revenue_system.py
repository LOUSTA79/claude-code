"""
Main Revenue Collection System

Orchestrates daily revenue collection from all platforms
"""
import asyncio
import logging
from decimal import Decimal
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path
import json

from .config import get_config
from .models import (
    DailyCollectionReport, PlatformRevenue, TransactionStatus,
    Alert, AlertLevel
)
from .collectors import CollectorFactory
from .tax_calculator import TaxOptimizer
from .bank_transfer import AutomatedBankTransfer
from .security import AuditLogger, FraudDetector
from .monitoring import AlertManager


logger = logging.getLogger(__name__)


class RevenueCollectionSystem:
    """
    Automated revenue collection from all platforms

    Features:
    - Parallel collection from multiple platforms
    - Error handling and retry logic
    - Tax calculation
    - Bank transfers with approvals
    - Fraud detection
    - Comprehensive audit logging
    - Daily reporting
    """

    def __init__(self):
        self.config = get_config()
        self.tax_optimizer = TaxOptimizer()
        self.bank_transfer = AutomatedBankTransfer()
        self.audit_logger = AuditLogger()
        self.fraud_detector = FraudDetector()
        self.alert_manager = AlertManager()
        self.collectors = {}
        self._initialize_collectors()

    def _initialize_collectors(self):
        """Initialize all enabled platform collectors"""
        for platform_name, platform_config in self.config.platforms.items():
            if platform_config.enabled:
                try:
                    self.collectors[platform_name] = CollectorFactory.create_collector(
                        platform_name
                    )
                    logger.info(f"✅ {platform_config.name} collector initialized")
                except Exception as e:
                    logger.error(f"❌ Failed to initialize {platform_name}: {e}")

    async def daily_collection_cycle(self) -> DailyCollectionReport:
        """
        Run daily collection cycle

        This should be scheduled to run at midnight via cron or cloud scheduler:
        0 0 * * * python -m src.revenue_system collect

        Steps:
        1. Collect revenue from all platforms (parallel)
        2. Aggregate totals
        3. Run fraud detection
        4. Calculate taxes
        5. Execute bank transfer (if approved)
        6. Generate daily report
        7. Send alerts if needed

        Returns:
            DailyCollectionReport with complete results
        """
        logger.info("=" * 60)
        logger.info("🚀 Starting Daily Revenue Collection Cycle")
        logger.info(f"   Time: {datetime.utcnow().isoformat()} UTC")
        logger.info("=" * 60)

        report = DailyCollectionReport()

        try:
            # Log cycle start
            await self.audit_logger.log(
                action="daily_collection_started",
                actor="system",
                resource="revenue_collection"
            )

            # Step 1: Collect from all platforms in parallel
            logger.info("\n📊 Collecting from platforms...")

            collection_tasks = [
                self._collect_from_platform(name, collector)
                for name, collector in self.collectors.items()
            ]

            platform_revenues = await asyncio.gather(*collection_tasks)
            report.platform_revenues = platform_revenues

            # Step 2: Calculate totals
            total_collected = sum(
                r.amount for r in platform_revenues
                if r.status == TransactionStatus.COMPLETED
            )

            report.total_gross = total_collected

            logger.info(f"\n💰 Total Collected: ${total_collected:.2f}")
            logger.info(f"   Successful: {report.successful_platforms}/{len(platform_revenues)}")

            if report.failed_platforms > 0:
                logger.warning(f"   Failed: {report.failed_platforms}")
                for revenue in platform_revenues:
                    if revenue.status == TransactionStatus.FAILED:
                        report.collection_errors.append(
                            f"{revenue.platform_name}: {revenue.error_message}"
                        )

            # Step 3: Fraud detection
            logger.info("\n🔍 Running fraud detection...")

            anomaly_alerts = await self.fraud_detector.check_anomalies(total_collected)

            for alert in anomaly_alerts:
                await self.alert_manager.send_alert(alert)
                logger.warning(f"⚠️ {alert.title}: {alert.message}")

            # Step 4: Calculate taxes
            logger.info("\n📋 Calculating taxes...")

            tax_calculation = self.tax_optimizer.calculate_withholding(total_collected)
            report.tax_calculation = tax_calculation
            report.total_tax = tax_calculation.total_tax
            report.total_net = tax_calculation.net_amount

            logger.info(f"   Gross: ${tax_calculation.gross_amount:.2f}")
            logger.info(f"   Tax: ${tax_calculation.total_tax:.2f} ({tax_calculation.effective_tax_rate:.1f}%)")
            logger.info(f"   Net: ${tax_calculation.net_amount:.2f}")

            # Step 5: Execute bank transfer
            if total_collected > 0:
                logger.info("\n💳 Initiating bank transfer...")

                bank_transfer = await self.bank_transfer.transfer_to_director(
                    amount=tax_calculation.net_amount,
                    tax_withheld=tax_calculation.total_tax,
                    report=[r.to_dict() for r in platform_revenues],
                    description=f"Daily Revenue Collection - {datetime.utcnow().strftime('%Y-%m-%d')}"
                )

                report.bank_transfer = bank_transfer

                if bank_transfer.status == TransactionStatus.COMPLETED:
                    logger.info(f"   ✅ Transfer completed: ${bank_transfer.amount:.2f}")
                elif bank_transfer.status == TransactionStatus.REQUIRES_APPROVAL:
                    logger.warning(f"   ⏳ Transfer pending approval")
                elif bank_transfer.status == TransactionStatus.PENDING:
                    logger.warning(f"   ⏰ Transfer scheduled (outside business hours)")
                else:
                    logger.error(f"   ❌ Transfer failed: {bank_transfer.error_message}")

                    # Send critical alert
                    await self.alert_manager.send_alert(Alert(
                        level=AlertLevel.CRITICAL,
                        title="Bank Transfer Failed",
                        message=f"Failed to transfer ${bank_transfer.amount:.2f}: {bank_transfer.error_message}",
                        source="RevenueCollectionSystem"
                    ))

            # Step 6: Generate report
            logger.info("\n📄 Generating daily report...")

            await self._save_daily_report(report)

            # Log cycle completion
            await self.audit_logger.log(
                action="daily_collection_completed",
                actor="system",
                resource="revenue_collection",
                status="success",
                details={
                    'total_collected': str(total_collected),
                    'total_tax': str(report.total_tax),
                    'total_net': str(report.total_net),
                    'platforms_successful': report.successful_platforms,
                    'platforms_failed': report.failed_platforms
                }
            )

            logger.info("\n" + "=" * 60)
            logger.info("✅ Daily Collection Cycle Completed")
            logger.info("=" * 60)

        except Exception as e:
            logger.error(f"\n❌ Collection cycle failed: {e}")

            # Log failure
            await self.audit_logger.log(
                action="daily_collection_failed",
                actor="system",
                resource="revenue_collection",
                status="failure",
                details={'error': str(e)}
            )

            # Send critical alert
            await self.alert_manager.send_alert(Alert(
                level=AlertLevel.CRITICAL,
                title="Revenue Collection Failed",
                message=f"Daily collection cycle failed: {e}",
                source="RevenueCollectionSystem"
            ))

            raise

        finally:
            # Cleanup
            await self._cleanup()

        return report

    async def _collect_from_platform(
        self,
        platform_name: str,
        collector
    ) -> PlatformRevenue:
        """Collect from a single platform with error handling"""
        try:
            revenue = await collector.collect_revenue()
            return revenue

        except Exception as e:
            logger.error(f"❌ {platform_name} collection error: {e}")

            # Send alert
            await self.alert_manager.send_alert(Alert(
                level=AlertLevel.ERROR,
                title=f"{platform_name} Collection Failed",
                message=str(e),
                source="RevenueCollectionSystem",
                metadata={'platform': platform_name}
            ))

            # Return failed revenue object
            return PlatformRevenue(
                platform_name=platform_name,
                status=TransactionStatus.FAILED,
                error_message=str(e)
            )

    async def _save_daily_report(self, report: DailyCollectionReport):
        """Save daily report to file"""
        reports_dir = Path.home() / '.revenue_collection' / 'reports'
        reports_dir.mkdir(parents=True, exist_ok=True)

        report_file = reports_dir / f"report_{report.date.strftime('%Y-%m-%d')}.json"

        with open(report_file, 'w') as f:
            json.dump(report.to_dict(), f, indent=2)

        logger.info(f"   Report saved: {report_file}")

    async def _cleanup(self):
        """Cleanup resources"""
        # Close all collector sessions
        for collector in self.collectors.values():
            try:
                await collector.close()
            except Exception as e:
                logger.error(f"Error closing collector: {e}")

        # Close bank transfer session
        try:
            await self.bank_transfer.close()
        except Exception as e:
            logger.error(f"Error closing bank transfer: {e}")

    def get_daily_report(self, date: datetime = None) -> Dict:
        """Retrieve daily report for a specific date"""
        if date is None:
            date = datetime.utcnow()

        reports_dir = Path.home() / '.revenue_collection' / 'reports'
        report_file = reports_dir / f"report_{date.strftime('%Y-%m-%d')}.json"

        if not report_file.exists():
            return {'error': f'No report found for {date.strftime("%Y-%m-%d")}'}

        with open(report_file, 'r') as f:
            return json.load(f)

    def get_monthly_summary(self, year: int = None, month: int = None) -> Dict:
        """Get summary for entire month"""
        if year is None:
            year = datetime.utcnow().year
        if month is None:
            month = datetime.utcnow().month

        reports_dir = Path.home() / '.revenue_collection' / 'reports'

        total_gross = Decimal('0')
        total_tax = Decimal('0')
        total_net = Decimal('0')
        days_with_revenue = 0

        # Iterate through all days in month
        from calendar import monthrange
        _, days_in_month = monthrange(year, month)

        for day in range(1, days_in_month + 1):
            date = datetime(year, month, day)
            report_file = reports_dir / f"report_{date.strftime('%Y-%m-%d')}.json"

            if report_file.exists():
                with open(report_file, 'r') as f:
                    report = json.load(f)

                total_gross += Decimal(report['total_gross'])
                total_tax += Decimal(report['total_tax'])
                total_net += Decimal(report['total_net'])
                days_with_revenue += 1

        return {
            'year': year,
            'month': month,
            'total_gross': str(total_gross),
            'total_tax': str(total_tax),
            'total_net': str(total_net),
            'days_with_revenue': days_with_revenue,
            'average_daily_gross': str(total_gross / days_with_revenue) if days_with_revenue > 0 else '0',
            'average_daily_net': str(total_net / days_with_revenue) if days_with_revenue > 0 else '0'
        }


async def main():
    """Main entry point for CLI"""
    import sys

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    if len(sys.argv) < 2:
        print("""
Revenue Collection System

Usage:
    python -m src.revenue_system collect                 - Run daily collection
    python -m src.revenue_system report [date]           - View daily report
    python -m src.revenue_system summary [year] [month]  - View monthly summary
    python -m src.revenue_system test                    - Test configuration

Example:
    python -m src.revenue_system collect
    python -m src.revenue_system report 2024-01-15
    python -m src.revenue_system summary 2024 1
        """)
        sys.exit(1)

    command = sys.argv[1]

    system = RevenueCollectionSystem()

    if command == 'collect':
        # Run collection
        report = await system.daily_collection_cycle()
        print(f"\nCollection complete! Report ID: {report.report_id}")

    elif command == 'report':
        # View report
        if len(sys.argv) > 2:
            date = datetime.fromisoformat(sys.argv[2])
        else:
            date = datetime.utcnow()

        report = system.get_daily_report(date)
        print(json.dumps(report, indent=2))

    elif command == 'summary':
        # Monthly summary
        year = int(sys.argv[2]) if len(sys.argv) > 2 else None
        month = int(sys.argv[3]) if len(sys.argv) > 3 else None

        summary = system.get_monthly_summary(year, month)
        print(json.dumps(summary, indent=2))

    elif command == 'test':
        # Test configuration
        print("Testing configuration...")
        valid, errors = system.config.validate()

        if valid:
            print("✅ Configuration valid")
        else:
            print("❌ Configuration errors:")
            for error in errors:
                print(f"   - {error}")
            sys.exit(1)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
