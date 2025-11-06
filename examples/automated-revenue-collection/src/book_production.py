"""
Book Production System - Generates and publishes books to platforms

Integrates with the revenue collection system to create a complete
automated publishing empire.
"""
import os
import asyncio
import logging
from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime
from pathlib import Path
import json

# Note: OpenAI SDK has changed - using new client pattern
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI not installed. Install with: pip install openai")


logger = logging.getLogger(__name__)


class BookProductionConfig:
    """Configuration for book production"""

    def __init__(self):
        self.api_cost_per_book = Decimal('2.00')  # Estimated GPT-4 cost
        self.cover_cost = Decimal('0.50')  # DALL-E or design cost
        self.total_cost_per_book = self.api_cost_per_book + self.cover_cost

        # Publishing settings
        self.default_price = Decimal('4.99')  # Optimal for 70% royalty
        self.royalty_rate = Decimal('0.70')  # 70% on $2.99-9.99
        self.expected_monthly_sales = 10  # Conservative estimate

        # Production limits
        self.daily_production_limit = 5  # Don't spam KDP
        self.quality_threshold = 0.7  # Minimum quality score


class RealAccountSetup:
    """
    Check if real accounts and credentials are configured

    Required for actual money generation:
    - OpenAI API key (for book generation)
    - Amazon KDP account (for publishing)
    - Bank account (for receiving payments)
    """

    def __init__(self):
        self.requirements = {
            "openai_api": False,
            "kdp_account": False,
            "bank_account": False,
            "tax_info": False
        }

    def check_requirements(self) -> tuple[bool, List[str]]:
        """
        Check if all requirements are met

        Returns:
            (all_ready, list_of_missing)
        """
        missing = []

        # 1. OpenAI API (for content generation)
        if os.getenv("OPENAI_API_KEY"):
            self.requirements["openai_api"] = True
            logger.info("✅ OpenAI API Key found")
        else:
            missing.append("OpenAI API Key - Get at: https://platform.openai.com/api-keys")
            logger.warning("❌ OpenAI API Key missing - REQUIRED for book content")
            logger.warning("   Cost: ~$2.00-5.00 per book")

        # 2. Amazon KDP Account
        kdp_configured = os.getenv("KDP_EMAIL") and os.getenv("KDP_PASSWORD")
        if kdp_configured:
            self.requirements["kdp_account"] = True
            logger.info("✅ Amazon KDP account configured")
        else:
            missing.append("Amazon KDP account - Sign up at: https://kdp.amazon.com")
            logger.warning("❌ Amazon KDP account missing - REQUIRED for publishing")
            logger.warning("   Requirements: Tax info, bank account")
            logger.warning("   Approval time: 24-48 hours")

        # 3. Bank Account (checked via revenue collection config)
        try:
            from .config import get_config
            config = get_config()
            # Just check if paths are configured
            if config.bank.account_number_path:
                self.requirements["bank_account"] = True
                logger.info("✅ Bank account configured")
        except Exception:
            missing.append("Bank account - Required for receiving payments")
            logger.warning("❌ Bank account not configured")

        # 4. Tax Info
        if os.getenv("TAX_ADVISOR_EMAIL") or os.getenv("TAX_JURISDICTION"):
            self.requirements["tax_info"] = True
            logger.info("✅ Tax information configured")
        else:
            missing.append("Tax information - Configure jurisdiction and advisor")
            logger.warning("⚠️  Tax information not configured")

        all_ready = all(self.requirements.values())

        if all_ready:
            logger.info("🟢 ALL SYSTEMS READY FOR REAL MONEY GENERATION!")
        else:
            logger.warning("🔴 MISSING REQUIREMENTS - System will run in demo mode")

        return all_ready, missing


class BookGenerator:
    """
    Generate book content using GPT-4/Claude

    IMPORTANT: This costs real money!
    - ~$2-5 per book in API costs
    - Quality varies - need human review
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        self.cost_tracker = Decimal('0.00')

        if OPENAI_AVAILABLE and self.api_key:
            self.client = AsyncOpenAI(api_key=self.api_key)

    async def generate_book(
        self,
        topic: str,
        genre: str,
        chapters: int = 10,
        words_per_chapter: int = 2500
    ) -> Dict:
        """
        Generate a complete book

        Args:
            topic: Book topic (e.g., "meditation for beginners")
            genre: Genre (e.g., "self-help", "fiction", "how-to")
            chapters: Number of chapters
            words_per_chapter: Target words per chapter

        Returns:
            Dict with book data

        Costs:
            ~$2-5 per book depending on length and model
        """
        if not self.client:
            raise RuntimeError(
                "OpenAI not configured. Set OPENAI_API_KEY environment variable."
            )

        logger.info(f"💰 Generating book: '{topic}' ({genre})")
        logger.info(f"   Cost estimate: $2-5")

        book_data = {
            "topic": topic,
            "genre": genre,
            "title": "",
            "description": "",
            "chapters": [],
            "word_count": 0,
            "api_cost": 0,
            "generated_at": datetime.utcnow().isoformat()
        }

        try:
            # Step 1: Generate outline and metadata
            outline_prompt = f"""
            Create a detailed outline for a {genre} book about {topic}.

            Include:
            1. A compelling, marketable title (max 60 characters)
            2. A book description optimized for Amazon (150-200 words, include benefits)
            3. {chapters} chapter titles with 2-sentence descriptions

            Make it highly commercial and sellable. Focus on reader value.
            """

            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": outline_prompt}],
                max_tokens=1500,
                temperature=0.7
            )

            outline = response.choices[0].message.content
            self.cost_tracker += Decimal('0.15')  # Rough estimate

            # Parse outline (simplified - would use better parsing in production)
            lines = outline.split('\n')
            book_data["title"] = topic.title()  # Placeholder
            book_data["description"] = outline[:300]  # Placeholder

            logger.info(f"   ✅ Outline generated")

            # Step 2: Generate each chapter
            for i in range(chapters):
                logger.info(f"   📝 Generating chapter {i+1}/{chapters}...")

                chapter_prompt = f"""
                Write Chapter {i+1} of a {genre} book about {topic}.

                Requirements:
                - Approximately {words_per_chapter} words
                - Engaging and valuable content
                - Clear structure with introduction and conclusion
                - Practical examples or stories
                - Reader-friendly language

                Make it high quality - this will be published.
                """

                response = await self.client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[{"role": "user", "content": chapter_prompt}],
                    max_tokens=3500,
                    temperature=0.7
                )

                chapter_content = response.choices[0].message.content
                book_data["chapters"].append({
                    "number": i + 1,
                    "content": chapter_content,
                    "word_count": len(chapter_content.split())
                })

                self.cost_tracker += Decimal('0.20')  # Rough estimate
                book_data["word_count"] += len(chapter_content.split())

                # Don't hammer the API
                await asyncio.sleep(1)

            book_data["api_cost"] = float(self.cost_tracker)

            logger.info(f"   ✅ Book generated!")
            logger.info(f"   Words: {book_data['word_count']:,}")
            logger.info(f"   Cost: ${self.cost_tracker:.2f}")

            # Save book locally
            await self._save_book(book_data)

            return book_data

        except Exception as e:
            logger.error(f"   ❌ Book generation failed: {e}")
            raise

    async def _save_book(self, book_data: Dict):
        """Save generated book to local storage"""
        books_dir = Path.home() / '.revenue_collection' / 'generated_books'
        books_dir.mkdir(parents=True, exist_ok=True)

        # Create filename from topic
        filename = book_data['topic'].lower().replace(' ', '_')[:50]
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        book_file = books_dir / f"{filename}_{timestamp}.json"

        with open(book_file, 'w') as f:
            json.dump(book_data, f, indent=2)

        logger.info(f"   💾 Book saved: {book_file}")


class KDPPublisher:
    """
    Publish books to Amazon KDP

    NOTE: This is a simplified implementation.
    Real KDP publishing requires:
    - Browser automation (Selenium/Playwright)
    - 2FA handling
    - CAPTCHA solving
    - Manuscript formatting (EPUB/MOBI)
    - Cover design
    - Metadata optimization
    """

    def __init__(self, email: str = None, password: str = None):
        self.email = email or os.getenv("KDP_EMAIL")
        self.password = password or os.getenv("KDP_PASSWORD")
        self.config = BookProductionConfig()

    async def publish_book(self, book_data: Dict) -> Dict:
        """
        Publish book to Amazon KDP

        Args:
            book_data: Book data from BookGenerator

        Returns:
            Publication result with ASIN and expected revenue
        """
        logger.info(f"📚 Publishing to Amazon KDP: '{book_data['title']}'")

        # In demo mode, simulate publishing
        if os.getenv('REVENUE_ENV') != 'production':
            logger.info("   🔸 DEMO MODE: Simulating KDP publication")

            result = {
                "success": True,
                "asin": f"B{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                "title": book_data["title"],
                "price": float(self.config.default_price),
                "royalty_rate": float(self.config.royalty_rate),
                "estimated_monthly_sales": self.config.expected_monthly_sales,
                "estimated_monthly_revenue": float(
                    self.config.default_price *
                    self.config.royalty_rate *
                    Decimal(str(self.config.expected_monthly_sales))
                ),
                "published_at": datetime.utcnow().isoformat(),
                "status": "live"
            }

            logger.info(f"   ✅ Published (demo): ASIN {result['asin']}")
            logger.info(f"   💰 Expected monthly: ${result['estimated_monthly_revenue']:.2f}")

            return result

        # Real KDP publishing would go here
        logger.warning("⚠️  REAL KDP PUBLISHING NOT YET IMPLEMENTED")
        logger.warning("   Requires: Selenium, 2FA handling, manuscript formatting")

        return {
            "success": False,
            "error": "Real KDP publishing requires additional implementation"
        }


class BookProductionSystem:
    """
    Complete book production system

    Workflow:
    1. Check requirements
    2. Generate book content (GPT-4)
    3. Quality check
    4. Format manuscript
    5. Design cover
    6. Publish to KDP
    7. Track in revenue system
    """

    def __init__(self):
        self.setup = RealAccountSetup()
        self.generator = BookGenerator()
        self.publisher = KDPPublisher()
        self.config = BookProductionConfig()

    async def produce_book(self, topic: str, genre: str) -> Dict:
        """
        Complete book production workflow

        Args:
            topic: Book topic
            genre: Book genre

        Returns:
            Production result with costs and revenue projections
        """
        logger.info("=" * 60)
        logger.info("🚀 Starting Book Production")
        logger.info(f"   Topic: {topic}")
        logger.info(f"   Genre: {genre}")
        logger.info("=" * 60)

        # Step 1: Check requirements
        all_ready, missing = self.setup.check_requirements()

        if not all_ready:
            logger.error("❌ Missing requirements:")
            for item in missing:
                logger.error(f"   - {item}")
            raise RuntimeError("Cannot proceed without all requirements")

        # Step 2: Calculate costs
        total_cost = self.config.total_cost_per_book
        logger.info(f"\n💰 Cost Analysis:")
        logger.info(f"   API costs: ${self.config.api_cost_per_book:.2f}")
        logger.info(f"   Cover design: ${self.config.cover_cost:.2f}")
        logger.info(f"   Total: ${total_cost:.2f}")

        # Step 3: Calculate expected ROI
        monthly_revenue = (
            self.config.default_price *
            self.config.royalty_rate *
            Decimal(str(self.config.expected_monthly_sales))
        )
        roi_months = total_cost / monthly_revenue if monthly_revenue > 0 else 999

        logger.info(f"\n📈 Revenue Projection:")
        logger.info(f"   Price: ${self.config.default_price:.2f}")
        logger.info(f"   Royalty: {self.config.royalty_rate * 100:.0f}%")
        logger.info(f"   Expected sales/month: {self.config.expected_monthly_sales}")
        logger.info(f"   Expected revenue/month: ${monthly_revenue:.2f}")
        logger.info(f"   Break-even: {roi_months:.1f} months")

        # Step 4: Confirm if interactive
        if os.getenv('REVENUE_ENV') == 'production':
            logger.warning("\n⚠️  PRODUCTION MODE - REAL MONEY WILL BE SPENT")
            # In production, would require approval workflow

        # Step 5: Generate book
        logger.info("\n📝 Generating book content...")
        book_data = await self.generator.generate_book(topic, genre)

        # Step 6: Publish to KDP
        logger.info("\n📚 Publishing to KDP...")
        publish_result = await self.publisher.publish_book(book_data)

        if not publish_result.get("success"):
            raise RuntimeError(f"Publishing failed: {publish_result.get('error')}")

        # Step 7: Record in revenue system
        result = {
            "book": book_data,
            "publication": publish_result,
            "costs": {
                "api": float(book_data.get("api_cost", 0)),
                "cover": float(self.config.cover_cost),
                "total": float(total_cost)
            },
            "projections": {
                "monthly_revenue": float(monthly_revenue),
                "break_even_months": float(roi_months),
                "yearly_revenue": float(monthly_revenue * 12)
            }
        }

        logger.info("\n" + "=" * 60)
        logger.info("✅ BOOK PRODUCTION COMPLETE")
        logger.info("=" * 60)
        logger.info(f"   ASIN: {publish_result.get('asin')}")
        logger.info(f"   Title: {book_data['title']}")
        logger.info(f"   Cost: ${total_cost:.2f}")
        logger.info(f"   Expected monthly revenue: ${monthly_revenue:.2f}")

        return result

    def calculate_profit_potential(self, num_books: int) -> Dict:
        """Calculate profit potential for multiple books"""
        cost_per_book = self.config.total_cost_per_book
        monthly_revenue_per_book = (
            self.config.default_price *
            self.config.royalty_rate *
            Decimal(str(self.config.expected_monthly_sales))
        )

        return {
            "num_books": num_books,
            "total_investment": float(cost_per_book * num_books),
            "monthly_revenue": float(monthly_revenue_per_book * num_books),
            "yearly_revenue": float(monthly_revenue_per_book * num_books * 12),
            "break_even_months": float(cost_per_book / monthly_revenue_per_book) if monthly_revenue_per_book > 0 else 999,
            "roi_12_months": float(
                ((monthly_revenue_per_book * 12 * num_books) /
                 (cost_per_book * num_books) - 1) * 100
            ) if cost_per_book > 0 else 0
        }


async def main():
    """CLI for book production"""
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    if len(sys.argv) < 2:
        print("""
Book Production System

Usage:
    python -m src.book_production check          - Check requirements
    python -m src.book_production produce <topic> <genre>  - Produce a book
    python -m src.book_production calculate <num_books>    - Calculate profit potential

Example:
    python -m src.book_production check
    python -m src.book_production produce "meditation for beginners" "self-help"
    python -m src.book_production calculate 10
        """)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'check':
        setup = RealAccountSetup()
        all_ready, missing = setup.check_requirements()

        if not all_ready:
            print("\n❌ Missing requirements:")
            for item in missing:
                print(f"   - {item}")
            sys.exit(1)
        else:
            print("\n✅ All requirements met! Ready to produce books.")

    elif command == 'produce':
        if len(sys.argv) < 4:
            print("Error: produce requires <topic> <genre>")
            sys.exit(1)

        topic = sys.argv[2]
        genre = sys.argv[3]

        system = BookProductionSystem()
        result = await system.produce_book(topic, genre)

        print(f"\n✅ Book produced: {result['publication']['asin']}")

    elif command == 'calculate':
        if len(sys.argv) < 3:
            print("Error: calculate requires <num_books>")
            sys.exit(1)

        num_books = int(sys.argv[2])
        system = BookProductionSystem()
        projections = system.calculate_profit_potential(num_books)

        print(f"\n📊 Profit Projections for {num_books} Books:")
        print(f"   Total Investment: ${projections['total_investment']:,.2f}")
        print(f"   Monthly Revenue: ${projections['monthly_revenue']:,.2f}")
        print(f"   Yearly Revenue: ${projections['yearly_revenue']:,.2f}")
        print(f"   Break-even: {projections['break_even_months']:.1f} months")
        print(f"   12-month ROI: {projections['roi_12_months']:.1f}%")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
