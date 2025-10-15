#!/usr/bin/env python3
"""
Demo script showing how to use the deploy agent.
"""

import os
import sys
from pathlib import Path

def demo():
    """Demonstrate the deploy agent."""
    print("🚀 Deploy Agent Demo")
    print("=" * 30)
    print()
    
    # Explanation of what the deploy agent does
    print("The deploy agent is a smart deployment tool that:")
    print("1. Automatically detects your project type")
    print("2. Recommends the best hosting platform using AI")
    print("3. Guides you through the deployment process")
    print()
    
    # Show available test projects
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_projects = [
        ("Static HTML Project", "test-project"),
        ("React Project", "react-test-project"),
        ("Vite Project", "vite-test-project"),
        ("Flask Project", "flask-test-project"),
    ]
    
    print("📁 Available Test Projects:")
    for i, (name, folder) in enumerate(test_projects, 1):
        path = os.path.join(base_dir, folder)
        status = "✅ Available" if os.path.exists(path) else "❌ Not found"
        print(f"  {i}. {name} - {status}")
    
    print()
    print("💡 To deploy any project:")
    print("   1. Navigate to the project directory")
    print("   2. Run: python ../deploy_agent.py")
    print()
    print("The deploy agent will:")
    print("   • Detect your project type")
    print("   • Recommend the best hosting platform")
    print("   • Guide you through installation of required tools")
    print("   • Help you deploy your site")
    print()
    
    print("🌐 Supported Platforms:")
    platforms = ["Netlify", "Vercel", "GitHub Pages", "Cloudflare Pages", "Render"]
    for platform in platforms:
        print(f"   • {platform}")
    
    print()
    print("✨ Features:")
    print("   • AI-powered platform recommendations")
    print("   • Automatic project type detection")
    print("   • Step-by-step deployment guidance")
    print("   • Support for multiple project types and platforms")

if __name__ == "__main__":
    demo()