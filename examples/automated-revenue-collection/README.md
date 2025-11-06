# Automated Revenue Collection System

A production-ready system for automating revenue collection from multiple platforms (Amazon KDP, Google Play Books, Apple Books, Stripe, PayPal), with proper security, tax calculations, and automated bank transfers.

## 🌟 NEW: Complete Automated Publishing Empire

This system now includes **book production** capabilities, creating a complete end-to-end automated publishing business:

- 📚 **Generate Books** - AI-powered book generation using GPT-4
- 📤 **Auto-Publish** - Publish to Amazon KDP automatically
- 💰 **Collect Revenue** - Daily revenue collection from all platforms
- 🏦 **Bank Transfers** - Automated transfers to your account
- 📊 **Performance Tracking** - ROI analysis and optimization

**See [EMPIRE_GUIDE.md](EMPIRE_GUIDE.md) for the complete automated publishing empire guide.**

**Quick Empire Launch:**
```bash
# Check readiness
python -m src.empire check

# Launch with books
python -m src.empire launch example_books.json

# Daily operations
python -m src.empire daily
```

## 🎯 Features

### Security & Compliance
- ✅ **Encrypted Secrets Management** - AWS Secrets Manager or local encrypted storage
- ✅ **Audit Logging** - Tamper-proof logs with 7-year retention
- ✅ **Fraud Detection** - Anomaly detection and velocity checks
- ✅ **Approval Workflows** - Multi-factor approval for large transfers
- ✅ **MFA Support** - Optional multi-factor authentication

### Revenue Collection
- ✅ **Multi-Platform Support** - Amazon KDP, Google Play, Apple Books, Kobo, Stripe, PayPal
- ✅ **Parallel Collection** - Async collection from all platforms simultaneously
- ✅ **Retry Logic** - Automatic retries with exponential backoff
- ✅ **Rate Limiting** - Respects API rate limits

### Financial Management
- ✅ **Tax Calculation** - Federal, state, local, and self-employment tax
- ✅ **Automated Transfers** - ACH/Wire transfers to bank account
- ✅ **Business Hours Check** - Only transfers during configured hours
- ✅ **Transfer Limits** - Daily and single-transfer limits enforced
- ✅ **Expense Tracking** - Track business expenses for tax deductions

### Monitoring & Alerts
- ✅ **Real-Time Dashboard** - Live revenue and system health metrics
- ✅ **Multi-Channel Alerts** - Email, SMS, Slack, PagerDuty
- ✅ **Daily Reports** - Comprehensive collection reports
- ✅ **Monthly Summaries** - Aggregated financial reports

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.9+
python --version

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. **Set Environment Variables**

```bash
export REVENUE_ENV=development  # or staging, production
export REVENUE_MASTER_PASSWORD='your-secure-password'
export ALERT_EMAIL='your@email.com'
export TAX_ADVISOR_EMAIL='accountant@example.com'
```

2. **Configure Secrets**

```bash
# Set up secrets for each platform
python -m src.secrets set revenue/amazon_kdp/api_key "your-kdp-api-key"
python -m src.secrets set revenue/stripe/secret_key "sk_live_..."
python -m src.secrets set revenue/bank/account_number "123456789"
python -m src.secrets set revenue/bank/routing_number "021000021"
python -m src.secrets set revenue/encryption/master_key "32-char-encryption-key-here"

# List all secrets
python -m src.secrets list
```

3. **Test Configuration**

```bash
python -m src.revenue_system test
```

### Run Daily Collection

```bash
# Run collection manually
python -m src.revenue_system collect

# View today's report
python -m src.revenue_system report

# View monthly summary
python -m src.revenue_system summary 2024 1
```

### Schedule Daily Collection

**Using Cron (Linux/Mac)**

```bash
# Edit crontab
crontab -e

# Add daily collection at midnight UTC
0 0 * * * cd /path/to/automated-revenue-collection && python -m src.revenue_system collect >> /var/log/revenue-collection.log 2>&1
```

**Using systemd Timer (Linux)**

Create `/etc/systemd/system/revenue-collection.service`:

```ini
[Unit]
Description=Daily Revenue Collection
After=network.target

[Service]
Type=oneshot
User=revenue
WorkingDirectory=/opt/revenue-collection
Environment="REVENUE_ENV=production"
Environment="REVENUE_MASTER_PASSWORD=..."
ExecStart=/usr/bin/python3 -m src.revenue_system collect

[Install]
WantedBy=multi-user.target
```

Create `/etc/systemd/system/revenue-collection.timer`:

```ini
[Unit]
Description=Daily Revenue Collection Timer

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 00:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable:

```bash
sudo systemctl enable revenue-collection.timer
sudo systemctl start revenue-collection.timer
```

## 📊 Monitoring Dashboard

### Start Real-Time Dashboard

```bash
python -m src.monitoring dashboard
```

### Generate Chairman Report

```bash
python -m src.monitoring report
```

Output:
```
╔════════════════════════════════════════════════════════╗
║     LOUSTA BOOKS - DAILY EXECUTIVE BRIEFING            ║
║     2024-01-15 10:30 UTC                              ║
╚════════════════════════════════════════════════════════╝

💰 FINANCIAL SUMMARY
────────────────────────────────────────────────────────
  Today's Revenue:        $       1,247.89
  This Month:             $      18,456.32

📊 OPERATIONS
────────────────────────────────────────────────────────
  Collections:              5 successful,   1 failed
  Pending Transfers:                      0
  System Status:                    HEALTHY
```

### View Active Alerts

```bash
python -m src.monitoring alerts
```

## 🔒 Security Best Practices

### Production Deployment Checklist

- [ ] Use AWS Secrets Manager (not local file storage)
- [ ] Enable MFA for all sensitive operations
- [ ] Configure dual approval for large transfers
- [ ] Set up SSL/TLS for all API communications
- [ ] Enable audit logging with proper retention
- [ ] Configure multiple alert channels
- [ ] Set reasonable transfer limits
- [ ] Regularly review audit logs
- [ ] Rotate secrets quarterly
- [ ] Enable fraud detection
- [ ] Backup audit logs off-site
- [ ] Test disaster recovery procedures

### Secrets Management

**Development**: Uses encrypted local file storage
**Production**: Use AWS Secrets Manager or HashiCorp Vault

To migrate to AWS Secrets Manager:

```python
from src.config import Config, Environment

config = Config(env=Environment.PRODUCTION)
# Automatically uses AWS Secrets Manager in production
```

## 💰 Tax Configuration

Edit configuration in `src/config.py` or set via environment:

```python
@property
def tax(self) -> TaxConfig:
    return TaxConfig(
        jurisdiction='US-CA',  # Change to your jurisdiction
        federal_tax_rate=0.24,  # 24% federal
        state_tax_rate=0.093,  # 9.3% CA state
        local_tax_rate=0.01,  # 1% local
        self_employment_tax_rate=0.153,  # 15.3% SE tax
        quarterly_estimated_tax=True,
        tax_advisor_email='accountant@example.com',
        auto_withhold=True
    )
```

**⚠️ IMPORTANT**: This is simplified tax calculation. Always consult a tax professional for accurate calculations specific to your situation.

### Export for Accountant

```bash
python -c "
from src.tax_calculator import TaxOptimizer
from pathlib import Path

optimizer = TaxOptimizer()
optimizer.export_for_accountant(Path('tax_export_2024.json'), year=2024)
"
```

## 🏦 Bank Transfer Configuration

Configure in `src/config.py`:

```python
@property
def bank(self) -> BankConfig:
    return BankConfig(
        bank_name='Your Bank',
        account_number_path='revenue/bank/account_number',
        routing_number_path='revenue/bank/routing_number',
        requires_dual_approval=True,  # For production
        max_daily_transfer=50000.00,  # $50k daily limit
        max_single_transfer=10000.00,  # $10k per transfer
        allowed_transfer_hours=(9, 17)  # 9 AM - 5 PM UTC
    )
```

### Approval Workflow

For transfers requiring approval:

```python
from src.security import ApprovalWorkflow

workflow = ApprovalWorkflow()

# Approve a pending transfer
await workflow.approve(
    request_id='approval-id-here',
    approver='user@example.com',
    mfa_token='123456'
)
```

## 📁 Project Structure

```
automated-revenue-collection/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── secrets.py             # Secrets management
│   ├── models.py              # Data models
│   ├── collectors.py          # Platform revenue collectors
│   ├── security.py            # Audit logging, fraud detection
│   ├── tax_calculator.py      # Tax calculations
│   ├── bank_transfer.py       # Bank transfer logic
│   ├── revenue_system.py      # Main orchestrator
│   └── monitoring.py          # Dashboard and alerts
├── tests/                     # Unit tests
├── docs/                      # Additional documentation
├── config/                    # Configuration files
├── scripts/                   # Utility scripts
├── requirements.txt
└── README.md
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_collectors.py
```

## 📖 API Documentation

### Revenue Collection

```python
from src import RevenueCollectionSystem

system = RevenueCollectionSystem()

# Run daily collection
report = await system.daily_collection_cycle()

# Get specific report
report = system.get_daily_report(date=datetime(2024, 1, 15))

# Get monthly summary
summary = system.get_monthly_summary(year=2024, month=1)
```

### Tax Calculation

```python
from src.tax_calculator import TaxOptimizer
from decimal import Decimal

optimizer = TaxOptimizer()

# Calculate tax
tax_calc = optimizer.calculate_withholding(Decimal('1000.00'))

print(f"Gross: ${tax_calc.gross_amount}")
print(f"Tax: ${tax_calc.total_tax} ({tax_calc.effective_tax_rate}%)")
print(f"Net: ${tax_calc.net_amount}")

# Get quarterly estimate
quarterly = optimizer.estimate_quarterly_payment()
```

### Bank Transfer

```python
from src.bank_transfer import AutomatedBankTransfer
from decimal import Decimal

transfer_system = AutomatedBankTransfer()

# Execute transfer
transfer = await transfer_system.transfer_to_director(
    amount=Decimal('5000.00'),
    tax_withheld=Decimal('2000.00'),
    report=[],
    description='Daily Revenue'
)

print(f"Status: {transfer.status}")
print(f"Transaction ID: {transfer.bank_transaction_id}")
```

## ⚠️ Important Disclaimers

1. **Tax Calculations**: The tax calculations in this system are simplified examples. Tax laws are complex and vary by jurisdiction. Always consult a licensed tax professional for accurate tax calculations.

2. **Financial Compliance**: This system is for educational and demonstration purposes. Ensure compliance with all applicable financial regulations in your jurisdiction before using in production.

3. **API Integration**: Real API implementations may differ from examples. Consult official API documentation for each platform.

4. **Security**: While this system implements security best practices, always conduct a security audit before deploying to production.

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Support

For issues or questions:
- Check the `/docs` directory for detailed documentation
- Review the code comments for implementation details
- Consult platform-specific API documentation

## 🎓 Educational Purpose

This project demonstrates production-ready patterns for:
- Async/await programming in Python
- Secure secrets management
- Financial system design
- Audit logging and compliance
- Error handling and retry logic
- Real-time monitoring and alerting
- Test-driven development

Use this as a learning resource and foundation for building reliable automated financial systems.
