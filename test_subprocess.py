#!/usr/bin/env python3
"""
Test subprocess execution with npm.
"""

import subprocess
import os

def test_subprocess():
    """Test subprocess execution."""
    print("🔍 Testing subprocess execution with npm...")
    print("=" * 50)
    
    # Test direct execution
    print("1. Testing direct subprocess execution:")
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, shell=True)
        print(f"   Return code: {result.returncode}")
        if result.returncode == 0:
            print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"   Error: {result.stderr}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    # Test with full path
    print("\n2. Testing with explicit shell:")
    try:
        result = subprocess.run("npm --version", capture_output=True, text=True, shell=True)
        print(f"   Return code: {result.returncode}")
        if result.returncode == 0:
            print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"   Error: {result.stderr}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    # Test current directory
    print(f"\n3. Current working directory: {os.getcwd()}")
    
    # Test PATH
    path = os.environ.get('PATH', '')
    print("\n4. PATH environment variable (first 200 chars):")
    print(f"   {path[:200]}...")

if __name__ == "__main__":
    test_subprocess()