#!/usr/bin/env python3
"""
Production Deployment Orchestrator

Deploys and configures the revenue collection system
"""
import asyncio
import sys
import subprocess
from pathlib import Path
from typing import Dict, List
import json


class DeploymentOrchestrator:
    """
    One-click deployment orchestrator

    Handles:
    - Environment setup
    - Dependencies installation
    - Configuration validation
    - Service setup
    - Health checks
    - Monitoring initialization
    """

    def __init__(self, environment: str = "development"):
        self.environment = environment
        self.deployment_log = []
        self.success = True

    def log(self, message: str, level: str = "INFO"):
        """Log deployment message"""
        timestamp = __import__('datetime').datetime.utcnow().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.deployment_log.append(log_entry)
        print(log_entry)

    async def deploy_production_system(self):
        """Deploy complete revenue collection system"""

        self.log("🚀 DEPLOYING AUTOMATED REVENUE COLLECTION SYSTEM")
        self.log(f"   Environment: {self.environment}")
        self.log("=" * 60)

        try:
            # Step 1: Pre-flight checks
            await self._preflight_checks()

            # Step 2: Setup environment
            await self._setup_environment()

            # Step 3: Install dependencies
            await self._install_dependencies()

            # Step 4: Configure secrets
            await self._configure_secrets()

            # Step 5: Validate configuration
            await self._validate_configuration()

            # Step 6: Setup database/storage
            await self._setup_storage()

            # Step 7: Setup monitoring
            await self._setup_monitoring()

            # Step 8: Setup schedulers
            await self._setup_schedulers()

            # Step 9: Health checks
            await self._health_checks()

            # Step 10: Final summary
            await self._deployment_summary()

        except Exception as e:
            self.log(f"❌ Deployment failed: {e}", "ERROR")
            self.success = False
            raise

    async def _preflight_checks(self):
        """Pre-flight system checks"""
        self.log("\n📋 Step 1: Pre-flight Checks")
        self.log("-" * 60)

        # Check Python version
        import sys
        python_version = sys.version_info
        if python_version < (3, 9):
            raise Exception(f"Python 3.9+ required, found {python_version}")

        self.log(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")

        # Check for required environment variables
        import os
        required_env_vars = ['REVENUE_MASTER_PASSWORD']

        for var in required_env_vars:
            if not os.getenv(var):
                self.log(f"⚠️  {var} not set", "WARNING")
            else:
                self.log(f"✅ {var} configured")

        # Check disk space
        import shutil
        stat = shutil.disk_usage('/')
        free_gb = stat.free / (1024 ** 3)

        if free_gb < 1:
            self.log(f"⚠️  Low disk space: {free_gb:.1f}GB", "WARNING")
        else:
            self.log(f"✅ Disk space: {free_gb:.1f}GB available")

    async def _setup_environment(self):
        """Setup environment"""
        self.log("\n🔧 Step 2: Environment Setup")
        self.log("-" * 60)

        # Create necessary directories
        from pathlib import Path
        dirs = [
            Path.home() / '.revenue_collection' / 'secrets',
            Path.home() / '.revenue_collection' / 'audit_logs',
            Path.home() / '.revenue_collection' / 'reports',
            Path.home() / '.revenue_collection' / 'backups'
        ]

        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            self.log(f"✅ Created directory: {dir_path}")

        # Set environment
        import os
        os.environ['REVENUE_ENV'] = self.environment
        self.log(f"✅ Environment set to: {self.environment}")

    async def _install_dependencies(self):
        """Install Python dependencies"""
        self.log("\n📦 Step 3: Installing Dependencies")
        self.log("-" * 60)

        requirements_file = Path(__file__).parent / 'requirements.txt'

        if not requirements_file.exists():
            self.log("⚠️  requirements.txt not found", "WARNING")
            return

        self.log("   Installing packages...")

        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                self.log("✅ Dependencies installed")
            else:
                self.log(f"⚠️  Some dependencies failed: {result.stderr}", "WARNING")

        except Exception as e:
            self.log(f"⚠️  Dependency installation error: {e}", "WARNING")

    async def _configure_secrets(self):
        """Configure secrets"""
        self.log("\n🔐 Step 4: Secrets Configuration")
        self.log("-" * 60)

        # Check if secrets are configured
        from src.secrets import LocalSecretsManager

        try:
            manager = LocalSecretsManager()
            secrets = manager.list_secrets()

            if secrets:
                self.log(f"✅ Found {len(secrets)} configured secrets")
            else:
                self.log("⚠️  No secrets configured", "WARNING")
                self.log("   Run: python -m src.secrets set <path> <value>")

        except Exception as e:
            self.log(f"⚠️  Secrets check failed: {e}", "WARNING")

    async def _validate_configuration(self):
        """Validate system configuration"""
        self.log("\n✓  Step 5: Configuration Validation")
        self.log("-" * 60)

        try:
            from src.config import get_config

            config = get_config()
            is_valid, errors = config.validate()

            if is_valid:
                self.log("✅ Configuration is valid")
            else:
                self.log("❌ Configuration errors found:", "ERROR")
                for error in errors:
                    self.log(f"   - {error}", "ERROR")
                raise Exception("Invalid configuration")

        except Exception as e:
            self.log(f"❌ Configuration validation failed: {e}", "ERROR")
            raise

    async def _setup_storage(self):
        """Setup storage/database"""
        self.log("\n💾 Step 6: Storage Setup")
        self.log("-" * 60)

        # For file-based storage, just verify directories exist
        storage_dirs = [
            Path.home() / '.revenue_collection' / 'reports',
            Path.home() / '.revenue_collection' / 'audit_logs'
        ]

        for dir_path in storage_dirs:
            if dir_path.exists():
                self.log(f"✅ Storage ready: {dir_path}")
            else:
                self.log(f"❌ Storage missing: {dir_path}", "ERROR")

    async def _setup_monitoring(self):
        """Setup monitoring and alerting"""
        self.log("\n📊 Step 7: Monitoring Setup")
        self.log("-" * 60)

        from src.config import get_config

        config = get_config()
        monitoring_config = config.monitoring

        if monitoring_config.get('alert_email'):
            self.log(f"✅ Email alerts → {monitoring_config['alert_email']}")
        else:
            self.log("⚠️  Email alerts not configured", "WARNING")

        if monitoring_config.get('enable_sms_alerts'):
            self.log("✅ SMS alerts enabled")
        else:
            self.log("   SMS alerts disabled")

        self.log("✅ Monitoring configured")

    async def _setup_schedulers(self):
        """Setup scheduled tasks"""
        self.log("\n⏰ Step 8: Scheduler Setup")
        self.log("-" * 60)

        if self.environment == 'production':
            self.log("   Production schedulers:")
            self.log("   - Daily collection: 00:00 UTC")
            self.log("   - Health checks: Every 5 minutes")
            self.log("   - Backup: Daily at 01:00 UTC")
            self.log("")
            self.log("⚠️  Configure cron/systemd for production:")
            self.log("   0 0 * * * python -m src.revenue_system collect")
        else:
            self.log("✅ Development mode - manual execution only")

    async def _health_checks(self):
        """Run health checks"""
        self.log("\n🏥 Step 9: Health Checks")
        self.log("-" * 60)

        checks = []

        # Check 1: Can import main module
        try:
            from src import RevenueCollectionSystem
            checks.append(("Import system", True, ""))
        except Exception as e:
            checks.append(("Import system", False, str(e)))

        # Check 2: Can load configuration
        try:
            from src.config import get_config
            config = get_config()
            checks.append(("Load config", True, ""))
        except Exception as e:
            checks.append(("Load config", False, str(e)))

        # Check 3: Can access secrets
        try:
            from src.secrets import LocalSecretsManager
            manager = LocalSecretsManager()
            checks.append(("Access secrets", True, ""))
        except Exception as e:
            checks.append(("Access secrets", False, str(e)))

        # Print results
        for check_name, passed, error in checks:
            if passed:
                self.log(f"✅ {check_name}")
            else:
                self.log(f"❌ {check_name}: {error}", "ERROR")
                self.success = False

    async def _deployment_summary(self):
        """Print deployment summary"""
        self.log("\n" + "=" * 60)

        if self.success:
            self.log("🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!")
            self.log("=" * 60)
            self.log("")
            self.log("Next steps:")
            self.log("1. Configure platform API keys:")
            self.log("   python -m src.secrets set revenue/amazon_kdp/api_key 'your-key'")
            self.log("")
            self.log("2. Test configuration:")
            self.log("   python -m src.revenue_system test")
            self.log("")
            self.log("3. Run first collection:")
            self.log("   python -m src.revenue_system collect")
            self.log("")
            self.log("4. View monitoring dashboard:")
            self.log("   python -m src.monitoring dashboard")
            self.log("")

            if self.environment == 'production':
                self.log("5. Setup cron for daily collection:")
                self.log("   crontab -e")
                self.log("   0 0 * * * cd $(pwd) && python -m src.revenue_system collect")
                self.log("")

        else:
            self.log("❌ DEPLOYMENT FAILED")
            self.log("=" * 60)
            self.log("Review the logs above for errors")

        # Save deployment log
        log_file = Path.home() / '.revenue_collection' / f'deployment_{self.environment}.log'
        log_file.write_text('\n'.join(self.deployment_log))
        self.log(f"Deployment log saved: {log_file}")


async def main():
    """Main deployment entry point"""
    if len(sys.argv) < 2:
        print("""
Deployment Orchestrator

Usage:
    python deploy.py [environment]

Environments:
    development  - Local development setup
    staging      - Staging environment
    production   - Production deployment

Example:
    python deploy.py development
    python deploy.py production
        """)
        sys.exit(1)

    environment = sys.argv[1]

    if environment not in ['development', 'staging', 'production']:
        print(f"Error: Unknown environment '{environment}'")
        print("Valid environments: development, staging, production")
        sys.exit(1)

    orchestrator = DeploymentOrchestrator(environment)

    try:
        await orchestrator.deploy_production_system()

        if orchestrator.success:
            sys.exit(0)
        else:
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n❌ Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Deployment failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
