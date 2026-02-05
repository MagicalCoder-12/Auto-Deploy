#!/usr/bin/env python3
"""
Auto Deploy Agent CLI - Automatically detect, build, and deploy web projects

This is the legacy monolithic version. For the modular version, please use:
python main.py
"""

# For backward compatibility, import and run the main function
from main import main

# Expose main function for CLI entry point
def main():
    """Main entry point for the CLI tool."""
    from main import main as _main
    _main()

if __name__ == "__main__":
    main()