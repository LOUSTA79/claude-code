#!/usr/bin/env python3
"""
Simple API key storage for demo environment
NOTE: For production, use proper encryption!
"""
import json
from pathlib import Path

# Configuration
SECRETS_DIR = Path.home() / '.revenue_collection' / 'secrets'
CONFIG_FILE = SECRETS_DIR / 'api_keys.json'

# Ensure directory exists
SECRETS_DIR.mkdir(parents=True, exist_ok=True)

# API Key provided
api_key = '6grXtwPoKAnCcKmgyGsKW1xLhdxi5mhRlT6ywRfZnKpg4AFo#nPNgXtPJl_izKrPGZ9pc-PtYnBpBgL-0NzNDg43LCk0'

# Analyze key format
print("🔍 Analyzing API Key Format...\n")
print(f"Length: {len(api_key)} characters")
print(f"Format: Contains '#' separator")
print(f"Segments: {len(api_key.split('#'))}")

if '#' in api_key:
    parts = api_key.split('#')
    print(f"Part 1: {parts[0][:20]}... ({len(parts[0])} chars)")
    print(f"Part 2: {parts[1][:20]}... ({len(parts[1])} chars)")

# Determine likely platform
print("\n📊 Platform Detection:")
likely_platforms = []

if api_key.startswith('sk-'):
    likely_platforms.append("OpenAI (starts with 'sk-')")
elif api_key.startswith('sk_test_') or api_key.startswith('sk_live_'):
    likely_platforms.append("Stripe (starts with 'sk_test_' or 'sk_live_')")
elif '#' in api_key:
    likely_platforms.append("Custom/Unknown (contains '#' separator)")
    likely_platforms.append("Possibly: Bitcoin/Crypto wallet")
    likely_platforms.append("Possibly: Custom authentication token")

if likely_platforms:
    for platform in likely_platforms:
        print(f"   • {platform}")
else:
    print("   • Unknown format")

# Store in config
config = {
    'api_keys': {
        'master_key': {
            'value': api_key,
            'format': 'custom_with_hash_separator',
            'length': len(api_key),
            'stored_at': 'demo_environment',
            'note': 'Use environment variables to specify which platform this is for'
        }
    },
    'environment_variables': {
        'OPENAI_API_KEY': 'Set this to the key if it\'s for OpenAI',
        'STRIPE_API_KEY': 'Set this to the key if it\'s for Stripe',
        'CUSTOM_API_KEY': 'Use this for custom platforms'
    }
}

CONFIG_FILE.write_text(json.dumps(config, indent=2))
import os
os.chmod(CONFIG_FILE, 0o600)

print(f"\n✅ API key stored at: {CONFIG_FILE}")
print(f"   File permissions: 0600 (owner read/write only)")

print("\n📋 Next Steps:")
print("   1. Identify which platform this key is for")
print("   2. Set the appropriate environment variable:")
print("      export OPENAI_API_KEY='<key>'  # For OpenAI")
print("      export STRIPE_API_KEY='<key>'  # For Stripe")
print("   3. Test the connection with that platform")

print("\n🔐 Security Note:")
print("   This demo storage is NOT encrypted!")
print("   For production, use proper secrets management")
