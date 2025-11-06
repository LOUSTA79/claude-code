#!/usr/bin/env python3
"""
Usage Tracking Hook
Tracks usage of premium features for billing and analytics after tool execution.
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def load_json(filepath):
    """Load JSON file safely."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_json(filepath, data):
    """Save JSON file safely."""
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}", file=sys.stderr)
        return False

def increment_usage(usage_key):
    """Increment usage counter for the current billing period."""
    plugin_dir = Path(__file__).parent.parent
    sub_file = plugin_dir / "data" / "user-subscriptions" / "current-user.json"

    # Load subscription
    subscription = load_json(sub_file)
    if not subscription:
        subscription = {
            "subscription": {
                "userId": "current-user",
                "plan": {"tier": "free"},
                "status": "active",
                "usage": {"currentPeriod": {}}
            }
        }

    # Increment usage
    current_period = subscription["subscription"]["usage"]["currentPeriod"]
    current_period[usage_key] = current_period.get(usage_key, 0) + 1

    # Save updated subscription
    save_json(sub_file, subscription)

    return current_period[usage_key]

def log_usage_event(tool_name, tool_input, usage_key, new_count):
    """Log usage event for analytics."""
    plugin_dir = Path(__file__).parent.parent
    events_file = plugin_dir / "data" / "usage-events" / f"{datetime.now().strftime('%Y-%m')}.jsonl"

    event = {
        "timestamp": datetime.now().isoformat(),
        "userId": "current-user",
        "toolName": tool_name,
        "usageKey": usage_key,
        "newCount": new_count,
        "metadata": {
            "toolInput": str(tool_input)[:200]  # Truncate for privacy
        }
    }

    try:
        events_file.parent.mkdir(parents=True, exist_ok=True)
        with open(events_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
    except Exception as e:
        print(f"Error logging event: {e}", file=sys.stderr)

def check_usage_threshold(usage_key, current_count):
    """Check if user is approaching usage limits and send warning."""
    plugin_dir = Path(__file__).parent.parent
    sub_file = plugin_dir / "data" / "user-subscriptions" / "current-user.json"
    pricing_file = plugin_dir / "data" / "pricing-config.json"

    subscription = load_json(sub_file)
    pricing_config = load_json(pricing_file)

    if not subscription or not pricing_config:
        return

    tier = subscription.get("subscription", {}).get("plan", {}).get("tier", "free")
    tier_config = pricing_config.get("tiers", {}).get(tier, {})

    # Find feature limit
    limit = None
    for feature_key, feature in tier_config.get("features", {}).items():
        if feature_key.lower().find(usage_key.lower()) != -1:
            limit = feature.get("limit")
            break

    if limit is None:
        return  # Unlimited

    # Calculate percentage
    percentage = (current_count / limit) * 100

    # Warn at 80% and 95%
    if percentage >= 95 and current_count - 1 < limit * 0.95:
        print(f"\n⚠️  Usage Warning: You've used {current_count}/{limit} ({percentage:.0f}%) of your {usage_key} limit.", file=sys.stderr)
        print(f"Consider upgrading to avoid service interruption: /billing upgrade\n", file=sys.stderr)
    elif percentage >= 80 and current_count - 1 < limit * 0.80:
        print(f"\n💡 Usage Notice: You've used {current_count}/{limit} ({percentage:.0f}%) of your {usage_key} limit.", file=sys.stderr)
        print(f"View your usage: /billing usage\n", file=sys.stderr)

def main():
    """Main tracking logic."""
    # Read input from stdin
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        sys.exit(0)  # Silent fail for non-blocking hook

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Map tool to usage key
    usage_key_map = {
        "tool-discovery": "toolSearches",
        "recommendation-engine": "recommendations",
        "tool-comparison": "comparisons",
        "workflow-builder": "workflows",
        "workflow": "workflowExecutions",
        "export-import": "exportOperations",
        "analytics-roi": "analyticsQueries"
    }

    # Determine usage key
    usage_key = None
    for key, mapped_key in usage_key_map.items():
        if key in tool_name.lower():
            usage_key = mapped_key
            break

    if not usage_key:
        sys.exit(0)  # Not a tracked feature

    # Increment usage
    new_count = increment_usage(usage_key)

    # Log event
    log_usage_event(tool_name, tool_input, usage_key, new_count)

    # Check thresholds
    check_usage_threshold(usage_key, new_count)

    sys.exit(0)

if __name__ == "__main__":
    main()
