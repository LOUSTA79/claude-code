"""
Automated Revenue Collection System

A production-ready system for collecting revenue from multiple platforms,
calculating taxes, and executing bank transfers with proper security controls.
"""

__version__ = '1.0.0'

from .config import get_config, Config, Environment
from .models import (
    PlatformRevenue,
    TaxCalculation,
    BankTransfer,
    DailyCollectionReport,
    Alert,
    TransactionStatus,
    Currency
)
from .revenue_system import RevenueCollectionSystem

__all__ = [
    'get_config',
    'Config',
    'Environment',
    'RevenueCollectionSystem',
    'PlatformRevenue',
    'TaxCalculation',
    'BankTransfer',
    'DailyCollectionReport',
    'Alert',
    'TransactionStatus',
    'Currency'
]
