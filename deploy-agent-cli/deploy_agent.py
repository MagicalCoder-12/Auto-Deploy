#!/usr/bin/env python3
"""
Auto Deploy Agent CLI - Automatically detect, build, and deploy web projects
"""

import os
import json
import subprocess
import sys
from pathlib import Path

# Use Ollama for smart decisions
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

PROJECT_DIR = Path.cwd()

def detect_project_type():
    """Detect what kind of web project this is."""
    files = [f.name for f in PROJECT_DIR.iterdir() if f.is_file()]
    folders = [f.name for f in PROJECT_DIR.iterdir() if f.is_dir()]

    if "package.json" in files:
        try:
            with open("package.json") as f:
                pkg = json.load(f)
                if "next" in pkg.get("dependencies", {}):
                    return "nextjs"
                elif "vite" in pkg.get("devDependencies", {}):
                    return "vite"
                elif "react" in pkg.get("dependencies", {}):
                    return "react"
        except json.JSONDecodeError:
            pass
    
    if "index.html" in files:
        return "static"
    
    if "requirements.txt" in files:
        return "python-flask"  # e.g., for Render
    
    return "unknown"

def recommend_platform(project_type):
    """Recommend a platform based on project type."""
    recommendations = {
        "nextjs": {
            "platform": "Vercel",
            "reason": "Vercel is the creators of Next.js and provides the best hosting experience",
            "setup_steps": [
                "Install Vercel CLI: npm install -g vercel",
                "Login to Vercel: vercel login",
                "Deploy: vercel --prod"
            ]
        },
        "vite": {
            "platform": "Netlify",
            "reason": "Netlify provides excellent support for modern static sites built with Vite",
            "setup_steps": [
                "Install Netlify CLI: npm install -g netlify-cli",
                "Login to Netlify: netlify login",
                "Deploy: netlify deploy --prod"
            ]
        },
        "react": {
            "platform": "Netlify",
            "reason": "Netlify offers great React support with automatic builds and deployments",
            "setup_steps": [
                "Install Netlify CLI: npm install -g netlify-cli",
                "Login to Netlify: netlify login",
                "Deploy: netlify deploy --prod"
            ]
        },
        "static": {
            "platform": "GitHub Pages",
            "reason": "GitHub Pages is perfect for static sites with no build requirements",
            "setup_steps": [
                "Ensure your site is in a GitHub repository",
                "Go to repository Settings > Pages",
                "Select source branch and folder",
                "Push to GitHub to deploy"
            ]
        },
        "python-flask": {
            "platform": "Render",
            "reason": "Render provides excellent support for Python web applications",
            "setup_steps": [
                "Create an account at render.com",
                "Connect your Git repository",
                "Set environment to Python",
                "Set build command to: pip install -r requirements.txt",
                "Set start command to: gunicorn app:app"
            ]
        }
    }
    
    return recommendations.get(project_type, {
        "platform": "Vercel",
        "reason": "Vercel supports most web frameworks and provides a great developer experience",
        "setup_steps": [
            "Install Vercel CLI: npm install -g vercel",
            "Login to Vercel: vercel login",
            "Deploy: vercel --prod"
        ]
    })

def install_cli(platform):
    """Guide user to install CLI."""
    cli_map = {
        "Netlify": "npm install -g netlify-cli",
        "Vercel": "npm install -g vercel",
        "Cloudflare Pages": "npm install -g wrangler",
        "GitHub Pages": "No CLI needed — uses Git",
        "Render": "No CLI — uses API or Git"
    }
    cmd = cli_map.get(platform)
    if cmd:
        print(f"👉 Please run this to install the CLI:\n   {cmd}")
        print("   IMPORTANT: Open a NEW terminal/command prompt and run the command above.")
        print("   After installation is complete, return to this terminal and press Enter.")
        input("Press Enter after installing...")
    else:
        print(f"✅ {platform} doesn't require a CLI.")

def check_node_installed():
    """Check if Node.js and npm are installed and accessible."""
    try:
        # Try to get node version
        node_result = subprocess.run("node --version", capture_output=True, text=True, shell=True)
        if node_result.returncode == 0:
            print(f"✅ Node.js version: {node_result.stdout.strip()}")
        else:
            print("❌ Node.js not found or not accessible.")
            print(f"   Error: {node_result.stderr}")
            return False
            
        # Try to get npm version
        npm_result = subprocess.run("npm --version", capture_output=True, text=True, shell=True)
        if npm_result.returncode == 0:
            print(f"✅ npm version: {npm_result.stdout.strip()}")
            return True
        else:
            print("❌ npm not found or not accessible.")
            print(f"   Error: {npm_result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error checking Node.js/npm: {e}")
        return False

def install_dependencies():
    """Install project dependencies."""
    print("📦 Installing project dependencies...")
    try:
        result = subprocess.run("npm install", capture_output=True, text=True, shell=True, cwd=PROJECT_DIR)
        if result.returncode == 0:
            print("✅ Dependencies installed successfully!")
            return True
        else:
            print("⚠️ Failed to install dependencies:")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def build_project(project_type):
    """Build the project if necessary."""
    print("🔨 Building project...")
    
    # Check if Node.js/npm are available first
    if project_type in ["nextjs", "vite", "react"]:
        if not check_node_installed():
            print("⚠️  Node.js is required for this project type but not found.")
            print("   Please install Node.js from https://nodejs.org/")
            print("   After installation, you may need to restart your terminal/command prompt.")
            retry = input("Would you like to check again? (y/n): ")
            if retry.lower() == 'y':
                if not check_node_installed():
                    return False
            else:
                return False
        
        # Check if node_modules exists, if not, install dependencies
        if not os.path.exists("node_modules"):
            print("⚠️ node_modules not found. Installing dependencies first...")
            if not install_dependencies():
                print("❌ Failed to install dependencies. Cannot proceed with build.")
                return False
    
    if project_type in ["nextjs", "vite", "react"]:
        try:
            print("🔧 Running npm run build...")
            # Use shell=True and string command for better Windows compatibility
            result = subprocess.run("npm run build", capture_output=True, text=True, cwd=PROJECT_DIR, shell=True)
            if result.returncode == 0:
                print("✅ Build successful!")
                return True
            else:
                print("⚠️ Build failed with return code:", result.returncode)
                if result.stderr:
                    print(f"   Error: {result.stderr}")
                # Check if it's a missing script error
                if result.stderr and "missing script" in result.stderr.lower():
                    print("💡 No build script found in package.json. Proceeding without build.")
                    return True
                # Also check stdout for missing script message
                if result.stdout and "missing script" in result.stdout.lower():
                    print("💡 No build script found in package.json. Proceeding without build.")
                    return True
                # Check for command not found errors
                if "not recognized" in result.stderr.lower() or "command not found" in result.stderr.lower():
                    print("💡 Build tool not found. You may need to install project dependencies.")
                    install_deps = input("Would you like to install dependencies now? (y/n): ")
                    if install_deps.lower() == 'y':
                        if install_dependencies():
                            # Try building again
                            print("🔧 Retrying build after installing dependencies...")
                            retry_result = subprocess.run("npm run build", capture_output=True, text=True, cwd=PROJECT_DIR, shell=True)
                            if retry_result.returncode == 0:
                                print("✅ Build successful on retry!")
                                return True
                            else:
                                print("❌ Build still failed after installing dependencies.")
                                return False
                        else:
                            return False
                return False
        except FileNotFoundError:
            print("❌ npm not found. Please install Node.js from https://nodejs.org/")
            print("   After installation, restart your command prompt and try again.")
            return False
        except Exception as e:
            print(f"❌ Build error: {e}")
            return False
    else:
        print("ℹ️ No build step required for this project type.")
        return True

def vercel_login():
    """Guide user through Vercel login process."""
    print("🔐 Vercel requires authentication.")
    print("   Running 'vercel login' to authenticate...")
    try:
        # Run vercel login and let the user authenticate through the browser
        result = subprocess.run("vercel login", capture_output=False, text=True, shell=True)
        if result.returncode == 0:
            print("✅ Vercel login successful!")
            return True
        else:
            print("⚠️ Vercel login failed.")
            print("   You can manually run 'vercel login' in your terminal and try again.")
            return False
    except Exception as e:
        print(f"❌ Error during Vercel login: {e}")
        return False

def deploy_to_netlify():
    """Deploy using Netlify CLI."""
    try:
        # First, try to initialize if not already done
        print("🔧 Initializing Netlify...")
        init_result = subprocess.run("netlify init --manual", capture_output=True, text=True, shell=True)
        if init_result.returncode != 0 and "already" not in init_result.stdout.lower():
            print("⚠️ Netlify init failed:", init_result.stderr)
            print("   You may need to run 'netlify login' first.")
            login_choice = input("Would you like to log in to Netlify now? (y/n): ")
            if login_choice.lower() == 'y':
                login_result = subprocess.run("netlify login", capture_output=True, text=True, shell=True)
                if login_result.returncode != 0:
                    print("⚠️ Netlify login failed. You can try manually running 'netlify login'.")
        
        # Deploy the site
        print("🚀 Deploying to Netlify...")
        result = subprocess.run("netlify deploy --prod", capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("✅ Deployed successfully to Netlify!")
            # Try to extract URL from output
            if "unique URL" in result.stdout:
                lines = result.stdout.split('\n')
                for line in lines:
                    if "unique URL" in line:
                        print(f"🔗 Live URL: {line.split(': ')[-1]}")
                        break
            return True
        else:
            print("⚠️ Deployment failed:", result.stderr)
            return False
    except FileNotFoundError:
        print("❌ Netlify CLI not found. Please install it first.")
        return False
    except Exception as e:
        print(f"❌ Netlify deployment error: {e}")
        return False

def deploy_to_vercel():
    """Deploy using Vercel CLI."""
    try:
        # Check if we're logged in first
        print("🔍 Checking Vercel authentication...")
        whoami_result = subprocess.run("vercel whoami", capture_output=True, text=True, shell=True)
        if whoami_result.returncode != 0:
            print("⚠️ Not logged in to Vercel.")
            login_choice = input("Would you like to log in to Vercel now? (y/n): ")
            if login_choice.lower() == 'y':
                if not vercel_login():
                    return False
            else:
                print("❌ Vercel deployment requires authentication.")
                return False
        
        # Initialize and deploy
        print("🚀 Deploying to Vercel...")
        result = subprocess.run("vercel --prod --yes", capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("✅ Deployed successfully to Vercel!")
            # Extract URL from output
            lines = result.stdout.split('\n')
            for line in lines:
                if line.startswith("https://"):
                    print(f"🔗 Live URL: {line.strip()}")
                    break
            return True
        else:
            print("⚠️ Deployment failed:", result.stderr)
            return False
    except FileNotFoundError:
        print("❌ Vercel CLI not found. Please install it first.")
        return False
    except Exception as e:
        print(f"❌ Vercel deployment error: {e}")
        return False

def deploy_to_github_pages():
    """Deploy to GitHub Pages (assumes gh-pages branch or docs/)."""
    print("🔧 Setting up GitHub Pages...")
    # Simple method: push to docs/ folder on main branch
    dist_folder = None
    for folder in ["dist", "build", "out"]:
        if os.path.exists(folder):
            dist_folder = folder
            break
    
    if dist_folder:
        if not os.path.exists("docs"):
            os.rename(dist_folder, "docs")
            print(f"✅ Moved {dist_folder} to docs/")
        else:
            print("✅ Using existing docs/ folder")
    else:
        print("⚠️ No build output folder found. Using current directory for deployment.")
    
    print("👉 To deploy to GitHub Pages:")
    print("   1. Make sure your repository is on GitHub")
    print("   2. Go to your repository Settings → Pages")
    print("   3. Set Source to 'Deploy from a branch'")
    print("   4. Select branch 'main' and folder '/docs'")
    print("   5. Commit and push your changes:")
    print("      git add .")
    print("      git commit -m 'Deploy to GitHub Pages'")
    print("      git push origin main")
    return True

def deploy_to_cloudflare_pages():
    """Deploy using Wrangler to Cloudflare Pages."""
    try:
        # Build the project first if needed
        build_folder = "dist"
        if os.path.exists("dist"):
            build_folder = "dist"
        elif os.path.exists("build"):
            build_folder = "build"
        elif os.path.exists("out"):
            build_folder = "out"
        else:
            build_folder = "."
            
        # Deploy using wrangler
        print("🚀 Deploying to Cloudflare Pages...")
        cmd = f"wrangler pages deploy {build_folder} --project-name {PROJECT_DIR.name}"
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("✅ Deployed successfully to Cloudflare Pages!")
            # Try to extract URL
            if "Visit your deployed site" in result.stdout:
                lines = result.stdout.split('\n')
                for line in lines:
                    if "https://" in line and "cloudflare" in line:
                        print(f"🔗 Live URL: {line.strip()}")
                        break
            return True
        else:
            print("⚠️ Deployment failed:", result.stderr)
            return False
    except FileNotFoundError:
        print("❌ Wrangler CLI not found. Please install it first.")
        return False
    except Exception as e:
        print(f"❌ Cloudflare deployment error: {e}")
        return False

def deploy_to_render():
    """Deploy to Render (instructions for manual setup)."""
    print("🔧 Render Deployment Instructions:")
    print("   1. Go to https://render.com and create an account")
    print("   2. Create a new Web Service")
    print("   3. Connect your Git repository (GitHub/GitLab)")
    print("   4. Configure the service:")
    
    # Detect project type and provide specific instructions
    files = [f.name for f in PROJECT_DIR.iterdir() if f.is_file()]
    
    if "requirements.txt" in files:
        print("      - Environment: Python")
        print("      - Build command: pip install -r requirements.txt")
        print("      - Start command: gunicorn app:app (adjust as needed)")
    else:
        print("      - Environment: Static Site")
        print("      - Build command: (leave empty for static sites)")
        print("      - Publish directory: . (or dist/build if applicable)")
    
    print("   5. Click 'Create Web Service'")
    print("✅ Render will automatically deploy your site on every git push!")
    return True

def deploy_to_platform_flask(platform):
    """Deploy Flask project to the specified platform."""
    print(f"🚀 Deploying Flask project to {platform}...")
    
    if platform == "Vercel":
        # For Flask projects on Vercel, we need specific handling
        return deploy_to_vercel_flask()
    elif platform == "Render":
        return deploy_to_render()
    else:
        # For other platforms, use the generic deployment
        return deploy_to_platform(platform)

def deploy_to_vercel_flask():
    """Deploy Flask project to Vercel with specific configuration."""
    try:
        # Check if we're logged in first
        print("🔍 Checking Vercel authentication...")
        whoami_result = subprocess.run("vercel whoami", capture_output=True, text=True, shell=True)
        if whoami_result.returncode != 0:
            print("⚠️ Not logged in to Vercel.")
            login_choice = input("Would you like to log in to Vercel now? (y/n): ")
            if login_choice.lower() == 'y':
                if not vercel_login():
                    return False
            else:
                print("❌ Vercel deployment requires authentication.")
                return False
        
        # For Flask projects, we need to ensure vercel.json exists
        if not os.path.exists("vercel.json"):
            print("⚠️ vercel.json configuration not found. Creating default configuration...")
            vercel_config = {
                "version": 2,
                "builds": [
                    {
                        "src": "api/index.py",
                        "use": "@vercel/python"
                    }
                ],
                "routes": [
                    {
                        "src": "/(.*)",
                        "dest": "api/index.py"
                    }
                ]
            }
            with open("vercel.json", "w") as f:
                json.dump(vercel_config, f, indent=2)
            print("✅ Created vercel.json configuration")
        
        # Initialize and deploy
        print("🚀 Deploying Flask project to Vercel...")
        result = subprocess.run("vercel --prod --yes", capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("✅ Deployed successfully to Vercel!")
            # Extract URL from output
            lines = result.stdout.split('\n')
            for line in lines:
                if line.startswith("https://"):
                    print(f"🔗 Live URL: {line.strip()}")
                    break
            return True
        else:
            print("⚠️ Deployment failed:", result.stderr)
            # Provide specific troubleshooting for Flask projects
            if "404" in result.stderr or "NOT_FOUND" in result.stderr:
                print("\n💡 Flask Deployment Troubleshooting:")
                print("   - Ensure your vercel.json is properly configured")
                print("   - Check that your Flask app exposes an 'application' variable")
                print("   - Verify requirements.txt includes gunicorn")
                print("   - Make sure your project structure matches Vercel's expectations")
            return False
    except FileNotFoundError:
        print("❌ Vercel CLI not found. Please install it first.")
        return False
    except Exception as e:
        print(f"❌ Vercel deployment error: {e}")
        return False

def deploy_to_platform(platform):
    """Deploy to the specified platform."""
    print(f"🚀 Deploying to {platform}...")
    
    if platform == "Netlify":
        return deploy_to_netlify()
    elif platform == "Vercel":
        return deploy_to_vercel()
    elif platform == "GitHub Pages":
        return deploy_to_github_pages()
    elif platform == "Cloudflare Pages":
        return deploy_to_cloudflare_pages()
    elif platform == "Render":
        return deploy_to_render()
    else:
        print(f"❓ Unsupported platform: {platform}")
        return False

def main():
    print("🚀 Welcome to the Auto Deploy Agent CLI!")
    print(f"Scanning project in: {PROJECT_DIR}")
    
    project_type = detect_project_type()
    print(f"🔍 Detected project type: {project_type}")
    
    if project_type == "unknown":
        print("❓ Could not detect project type. Is this a web project?")
        return

    # Get recommendation
    rec = recommend_platform(project_type)
    platform = rec["platform"]
    print(f"\n💡 Recommended platform: {platform}")
    print(f"   Reason: {rec['reason']}")
    print("\n📋 Setup steps:")
    for i, step in enumerate(rec["setup_steps"], 1):
        print(f"   {i}. {step}")
    
    print("\n")
    install_cli(platform)
    
    # Build project if necessary
    if not build_project(project_type):
        print("❌ Build failed. Cannot proceed with deployment.")
        return
    
    # Deploy to the recommended platform
    if project_type == "python-flask":
        success = deploy_to_platform_flask(platform)
    else:
        success = deploy_to_platform(platform)
    
    if success:
        print(f"\n🎉 Deployment to {platform} completed successfully!")
    else:
        print(f"\n❌ Deployment to {platform} failed.")
        print("But don't worry! You can still deploy manually using the platform's dashboard or CLI.")
        print("\n📝 Troubleshooting tips:")
        print("   1. Make sure you've installed the required CLI tool")
        print("   2. Check that you're logged in to the platform")
        print("   3. Ensure you have an internet connection")
        print("   4. Try running the deploy command manually")

if __name__ == "__main__":
    main()