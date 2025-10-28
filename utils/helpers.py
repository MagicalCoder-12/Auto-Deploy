#!/usr/bin/env python3
"""Utility functions for Auto Deploy Agent"""

def sanitize_project_name(name):
    """Sanitize project name for use in file names and URLs."""
    return name.lower().replace(" ", "-").replace("_", "-")

def get_project_name():
    """Get the current project name from the directory name."""
    import os
    return os.path.basename(os.getcwd())