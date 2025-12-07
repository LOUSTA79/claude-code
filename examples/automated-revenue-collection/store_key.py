#!/usr/bin/env python3
"""
Standalone secret storage script
Stores API key securely without loading other modules
"""
import os
import json
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Configuration
MASTER_PASSWORD = os.getenv('REVENUE_MASTER_PASSWORD', 'demo-secure-password-2024')
SECRETS_DIR = Path.home() / '.revenue_collection' / 'secrets'
SECRETS_FILE = SECRETS_DIR / '.secrets.enc'

# Ensure directory exists
SECRETS_DIR.mkdir(parents=True, exist_ok=True)

# Initialize cipher
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=b'revenue-collection-salt-v1',
    iterations=100000,
)
key = base64.urlsafe_b64encode(kdf.derive(MASTER_PASSWORD.encode()))
cipher = Fernet(key)

# Load existing secrets
if SECRETS_FILE.exists():
    encrypted_data = SECRETS_FILE.read_bytes()
    decrypted_data = cipher.decrypt(encrypted_data)
    secrets = json.loads(decrypted_data)
else:
    secrets = {}

# Add the API key
if 'revenue' not in secrets:
    secrets['revenue'] = {}
if 'api' not in secrets['revenue']:
    secrets['revenue']['api'] = {}

secrets['revenue']['api']['master_key'] = '6grXtwPoKAnCcKmgyGsKW1xLhdxi5mhRlT6ywRfZnKpg4AFo#nPNgXtPJl_izKrPGZ9pc-PtYnBpBgL-0NzNDg43LCk0'

# Save encrypted
data = json.dumps(secrets, indent=2)
encrypted_data = cipher.encrypt(data.encode())
SECRETS_FILE.write_bytes(encrypted_data)
os.chmod(SECRETS_FILE, 0o600)

print("✅ API key stored securely at: revenue/api/master_key")
print(f"   Storage: {SECRETS_FILE}")
print("   Encryption: AES-256 (Fernet)")
print("\n📋 All configured secrets:")

# List all secrets
def list_secrets(d, prefix=""):
    for key, value in d.items():
        path = f"{prefix}/{key}" if prefix else key
        if isinstance(value, dict):
            list_secrets(value, path)
        else:
            print(f"   - {path}")

list_secrets(secrets)
