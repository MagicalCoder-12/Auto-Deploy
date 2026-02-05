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
from core.git_handler import init_git_repo, is_git_repo, get_git_remote_url, git_add_and_commit, git_push_to_remote, has_uncommitted_changes, generate_commit_message
from core.builder import build_project
from core.deployer import deploy_to_platform, deploy_to_platform_flask, validate_deployment, check_paid_platform_confirmation
from core.model_selector import get_model_name

def ensure_git_ready_for_deployment(platform):
    """Ensure Git repository is ready for deployment (fully automated, no prompts)."""
    # Platforms that require Git
    git_required_platforms = ["GitHub Pages", "Render"]
    
    if platform not in git_required_platforms:
        return True
    
    print(f"\nEnsuring Git repository is ready for {platform} deployment...")
    
    # Check if this is a Git repository, if not initialize it
    if not is_git_repo():
        print(f"{platform} requires a Git repository. Initializing one...")
        if not init_git_repo(auto_init=True):
            print("Failed to initialize Git repository.")
            return False
    
    # Check if there's a remote URL configured
    remote_url = get_git_remote_url()
    if not remote_url:
        print(f"⚠️  No remote repository configured for {platform}.")
        print("Set up a remote with: git remote add origin <your-repo-url>")
        return False  # Cannot auto-configure remote without user input
    
    print(f"✓ Connected to remote: {remote_url}")
    
    # Auto-detect changes, commit, and push (no prompts)
    if has_uncommitted_changes():
        print("Detected changes. Auto-committing...")
        commit_msg = generate_commit_message()
        print(f"  Commit message: {commit_msg}")
        if not git_add_and_commit(commit_msg):
            print("Failed to commit changes.")
            return False
        
        print("Pushing to remote...")
        if not git_push_to_remote():
            print("Failed to push to remote repository.")
            return False
    else:
        print("✓ No changes to commit.")
    
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

    # 6. Initialize git repo (auto-init if not already initialized)
    print("\nInitializing Git repository...")
    if not init_git_repo(auto_init=True):
        print("⚠️  Git initialization skipped or failed.")
    
    # 7. For platforms that require Git, ensure repository is ready for deployment
    if not ensure_git_ready_for_deployment(platform):
        # The error message is handled within ensure_git_ready_for_deployment
        return
    
    # 8. Auto-commit any remaining project changes before build/deploy (universal for all platforms)
    if is_git_repo() and has_uncommitted_changes():
        print("\nAuto-committing project changes...")
        commit_msg = generate_commit_message()
        print(f"  Commit: {commit_msg}")
        git_add_and_commit(commit_msg)
        
        # Push if remote is configured
        if get_git_remote_url():
            print("Pushing to remote...")
            git_push_to_remote()

    # 9. Build project if necessary
    print("\nBuilding project...")
    if not build_project(project_type):
        print("Build failed. Cannot proceed.")
        return

    # 10. Deploy to the selected platform
    print(f"\nDeploying to {platform}...")
    if project_type == "python-flask":
        success = deploy_to_platform_flask(platform)
    else:
        success = deploy_to_platform(platform)

    if success:
        print(f"\n✓ Deployment to {platform} completed successfully!")
        
        # 11. Validate deployment
        validate_deployment(platform, project_type)
        
        print("\nThank you for using Auto Deploy Agent CLI!")
        print("Your project is now live and automatically deployed.")
        
        # 12. For Netlify, show final status
        if platform == "Netlify":
            print("\n" + "="*75)
            print("NETLIFY DEPLOYMENT STATUS")
            print("="*75)
            try:
                import subprocess
                        status_result = subprocess.run(["netlify", "status"], capture_output=True, text=False, shell=False, timeout=30)
                        if status_result.returncode == 0:
                            out = status_result.stdout
                            if isinstance(out, (bytes, bytearray)):
                                out = out.decode('utf-8', errors='replace')
                            else:
                                out = str(out)
                            print(out)
                else:
                    print("Could not retrieve status from Netlify CLI")
            except Exception as e:
                print(f"Status check skipped: {e}")
    else:
        print(f"\n✗ Deployment failed.")
        print("Troubleshooting: Check CLI login, internet, project setup.")
        print("Try manual deploy via platform dashboard.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()