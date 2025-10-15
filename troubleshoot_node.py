#!/usr/bin/env python3
"""
Node.js and npm troubleshooting script.
"""

import subprocess
import os
import sys

def check_node_npm():
    """Check Node.js and npm installation."""
    print("🔍 Checking Node.js and npm installation...")
    print("=" * 50)
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"✅ Node.js is installed: {result.stdout.strip()}")
        else:
            print("❌ Node.js is not installed or not in PATH")
    except FileNotFoundError:
        print("❌ Node.js is not installed or not in PATH")
    except Exception as e:
        print(f"❌ Error checking Node.js: {e}")
    
    # Check npm
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"✅ npm is installed: {result.stdout.strip()}")
        else:
            print("❌ npm is not installed or not in PATH")
    except FileNotFoundError:
        print("❌ npm is not installed or not in PATH")
    except Exception as e:
        print(f"❌ Error checking npm: {e}")
    
    # Check PATH
    path = os.environ.get('PATH', '')
    node_paths = [p for p in path.split(os.pathsep) if 'node' in p.lower()]
    if node_paths:
        print("\n📁 Node.js paths found in PATH:")
        for p in node_paths:
            print(f"   {p}")
    else:
        print("\n⚠️  No Node.js paths found in PATH")
    
    # Try to find node executable
    print("\n🔍 Searching for node executable...")
    extensions = ['.exe', '']  # Windows uses .exe
    paths = os.environ.get('PATH', '').split(os.pathsep)
    
    found = False
    for path in paths:
        for ext in extensions:
            node_path = os.path.join(path, 'node' + ext)
            if os.path.exists(node_path):
                print(f"✅ Found node at: {node_path}")
                found = True
                break
        if found:
            break
    
    if not found:
        print("❌ Could not find node executable in PATH")
        print("\n💡 Troubleshooting tips:")
        print("   1. Install Node.js from https://nodejs.org/")
        print("   2. Restart your command prompt/terminal after installation")
        print("   3. Add Node.js to your PATH manually if needed")
        print("   4. Check if you're using nvm (Node Version Manager)")

if __name__ == "__main__":
    check_node_npm()