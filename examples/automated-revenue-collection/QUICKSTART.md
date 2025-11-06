# Quick Start Guide

Get the revenue collection system running in 5 minutes.

## Step 1: Install Dependencies (1 minute)

```bash
cd examples/automated-revenue-collection

# Install Python dependencies
pip install -r requirements.txt
```

## Step 2: Deploy System (2 minutes)

```bash
# Set master password
export REVENUE_MASTER_PASSWORD='choose-a-secure-password-here'

# Deploy to development environment
python deploy.py development
```

## Step 3: Configure Secrets (1 minute)

```bash
# Configure platform API keys
python -m src.secrets set revenue/amazon_kdp/api_key "your-kdp-api-key"
python -m src.secrets set revenue/amazon_kdp/account_id "your-account-id"

python -m src.secrets set revenue/stripe/secret_key "sk_test_..."
python -m src.secrets set revenue/stripe/account_id "acct_..."

python -m src.secrets set revenue/paypal/client_id "your-client-id"
python -m src.secrets set revenue/paypal/client_secret "your-client-secret"

# Configure bank account (for transfers)
python -m src.secrets set revenue/bank/account_number "123456789"
python -m src.secrets set revenue/bank/routing_number "021000021"

# Set encryption key (32 characters)
python -m src.secrets set revenue/encryption/master_key "your-32-char-encryption-key-12"

# List configured secrets
python -m src.secrets list
```

## Step 4: Test Configuration (<1 minute)

```bash
# Validate configuration
python -m src.revenue_system test
```

Expected output:
```
✅ Configuration valid
```

## Step 5: Run First Collection (1 minute)

```bash
# Run manual collection
python -m src.revenue_system collect
```

Expected output:
```
🚀 Starting Daily Revenue Collection Cycle
   Time: 2024-01-15T10:30:00 UTC
============================================================

📊 Collecting from platforms...
✅ Collected $247.89 from Amazon KDP
✅ Collected $89.50 from Stripe
✅ Collected $45.00 from PayPal

💰 Total Collected: $382.39
   Successful: 3/6

🔍 Running fraud detection...

📋 Calculating taxes...
   Gross: $382.39
   Tax: $190.32 (49.8%)
   Net: $192.07

💳 Initiating bank transfer...
   ⏰ Transfer scheduled (outside business hours)

✅ Daily Collection Cycle Completed
============================================================
```

## Next Steps

### View Reports

```bash
# View today's report
python -m src.revenue_system report

# View monthly summary
python -m src.revenue_system summary 2024 1
```

### Start Monitoring Dashboard

```bash
# Real-time dashboard
python -m src.monitoring dashboard

# Generate executive report
python -m src.monitoring report
```

### Schedule Daily Collection

**Option 1: Cron (Linux/Mac)**

```bash
crontab -e

# Add this line (runs at midnight UTC daily)
0 0 * * * cd /path/to/automated-revenue-collection && python -m src.revenue_system collect
```

**Option 2: Task Scheduler (Windows)**

Create a scheduled task to run:
```
python -m src.revenue_system collect
```

**Option 3: Cloud Scheduler**

Deploy to AWS Lambda, Google Cloud Functions, or Azure Functions and configure a daily trigger.

## Configuration Tips

### Development vs Production

**Development** (default):
- Local encrypted file storage
- Simulated bank transfers
- Relaxed security checks
- No approval requirements

**Production**:
- AWS Secrets Manager
- Real bank transfers
- Strict security
- Approval workflows
- MFA required

To switch to production:
```bash
export REVENUE_ENV=production
python deploy.py production
```

### Tax Configuration

Edit `src/config.py` to match your tax situation:

```python
federal_tax_rate=0.24,      # 24% federal
state_tax_rate=0.093,       # 9.3% CA state (adjust for your state)
local_tax_rate=0.01,        # 1% local
self_employment_tax_rate=0.153  # 15.3% SE tax
```

⚠️ **Always consult a tax professional** for accurate tax calculations!

### Alert Configuration

Set up alerts:

```bash
export ALERT_EMAIL='your@email.com'
export ALERT_PHONE='+1234567890'
```

## Troubleshooting

### "Secret not found" error

Make sure you've configured all required secrets:
```bash
python -m src.secrets list
```

Required secrets:
- `revenue/bank/account_number`
- `revenue/bank/routing_number`
- `revenue/encryption/master_key`
- At least one platform's API credentials

### "Configuration errors"

Run the test command to see specific errors:
```bash
python -m src.revenue_system test
```

### "Master password required"

Set the environment variable:
```bash
export REVENUE_MASTER_PASSWORD='your-password'
```

### Collections failing

Check API credentials:
```bash
python -m src.secrets get revenue/stripe/secret_key
```

Verify the API key is correct and has the necessary permissions.

## Security Checklist

Before going to production:

- [ ] Use strong master password (20+ characters)
- [ ] Enable AWS Secrets Manager
- [ ] Configure MFA for approvals
- [ ] Set reasonable transfer limits
- [ ] Enable all alert channels
- [ ] Configure dual approval for large transfers
- [ ] Test disaster recovery
- [ ] Review audit logs regularly
- [ ] Rotate secrets quarterly

## Support

- 📖 Full documentation: See [README.md](README.md)
- 🔍 Review code: All files are commented
- 📝 Check logs: `~/.revenue_collection/`

## What's Next?

Once you have the basics working:

1. **Integrate with accounting software** - Export data for QuickBooks, Xero, etc.
2. **Add more platforms** - Extend collectors for additional revenue sources
3. **Custom reporting** - Build dashboards in Grafana, Tableau, etc.
4. **Machine learning** - Add revenue forecasting
5. **Mobile app** - Build iOS/Android app for real-time monitoring

This system is designed to be extended and customized for your specific needs!
