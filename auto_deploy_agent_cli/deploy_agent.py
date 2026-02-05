#!/usr/bin/env python3
"""
Auto Deploy Agent CLI - Automatically detect, build, and deploy web projects

This is the legacy monolithic version. For the modular version, please use:
python main.py
"""

# Expose main function for CLI entry point
def main():
    """Main entry point for the CLI tool."""
    # Import main function locally to avoid circular imports
    import sys
    import os
    # Add parent directory to path to import main
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from main import main as _main
    _main()

if __name__ == "__main__":
    main()