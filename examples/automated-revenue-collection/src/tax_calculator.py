"""
Tax Calculation and Compliance System

IMPORTANT: This is educational/demonstration code.
Always consult a tax professional for actual tax calculations.
"""
import logging
from decimal import Decimal
from datetime import datetime
from typing import Optional
import json
from pathlib import Path

from .models import TaxCalculation
from .config import get_config, TaxConfig


logger = logging.getLogger(__name__)


class TaxOptimizer:
    """
    Calculate and optimize tax withholdings

    DISCLAIMER: This is simplified demonstration code.
    Real tax calculations are complex and jurisdiction-specific.
    Always consult with a licensed tax professional.
    """

    def __init__(self):
        self.config = get_config()
        self.tax_config = self.config.tax
        self.ytd_revenue = self._load_ytd_revenue()

    def _load_ytd_revenue(self) -> Decimal:
        """Load year-to-date revenue"""
        data_file = Path.home() / '.revenue_collection' / 'ytd_revenue.json'

        if data_file.exists():
            with open(data_file, 'r') as f:
                data = json.load(f)
                return Decimal(data.get('ytd_revenue', '0'))

        return Decimal('0')

    def _save_ytd_revenue(self, amount: Decimal):
        """Update year-to-date revenue"""
        self.ytd_revenue += amount

        data_file = Path.home() / '.revenue_collection' / 'ytd_revenue.json'
        data_file.parent.mkdir(parents=True, exist_ok=True)

        with open(data_file, 'w') as f:
            json.dump({
                'ytd_revenue': str(self.ytd_revenue),
                'year': datetime.utcnow().year,
                'updated_at': datetime.utcnow().isoformat()
            }, f)

    def calculate_withholding(
        self,
        gross_amount: Decimal,
        override_rates: Optional[TaxConfig] = None
    ) -> TaxCalculation:
        """
        Calculate tax withholding

        Args:
            gross_amount: Gross revenue amount
            override_rates: Optional custom tax rates

        Returns:
            TaxCalculation with breakdown

        IMPORTANT: This is a simplified calculation.
        Actual tax calculation should consider:
        - Progressive tax brackets
        - Deductions and credits
        - Estimated quarterly payments
        - State/local variations
        - Business expenses
        - Self-employment tax limits
        """
        tax_config = override_rates or self.tax_config

        # Calculate each tax component
        federal_tax = gross_amount * Decimal(str(tax_config.federal_tax_rate))
        state_tax = gross_amount * Decimal(str(tax_config.state_tax_rate))
        local_tax = gross_amount * Decimal(str(tax_config.local_tax_rate))

        # Self-employment tax (Social Security + Medicare)
        # Note: In reality, this has income limits and is calculated on net profit
        self_employment_tax = gross_amount * Decimal(str(tax_config.self_employment_tax_rate))

        # Total tax
        total_tax = federal_tax + state_tax + local_tax + self_employment_tax

        # Net amount
        net_amount = gross_amount - total_tax

        # Quarterly estimated payment (if enabled)
        quarterly_estimated = None
        if tax_config.quarterly_estimated_tax:
            # Update YTD
            self._save_ytd_revenue(gross_amount)

            # Estimate quarterly payment
            # (Simplified - should use Form 1040-ES worksheets)
            quarterly_estimated = (self.ytd_revenue * Decimal('0.25')) / 4

        calculation = TaxCalculation(
            gross_amount=gross_amount,
            federal_tax=federal_tax,
            state_tax=state_tax,
            local_tax=local_tax,
            self_employment_tax=self_employment_tax,
            total_tax=total_tax,
            net_amount=net_amount,
            jurisdiction=tax_config.jurisdiction,
            quarterly_estimated_payment=quarterly_estimated
        )

        logger.info(
            f"Tax calculated: Gross ${gross_amount:.2f}, "
            f"Tax ${total_tax:.2f} ({calculation.effective_tax_rate:.1f}%), "
            f"Net ${net_amount:.2f}"
        )

        # Alert if effective rate seems high
        if calculation.effective_tax_rate > 50:
            logger.warning(
                f"⚠️ High effective tax rate: {calculation.effective_tax_rate:.1f}%. "
                "Consider consulting a tax professional."
            )

        return calculation

    def estimate_quarterly_payment(self) -> Decimal:
        """
        Estimate quarterly estimated tax payment

        For self-employed individuals, estimated taxes are typically
        due quarterly (April 15, June 15, Sept 15, Jan 15)
        """
        if not self.tax_config.quarterly_estimated_tax:
            return Decimal('0')

        # Calculate annual estimated tax based on YTD
        months_elapsed = datetime.utcnow().month
        annual_projection = (self.ytd_revenue / Decimal(months_elapsed)) * 12

        # Calculate tax on projected annual income
        estimated_annual_tax = self.calculate_withholding(annual_projection).total_tax

        # Divide by 4 for quarterly payment
        quarterly_payment = estimated_annual_tax / 4

        logger.info(
            f"Quarterly estimated tax: ${quarterly_payment:.2f} "
            f"(based on YTD ${self.ytd_revenue:.2f})"
        )

        return quarterly_payment

    def generate_tax_summary(self, year: int = None) -> dict:
        """
        Generate annual tax summary for reporting

        This should be used for:
        - Quarterly tax estimates
        - Annual tax filing preparation
        - Accounting reports
        """
        if year is None:
            year = datetime.utcnow().year

        summary = {
            'year': year,
            'jurisdiction': self.tax_config.jurisdiction,
            'ytd_revenue': str(self.ytd_revenue),
            'tax_rates': {
                'federal': self.tax_config.federal_tax_rate,
                'state': self.tax_config.state_tax_rate,
                'local': self.tax_config.local_tax_rate,
                'self_employment': self.tax_config.self_employment_tax_rate
            },
            'estimated_quarterly_payment': str(self.estimate_quarterly_payment()),
            'tax_advisor': self.tax_config.tax_advisor_email,
            'generated_at': datetime.utcnow().isoformat(),
            'disclaimer': (
                "This is an automated estimate. "
                "Consult a tax professional for accurate calculations."
            )
        }

        return summary

    def export_for_accountant(self, output_path: Path, year: int = None):
        """
        Export tax data for accountant/tax preparer

        Includes:
        - Revenue by platform
        - Expenses
        - Withholdings
        - Estimated payments
        """
        if year is None:
            year = datetime.utcnow().year

        # Load all revenue data for year
        # (This would integrate with database in production)

        export_data = {
            'business_info': {
                'year': year,
                'jurisdiction': self.tax_config.jurisdiction
            },
            'income': {
                'gross_revenue': str(self.ytd_revenue),
                'by_platform': {}  # Would be populated from actual data
            },
            'tax_summary': self.generate_tax_summary(year),
            'quarterly_payments': [],  # Would track actual payments made
            'notes': [
                "All amounts in USD",
                "Revenue is from digital book sales",
                "Self-employed business income"
            ]
        }

        output_path.write_text(json.dumps(export_data, indent=2))

        logger.info(f"Tax data exported to: {output_path}")

        # Send to tax advisor if configured
        if self.tax_config.tax_advisor_email:
            logger.info(
                f"📧 Send {output_path} to tax advisor: "
                f"{self.tax_config.tax_advisor_email}"
            )


class ExpenseTracker:
    """
    Track business expenses for tax deductions

    Common deductions for online publishing business:
    - API costs (OpenAI, cover design, etc.)
    - Marketing and advertising
    - Software subscriptions
    - Professional services (editing, design)
    - Home office deduction
    - Internet and phone
    """

    def __init__(self):
        self.expenses_file = Path.home() / '.revenue_collection' / 'expenses.json'
        self.expenses = self._load_expenses()

    def _load_expenses(self) -> list:
        """Load expenses from file"""
        if self.expenses_file.exists():
            with open(self.expenses_file, 'r') as f:
                return json.load(f).get('expenses', [])
        return []

    def _save_expenses(self):
        """Save expenses to file"""
        self.expenses_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.expenses_file, 'w') as f:
            json.dump({
                'expenses': self.expenses,
                'updated_at': datetime.utcnow().isoformat()
            }, f, indent=2)

    def add_expense(
        self,
        amount: Decimal,
        category: str,
        description: str,
        date: Optional[datetime] = None
    ):
        """
        Add business expense

        Args:
            amount: Expense amount
            category: Category (e.g., "api_costs", "marketing")
            description: Description of expense
            date: Expense date (defaults to today)
        """
        expense = {
            'amount': str(amount),
            'category': category,
            'description': description,
            'date': (date or datetime.utcnow()).isoformat()
        }

        self.expenses.append(expense)
        self._save_expenses()

        logger.info(f"Expense added: {category} ${amount:.2f} - {description}")

    def get_ytd_expenses(self, category: Optional[str] = None) -> Decimal:
        """Get year-to-date expenses, optionally filtered by category"""
        current_year = datetime.utcnow().year
        total = Decimal('0')

        for expense in self.expenses:
            expense_date = datetime.fromisoformat(expense['date'])

            if expense_date.year != current_year:
                continue

            if category and expense['category'] != category:
                continue

            total += Decimal(expense['amount'])

        return total

    def generate_expense_report(self, year: int = None) -> dict:
        """Generate expense report for tax purposes"""
        if year is None:
            year = datetime.utcnow().year

        # Filter expenses for year
        year_expenses = [
            e for e in self.expenses
            if datetime.fromisoformat(e['date']).year == year
        ]

        # Group by category
        by_category = {}
        for expense in year_expenses:
            category = expense['category']
            amount = Decimal(expense['amount'])

            if category not in by_category:
                by_category[category] = Decimal('0')

            by_category[category] += amount

        total = sum(by_category.values(), Decimal('0'))

        return {
            'year': year,
            'total_expenses': str(total),
            'by_category': {k: str(v) for k, v in by_category.items()},
            'expense_count': len(year_expenses),
            'generated_at': datetime.utcnow().isoformat()
        }
