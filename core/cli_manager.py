#!/usr/bin/env python3
"""CLI tool management module for Auto Deploy Agent"""

import subprocess
from config import CLI_MAP

def check_cli_installed(cli_command):
    """Check if a CLI tool is installed by running --version."""
    try:
        result = subprocess.run(f"{cli_command} --version", capture_output=True, text=True, encoding="utf-8", errors="replace", shell=True, timeout=10)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"Command '{cli_command} --version' timed out")
        return False
    except Exception as e:
        print(f"Error checking {cli_command}: {e}")
        return False

def install_cli(platform):
    """Check if CLI is available, ask permission to install if not."""
    cli_info = CLI_MAP.get(platform)
    
    if not cli_info:
        print(f"{platform} doesn't require a specific CLI.")
        return True

    if check_cli_installed(cli_info["cmd"]):
        print(f"{cli_info['cmd']} is already installed.")
        return True

    print(f"{cli_info['cmd']} not found.")
    
    if cli_info["auto_install"]:
        permission = input(f"Do you want me to install it automatically? (y/n): ")
        if permission.lower() == 'y':
            try:
                print(f"Installing {cli_info['cmd']}...")
                result = subprocess.run(cli_info["install"], capture_output=True, text=True, encoding="utf-8", errors="replace", shell=True, timeout=120)
                if result.returncode == 0:
                    print("Installation successful!")
                    return True
                else:
                    print(f"Installation failed: {result.stderr}")
                    return False
            except subprocess.TimeoutExpired:
                print(f"Installation of {cli_info['cmd']} timed out")
                return False
            except Exception as e:
                print(f"Error installing: {e}")
                return False
        else:
            print(f"Please install manually: {cli_info['install']}")
            print("After installation, restart your terminal and run this script again.")
            return False
    else:
        # Tools that require manual installation
        print(f"{cli_info['cmd']} requires manual installation.")
        print(f"Please download and install from: {cli_info['install']}")
        print("After installation, restart your terminal.")
        input("Press Enter after installing...")
        
        # Verify installation
        if check_cli_installed(cli_info["cmd"]):
            print(f"{cli_info['cmd']} successfully installed!")
            return True
        else:
            print(f"{cli_info['cmd']} still not found. Please verify installation.")
            return False