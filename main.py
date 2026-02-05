#!/usr/bin/env python3
"""Main entry point for Auto Deploy Agent CLI"""

import time
import sys

from config import PROJECT_DIR
try:
    from dotenv import load_dotenv
    from pathlib import Path
    # Load .env from the project root (same directory as this file)
    base_dir = Path(__file__).resolve().parent
    load_dotenv(dotenv_path=base_dir / ".env")
except ImportError:
    print("python-dotenv not installed; .env will not be loaded automatically. Run: pip install python-dotenv")
from core.detector import detect_project_type
from core.recommender import recommend_platform
from core.cli_manager import install_cli
from core.file_manager import create_required_files
from core.git_handler import init_git_repo, is_git_repo, get_git_remote_url, git_add_and_commit, git_push_to_remote, has_uncommitted_changes
from core.builder import build_project
from core.deployer import deploy_to_platform, deploy_to_platform_flask, validate_deployment, check_paid_platform_confirmation
from core.model_selector import get_model_name

def ensure_git_ready_for_deployment(platform):
    """Ensure Git repository is ready for deployment to Git-dependent platforms."""
    # Platforms that require Git
    git_required_platforms = ["GitHub Pages", "Render"]
    
    if platform not in git_required_platforms:
        return True
    
    print(f"\nEnsuring Git repository is ready for {platform} deployment...")
    
    # Check if this is a Git repository
    if not is_git_repo():
        print(f"{platform} requires a Git repository, but this directory is not a Git repository.")
        permission = input("Do you want me to initialize a git repository for this project? (y/n): ")
        if permission.lower() != 'y':
            print("\nNo problem! Git repository initialization was skipped as requested. Since GitHub Pages requires a Git repository, deployment cannot continue.")
            print("Thanks for trying Auto Deploy Agent — see you next deploy 🚀")
            return False
            
        # Initialize Git repository
        if not init_git_repo():
            print("Failed to initialize Git repository.")
            return False
    
    # Check if there's a remote URL
    remote_url = get_git_remote_url()
    if not remote_url:
        print(f"{platform} requires a remote Git repository, but none is configured.")
        repo_url = input("Enter your remote Git repository URL (e.g., https://github.com/user/repo.git): ").strip()
        if not repo_url:
            print("Cannot proceed with deployment without remote repository.")
            return False
            
        try:
            import subprocess
            subprocess.run(f"git remote add origin {repo_url}", check=True, shell=True, timeout=30)
            subprocess.run("git branch -M main", check=True, shell=True, timeout=30)
        except Exception as e:
            print(f"Failed to configure remote repository: {e}")
            return False
    
    # Check for uncommitted changes and commit them
    if has_uncommitted_changes():
        print("Found uncommitted changes. Committing them before deployment...")
        commit_msg = input("Enter commit message (default: 'Prepare for deployment'): ") or "Prepare for deployment"
        if not git_add_and_commit(commit_msg):
            print("Failed to commit changes.")
            return False
    else:
        print("No changes to commit.")
    
    # Push to remote repository
    push_permission = input("Do you want to push changes to the remote repository before deployment? (y/n): ")
    if push_permission.lower() == 'y':
        if not git_push_to_remote():
            print("Failed to push to remote repository.")
            return False
    
    return True

def main():
    # Ensure stdout and stderr are properly encoded
    if sys.stdout.encoding is None:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if sys.stderr.encoding is None:
        import io
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    print("Welcome to the Auto Deploy Agent CLI!")
    print(f"Scanning project in: {PROJECT_DIR}")
    
    # Select Ollama model
    selected_model = get_model_name()
    # Update the config with the selected model
    import config
    setattr(config, 'OLLAMA_MODEL', selected_model)
    
    # Add a small delay to let user read the welcome message
    time.sleep(1)

    # 1. Detect project type using Llama3
    project_type = detect_project_type()
    print(f"Detected project type: {project_type}")

    if project_type == "unknown":
        print("Could not detect project type. Is this a web project?")
        return

    # 2. Recommend platform using Llama3
    rec = recommend_platform(project_type)
    platform = rec["platform"]
    print(f"\nRecommended platform: {platform}")
    print(f"   Reason: {rec['reason']}")
    print("\nSetup steps:")
    for i, step in enumerate(rec["setup_steps"], 1):
        print(f"   {i}. {step}")

    # 3. Check for paid platform and get user confirmation
    if not check_paid_platform_confirmation(platform):
        print("\nLooking for an alternative free platform...")
        # If user declined paid platform, recommend an alternative
        rec = recommend_platform(project_type)  # This will still suggest free platforms only
        platform = rec["platform"]
        print(f"\nRecommended alternative platform: {platform}")
        print(f"   Reason: {rec['reason']}")
        print("\nSetup steps:")
        for i, step in enumerate(rec["setup_steps"], 1):
            print(f"   {i}. {step}")

    # 4. Check and install CLI tools with user permission
    print(f"\nChecking if {platform} CLI is installed...")
    if not install_cli(platform):
        print("CLI installation failed. Cannot proceed.")
        return

    # 5. Create required deployment files
    print("\nCreating required deployment files...")
    if not create_required_files(project_type, platform):
        print("Failed to create required files. Cannot proceed.")
        return

    # 6. Initialize git repo with user permission and connect to remote
    print("\nInitializing Git repository...")
    if not init_git_repo():
        print("\nNo problem! Git repository initialization was skipped as requested. Since GitHub Pages requires a Git repository, deployment cannot continue.")
        print("Thanks for trying Auto Deploy Agent — see you next deploy 🚀")
        return

    # 7. For platforms that require Git, ensure repository is ready for deployment
    if not ensure_git_ready_for_deployment(platform):
        # The error message is handled within ensure_git_ready_for_deployment
        return

    # 8. Build project if necessary
    print("\nBuilding project...")
    if not build_project(project_type):
        print("Build failed. Cannot proceed.")
        return

    # 9. Deploy to the selected platform
    print(f"\nDeploying to {platform}...")
    if project_type == "python-flask":
        success = deploy_to_platform_flask(platform)
    else:
        success = deploy_to_platform(platform)

    if success:
        print(f"\nDeployment to {platform} completed successfully!")
        if platform in ["GitHub Pages", "Render"]:
            print("Note: For git-based platforms, push changes for updates.")
        
        # 10. Validate deployment
        validate_deployment(platform, project_type)
        
        print("\nThank you for using Auto Deploy Agent CLI!")
        print("   If you have any issues or suggestions, please let us know.")
    else:
        print(f"\nDeployment failed.")
        print("Troubleshooting: Check CLI login, internet, project setup.")
        print("Try manual deploy via platform dashboard.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()