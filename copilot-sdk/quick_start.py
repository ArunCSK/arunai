#!/usr/bin/env python3
"""Quick start guide and setup verification script."""
import os
import sys
from pathlib import Path


def check_environment():
    """Check if the environment is properly configured."""
    print("🔍 Checking Stock Analysis Dashboard Setup...\n")
    
    # Check Python version
    print(f"✓ Python {sys.version.split()[0]}")
    
    # Check working directory
    cwd = Path.cwd()
    print(f"✓ Working directory: {cwd}")
    
    # Check required files
    required_files = [
        "app.py",
        "agent.py", 
        "agent_tools.py",
        "requirements.txt",
        ".env"
    ]
    
    print("\n📋 Required Files:")
    for file in required_files:
        if (cwd / file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            return False
    
    # Check .env configuration
    print("\n🔑 Configuration Check:")
    env_path = cwd / ".env"
    if env_path.exists():
        with open(env_path, 'r') as f:
            content = f.read()
            if "OPENAI_API_KEY=" in content:
                # Check if API key is set (not placeholder)
                for line in content.split('\n'):
                    if line.startswith("OPENAI_API_KEY="):
                        key = line.split("=", 1)[1].strip()
                        if key and not key.startswith("sk-your-"):
                            print("  ✓ OpenAI API Key configured")
                        else:
                            print("  ⚠️  OpenAI API Key not set (using placeholder)")
                            print("     → Get free key from: https://platform.openai.com/api-keys")
                        break
        print("  ✓ .env file found")
    else:
        print("  ✗ .env file not found")
        return False
    
    # Check Python packages (skip agent_framework due to circular imports)
    print("\n📦 Python Packages:")
    required_packages = [
        ("agent_framework", "Agent Framework"),
        ("openai", "OpenAI"),
        ("streamlit", "Streamlit"),
        ("yfinance", "yfinance"),
        ("pandas", "Pandas"),
        ("plotly", "Plotly")
    ]
    
    missing_packages = []
    for package_name, display_name in required_packages:
        try:
            if package_name == "agent_framework":
                # Special handling for agent_framework (might have import issues)
                import pkg_resources
                pkg_resources.require("agent-framework-core")
                pkg_resources.require("agent-framework-azure-ai")
                print(f"  ✓ {display_name}")
            else:
                __import__(package_name)
                print(f"  ✓ {display_name}")
        except Exception as e:
            print(f"  ✗ {display_name} - ERROR: {str(e)[:50]}")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n⚠️  Issues with packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        # Don't return False for this, as it might be a transient issue
    
    return True


def print_quick_start():
    """Print quick start instructions."""
    print("\n" + "="*60)
    print("🚀 QUICK START")
    print("="*60)
    
    print("\n1️⃣  Set your OpenAI API Key:")
    print(f"   - Open .env file")
    print(f"   - Replace 'sk-your-api-key-here' with your actual key")
    print(f"   - Get free key: https://platform.openai.com/api-keys")
    
    print("\n2️⃣  Run the app:")
    print(f"   streamlit run app.py")
    
    print("\n3️⃣  Open browser:")
    print(f"   http://localhost:8501")
    
    print("\n4️⃣  Try these queries:")
    print(f"   - 'What is the price of Apple?'")
    print(f"   - 'Show me Microsoft 5-day price trend'")
    print(f"   - 'Compare Apple and Google'")
    
    print("\n" + "="*60)
    print("📚 For more info, see README.md")
    print("="*60 + "\n")


if __name__ == "__main__":
    if check_environment():
        print("\n✅ All checks passed! Ready to start.\n")
        print_quick_start()
    else:
        print("\n❌ Setup incomplete. Please fix the issues above.\n")
        sys.exit(1)
