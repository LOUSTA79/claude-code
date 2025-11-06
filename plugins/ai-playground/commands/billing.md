---
description: Manage subscriptions, billing, and payments
argument-hint: "[operation] [options]"
allowed-tools:
  - Task:*
  - Read:**/*
  - Write:**/*
  - Grep:**/*
---

# Billing & Subscription Management

Manage your AI Playground subscription, billing, payments, and usage tracking.

## Usage

```bash
# View subscription status
/billing status
/billing

# View pricing plans
/billing plans
/billing pricing

# View usage and limits
/billing usage
/billing limits

# Start trial
/billing trial [pro|team]

# Upgrade subscription
/billing upgrade [pro|team|enterprise]

# Downgrade subscription
/billing downgrade [free|pro]

# Manage payment method
/billing payment update
/billing payment info

# View invoices
/billing invoices
/billing invoice [invoice-id]

# Cancel subscription
/billing cancel

# Reactivate subscription
/billing reactivate

# Manage add-ons
/billing addons
/billing addon add [addon-name]

# Apply discount code
/billing discount [code]
```

## Commands

### `/billing status`
View your current subscription status, usage, and billing information.

**Output:**
```
📋 Subscription Status

Plan: Pro (Monthly)
Status: ✅ Active
Next Billing: December 1, 2025
Amount: $29.00 USD

Usage This Period (Nov 1 - Dec 1):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tool Searches:        127 / Unlimited  ✅
Recommendations:       45 / Unlimited  ✅
Workflows:             12 / 25         ████████░░ 48%
Workflow Executions: 1,250 / 5,000    ██████░░░░ 25%
API Requests:        8,500 / 1M       ░░░░░░░░░░  1%

Features:
✅ Unlimited tool searches
✅ Unlimited recommendations
✅ Advanced analytics (1 year)
✅ Priority support
✅ API access

Payment Method: Visa •••• 4242
Auto-Renew: Enabled

Commands:
• Manage: /billing manage
• Upgrade: /billing upgrade
• Cancel: /billing cancel
```

### `/billing plans`
Compare all available pricing plans.

**Output:**
```
💳 AI Playground Pricing Plans

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FREE                    PRO ⭐️               TEAM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$0/month                $29/month             $99/month

Perfect for             For professionals     For teams
exploring               needing advanced      collaborating

✓ 50 searches/month     ✓ Unlimited searches  ✓ All Pro features
✓ 10 recommendations    ✓ Unlimited recs      ✓ Team collaboration
✓ 3 workflows           ✓ 25 workflows        ✓ 100 workflows
✓ 100 executions/month  ✓ 5K executions/month ✓ 25K executions/month
✓ Basic analytics       ✓ Advanced analytics  ✓ Team analytics
✓ Community support     ✓ Priority support    ✓ Advanced support
                        ✓ API access          ✓ User management
                        ✓ Custom integrations ✓ Audit logs

                        🎁 14-day free trial  🎁 14-day free trial
                        💰 Save 20% annually  💰 Save 20% annually

[Start Free]            [Start Trial]         [Start Trial]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ENTERPRISE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Custom Pricing

For organizations requiring advanced security & compliance

✓ Unlimited everything
✓ SSO & advanced security
✓ Custom branding
✓ Dedicated instance
✓ Dedicated account manager
✓ 99.9% uptime SLA
✓ Professional services
✓ Custom contracts

[Contact Sales]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Add-Ons Available:
• Extra Workflow Executions: $10/1,000 executions
• Additional Team Seats: $29/seat/month
• Extended Analytics: $49/month (5-year retention)
• Premium Support: $199/month (1-hour SLA)

Special Discounts:
• 50% off for nonprofits & education
• 30% off for startups (12 months)
• 20% off with annual billing

Commands:
• Start trial: /billing trial [pro|team]
• Upgrade: /billing upgrade [plan]
• Contact sales: /billing contact
```

### `/billing usage`
View detailed usage statistics for the current billing period.

**Output:**
```
📊 Usage Report

Billing Period: Nov 1 - Dec 1, 2025
Plan: Pro (Monthly)

Feature Usage:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tool Searches
  Used: 127
  Limit: Unlimited
  Status: ✅ Available

Recommendations
  Used: 45
  Limit: Unlimited
  Status: ✅ Available

Tool Comparisons
  Used: 23
  Limit: Unlimited
  Status: ✅ Available

Workflows Created
  Used: 12
  Limit: 25
  Status: ✅ 13 remaining (52%)
  █████████████░░░░░░░░░░░

Workflow Executions
  Used: 1,250
  Limit: 5,000
  Status: ✅ 3,750 remaining (25%)
  ███████░░░░░░░░░░░░░░░░░

API Requests (hourly)
  Used: 45
  Limit: 1,000
  Status: ✅ 955 remaining (5%)
  ██░░░░░░░░░░░░░░░░░░░░░░

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Projected Usage:
Based on current trends, you'll use:
• 254 tool searches (well within limit)
• 2,500 workflow executions (50% of limit)

Recommendations:
✅ Your usage is healthy
✅ No action needed this month

Need more capacity?
• Upgrade: /billing upgrade team
• Add-ons: /billing addons

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### `/billing trial [plan]`
Start a free trial of a paid plan.

**Arguments:**
- `plan`: The plan to trial (`pro` or `team`)

**Example:**
```bash
/billing trial pro
```

**Output:**
```
🎉 Start Your Pro Trial

14-Day Free Trial - No Credit Card Required*
(*Credit card needed for auto-conversion to paid)

What You Get:
✓ Unlimited tool searches & recommendations
✓ 25 workflows & 5,000 executions/month
✓ Advanced analytics (1 year retention)
✓ Priority email support
✓ API access (1,000 requests/hour)
✓ Custom tool integrations (10 max)

Trial Details:
• Start Date: Today
• End Date: December 20, 2025
• Auto-Converts: Yes ($29/month after trial)
• Cancel Anytime: Yes, zero charges if canceled before end

Your trial starts immediately with full access to all Pro features.

Next Steps:
1. ✅ Trial activated
2. Explore Pro features
3. Get email reminders at days 7, 11, and 13
4. Decision on day 14: Keep Pro or revert to Free

Start exploring now!
• Discover tools: /discover
• Get recommendations: /recommend
• Build workflows: /workflow

Trial Terms: https://aiplayground.com/trial-terms
Questions? support@aiplayground.com
```

### `/billing upgrade [plan]`
Upgrade to a higher tier plan.

**Arguments:**
- `plan`: Target plan (`pro`, `team`, or `enterprise`)

**Example:**
```bash
/billing upgrade team
```

**Output:**
```
🚀 Upgrade to Team Plan

Current: Pro ($29/month)
New: Team ($99/month for 3 seats)

You'll Get:
✅ Team collaboration and sharing
✅ 100 workflows (vs 25)
✅ 25,000 executions/month (vs 5,000)
✅ 10,000 API req/hour (vs 1,000)
✅ User management & permissions
✅ Audit logs (90 days)
✅ Advanced support (4-hour SLA)

Cost Breakdown:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Current plan credit: -$14.50
  (21 days remaining at $29/month)

• Team plan (21 days): +$69.30
  (Prorated for remainder of period)

• Amount due today: $54.80
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Next billing (Dec 1): $99.00
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Savings:
Team plan: $99/month for 3 seats
3× Pro plans would be: $87/month
You save: $27/month (23%)

Your upgrade will:
• Take effect immediately
• Charge $54.80 today (prorated)
• Set new billing amount to $99/month

Payment Method: Visa •••• 4242

Confirm upgrade?
• Yes, upgrade now: /billing upgrade team confirm
• View other plans: /billing plans
• Cancel: (do nothing)
```

### `/billing cancel`
Cancel your subscription.

**Output:**
```
😔 Cancel Subscription

Before You Go...

Your Plan: Pro (Monthly)
Next Billing: December 1, 2025 ($29.00)

If you cancel:
• Subscription ends: December 1, 2025
• You keep access until: December 1, 2025
• No refund for current period
• Data remains accessible for 30 days

We'd hate to see you go! Can we help?

Common Issues & Solutions:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❓ "Too expensive"
   → Save 20% with annual billing
   → Or try our Free plan (keeps your data)

❓ "Not using it enough"
   → Pause subscription for up to 3 months
   → Or downgrade to save money

❓ "Missing features"
   → Tell us what you need - we're building!
   → Priority feature requests for paid users

❓ "Found an alternative"
   → We offer price matching for annual plans
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Special Offers:
🎁 Stay for 20% off next 3 months ($23.20/month)
🎁 Pause subscription (keep your spot)
🎁 Downgrade to free (keep all your data)

What would you like to do?
• Accept 20% discount: /billing discount STAY20
• Pause subscription: /billing pause
• Downgrade to Free: /billing downgrade free
• Continue with cancellation: /billing cancel confirm

Questions? We're here to help!
Email: support@aiplayground.com
Chat: /support chat
```

### `/billing payment update`
Update your payment method.

**Output:**
```
💳 Update Payment Method

Current Payment Method:
  Visa ending in 4242
  Expires: 12/2027

Update Options:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Credit/Debit Card
   • Visa, Mastercard, Amex, Discover
   • Secure processing via Stripe
   • Instant verification

2. PayPal
   • Link your PayPal account
   • Automatic recurring payments

3. Bank Transfer (Enterprise only)
   • ACH or wire transfer
   • Invoice-based billing

Security:
🔒 PCI DSS Level 1 certified
🔒 256-bit SSL encryption
🔒 Never store full card numbers
🔒 Tokenized payment processing

Update Now:
This will open a secure payment form.
Your current subscription will continue uninterrupted.

• Update card: /billing payment update card
• Add PayPal: /billing payment update paypal
• Contact billing: support@aiplayground.com

All payment methods are processed securely through
our PCI-compliant payment processor (Stripe).
```

### `/billing invoices`
View billing history and invoices.

**Output:**
```
🧾 Billing History

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date         Invoice         Amount    Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Nov 1, 2025  INV-2025-11-001 $55.30    ✅ Paid
Oct 1, 2025  INV-2025-10-001 $29.00    ✅ Paid
Sep 1, 2025  INV-2025-09-001 $29.00    ✅ Paid
Aug 1, 2025  INV-2025-08-001 $29.00    ✅ Paid
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                      Total: $142.30
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Upcoming:
Dec 1, 2025  Pro Plan (Monthly)  $29.00  (Scheduled)

Commands:
• View invoice: /billing invoice INV-2025-11-001
• Download all: /billing invoices download
• Email invoice: /billing invoice INV-2025-11-001 email
```

### `/billing invoice [invoice-id]`
View detailed invoice information.

**Example:**
```bash
/billing invoice INV-2025-11-001
```

**Output:**
```
🧾 Invoice Details

Invoice Number: INV-2025-11-001
Date: November 1, 2025
Status: ✅ Paid
Due Date: November 1, 2025
Paid Date: November 1, 2025 10:30 AM

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Bill To:
John Doe
john@example.com
Acme Corporation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Description                          Amount
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI Playground Pro - Monthly          $29.00
  Nov 1, 2025 - Dec 1, 2025

Extra Workflow Executions             $50.00
  5,000 additional executions

                            Subtotal: $79.00
                   Tax (0%): $0.00
           Discount (30%):  -$23.70
                              -------
                       Total: $55.30

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Discount Applied:
STARTUP30 - 30% off for startups (8 months remaining)

Payment Method:
Visa ending in 4242
Transaction ID: txn_abc123
Payment Gateway: Stripe

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Actions:
• Download PDF: /billing invoice INV-2025-11-001 pdf
• Email copy: /billing invoice INV-2025-11-001 email
• Print: /billing invoice INV-2025-11-001 print

Questions about this invoice?
Email: billing@aiplayground.com
Phone: 1-800-AI-PLAYGROUND
```

### `/billing addons`
View and manage add-ons.

**Output:**
```
🎁 Available Add-Ons

Available for your Pro plan:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Extra Workflow Executions
   $10 per 1,000 executions
   • Need more than 5,000/month?
   • Add as many as you need
   • Billed monthly

2. Premium Support
   $199/month
   • 1-hour response SLA
   • Phone support included
   • Dedicated support engineer
   • Priority bug fixes

3. Custom Tool Integration
   $499 one-time
   • Professional services
   • Integrate any tool
   • Full testing & documentation
   • 30-day support included

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current Add-Ons:
• Extra Executions (5× 1,000): $50/month

Commands:
• Add extra executions: /billing addon add executions [quantity]
• Add premium support: /billing addon add support
• Request custom integration: /billing addon add integration

Need something else?
Contact us: sales@aiplayground.com
```

### `/billing discount [code]`
Apply a discount code to your subscription.

**Example:**
```bash
/billing discount STARTUP30
```

**Output:**
```
🎉 Discount Code Applied!

Code: STARTUP30
Discount: 30% off for 12 months

Your Savings:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pro Plan: $29/month
Discount: -$8.70/month (30%)
New Price: $20.30/month
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Annual Savings: $104.40
Total over 12 months: $243.60 (vs $348)

Duration: 12 months (Nov 2025 - Nov 2026)
Months Remaining: 12

This discount will be automatically applied to your
next invoice and all subsequent invoices for 12 months.

After the discount period:
Your subscription will revert to standard pricing
($29/month) unless canceled.

View updated billing: /billing status
```

## Pricing Tiers

### Free - $0/month
- 50 tool searches/month
- 10 recommendations/month
- 20 tool comparisons/month
- 3 workflows, 100 executions/month
- Basic analytics (30 days)
- Export in JSON only
- Community support

### Pro - $29/month ($279/year)
- ⭐ Most Popular
- Unlimited searches & recommendations
- Unlimited comparisons
- 25 workflows, 5,000 executions/month
- Advanced analytics (1 year)
- All export formats
- Custom integrations (10)
- Priority support (24-hour response)
- API access (1,000 req/hour)
- 14-day free trial

### Team - $99/month for 3 seats ($950/year)
- All Pro features
- Team collaboration & sharing
- 100 workflows, 25,000 executions/month
- User management & permissions
- Audit logs (90 days)
- Advanced support (4-hour SLA)
- API access (10,000 req/hour)
- 14-day free trial

### Enterprise - Custom Pricing
- Unlimited everything
- SSO & advanced security
- Custom branding & deployment
- Dedicated account manager
- 99.9% uptime SLA
- Professional services
- Custom contracts
- 30-day trial

## Payment Methods

Accepted payment methods:
- Credit/Debit Cards (Visa, Mastercard, Amex, Discover)
- PayPal
- Bank Transfer (Enterprise only)
- Invoice (Enterprise only)

## Billing Policies

### Refund Policy
- 30-day money-back guarantee
- Prorated refunds for annual plans
- No refunds for usage-based add-ons
- Contact support for refund requests

### Cancellation Policy
- Cancel anytime
- Access continues until end of billing period
- No prorated refunds for monthly plans
- Data retained for 30 days after cancellation

### Fair Usage Policy
- Reasonable usage expected
- Excessive usage may require upgrade
- Prevents abuse and ensures quality for all users

## Security & Compliance

### Payment Security
- PCI DSS Level 1 certified
- 256-bit SSL encryption
- Tokenized payment processing
- Never store full card numbers

### Data Privacy
- GDPR compliant
- SOC 2 Type II certified
- Data encryption at rest and in transit
- Regular security audits

---

## Implementation

**Agent Used**: subscription-manager (Sonnet model)
**Tools**: Read (subscription data), Write (updates), WebFetch (payment gateway)
**Data Location**: `/plugins/ai-playground/data/pricing-config.json`
**Subscription Storage**: `/plugins/ai-playground/data/user-subscriptions/`
