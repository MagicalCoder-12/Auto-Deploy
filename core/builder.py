#!/usr/bin/env python3
"""Build process module for Auto Deploy Agent"""

import subprocess
import os
from config import PROJECT_DIR

def check_node_installed():
    """Check if Node.js and npm are installed and accessible."""
    try:
        node_result = subprocess.run("node --version", capture_output=True, text=True, shell=True, timeout=10)
        if node_result.returncode != 0:
            print("❌ Node.js not found.")
            return False
        print(f"✅ Node.js version: {node_result.stdout.strip()}")

        npm_result = subprocess.run("npm --version", capture_output=True, text=True, shell=True, timeout=10)
        if npm_result.returncode != 0:
            print("❌ npm not found.")
            return False
        print(f"✅ npm version: {npm_result.stdout.strip()}")
        return True
    except subprocess.TimeoutExpired:
        print("⚠️ Checking Node.js/npm timed out")
        return False
    except Exception as e:
        print(f"❌ Error checking Node.js/npm: {e}")
        return False

def install_dependencies():
    """Install project dependencies."""
    print("📦 Installing project dependencies...")
    try:
        result = subprocess.run("npm install", capture_output=True, text=True, shell=True, cwd=PROJECT_DIR, timeout=300)
        if result.returncode == 0:
            print("✅ Dependencies installed successfully!")
            return True
        else:
            print(f"⚠️ Failed to install dependencies: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("⚠️ Installing dependencies timed out")
        return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def build_project(project_type):
    """Build the project if necessary."""
    print("🔨 Building project...")

    # Check if Node.js/npm are available first for JS projects
    if project_type in ["nextjs", "vite", "react"]:
        if not check_node_installed():
            print("⚠️ Node.js is required. Please install from https://nodejs.org/")
            retry = input("Check again after install? (y/n): ")
            if retry.lower() == 'y' and not check_node_installed():
                return False
            return False

        if not os.path.exists("node_modules"):
            if not install_dependencies():
                return False

        try:
            print("🔧 Running npm run build...")
            result = subprocess.run("npm run build", capture_output=True, text=True, cwd=PROJECT_DIR, shell=True, timeout=600)
            if result.returncode == 0:
                print("✅ Build successful!")
                return True
            else:
                print(f"⚠️ Build failed: {result.stderr}")
                if "missing script" in result.stderr.lower() or "missing script" in result.stdout.lower():
                    print("💡 No build script found. Proceeding without build.")
                    return True
                if "not recognized" in result.stderr.lower() or "command not found" in result.stderr.lower():
                    if input("Install dependencies now? (y/n): ").lower() == 'y':
                        if install_dependencies():
                            retry_result = subprocess.run("npm run build", capture_output=True, text=True, cwd=PROJECT_DIR, shell=True, timeout=600)
                            if retry_result.returncode == 0:
                                return True
                return False
        except subprocess.TimeoutExpired:
            print("⚠️ Build process timed out")
            return False
        except Exception as e:
            print(f"❌ Build error: {e}")
            return False
    else:
        print("ℹ️ No build step required.")
        return True