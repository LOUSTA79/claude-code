"""
Secure Secrets Management

Production: Uses AWS Secrets Manager or HashiCorp Vault
Development: Uses encrypted local file storage
"""
import os
import json
import base64
from pathlib import Path
from typing import Dict, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class LocalSecretsManager:
    """
    Local file-based secrets manager for development

    SECURITY NOTES:
    - Only for development/testing
    - Secrets encrypted at rest using Fernet (AES-128)
    - Master password from environment variable
    - Never commit .secrets.enc to version control!
    """

    def __init__(self, secrets_dir: Optional[Path] = None):
        self.secrets_dir = secrets_dir or Path.home() / '.revenue_collection' / 'secrets'
        self.secrets_dir.mkdir(parents=True, exist_ok=True)
        self.secrets_file = self.secrets_dir / '.secrets.enc'
        self._cipher = self._init_cipher()
        self._secrets_cache: Optional[Dict] = None

    def _init_cipher(self) -> Fernet:
        """Initialize encryption cipher"""
        # Get master password from environment
        master_password = os.getenv('REVENUE_MASTER_PASSWORD')
        if not master_password:
            raise ValueError(
                "REVENUE_MASTER_PASSWORD environment variable required. "
                "Set a strong password: export REVENUE_MASTER_PASSWORD='your-secure-password'"
            )

        # Derive encryption key from password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'revenue-collection-salt-v1',  # In prod, use random salt
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(
            kdf.derive(master_password.encode())
        )
        return Fernet(key)

    def _load_secrets(self) -> Dict:
        """Load and decrypt secrets from file"""
        if self._secrets_cache is not None:
            return self._secrets_cache

        if not self.secrets_file.exists():
            # Initialize with empty secrets
            self._secrets_cache = {}
            self._save_secrets()
            return self._secrets_cache

        try:
            encrypted_data = self.secrets_file.read_bytes()
            decrypted_data = self._cipher.decrypt(encrypted_data)
            self._secrets_cache = json.loads(decrypted_data)
            return self._secrets_cache
        except Exception as e:
            raise RuntimeError(
                f"Failed to decrypt secrets. Wrong password? Error: {e}"
            )

    def _save_secrets(self):
        """Encrypt and save secrets to file"""
        data = json.dumps(self._secrets_cache, indent=2)
        encrypted_data = self._cipher.encrypt(data.encode())
        self.secrets_file.write_bytes(encrypted_data)
        # Secure file permissions (owner read/write only)
        os.chmod(self.secrets_file, 0o600)

    def get_secret(self, secret_path: str) -> str:
        """
        Get secret by path

        Args:
            secret_path: Path like 'revenue/bank/account_number'

        Returns:
            Secret value

        Raises:
            KeyError: If secret not found
        """
        secrets = self._load_secrets()

        # Navigate nested path
        parts = secret_path.split('/')
        current = secrets
        for part in parts:
            if part not in current:
                raise KeyError(
                    f"Secret not found: {secret_path}. "
                    f"Use set_secret() to add it."
                )
            current = current[part]

        return current

    def set_secret(self, secret_path: str, value: str):
        """
        Set secret at path

        Args:
            secret_path: Path like 'revenue/bank/account_number'
            value: Secret value
        """
        secrets = self._load_secrets()

        # Navigate/create nested path
        parts = secret_path.split('/')
        current = secrets
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]

        # Set value at final key
        current[parts[-1]] = value

        # Save encrypted
        self._save_secrets()
        print(f"✅ Secret saved: {secret_path}")

    def delete_secret(self, secret_path: str):
        """Delete secret at path"""
        secrets = self._load_secrets()

        parts = secret_path.split('/')
        current = secrets
        for part in parts[:-1]:
            current = current[part]

        del current[parts[-1]]
        self._save_secrets()
        print(f"🗑️  Secret deleted: {secret_path}")

    def list_secrets(self, prefix: str = "") -> list[str]:
        """List all secret paths with optional prefix filter"""
        secrets = self._load_secrets()

        def _get_paths(d, current_path=""):
            paths = []
            for key, value in d.items():
                path = f"{current_path}/{key}" if current_path else key
                if isinstance(value, dict):
                    paths.extend(_get_paths(value, path))
                else:
                    if not prefix or path.startswith(prefix):
                        paths.append(path)
            return paths

        return _get_paths(secrets)

    def export_secrets(self, output_file: Path):
        """
        Export secrets to JSON file (UNENCRYPTED - BE CAREFUL!)

        Use for backup or migration only
        """
        secrets = self._load_secrets()
        output_file.write_text(json.dumps(secrets, indent=2))
        os.chmod(output_file, 0o600)
        print(f"⚠️  UNENCRYPTED secrets exported to: {output_file}")
        print("   Delete this file after use!")

    def import_secrets(self, input_file: Path):
        """Import secrets from JSON file"""
        data = json.loads(input_file.read_text())
        self._secrets_cache = data
        self._save_secrets()
        print(f"✅ Secrets imported from: {input_file}")


class AWSSecretsManager:
    """
    Production secrets manager using AWS Secrets Manager

    Features:
    - Automatic rotation
    - Audit logging
    - Fine-grained IAM permissions
    - Cross-region replication
    """

    def __init__(self, region: str = 'us-east-1'):
        try:
            import boto3
            self.client = boto3.client('secretsmanager', region_name=region)
        except ImportError:
            raise RuntimeError(
                "boto3 required for AWS Secrets Manager. "
                "Install: pip install boto3"
            )

    def get_secret(self, secret_path: str) -> str:
        """Get secret from AWS Secrets Manager"""
        try:
            response = self.client.get_secret_value(SecretId=secret_path)
            return response['SecretString']
        except self.client.exceptions.ResourceNotFoundException:
            raise KeyError(f"Secret not found in AWS: {secret_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve secret: {e}")

    def set_secret(self, secret_path: str, value: str):
        """Create or update secret in AWS"""
        try:
            # Try to update existing secret
            self.client.put_secret_value(
                SecretId=secret_path,
                SecretString=value
            )
        except self.client.exceptions.ResourceNotFoundException:
            # Create new secret
            self.client.create_secret(
                Name=secret_path,
                SecretString=value,
                Tags=[
                    {'Key': 'Application', 'Value': 'RevenueCollection'},
                    {'Key': 'ManagedBy', 'Value': 'AutomatedSystem'}
                ]
            )

    def enable_rotation(self, secret_path: str, rotation_lambda_arn: str):
        """Enable automatic secret rotation"""
        self.client.rotate_secret(
            SecretId=secret_path,
            RotationLambdaARN=rotation_lambda_arn,
            RotationRules={'AutomaticallyAfterDays': 30}
        )


def init_secrets_cli():
    """
    CLI tool for managing secrets

    Usage:
        python -m src.secrets set revenue/bank/account_number "123456789"
        python -m src.secrets get revenue/bank/account_number
        python -m src.secrets list
    """
    import sys

    if len(sys.argv) < 2:
        print("""
Revenue Collection Secrets Manager

Usage:
    python -m src.secrets set <path> <value>    - Set a secret
    python -m src.secrets get <path>            - Get a secret
    python -m src.secrets delete <path>         - Delete a secret
    python -m src.secrets list [prefix]         - List secrets
    python -m src.secrets export <file>         - Export to JSON
    python -m src.secrets import <file>         - Import from JSON

Example:
    python -m src.secrets set revenue/bank/account_number "123456789"
    python -m src.secrets get revenue/bank/account_number
    python -m src.secrets list revenue/bank

IMPORTANT: Set REVENUE_MASTER_PASSWORD environment variable first!
    export REVENUE_MASTER_PASSWORD='your-secure-password'
        """)
        sys.exit(1)

    manager = LocalSecretsManager()
    command = sys.argv[1]

    if command == 'set':
        if len(sys.argv) < 4:
            print("Error: set requires <path> <value>")
            sys.exit(1)
        path, value = sys.argv[2], sys.argv[3]
        manager.set_secret(path, value)

    elif command == 'get':
        if len(sys.argv) < 3:
            print("Error: get requires <path>")
            sys.exit(1)
        path = sys.argv[2]
        try:
            value = manager.get_secret(path)
            print(f"{path}: {value}")
        except KeyError as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Error: delete requires <path>")
            sys.exit(1)
        path = sys.argv[2]
        manager.delete_secret(path)

    elif command == 'list':
        prefix = sys.argv[2] if len(sys.argv) > 2 else ""
        secrets = manager.list_secrets(prefix)
        print(f"\nSecrets (prefix: '{prefix}'):")
        for secret in secrets:
            print(f"  - {secret}")
        print(f"\nTotal: {len(secrets)} secrets")

    elif command == 'export':
        if len(sys.argv) < 3:
            print("Error: export requires <file>")
            sys.exit(1)
        output_file = Path(sys.argv[2])
        manager.export_secrets(output_file)

    elif command == 'import':
        if len(sys.argv) < 3:
            print("Error: import requires <file>")
            sys.exit(1)
        input_file = Path(sys.argv[2])
        manager.import_secrets(input_file)

    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)


if __name__ == '__main__':
    init_secrets_cli()
