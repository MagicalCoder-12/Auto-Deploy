#!/usr/bin/env python3
"""Main entry point for Auto Deploy Agent CLI"""

import time
from config import PROJECT_DIR
from core.detector import detect_project_type
from core.recommender import recommend_platform
from core.cli_manager import install_cli
from core.file_manager import create_required_files
from core.git_handler import init_git_repo
from core.builder import build_project
from core.deployer import deploy_to_platform, deploy_to_platform_flask, validate_deployment

def main():
    print("🚀 Welcome to the Auto Deploy Agent CLI!")
    print(f"Scanning project in: {PROJECT_DIR}")
    
    # Add a small delay to let user read the welcome message
    time.sleep(1)

    # 1. Detect project type using Llama3
    project_type = detect_project_type()
    print(f"🔍 Detected project type: {project_type}")

    if project_type == "unknown":
        print("❓ Could not detect project type. Is this a web project?")
        return

    # 2. Recommend platform using Llama3
    rec = recommend_platform(project_type)
    platform = rec["platform"]
    print(f"\n💡 Recommended platform: {platform}")
    print(f"   Reason: {rec['reason']}")
    print("\n📋 Setup steps:")
    for i, step in enumerate(rec["setup_steps"], 1):
        print(f"   {i}. {step}")

    # 3. Check and install CLI tools with user permission
    print(f"\n🔧 Checking if {platform} CLI is installed...")
    if not install_cli(platform):
        print("❌ CLI installation failed. Cannot proceed.")
        return

    # 4. Create required deployment files
    print("\n📄 Creating required deployment files...")
    if not create_required_files(project_type, platform):
        print("❌ Failed to create required files. Cannot proceed.")
        return

    # 5. Initialize git repo with user permission and connect to remote
    print("\n🔧 Initializing Git repository...")
    if not init_git_repo():
        print("❌ Git repo init skipped/failed. Cannot proceed.")
        return

    # 6. Build project if necessary
    print("\n🔨 Building project...")
    if not build_project(project_type):
        print("❌ Build failed. Cannot proceed.")
        return

    # 7. Deploy to the selected platform
    print(f"\n🚀 Deploying to {platform}...")
    if project_type == "python-flask":
        success = deploy_to_platform_flask(platform)
    else:
        success = deploy_to_platform(platform)

    if success:
        print(f"\n🎉 Deployment to {platform} completed successfully!")
        if platform in ["GitHub Pages", "Render"]:
            print("💡 Note: For git-based platforms, push changes for updates.")
        
        # 8. Validate deployment
        validate_deployment(platform, project_type)
        
        print("\n🎊 Thank you for using Auto Deploy Agent CLI!")
        print("   If you have any issues or suggestions, please let us know.")
    else:
        print(f"\n❌ Deployment failed.")
        print("Troubleshooting: Check CLI login, internet, project setup.")
        print("Try manual deploy via platform dashboard.")

if __name__ == "__main__":
    main()