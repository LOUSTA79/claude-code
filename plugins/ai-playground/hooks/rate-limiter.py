#!/usr/bin/env python3
"""
API Rate Limiter Hook
Enforces API rate limits based on subscription tier.
"""

import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque

# Exit codes
ALLOW = 0
BLOCK_SILENT = 1
BLOCK_WITH_MESSAGE = 2

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
    except Exception:
        return False

def get_rate_limit(tier):
    """Get rate limit for tier (requests per hour)."""
    limits = {
        "free": 100,
        "pro": 1000,
        "team": 10000,
        "enterprise": None  # Unlimited
    }
    return limits.get(tier, 100)

def check_rate_limit(tier):
    """Check if user is within rate limit."""
    plugin_dir = Path(__file__).parent.parent
    rate_file = plugin_dir / "data" / "rate-limits" / "current-user.json"

    # Load rate limit data
    rate_data = load_json(rate_file)
    if not rate_data:
        rate_data = {"requests": [], "lastCleanup": datetime.now().isoformat()}

    # Parse timestamps
    requests = []
    cutoff = datetime.now() - timedelta(hours=1)
    for req_time in rate_data.get("requests", []):
        req_dt = datetime.fromisoformat(req_time)
        if req_dt > cutoff:
            requests.append(req_time)

    # Get limit for tier
    limit = get_rate_limit(tier)
    if limit is None:
        return True, None, 0  # Unlimited

    # Check if within limit
    if len(requests) >= limit:
        # Calculate when oldest request will expire
        oldest = datetime.fromisoformat(requests[0])
        wait_until = oldest + timedelta(hours=1)
        wait_seconds = (wait_until - datetime.now()).total_seconds()
        return False, limit, max(0, int(wait_seconds))

    # Add current request
    requests.append(datetime.now().isoformat())
    rate_data["requests"] = requests
    rate_data["lastCleanup"] = datetime.now().isoformat()

    # Save updated data
    save_json(rate_file, rate_data)

    return True, limit, len(requests)

def format_rate_limit_message(tier, limit, current, wait_seconds):
    """Format rate limit exceeded message."""
    wait_minutes = wait_seconds // 60
    wait_hours = wait_minutes // 60
    wait_minutes = wait_minutes % 60

    wait_str = f"{wait_hours}h {wait_minutes}m" if wait_hours > 0 else f"{wait_minutes}m"

    return f"""
╔════════════════════════════════════════════════════════════╗
║  ⚠️  API Rate Limit Exceeded                               ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Your Plan: {tier.capitalize():<47} ║
║  Rate Limit: {limit:,} requests/hour                           ║
║  Current Usage: {current:,}/{limit:,} requests                      ║
║                                                            ║
║  You've reached your hourly API rate limit.                ║
║                                                            ║
║  Please wait {wait_str:<45} ║
║  or upgrade to a higher tier for more capacity.            ║
║                                                            ║
║  Rate Limits by Tier:                                      ║
║  • Free: 100 requests/hour                                 ║
║  • Pro: 1,000 requests/hour                                ║
║  • Team: 10,000 requests/hour                              ║
║  • Enterprise: Unlimited                                   ║
║                                                            ║
║  Commands:                                                 ║
║  • View usage: /billing usage                              ║
║  • Upgrade: /billing upgrade                               ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"""

def main():
    """Main rate limiting logic."""
    # Read input from stdin
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        sys.exit(ALLOW)  # Allow on error

    # Load subscription
    plugin_dir = Path(__file__).parent.parent
    sub_file = plugin_dir / "data" / "user-subscriptions" / "current-user.json"
    subscription = load_json(sub_file)

    if not subscription:
        tier = "free"
    else:
        tier = subscription.get("subscription", {}).get("plan", {}).get("tier", "free")

    # Check rate limit
    within_limit, limit, current = check_rate_limit(tier)

    if not within_limit:
        # Calculate wait time
        plugin_dir = Path(__file__).parent.parent
        rate_file = plugin_dir / "data" / "rate-limits" / "current-user.json"
        rate_data = load_json(rate_file)

        if rate_data and rate_data.get("requests"):
            oldest = datetime.fromisoformat(rate_data["requests"][0])
            wait_until = oldest + timedelta(hours=1)
            wait_seconds = max(0, int((wait_until - datetime.now()).total_seconds()))
        else:
            wait_seconds = 0

        print(format_rate_limit_message(tier, limit, current, wait_seconds), file=sys.stderr)
        sys.exit(BLOCK_WITH_MESSAGE)

    # Allow the request
    sys.exit(ALLOW)

if __name__ == "__main__":
    main()
