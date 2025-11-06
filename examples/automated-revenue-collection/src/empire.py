"""
LOUSTA BOOKS EMPIRE - Complete Automated Publishing System

Combines:
1. Book Production (generate & publish)
2. Revenue Collection (collect earnings)
3. Financial Management (taxes & transfers)
4. Monitoring & Reporting

This is the "one-click empire" - fully automated book publishing business
"""
import asyncio
import logging
from typing import Dict, List
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
import json

from .book_production import BookProductionSystem, RealAccountSetup
from .revenue_system import RevenueCollectionSystem
from .monitoring import RealTimeMonitoringDashboard, AlertManager
from .models import Alert, AlertLevel


logger = logging.getLogger(__name__)


class LoustaEmpire:
    """
    Complete automated publishing empire

    Features:
    - Automated book generation and publishing
    - Daily revenue collection from all platforms
    - Tax calculation and bank transfers
    - Real-time monitoring and alerts
    - Performance tracking and optimization
    """

    def __init__(self):
        self.production = BookProductionSystem()
        self.revenue = RevenueCollectionSystem()
        self.monitoring = RealTimeMonitoringDashboard()
        self.alert_manager = AlertManager()
        self.empire_data = self._load_empire_data()

    def _load_empire_data(self) -> Dict:
        """Load empire state"""
        data_file = Path.home() / '.revenue_collection' / 'empire_state.json'

        if data_file.exists():
            with open(data_file, 'r') as f:
                return json.load(f)

        return {
            'books_published': 0,
            'total_investment': 0.0,
            'total_revenue': 0.0,
            'active_books': [],
            'created_at': datetime.utcnow().isoformat()
        }

    def _save_empire_data(self):
        """Save empire state"""
        data_file = Path.home() / '.revenue_collection' / 'empire_state.json'
        data_file.parent.mkdir(parents=True, exist_ok=True)

        with open(data_file, 'w') as f:
            json.dump(self.empire_data, f, indent=2)

    async def check_readiness(self) -> tuple[bool, List[str]]:
        """
        Check if empire is ready to launch

        Returns:
            (is_ready, list_of_issues)
        """
        logger.info("🔍 Checking Empire Readiness...")

        issues = []

        # Check production requirements
        setup = RealAccountSetup()
        prod_ready, prod_missing = setup.check_requirements()

        if not prod_ready:
            issues.extend([f"Production: {item}" for item in prod_missing])

        # Check revenue collection config
        try:
            valid, config_errors = self.revenue.config.validate()
            if not valid:
                issues.extend([f"Revenue Config: {err}" for err in config_errors])
        except Exception as e:
            issues.append(f"Revenue System: {e}")

        is_ready = len(issues) == 0

        if is_ready:
            logger.info("✅ Empire is ready to launch!")
        else:
            logger.error("❌ Empire not ready:")
            for issue in issues:
                logger.error(f"   - {issue}")

        return is_ready, issues

    async def produce_and_publish_book(
        self,
        topic: str,
        genre: str
    ) -> Dict:
        """
        Produce and publish a single book

        Args:
            topic: Book topic
            genre: Book genre

        Returns:
            Production result
        """
        logger.info("\n" + "=" * 60)
        logger.info("📚 PRODUCING NEW BOOK")
        logger.info("=" * 60)

        # Produce book
        result = await self.production.produce_book(topic, genre)

        # Update empire state
        self.empire_data['books_published'] += 1
        self.empire_data['total_investment'] += result['costs']['total']
        self.empire_data['active_books'].append({
            'asin': result['publication']['asin'],
            'title': result['book']['title'],
            'topic': topic,
            'genre': genre,
            'published_at': datetime.utcnow().isoformat(),
            'cost': result['costs']['total'],
            'projected_monthly_revenue': result['projections']['monthly_revenue']
        })
        self._save_empire_data()

        # Send success alert
        await self.alert_manager.send_alert(Alert(
            level=AlertLevel.INFO,
            title="New Book Published",
            message=f"'{result['book']['title']}' published successfully. ASIN: {result['publication']['asin']}",
            source="LoustaEmpire"
        ))

        return result

    async def daily_empire_cycle(self):
        """
        Daily empire operations

        Run at midnight:
        1. Collect revenue from all books
        2. Calculate taxes
        3. Transfer to bank
        4. Generate reports
        5. Check for optimization opportunities
        """
        logger.info("\n" + "=" * 60)
        logger.info("🌅 DAILY EMPIRE CYCLE")
        logger.info(f"   {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
        logger.info("=" * 60)

        # Step 1: Revenue collection
        logger.info("\n💰 Step 1: Revenue Collection")
        report = await self.revenue.daily_collection_cycle()

        # Update empire revenue
        self.empire_data['total_revenue'] += float(report.total_net)
        self._save_empire_data()

        # Step 2: Performance analysis
        logger.info("\n📊 Step 2: Performance Analysis")
        analysis = await self._analyze_performance()

        # Step 3: Optimization recommendations
        logger.info("\n🎯 Step 3: Optimization Recommendations")
        recommendations = await self._generate_recommendations(analysis)

        # Step 4: Generate empire report
        logger.info("\n📄 Step 4: Empire Report")
        empire_report = await self._generate_empire_report(report, analysis, recommendations)

        logger.info("\n" + "=" * 60)
        logger.info("✅ DAILY EMPIRE CYCLE COMPLETE")
        logger.info("=" * 60)

        return empire_report

    async def _analyze_performance(self) -> Dict:
        """Analyze empire performance"""
        books = self.empire_data['active_books']
        total_investment = Decimal(str(self.empire_data['total_investment']))
        total_revenue = Decimal(str(self.empire_data['total_revenue']))

        if total_investment > 0:
            roi = ((total_revenue / total_investment) - 1) * 100
        else:
            roi = Decimal('0')

        # Calculate revenue per book
        if len(books) > 0:
            revenue_per_book = total_revenue / len(books)
        else:
            revenue_per_book = Decimal('0')

        analysis = {
            'books_published': len(books),
            'total_investment': float(total_investment),
            'total_revenue': float(total_revenue),
            'total_profit': float(total_revenue - total_investment),
            'roi_percent': float(roi),
            'revenue_per_book': float(revenue_per_book),
            'avg_cost_per_book': float(total_investment / len(books)) if books else 0
        }

        logger.info(f"   Books: {analysis['books_published']}")
        logger.info(f"   Investment: ${analysis['total_investment']:,.2f}")
        logger.info(f"   Revenue: ${analysis['total_revenue']:,.2f}")
        logger.info(f"   Profit: ${analysis['total_profit']:,.2f}")
        logger.info(f"   ROI: {analysis['roi_percent']:.1f}%")

        return analysis

    async def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []

        # Check ROI
        if analysis['roi_percent'] < 0:
            recommendations.append(
                "⚠️ Negative ROI - Consider quality improvements or different niches"
            )
        elif analysis['roi_percent'] < 50:
            recommendations.append(
                "📈 Low ROI - Focus on better-performing genres and topics"
            )

        # Check book count
        if analysis['books_published'] < 10:
            recommendations.append(
                "📚 Scale up - More books = more consistent revenue"
            )

        # Check revenue per book
        if analysis['revenue_per_book'] < 20:
            recommendations.append(
                "💡 Improve marketing - Revenue per book is below target"
            )

        if not recommendations:
            recommendations.append("✅ Empire performing well - maintain current strategy")

        for rec in recommendations:
            logger.info(f"   {rec}")

        return recommendations

    async def _generate_empire_report(
        self,
        revenue_report,
        analysis: Dict,
        recommendations: List[str]
    ) -> Dict:
        """Generate comprehensive empire report"""
        report = {
            'date': datetime.utcnow().isoformat(),
            'empire': {
                'books_published': analysis['books_published'],
                'total_investment': analysis['total_investment'],
                'total_revenue': analysis['total_revenue'],
                'total_profit': analysis['total_profit'],
                'roi_percent': analysis['roi_percent']
            },
            'revenue_collection': revenue_report.to_dict(),
            'recommendations': recommendations
        }

        # Save report
        reports_dir = Path.home() / '.revenue_collection' / 'empire_reports'
        reports_dir.mkdir(parents=True, exist_ok=True)

        report_file = reports_dir / f"empire_{datetime.utcnow().strftime('%Y-%m-%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"   Report saved: {report_file}")

        return report

    async def launch_empire(
        self,
        initial_books: List[Dict[str, str]],
        auto_mode: bool = False
    ):
        """
        Launch the empire with initial books

        Args:
            initial_books: List of {'topic': str, 'genre': str}
            auto_mode: If True, continues producing books automatically
        """
        logger.info("\n" + "=" * 60)
        logger.info("🚀 LAUNCHING LOUSTA BOOKS EMPIRE")
        logger.info("=" * 60)

        # Check readiness
        is_ready, issues = await self.check_readiness()

        if not is_ready:
            raise RuntimeError(
                f"Empire not ready to launch. Issues: {', '.join(issues)}"
            )

        logger.info(f"\n📚 Producing {len(initial_books)} initial books...")

        # Produce initial books
        for i, book_spec in enumerate(initial_books, 1):
            logger.info(f"\n📖 Book {i}/{len(initial_books)}")

            try:
                result = await self.produce_and_publish_book(
                    topic=book_spec['topic'],
                    genre=book_spec['genre']
                )
                logger.info(f"   ✅ Published: {result['publication']['asin']}")

                # Wait between publications (don't spam KDP)
                if i < len(initial_books):
                    logger.info("   ⏳ Waiting 60s before next book...")
                    await asyncio.sleep(60)

            except Exception as e:
                logger.error(f"   ❌ Failed: {e}")

                # Send alert
                await self.alert_manager.send_alert(Alert(
                    level=AlertLevel.ERROR,
                    title="Book Production Failed",
                    message=f"Failed to produce book on '{book_spec['topic']}': {e}",
                    source="LoustaEmpire"
                ))

        # Show summary
        logger.info("\n" + "=" * 60)
        logger.info("✅ EMPIRE LAUNCH COMPLETE")
        logger.info("=" * 60)
        logger.info(f"   Books Published: {self.empire_data['books_published']}")
        logger.info(f"   Total Investment: ${self.empire_data['total_investment']:,.2f}")
        logger.info("")
        logger.info("🌟 Next Steps:")
        logger.info("   1. Monitor daily revenue collection")
        logger.info("   2. Review performance reports")
        logger.info("   3. Produce more books in successful niches")
        logger.info("   4. Optimize based on recommendations")

        # Start monitoring if auto mode
        if auto_mode:
            logger.info("\n🤖 Auto mode enabled - starting monitoring loop...")
            await self._auto_mode_loop()

    async def _auto_mode_loop(self):
        """Automated operation loop"""
        logger.info("🤖 Empire running in auto mode")
        logger.info("   Press Ctrl+C to stop")

        try:
            while True:
                # Wait until next midnight for daily cycle
                now = datetime.utcnow()
                tomorrow = now + timedelta(days=1)
                midnight = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
                wait_seconds = (midnight - now).total_seconds()

                logger.info(f"⏰ Next cycle in {wait_seconds/3600:.1f} hours")

                await asyncio.sleep(wait_seconds)

                # Run daily cycle
                await self.daily_empire_cycle()

        except KeyboardInterrupt:
            logger.info("\n👋 Auto mode stopped")

    def generate_chairman_briefing(self) -> str:
        """Generate executive briefing"""
        books = self.empire_data['books_published']
        investment = Decimal(str(self.empire_data['total_investment']))
        revenue = Decimal(str(self.empire_data['total_revenue']))
        profit = revenue - investment
        roi = ((revenue / investment) - 1) * 100 if investment > 0 else Decimal('0')

        briefing = f"""
╔════════════════════════════════════════════════════════╗
║         LOUSTA BOOKS EMPIRE - EXECUTIVE BRIEFING       ║
║         {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}                                   ║
╚════════════════════════════════════════════════════════╝

📚 EMPIRE STATUS
────────────────────────────────────────────────────────
  Books Published:        {books:>15}
  Books Active:           {len(self.empire_data['active_books']):>15}

💰 FINANCIAL SUMMARY
────────────────────────────────────────────────────────
  Total Investment:       ${investment:>14,.2f}
  Total Revenue:          ${revenue:>14,.2f}
  Total Profit:           ${profit:>14,.2f}
  ROI:                    {roi:>14.1f}%

📊 PERFORMANCE METRICS
────────────────────────────────────────────────────────
  Revenue per Book:       ${revenue/books if books > 0 else 0:>14,.2f}
  Avg Book Cost:          ${investment/books if books > 0 else 0:>14,.2f}

🎯 STATUS
────────────────────────────────────────────────────────
  {"✅ Profitable" if profit > 0 else "⏳ Building"}
  {"🚀 Scaling" if books > 10 else "📈 Growing"}

════════════════════════════════════════════════════════
  Empire Age: {(datetime.utcnow() - datetime.fromisoformat(self.empire_data['created_at'])).days} days
  Next Action: Daily revenue collection at midnight UTC
════════════════════════════════════════════════════════
        """

        return briefing


async def main():
    """CLI for empire management"""
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    if len(sys.argv) < 2:
        print("""
LOUSTA BOOKS EMPIRE - Automated Publishing System

Usage:
    python -m src.empire check             - Check if ready to launch
    python -m src.empire launch <file>     - Launch with books from JSON file
    python -m src.empire daily             - Run daily cycle
    python -m src.empire status            - Show empire status
    python -m src.empire briefing          - Generate executive briefing

Example JSON file (books.json):
[
    {"topic": "meditation for beginners", "genre": "self-help"},
    {"topic": "python programming basics", "genre": "education"},
    {"topic": "healthy meal prep", "genre": "cookbook"}
]

Example:
    python -m src.empire check
    python -m src.empire launch books.json
    python -m src.empire status
        """)
        sys.exit(1)

    command = sys.argv[1]
    empire = LoustaEmpire()

    if command == 'check':
        is_ready, issues = await empire.check_readiness()
        if not is_ready:
            sys.exit(1)

    elif command == 'launch':
        if len(sys.argv) < 3:
            print("Error: launch requires <books_file>")
            sys.exit(1)

        books_file = Path(sys.argv[2])
        if not books_file.exists():
            print(f"Error: File not found: {books_file}")
            sys.exit(1)

        with open(books_file, 'r') as f:
            books = json.load(f)

        await empire.launch_empire(books, auto_mode=False)

    elif command == 'daily':
        await empire.daily_empire_cycle()

    elif command == 'status':
        analysis = await empire._analyze_performance()
        print(json.dumps(analysis, indent=2))

    elif command == 'briefing':
        print(empire.generate_chairman_briefing())

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
