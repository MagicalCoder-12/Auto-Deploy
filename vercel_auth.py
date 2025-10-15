#!/usr/bin/env python3
"""
Vercel authentication helper script.
"""

import subprocess
import sys

def vercel_auth():
    """Help with Vercel authentication."""
    print("🔐 Vercel Authentication Helper")
    print("=" * 35)
    print()
    
    # Check if Vercel CLI is installed
    print("🔍 Checking Vercel CLI installation...")
    try:
        result = subprocess.run("vercel --version", capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("✅ Vercel CLI is installed")
            # Extract version from output
            lines = result.stdout.split('\n')
            if lines:
                print(f"   Version: {lines[0]}")
        else:
            print("❌ Vercel CLI is not installed")
            print("   Please run: npm install -g vercel")
            return
    except Exception as e:
        print(f"❌ Error checking Vercel CLI: {e}")
        print("   Please make sure Vercel CLI is installed: npm install -g vercel")
        return
    
    # Check current authentication status
    print("\n🔍 Checking authentication status...")
    try:
        result = subprocess.run("vercel whoami", capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("✅ You are already logged in to Vercel")
            print(f"   User: {result.stdout.strip()}")
        else:
            print("⚠️ You are not logged in to Vercel")
            login()
    except Exception as e:
        print(f"❌ Error checking authentication: {e}")
        login()

def login():
    """Perform Vercel login."""
    print("\n🔐 Logging in to Vercel...")
    print("   This will open a browser window for you to authenticate")
    print("   Press Ctrl+C if you need to cancel")
    
    try:
        input("Press Enter to continue with login...")
        result = subprocess.run("vercel login", capture_output=False, text=True, shell=True)
        if result.returncode == 0:
            print("✅ Login successful!")
        else:
            print("⚠️ Login process completed with issues")
    except KeyboardInterrupt:
        print("\n⚠️ Login cancelled by user")
    except Exception as e:
        print(f"❌ Error during login: {e}")

def logout():
    """Perform Vercel logout."""
    print("\n🔓 Logging out of Vercel...")
    try:
        result = subprocess.run("vercel logout", capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("✅ Logout successful!")
        else:
            print("⚠️ Logout failed:", result.stderr)
    except Exception as e:
        print(f"❌ Error during logout: {e}")

def main():
    """Main function."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "login":
            vercel_auth()  # This will check status and login if needed
        elif sys.argv[1] == "logout":
            logout()
        else:
            print("Usage: python vercel_auth.py [login|logout]")
            print("   login  - Check auth status and login if needed")
            print("   logout - Logout from Vercel")
    else:
        vercel_auth()

if __name__ == "__main__":
    main()