#!/usr/bin/env python3
"""
Test dependency installation functionality.
"""

import subprocess
import os
import shutil

def test_dependency_installation():
    """Test dependency installation."""
    print("📦 Testing dependency installation...")
    print("=" * 40)
    
    # Check if we're in a directory with package.json
    if not os.path.exists("package.json"):
        print("❌ No package.json found in current directory")
        return
    
    # Check if node_modules already exists
    if os.path.exists("node_modules"):
        print("⚠️ node_modules already exists")
        # Optionally remove it for testing
        remove = input("Remove existing node_modules for testing? (y/n): ")
        if remove.lower() == 'y':
            try:
                shutil.rmtree("node_modules")
                print("✅ Removed existing node_modules")
            except Exception as e:
                print(f"❌ Error removing node_modules: {e}")
                return
    else:
        print("✅ node_modules does not exist (clean test)")
    
    # Test dependency installation
    print("🔧 Installing dependencies...")
    try:
        result = subprocess.run("npm install", capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("✅ Dependencies installed successfully!")
            if os.path.exists("node_modules"):
                print("✅ node_modules folder created")
                # Count directories in node_modules as a basic verification
                try:
                    dirs = [d for d in os.listdir("node_modules") if os.path.isdir(os.path.join("node_modules", d))]
                    print(f"✅ Found {len(dirs)} packages in node_modules")
                except:
                    pass
            else:
                print("⚠️ node_modules folder not found after installation")
        else:
            print("❌ Failed to install dependencies:")
            print(f"   Error: {result.stderr}")
    except Exception as e:
        print(f"❌ Error during installation: {e}")

if __name__ == "__main__":
    test_dependency_installation()