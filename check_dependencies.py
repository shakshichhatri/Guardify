#!/usr/bin/env python3
"""
Dependency checker for Respect Ranger
Verifies all required dependencies are installed and properly configured
"""

import sys
import subprocess


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print("Checking Python version...")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - FAILED")
        print("   Respect Ranger requires Python 3.8 or higher")
        return False


def check_package(package_name, import_name=None):
    """Check if a Python package is installed."""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✅ {package_name} - OK")
        return True
    except ImportError:
        print(f"❌ {package_name} - NOT INSTALLED")
        print(f"   Install with: pip install {package_name}")
        return False


def check_textblob_data():
    """Check if TextBlob corpora are downloaded."""
    print("Checking TextBlob corpora...")
    try:
        from textblob import TextBlob
        # Try to use TextBlob - will fail if data not downloaded
        blob = TextBlob("test")
        _ = blob.sentiment
        print("✅ TextBlob corpora - OK")
        return True
    except LookupError:
        print("❌ TextBlob corpora - NOT DOWNLOADED")
        print("   Download with: python -m textblob.download_corpora")
        return False
    except Exception as e:
        print(f"⚠️  TextBlob check - WARNING: {e}")
        return True


def check_config():
    """Check if configuration exists."""
    import os
    
    print("Checking configuration...")
    
    # Check for environment variable
    token = os.getenv('DISCORD_BOT_TOKEN')
    config_exists = os.path.exists('config.json')
    
    if token:
        print("✅ Bot token found in environment variable")
        return True
    elif config_exists:
        print("✅ config.json found")
        return True
    else:
        print("⚠️  No configuration found")
        print("   Set DISCORD_BOT_TOKEN environment variable or create config.json")
        print("   See config.json.example for template")
        return False


def run_tests():
    """Run the test suite."""
    print("\nRunning test suite...")
    try:
        result = subprocess.run(
            [sys.executable, 'test_bot.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Count tests
            output = result.stderr
            if 'OK' in output:
                print("✅ All tests passed")
                return True
            else:
                print("⚠️  Tests completed with warnings")
                return True
        else:
            print("❌ Some tests failed")
            print(result.stderr[-500:])  # Show last 500 chars
            return False
    except subprocess.TimeoutExpired:
        print("⚠️  Tests timed out")
        return False
    except Exception as e:
        print(f"⚠️  Could not run tests: {e}")
        return False


def main():
    """Run all checks."""
    print("=" * 60)
    print("RESPECT RANGER - DEPENDENCY CHECKER")
    print("=" * 60)
    print()
    
    checks = []
    
    # Python version
    checks.append(check_python_version())
    print()
    
    # Required packages
    print("Checking required packages...")
    checks.append(check_package('discord.py', 'discord'))
    checks.append(check_package('textblob'))
    print()
    
    # TextBlob data
    checks.append(check_textblob_data())
    print()
    
    # Configuration
    check_config()  # Don't fail on missing config
    print()
    
    # Run tests if packages are installed
    if all(checks):
        run_tests()
    
    print()
    print("=" * 60)
    
    if all(checks):
        print("✅ ALL CHECKS PASSED")
        print("=" * 60)
        print("\nYou're ready to run the bot!")
        print("Run: python bot.py")
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print("=" * 60)
        print("\nPlease fix the issues above before running the bot.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
