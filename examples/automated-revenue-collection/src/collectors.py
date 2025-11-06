"""
Platform Revenue Collectors with Error Handling and Retry Logic
"""
import asyncio
import aiohttp
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging
from abc import ABC, abstractmethod

from .models import (
    PlatformRevenue, TransactionStatus, Currency, Alert, AlertLevel
)
from .config import get_config, PlatformConfig


logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter for API calls"""

    def __init__(self, calls_per_minute: int):
        self.calls_per_minute = calls_per_minute
        self.calls = []

    async def acquire(self):
        """Wait if rate limit would be exceeded"""
        now = datetime.utcnow()
        # Remove calls older than 1 minute
        self.calls = [
            call_time for call_time in self.calls
            if now - call_time < timedelta(minutes=1)
        ]

        if len(self.calls) >= self.calls_per_minute:
            # Wait until oldest call expires
            wait_until = self.calls[0] + timedelta(minutes=1)
            wait_seconds = (wait_until - now).total_seconds()
            if wait_seconds > 0:
                logger.info(f"Rate limit reached, waiting {wait_seconds:.1f}s")
                await asyncio.sleep(wait_seconds)

        self.calls.append(now)


class BaseCollector(ABC):
    """Base class for revenue collectors"""

    def __init__(self, config: PlatformConfig):
        self.config = config
        self.rate_limiter = RateLimiter(config.rate_limit_per_minute)
        self._session: Optional[aiohttp.ClientSession] = None

    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session"""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout_seconds)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def close(self):
        """Close HTTP session"""
        if self._session and not self._session.closed:
            await self._session.close()

    async def collect_revenue(self) -> PlatformRevenue:
        """
        Collect revenue from platform

        Returns:
            PlatformRevenue object with collection results
        """
        revenue = PlatformRevenue(
            platform_name=self.config.name,
            status=TransactionStatus.PENDING
        )

        try:
            # Rate limiting
            await self.rate_limiter.acquire()

            # Perform collection with retries
            for attempt in range(self.config.max_retries):
                try:
                    result = await self._collect_with_timeout()
                    revenue.amount = result['amount']
                    revenue.currency = result['currency']
                    revenue.transaction_count = result['transaction_count']
                    revenue.platform_transaction_id = result.get('transaction_id')
                    revenue.breakdown = result.get('breakdown', {})
                    revenue.status = TransactionStatus.COMPLETED

                    logger.info(
                        f"✅ {self.config.name}: Collected ${revenue.amount}"
                    )
                    break

                except asyncio.TimeoutError:
                    logger.warning(
                        f"⏱️ {self.config.name}: Timeout on attempt {attempt + 1}"
                    )
                    if attempt == self.config.max_retries - 1:
                        raise
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff

                except Exception as e:
                    logger.error(
                        f"❌ {self.config.name}: Error on attempt {attempt + 1}: {e}"
                    )
                    if attempt == self.config.max_retries - 1:
                        raise
                    await asyncio.sleep(2 ** attempt)

        except Exception as e:
            revenue.status = TransactionStatus.FAILED
            revenue.error_message = str(e)
            logger.error(f"❌ {self.config.name}: Collection failed: {e}")

        finally:
            revenue.collection_timestamp = datetime.utcnow()

        return revenue

    @abstractmethod
    async def _collect_with_timeout(self) -> Dict:
        """
        Platform-specific collection logic

        Must return dict with:
        - amount: Decimal
        - currency: Currency
        - transaction_count: int
        - transaction_id: str (optional)
        - breakdown: dict (optional)
        """
        pass


class AmazonKDPCollector(BaseCollector):
    """
    Collect royalties from Amazon KDP

    API Documentation:
    https://advertising.amazon.com/API/docs/en-us/
    """

    async def _collect_with_timeout(self) -> Dict:
        """Collect KDP royalties"""
        config = get_config()
        api_key = config.get_secret(self.config.api_key_path)
        account_id = config.get_secret(self.config.account_id_path)

        session = await self.get_session()

        # Get available balance
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Amazon-Advertising-API-ClientId': account_id,
            'Content-Type': 'application/json'
        }

        # Note: This is a simplified example. Real KDP API is more complex
        # and may require web scraping or unofficial APIs

        endpoint = f"{self.config.api_endpoint}/v2/reports"

        # Request last 24 hours of sales
        yesterday = (datetime.utcnow() - timedelta(days=1)).strftime('%Y%m%d')
        today = datetime.utcnow().strftime('%Y%m%d')

        report_request = {
            'reportDate': yesterday,
            'metrics': 'sales,royalties'
        }

        async with session.post(endpoint, headers=headers, json=report_request) as resp:
            if resp.status == 401:
                raise Exception("Authentication failed - check API key")
            elif resp.status == 429:
                raise Exception("Rate limit exceeded")
            elif resp.status != 200:
                raise Exception(f"API error: {resp.status}")

            data = await resp.json()

        # Parse response
        total_royalties = Decimal(str(data.get('totalRoyalties', 0)))
        sales_count = int(data.get('unitsSold', 0))
        pages_read = int(data.get('pagesRead', 0))
        kenp_royalties = Decimal(str(data.get('kenpRoyalties', 0)))

        return {
            'amount': total_royalties,
            'currency': Currency.USD,
            'transaction_count': sales_count,
            'transaction_id': data.get('reportId'),
            'breakdown': {
                'book_sales': str(total_royalties - kenp_royalties),
                'kindle_unlimited': str(kenp_royalties),
                'pages_read': pages_read,
                'units_sold': sales_count
            }
        }


class GooglePlayCollector(BaseCollector):
    """
    Collect revenue from Google Play Books

    API Documentation:
    https://developers.google.com/books/
    """

    async def _collect_with_timeout(self) -> Dict:
        """Collect Google Play Books revenue"""
        config = get_config()
        api_key = config.get_secret(self.config.api_key_path)
        publisher_id = config.get_secret(self.config.account_id_path)

        session = await self.get_session()

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        # Get earnings report
        endpoint = (
            f"{self.config.api_endpoint}/earnings/reports"
            f"?publisherId={publisher_id}"
            f"&startDate={datetime.utcnow().date()}"
        )

        async with session.get(endpoint, headers=headers) as resp:
            if resp.status != 200:
                raise Exception(f"API error: {resp.status}")

            data = await resp.json()

        earnings = Decimal(str(data.get('totalEarnings', 0)))
        transactions = int(data.get('transactionCount', 0))

        return {
            'amount': earnings,
            'currency': Currency.USD,
            'transaction_count': transactions,
            'transaction_id': data.get('reportId'),
            'breakdown': {
                'book_sales': str(earnings),
                'subscription_earnings': str(data.get('subscriptionEarnings', 0))
            }
        }


class AppleBooksCollector(BaseCollector):
    """
    Collect revenue from Apple Books

    API Documentation:
    https://developer.apple.com/documentation/appstoreconnectapi
    """

    async def _collect_with_timeout(self) -> Dict:
        """Collect Apple Books revenue"""
        config = get_config()
        api_key = config.get_secret(self.config.api_key_path)
        vendor_id = config.get_secret(self.config.account_id_path)

        session = await self.get_session()

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        # Get sales report
        endpoint = (
            f"{self.config.api_endpoint}/v1/salesReports"
            f"?filter[vendorNumber]={vendor_id}"
            f"&filter[reportDate]={datetime.utcnow().date()}"
        )

        async with session.get(endpoint, headers=headers) as resp:
            if resp.status != 200:
                raise Exception(f"API error: {resp.status}")

            data = await resp.json()

        proceeds = Decimal(str(data.get('proceeds', 0)))
        units = int(data.get('units', 0))

        return {
            'amount': proceeds,
            'currency': Currency.USD,
            'transaction_count': units,
            'transaction_id': data.get('reportId'),
            'breakdown': {
                'book_sales': str(proceeds)
            }
        }


class KoboCollector(BaseCollector):
    """Collect revenue from Kobo Writing Life"""

    async def _collect_with_timeout(self) -> Dict:
        """Collect Kobo revenue"""
        config = get_config()
        api_key = config.get_secret(self.config.api_key_path)
        account_id = config.get_secret(self.config.account_id_path)

        session = await self.get_session()

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        endpoint = f"{self.config.api_endpoint}/v1/sales"

        async with session.get(endpoint, headers=headers, params={'account': account_id}) as resp:
            if resp.status != 200:
                raise Exception(f"API error: {resp.status}")

            data = await resp.json()

        earnings = Decimal(str(data.get('earnings', 0)))
        units = int(data.get('unitsSold', 0))

        return {
            'amount': earnings,
            'currency': Currency.USD,
            'transaction_count': units,
            'transaction_id': data.get('reportId')
        }


class StripeCollector(BaseCollector):
    """
    Collect revenue from Stripe (direct sales)

    API Documentation:
    https://stripe.com/docs/api
    """

    async def _collect_with_timeout(self) -> Dict:
        """Collect Stripe revenue"""
        config = get_config()
        secret_key = config.get_secret(self.config.api_key_path)

        session = await self.get_session()

        headers = {
            'Authorization': f'Bearer {secret_key}',
            'Content-Type': 'application/json'
        }

        # Get balance
        balance_endpoint = f"{self.config.api_endpoint}/v1/balance"

        async with session.get(balance_endpoint, headers=headers) as resp:
            if resp.status != 200:
                raise Exception(f"API error: {resp.status}")

            balance_data = await resp.json()

        available_balance = Decimal('0')
        for balance_item in balance_data.get('available', []):
            if balance_item['currency'] == 'usd':
                # Stripe amounts are in cents
                available_balance = Decimal(balance_item['amount']) / 100

        # Get transaction count for today
        transactions_endpoint = f"{self.config.api_endpoint}/v1/charges"
        created_after = int((datetime.utcnow() - timedelta(days=1)).timestamp())

        async with session.get(
            transactions_endpoint,
            headers=headers,
            params={'created[gte]': created_after, 'limit': 100}
        ) as resp:
            if resp.status != 200:
                raise Exception(f"API error: {resp.status}")

            transactions_data = await resp.json()

        transaction_count = len(transactions_data.get('data', []))

        return {
            'amount': available_balance,
            'currency': Currency.USD,
            'transaction_count': transaction_count,
            'breakdown': {
                'available_balance': str(available_balance)
            }
        }


class PayPalCollector(BaseCollector):
    """
    Collect revenue from PayPal

    API Documentation:
    https://developer.paypal.com/docs/api/
    """

    async def _collect_with_timeout(self) -> Dict:
        """Collect PayPal revenue"""
        config = get_config()
        client_secret = config.get_secret(self.config.api_key_path)
        client_id = config.get_secret(self.config.account_id_path)

        session = await self.get_session()

        # Get OAuth token
        auth_endpoint = f"{self.config.api_endpoint}/v1/oauth2/token"

        async with session.post(
            auth_endpoint,
            auth=aiohttp.BasicAuth(client_id, client_secret),
            data={'grant_type': 'client_credentials'}
        ) as resp:
            if resp.status != 200:
                raise Exception(f"Auth failed: {resp.status}")

            auth_data = await resp.json()
            access_token = auth_data['access_token']

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Get balance
        balance_endpoint = f"{self.config.api_endpoint}/v1/reporting/balances"

        async with session.get(balance_endpoint, headers=headers) as resp:
            if resp.status != 200:
                raise Exception(f"API error: {resp.status}")

            balance_data = await resp.json()

        # Parse balance
        available = Decimal('0')
        for balance in balance_data.get('balances', []):
            if balance['currency'] == 'USD':
                available = Decimal(balance['available_balance']['value'])

        # Get transactions
        transactions_endpoint = f"{self.config.api_endpoint}/v1/reporting/transactions"
        start_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        end_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        async with session.get(
            transactions_endpoint,
            headers=headers,
            params={'start_date': start_date, 'end_date': end_date}
        ) as resp:
            if resp.status != 200:
                raise Exception(f"API error: {resp.status}")

            transactions_data = await resp.json()

        transaction_count = len(transactions_data.get('transaction_details', []))

        return {
            'amount': available,
            'currency': Currency.USD,
            'transaction_count': transaction_count,
            'breakdown': {
                'available_balance': str(available)
            }
        }


class CollectorFactory:
    """Factory for creating revenue collectors"""

    @staticmethod
    def create_collector(platform_name: str) -> BaseCollector:
        """Create collector for platform"""
        config = get_config()
        platform_config = config.platforms.get(platform_name)

        if not platform_config:
            raise ValueError(f"Unknown platform: {platform_name}")

        if not platform_config.enabled:
            raise ValueError(f"Platform disabled: {platform_name}")

        collectors = {
            'amazon_kdp': AmazonKDPCollector,
            'google_play': GooglePlayCollector,
            'apple_books': AppleBooksCollector,
            'kobo': KoboCollector,
            'stripe': StripeCollector,
            'paypal': PayPalCollector
        }

        collector_class = collectors.get(platform_name)
        if not collector_class:
            raise ValueError(f"No collector implementation for: {platform_name}")

        return collector_class(platform_config)
