#!/usr/bin/env python3
"""
Test the Node.js/npm fix for Windows.
"""

import subprocess
import os

def test_node_npm_fix():
    """Test the Node.js/npm fix."""
    print("🔧 Testing Node.js/npm fix for Windows...")
    print("=" * 50)
    
    # Test the exact approach used in the deploy agent
    print("1. Testing check_node_installed() approach:")
    try:
        # This is the approach used in the updated deploy agent
        node_result = subprocess.run("node --version", capture_output=True, text=True, shell=True)
        if node_result.returncode == 0:
            print(f"   ✅ Node.js version: {node_result.stdout.strip()}")
        else:
            print(f"   ❌ Node.js error: {node_result.stderr}")
            
        npm_result = subprocess.run("npm --version", capture_output=True, text=True, shell=True)
        if npm_result.returncode == 0:
            print(f"   ✅ npm version: {npm_result.stdout.strip()}")
        else:
            print(f"   ❌ npm error: {npm_result.stderr}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test the build command approach
    print("\n2. Testing build command approach:")
    try:
        # Simulate what happens in build_project()
        print("   Running: npm run build")
        result = subprocess.run("npm run build", capture_output=True, text=True, shell=True, cwd=os.getcwd())
        if result.returncode == 0:
            print("   ✅ Build command successful")
        else:
            print(f"   ⚠️  Build command failed with code {result.returncode}")
            if "missing script" in result.stderr.lower() or "missing script" in result.stdout.lower():
                print("   💡 No build script found - this is normal for minimal test projects")
            else:
                print(f"   Error: {result.stderr}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")

if __name__ == "__main__":
    test_node_npm_fix()