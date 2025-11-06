#!/usr/bin/env python3
"""
Subscription Validation Hook
Validates subscription tier and enforces feature gates and usage limits before tool execution.
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Exit codes
ALLOW = 0
BLOCK_SILENT = 1
BLOCK_WITH_MESSAGE = 2

def load_json(filepath):
    """Load JSON file safely."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def get_user_subscription():
    """Load user subscription data."""
    # In production, this would query actual subscription database
    # For demo, we'll use a local file
    plugin_dir = Path(__file__).parent.parent
    sub_file = plugin_dir / "data" / "user-subscriptions" / "current-user.json"

    if not sub_file.exists():
        # Default to free tier if no subscription found
        return {
            "subscription": {
                "userId": "current-user",
                "plan": {"tier": "free"},
                "status": "active",
                "usage": {"currentPeriod": {}}
            }
        }

    return load_json(sub_file)

def load_pricing_config():
    """Load pricing configuration."""
    plugin_dir = Path(__file__).parent.parent
    pricing_file = plugin_dir / "data" / "pricing-config.json"
    return load_json(pricing_file)

def check_feature_access(tool_name, tier_config):
    """Check if user's tier has access to the feature."""
    # Map tool names to feature keys
    feature_map = {
        "tool-discovery": "toolDiscovery",
        "recommendation-engine": "advancedRecommendations",
        "tool-comparison": "toolComparison",
        "workflow-builder": "advancedWorkflows",
        "analytics-roi": "advancedAnalytics"
    }

    for key, feature_key in feature_map.items():
        if key in tool_name:
            feature = tier_config.get("features", {}).get(feature_key)
            if feature:
                return feature.get("enabled", False)
            # Check for basic version of feature
            basic_key = feature_key.replace("advanced", "basic").replace("Advanced", "basic")
            feature = tier_config.get("features", {}).get(basic_key)
            if feature:
                return feature.get("enabled", False)

    return True  # Allow by default for unmapped features

def check_usage_limit(feature_key, current_usage, tier_config):
    """Check if usage is within limits for the feature."""
    feature = tier_config.get("features", {}).get(feature_key)
    if not feature:
        return True, None  # No limit defined

    limit = feature.get("limit")
    if limit is None:
        return True, None  # Unlimited

    usage = current_usage.get(feature_key, 0)
    if usage >= limit:
        return False, limit  # Over limit

    return True, limit  # Within limit

def format_upgrade_message(tier, feature_name):
    """Format upgrade prompt message."""
    messages = {
        "free": f"""
╔════════════════════════════════════════════════════════════╗
║  🔒 Upgrade Required                                       ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Feature: {feature_name:<48} ║
║  Your Plan: Free                                           ║
║                                                            ║
║  This feature requires a Pro plan or higher.               ║
║                                                            ║
║  Pro Plan - $29/month:                                     ║
║  ✓ Unlimited searches & recommendations                    ║
║  ✓ Advanced analytics                                      ║
║  ✓ Priority support                                        ║
║  ✓ API access                                              ║
║                                                            ║
║  Try Pro free for 14 days!                                 ║
║                                                            ║
║  Commands:                                                 ║
║  • View plans: /billing plans                              ║
║  • Start trial: /billing trial pro                         ║
║  • Upgrade now: /billing upgrade pro                       ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
""",
        "pro": f"""
╔════════════════════════════════════════════════════════════╗
║  🔒 Upgrade Required                                       ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Feature: {feature_name:<48} ║
║  Your Plan: Pro                                            ║
║                                                            ║
║  This feature requires a Team plan or higher.              ║
║                                                            ║
║  Team Plan - $99/month (3 seats):                          ║
║  ✓ Team collaboration & sharing                            ║
║  ✓ 100 workflows & 25K executions/month                    ║
║  ✓ User management & permissions                           ║
║  ✓ Advanced support (4-hour SLA)                           ║
║                                                            ║
║  Commands:                                                 ║
║  • View plans: /billing plans                              ║
║  • Upgrade now: /billing upgrade team                      ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"""
    }
    return messages.get(tier, messages["free"])

def format_limit_message(feature_name, current, limit, tier):
    """Format usage limit exceeded message."""
    percentage = int((current / limit) * 100) if limit > 0 else 100

    return f"""
╔════════════════════════════════════════════════════════════╗
║  ⚠️  Usage Limit Reached                                   ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Feature: {feature_name:<48} ║
║  Usage: {current}/{limit} ({percentage}%)                                    ║
║  Your Plan: {tier.capitalize():<47} ║
║                                                            ║
║  You've reached your monthly limit for this feature.       ║
║                                                            ║
║  Options:                                                  ║
║  1. Upgrade to higher tier for more capacity               ║
║  2. Purchase add-on for extra usage                        ║
║  3. Wait until next billing cycle (auto-resets)            ║
║                                                            ║
║  Commands:                                                 ║
║  • View usage: /billing usage                              ║
║  • View plans: /billing plans                              ║
║  • Upgrade: /billing upgrade                               ║
║  • Add-ons: /billing addons                                ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"""

def main():
    """Main validation logic."""
    # Read input from stdin
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(ALLOW)  # Allow on error to avoid blocking

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Load subscription data
    subscription = get_user_subscription()
    pricing_config = load_pricing_config()

    if not subscription or not pricing_config:
        # Allow if data can't be loaded
        sys.exit(ALLOW)

    # Get user's tier
    tier = subscription.get("subscription", {}).get("plan", {}).get("tier", "free")
    status = subscription.get("subscription", {}).get("status", "active")

    # Block if subscription is not active
    if status not in ["active", "trial"]:
        print(f"""
╔════════════════════════════════════════════════════════════╗
║  ⚠️  Subscription Inactive                                 ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Your subscription status: {status.upper():<33} ║
║                                                            ║
║  Please update your payment method or reactivate your      ║
║  subscription to continue using premium features.          ║
║                                                            ║
║  Commands:                                                 ║
║  • View status: /billing status                            ║
║  • Update payment: /billing payment update                 ║
║  • Reactivate: /billing reactivate                         ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
""", file=sys.stderr)
        sys.exit(BLOCK_WITH_MESSAGE)

    # Get tier configuration
    tier_config = pricing_config.get("tiers", {}).get(tier, {})

    # Check feature access
    if not check_feature_access(tool_name, tier_config):
        feature_name = tool_name.split("*")[-1].replace("-", " ").title()
        print(format_upgrade_message(tier, feature_name), file=sys.stderr)
        sys.exit(BLOCK_WITH_MESSAGE)

    # Check usage limits
    current_usage = subscription.get("subscription", {}).get("usage", {}).get("currentPeriod", {})

    # Map tool to usage key
    usage_key_map = {
        "tool-discovery": "toolSearches",
        "recommendation-engine": "recommendations",
        "tool-comparison": "comparisons",
        "workflow-builder": "workflowExecutions"
    }

    for key, usage_key in usage_key_map.items():
        if key in tool_name:
            within_limit, limit = check_usage_limit(usage_key, current_usage, tier_config)
            if not within_limit:
                feature_name = usage_key.replace("tool", "Tool ").replace("workflow", "Workflow ")
                current = current_usage.get(usage_key, 0)
                print(format_limit_message(feature_name, current, limit, tier), file=sys.stderr)
                sys.exit(BLOCK_WITH_MESSAGE)
            break

    # Allow the operation
    sys.exit(ALLOW)

if __name__ == "__main__":
    main()
