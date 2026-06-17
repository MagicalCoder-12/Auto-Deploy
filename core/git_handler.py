#!/usr/bin/env python3
"""Git operations module for Auto Deploy Agent - Production Ready Version

This module provides robust Git operations with human-in-the-loop verification,
proper error handling, timeout management, and comprehensive logging for real-time
application deployments.
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from config import PROJECT_DIR


class GitOperationError(Exception):
    """Custom exception for Git operation failures."""
    pass


class GitHandler:
    """Production-ready Git handler with human-in-the-loop verification."""
    
    def __init__(self, project_dir: Optional[Path] = None):
        self.project_dir = project_dir or PROJECT_DIR
        self.git_available = self._check_git_installed()
        
    def _check_git_installed(self) -> bool:
        """Check if git is installed and available."""
        try:
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_dir
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return False
    
    def check_and_install_git(self) -> bool:
        """Check if git is installed, guide user to install if not."""
        if self.git_available:
            return True
        
        print("\n⚠️  Git is not installed or not found in PATH.")
        print("Git is required for deployment to most platforms.")
        print("\nPlease install Git:")
        print("  - Windows: https://git-scm.com/download/win")
        print("  - macOS: brew install git")
        print("  - Linux: sudo apt-get install git")
        print("\nAfter installation, restart this tool.")
        
        return False
    
    def is_git_repo(self) -> bool:
        """Check if the current directory is a Git repository."""
        git_dir = self.project_dir / ".git"
        return git_dir.exists() and git_dir.is_dir()
    
    def get_git_status(self) -> Dict[str, Any]:
        """Get detailed git status including staged/unstaged changes."""
        if not self.is_git_repo():
            return {"is_repo": False, "error": "Not a git repository"}
        
        try:
            # Get staged files
            staged_result = subprocess.run(
                ["git", "diff", "--name-only", "--cached"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_dir
            )
            staged_files = [f.strip() for f in staged_result.stdout.strip().split('\n') if f.strip()]
            
            # Get unstaged files
            unstaged_result = subprocess.run(
                ["git", "diff", "--name-only"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_dir
            )
            unstaged_files = [f.strip() for f in unstaged_result.stdout.strip().split('\n') if f.strip()]
            
            # Get untracked files
            untracked_result = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_dir
            )
            untracked_files = [f.strip() for f in untracked_result.stdout.strip().split('\n') if f.strip()]
            
            # Get current branch
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_dir
            )
            current_branch = branch_result.stdout.strip() or "unknown"
            
            # Get remote URL
            remote_url = self.get_git_remote_url()
            
            # Get last commit info
            last_commit = self._get_last_commit_info()
            
            return {
                "is_repo": True,
                "current_branch": current_branch,
                "remote_url": remote_url,
                "staged_files": staged_files,
                "unstaged_files": unstaged_files,
                "untracked_files": untracked_files,
                "has_changes": bool(staged_files or unstaged_files or untracked_files),
                "last_commit": last_commit
            }
            
        except subprocess.TimeoutExpired:
            return {"is_repo": True, "error": "Git status check timed out"}
        except Exception as e:
            return {"is_repo": True, "error": str(e)}
    
    def _get_last_commit_info(self) -> Optional[Dict[str, str]]:
        """Get information about the last commit."""
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--format=%H|%an|%ae|%ai|%s"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_dir
            )
            if result.returncode == 0 and result.stdout.strip():
                parts = result.stdout.strip().split('|', 4)
                if len(parts) == 5:
                    return {
                        "hash": parts[0][:8],
                        "author": parts[1],
                        "email": parts[2],
                        "date": parts[3],
                        "message": parts[4]
                    }
        except Exception:
            pass
        return None
    
    def get_git_remote_url(self) -> Optional[str]:
        """Get the remote URL of the Git repository if it exists."""
        if not self.is_git_repo():
            return None
        
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_dir
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except subprocess.TimeoutExpired:
            print("⚠️  Checking remote repository timed out")
        except Exception as e:
            print(f"⚠️  Error checking remote repository: {e}")
        return None
    
    def show_commit_preview(self, files: List[str], commit_message: str) -> None:
        """Display a preview of what will be committed for human verification."""
        print("\n" + "="*75)
        print("📋 GIT COMMIT PREVIEW - HUMAN VERIFICATION REQUIRED")
        print("="*75)
        print(f"\nProposed commit message: \"{commit_message}\"")
        print(f"\nFiles to be committed ({len(files)} files):\n")
        
        if not files:
            print("  No files to commit.")
        else:
            # Categorize files for better readability
            categories = {
                "Source Code": [],
                "Configuration": [],
                "Documentation": [],
                "Dependencies": [],
                "Other": []
            }
            
            for file in files:
                if any(file.endswith(ext) for ext in ['.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css']):
                    categories["Source Code"].append(file)
                elif any(x in file.lower() for x in ['config', '.json', '.yaml', '.yml', '.env', 'requirements', 'package']):
                    categories["Configuration"].append(file)
                elif any(file.endswith(ext) for ext in ['.md', '.rst', '.txt']):
                    categories["Documentation"].append(file)
                elif any(x in file for x in ['node_modules', 'vendor', 'lock']):
                    categories["Dependencies"].append(file)
                else:
                    categories["Other"].append(file)
            
            for category, cat_files in categories.items():
                if cat_files:
                    print(f"  {category}:")
                    for f in cat_files[:10]:  # Show first 10 in each category
                        print(f"    + {f}")
                    if len(cat_files) > 10:
                        print(f"    ... and {len(cat_files) - 10} more")
        
        # Show diff summary if possible
        print("\nChange summary:")
        try:
            diff_result = subprocess.run(
                ["git", "diff", "--stat", "--cached"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_dir
            )
            if diff_result.stdout.strip():
                print(f"  {diff_result.stdout.strip()}")
            else:
                # Try unstaged diff
                diff_result = subprocess.run(
                    ["git", "diff", "--stat"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    cwd=self.project_dir
                )
                if diff_result.stdout.strip():
                    print(f"  {diff_result.stdout.strip()}")
        except Exception:
            print("  Could not retrieve diff statistics")
        
        print("\n" + "="*75)
    
    def generate_commit_message(self, use_ai: bool = True) -> str:
        """Generate a meaningful commit message using AI (with fallback)."""
        if not self.is_git_repo():
            return "Initial commit"
        
        try:
            # Get all changed files
            status = self.get_git_status()
            if not status.get("is_repo"):
                return "Auto-generated commit"
            
            all_files = (
                status.get("staged_files", []) + 
                status.get("unstaged_files", []) + 
                status.get("untracked_files", [])
            )
            all_files = [f for f in all_files if f]
            
            if not all_files:
                return "Update project files"
            
            # Try AI-generated message if requested
            if use_ai:
                ai_message = self._generate_ai_commit_message(all_files)
                if ai_message:
                    return ai_message
            
            # Fallback: Rule-based message generation
            return self._generate_rule_based_commit_message(all_files)
            
        except Exception as e:
            print(f"⚠️  Error generating commit message: {e}")
            return "Auto-generated commit"
    
    def _generate_ai_commit_message(self, files: List[str]) -> Optional[str]:
        """Attempt to generate commit message using Ollama."""
        try:
            import ollama
            from config import OLLAMA_MODEL
            
            # Get git diff content
            diff_result = subprocess.run(
                ["git", "diff", "--no-color", "HEAD"],
                capture_output=True,
                text=True,
                timeout=15,
                cwd=self.project_dir
            )
            diff_content = diff_result.stdout[:2000]  # Limit to avoid token overflow
            
            files_list = ", ".join(files[:10])
            
            prompt = f"""Analyze these git changes and generate a concise, conventional commit message.
Format: type: description (max 50 characters)
Files changed: {files_list}
{'...' if len(files) > 10 else ''}

Diff preview:
{diff_content}

Generate ONLY the commit message. No extra text, no quotes."""
            
            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}],
                options={"timeout": 10}
            )
            
            commit_msg = response["message"]["content"].strip()
            # Clean up the message
            commit_msg = commit_msg.replace('"', '').replace("'", "").strip()
            
            # Validate message
            if commit_msg and 0 < len(commit_msg) < 200:
                return commit_msg
                
        except ImportError:
            pass  # ollama not installed
        except Exception as e:
            print(f"⚠️  AI commit message generation failed: {e}")
        
        return None
    
    def _generate_rule_based_commit_message(self, files: List[str]) -> str:
        """Generate commit message based on file patterns."""
        config_files = [f for f in files if any(x in f.lower() for x in ['config', '.env', '.json', 'requirements', 'package'])]
        src_files = [f for f in files if any(x in f for x in ['src/', 'app.py', 'index', '.py', '.js', '.ts', '.jsx', '.tsx'])]
        doc_files = [f for f in files if any(x in f for x in ['README', '.md', 'docs/', 'CHANGELOG'])]
        deploy_files = [f for f in files if any(x in f for x in ['vercel', 'netlify', 'deploy', '.github', 'Dockerfile'])]
        
        # Prioritize certain file types
        if deploy_files and len(files) <= 3:
            return "chore: update deployment configuration"
        elif config_files and src_files:
            return "feat: update application code and configuration"
        elif src_files:
            change_type = "feat" if len(src_files) > 1 else "fix"
            return f"{change_type}: update application code ({len(src_files)} files)"
        elif config_files:
            return "chore: update configuration files"
        elif doc_files:
            return "docs: update documentation"
        else:
            return f"chore: update project files ({len(files)} files)"
    
    def git_add_all(self) -> Tuple[bool, List[str]]:
        """Add all files to staging area. Returns (success, list of added files)."""
        if not self.is_git_repo():
            return False, []
        
        try:
            # First add all files
            result = subprocess.run(
                ["git", "add", "-A"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.project_dir
            )
            
            if result.returncode != 0 and "nothing to commit" not in result.stderr:
                print(f"⚠️  Error adding files: {result.stderr}")
                return False, []
            
            # Get list of staged files
            diff_result = subprocess.run(
                ["git", "diff", "--name-only", "--cached"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_dir
            )
            staged_files = [f.strip() for f in diff_result.stdout.strip().split('\n') if f.strip()]
            
            return True, staged_files
            
        except subprocess.TimeoutExpired:
            print("⚠️  Git add operation timed out")
            return False, []
        except Exception as e:
            print(f"⚠️  Error adding files: {e}")
            return False, []
    
    def git_commit(self, message: str, allow_empty: bool = False) -> bool:
        """Commit staged changes with the given message."""
        if not self.is_git_repo():
            return False
        
        try:
            cmd = ["git", "commit", "-m", message]
            if allow_empty:
                cmd.append("--allow-empty")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.project_dir
            )
            
            if result.returncode == 0:
                print(f"✓ Committed: {message}")
                return True
            elif "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                print("ℹ️  No changes to commit")
                return True
            else:
                print(f"⚠️  Commit failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("⚠️  Git commit timed out")
            return False
        except Exception as e:
            print(f"⚠️  Git commit error: {e}")
            return False
    
    def git_push(self, branch: str = "main", force: bool = False) -> bool:
        """Push changes to remote repository."""
        if not self.is_git_repo():
            return False
        
        remote_url = self.get_git_remote_url()
        if not remote_url:
            print("⚠️  No remote repository configured")
            return False
        
        try:
            print(f"Pushing to remote ({branch})...")
            cmd = ["git", "push", "-u", "origin", branch]
            if force:
                cmd.insert(2, "-f")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=self.project_dir
            )
            
            if result.returncode == 0:
                print("✓ Pushed to remote repository")
                return True
            else:
                print(f"⚠️  Push failed: {result.stderr}")
                # Check for common issues
                if "Authentication failed" in result.stderr or "could not read Username" in result.stderr:
                    print("ℹ️  Authentication issue - please ensure you're logged in to your Git provider")
                elif "rejected" in result.stderr:
                    print("ℹ️  Remote has changes - try pulling first or use force push")
                return False
                
        except subprocess.TimeoutExpired:
            print("⚠️  Git push timed out")
            return False
        except Exception as e:
            print(f"⚠️  Git push error: {e}")
            return False
    
    def init_repo(self, auto_init: bool = False, set_remote: Optional[str] = None) -> bool:
        """Initialize a git repository with optional remote configuration."""
        
        if self.is_git_repo():
            print("ℹ️  Directory is already a git repository")
            remote_url = self.get_git_remote_url()
            if remote_url:
                print(f"✓ Remote configured: {remote_url}")
            return True
        
        if not auto_init:
            print("\n📁 This directory is not a git repository.")
            response = input("Initialize git repository? (y/n): ").lower().strip()
            if response not in ['y', 'yes']:
                return False
        
        print("Initializing git repository...")
        
        try:
            # Initialize repo
            result = subprocess.run(
                ["git", "init"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.project_dir
            )
            
            if result.returncode != 0:
                print(f"⚠️  Git init failed: {result.stderr}")
                return False
            
            # Set default branch to main
            subprocess.run(
                ["git", "branch", "-M", "main"],
                capture_output=True,
                timeout=10,
                cwd=self.project_dir
            )
            
            # Create .gitignore if needed
            self._create_gitignore()
            
            # Set remote if provided
            if set_remote:
                try:
                    subprocess.run(
                        ["git", "remote", "add", "origin", set_remote],
                        capture_output=True,
                        text=True,
                        timeout=10,
                        cwd=self.project_dir
                    )
                    print(f"✓ Remote configured: {set_remote}")
                except Exception as e:
                    print(f"⚠️  Could not set remote: {e}")
            
            print("✓ Git repository initialized")
            return True
            
        except subprocess.TimeoutExpired:
            print("⚠️  Git initialization timed out")
            return False
        except Exception as e:
            print(f"⚠️  Git init error: {e}")
            return False
    
    def _create_gitignore(self) -> None:
        """Create a .gitignore file if one doesn't exist."""
        gitignore_path = self.project_dir / ".gitignore"
        
        if gitignore_path.exists():
            return
        
        # Comprehensive gitignore content
        gitignore_content = """# Dependencies
node_modules/
.pnp
.pnp.js

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
.venv
venv/
ENV/

# Build outputs
dist/
build/
.next/
.nuxt/
out/
.cache/

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage
coverage/
*.lcov
.nyc_output/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
.pytest_cache/
.mypy_cache/

# Node
.npm
.eslintcache
.parcel-cache

# Temporary files
tmp/
temp/
"""
        
        try:
            with open(gitignore_path, "w") as f:
                f.write(gitignore_content)
            print("✓ Created .gitignore")
        except Exception as e:
            print(f"⚠️  Could not create .gitignore: {e}")
    
    def human_in_the_loop_commit(self, commit_message: Optional[str] = None, 
                                  require_approval: bool = True) -> bool:
        """
        Perform a commit with human-in-the-loop verification.
        
        This is the main method for production use - it shows what will be
        committed and requires user approval before proceeding.
        
        Args:
            commit_message: Optional custom commit message. If None, auto-generated.
            require_approval: If True, requires user confirmation before committing.
        
        Returns:
            bool: True if commit was successful, False otherwise.
        """
        if not self.is_git_repo():
            print("⚠️  Not a git repository. Cannot commit.")
            return False
        
        # Stage all changes
        print("\nStaging changes...")
        success, staged_files = self.git_add_all()
        
        if not success:
            print("⚠️  Failed to stage changes")
            return False
        
        if not staged_files:
            print("ℹ️  No changes to commit")
            return True
        
        # Generate or use provided commit message
        if not commit_message:
            commit_message = self.generate_commit_message(use_ai=True)
        
        # Show preview for human verification
        self.show_commit_preview(staged_files, commit_message)
        
        if require_approval:
            print("\nOptions:")
            print("  [Y] Yes, commit these changes")
            print("  [N] No, skip commit")
            print("  [E] Edit commit message")
            print("  [V] View detailed diff")
            
            while True:
                choice = input("\nYour choice [Y/N/E/V]: ").lower().strip()
                
                if choice in ['y', 'yes']:
                    break
                elif choice in ['n', 'no']:
                    print("ℹ️  Commit skipped")
                    return True  # Not an error, just skipped
                elif choice == 'e':
                    new_message = input("Enter commit message: ").strip()
                    if new_message:
                        commit_message = new_message
                        self.show_commit_preview(staged_files, commit_message)
                elif choice == 'v':
                    self._show_detailed_diff()
                else:
                    print("Invalid choice. Please enter Y, N, E, or V.")
        
        # Perform the commit
        print("\nCommitting changes...")
        return self.git_commit(commit_message)
    
    def _show_detailed_diff(self) -> None:
        """Show detailed diff of staged changes."""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--color=never"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.project_dir
            )
            if result.stdout:
                print("\n" + "-"*75)
                print(result.stdout)
                print("-"*75)
            else:
                print("No staged changes to show diff for.")
        except Exception as e:
            print(f"⚠️  Could not show diff: {e}")


# Legacy function wrappers for backward compatibility
def check_and_install_git():
    """Legacy wrapper - use GitHandler class instead."""
    handler = GitHandler()
    return handler.check_and_install_git()

def is_git_repo():
    """Legacy wrapper - use GitHandler class instead."""
    handler = GitHandler()
    return handler.is_git_repo()

def get_git_remote_url():
    """Legacy wrapper - use GitHandler class instead."""
    handler = GitHandler()
    return handler.get_git_remote_url()

def has_uncommitted_changes():
    """Legacy wrapper - use GitHandler class instead."""
    handler = GitHandler()
    status = handler.get_git_status()
    return status.get("has_changes", False)

def generate_commit_message():
    """Legacy wrapper - use GitHandler class instead."""
    handler = GitHandler()
    return handler.generate_commit_message()

def git_add_and_commit(commit_message="Initial commit"):
    """Legacy wrapper - use GitHandler.human_in_the_loop_commit() instead."""
    handler = GitHandler()
    return handler.human_in_the_loop_commit(commit_message, require_approval=False)

def git_push_to_remote():
    """Legacy wrapper - use GitHandler.git_push() instead."""
    handler = GitHandler()
    return handler.git_push()

def init_git_repo(auto_init=False):
    """Legacy wrapper - use GitHandler.init_repo() instead."""
    handler = GitHandler()
    return handler.init_repo(auto_init=auto_init)