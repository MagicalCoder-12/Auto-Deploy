#!/usr/bin/env python3
"""
Test script to demonstrate the deploy agent functionality without actual deployment.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to sys.path to import deploy_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import deploy_agent

def test_detect_project_type():
    """Test project type detection."""
    print("🧪 Testing Project Type Detection")
    print("=" * 40)
    
    # Get the base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Test with our sample projects
    test_cases = [
        ("Static HTML Project", os.path.join(base_dir, "test-project")),
        ("React Project", os.path.join(base_dir, "react-test-project")),
        ("Vite Project", os.path.join(base_dir, "vite-test-project")),
        ("Flask Project", os.path.join(base_dir, "flask-test-project")),
    ]
    
    for name, path in test_cases:
        if os.path.exists(path):
            # Change to the project directory
            original_cwd = os.getcwd()
            os.chdir(path)
            deploy_agent.PROJECT_DIR = Path.cwd()
            
            # Detect project type
            project_type = deploy_agent.detect_project_type()
            print(f"{name}: {project_type}")
            
            # Return to original directory
            os.chdir(original_cwd)
        else:
            print(f"{name}: Path not found ({path})")
    
    print()

def test_recommend_platform():
    """Test platform recommendation."""
    print("🤖 Testing Platform Recommendations")
    print("=" * 40)
    
    project_types = ["static", "react", "vite", "nextjs", "python-flask"]
    
    for project_type in project_types:
        try:
            print(f"Project Type: {project_type}")
            rec = deploy_agent.recommend_platform(project_type)
            print(f"  Recommended Platform: {rec['platform']}")
            print(f"  Reason: {rec['reason']}")
            print(f"  Setup Steps: {', '.join(rec['setup_steps'])}")
            print()
        except Exception as e:
            print(f"  Error getting recommendation for {project_type}: {e}")
            print()

def test_deployment_functions():
    """Test deployment functions."""
    print("📦 Testing Deployment Functions")
    print("=" * 40)
    
    platforms = ["Netlify", "Vercel", "GitHub Pages", "Cloudflare Pages", "Render"]
    
    for platform in platforms:
        print(f"Testing deployment function for {platform}")
        # Just test that the function exists and can be called
        # We won't actually run the deployment
        try:
            func_name = f"deploy_to_{platform.lower().replace(' ', '_')}"
            if hasattr(deploy_agent, func_name):
                print(f"  ✅ Function {func_name} exists")
            else:
                print(f"  ❌ Function {func_name} not found")
        except Exception as e:
            print(f"  ❌ Error testing {platform}: {e}")
        print()

def main():
    """Run all tests."""
    print("🚀 Deploy Agent Test Suite")
    print("=" * 50)
    print()
    
    test_detect_project_type()
    test_recommend_platform()
    test_deployment_functions()
    
    print("🏁 All tests completed!")

if __name__ == "__main__":
    main()