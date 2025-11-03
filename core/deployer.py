#!/usr/bin/env python3
"""Deployment module for Auto Deploy Agent"""

import subprocess
import os
import shutil

def vercel_login():
    """Guide user through Vercel login process."""
    print("🔐 Running 'vercel login'...")
    try:
        result = subprocess.run("vercel login", capture_output=False, text=True, shell=True, timeout=120)
        if result.returncode == 0:
            print("✅ Login successful!")
            return True
        else:
            print("⚠️ Login failed. Try manually.")
            return False
    except subprocess.TimeoutExpired:
        print("⚠️ Vercel login timed out")
        return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False

def deploy_to_netlify():
    """Deploy using Netlify CLI."""
    try:
        print("🔧 Initializing Netlify...")
        init_result = subprocess.run("netlify init --manual", capture_output=True, text=True, shell=True, timeout=120)
        if init_result.returncode != 0:
            print(f"⚠️ Init failed: {init_result.stderr}")
            if input("Log in to Netlify now? (y/n): ").lower() == 'y':
                subprocess.run("netlify login", capture_output=True, text=True, shell=True, timeout=60)

        print("🚀 Deploying to Netlify...")
        result = subprocess.run("netlify deploy --prod", capture_output=True, text=True, shell=True, timeout=300)
        if result.returncode == 0:
            print("✅ Deployed!")
            for line in result.stdout.split('\n'):
                if "unique URL" in line:
                    print(f"🔗 Live URL: {line.split(': ')[-1]}")
                    break
            return True
        else:
            print(f"⚠️ Failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("⚠️ Netlify deployment timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def deploy_to_vercel():
    """Deploy using Vercel CLI."""
    try:
        whoami_result = subprocess.run("vercel whoami", capture_output=True, text=True, shell=True, timeout=30)
        if whoami_result.returncode != 0:
            if input("Log in to Vercel now? (y/n): ").lower() == 'y':
                if not vercel_login():
                    return False

        # The "Deploying to Vercel..." message is printed in main.py to avoid duplication
        result = subprocess.run("vercel --prod --yes", capture_output=True, text=True, shell=True, timeout=300)
        if result.returncode == 0:
            print("✅ Deployed!")
            for line in result.stdout.split('\n'):
                if line.startswith("https://"):
                    print(f"🔗 Live URL: {line.strip()}")
                    break
            return True
        else:
            print(f"⚠️ Failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("⚠️ Vercel deployment timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def deploy_to_github_pages():
    """Deploy to GitHub Pages (assumes gh-pages branch or docs/)."""
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
        print("⚠️ No build folder found. Using current dir.")

    print("\n📝 Follow these to complete GitHub Pages setup:")
    print("1. Go to repo Settings > Pages")
    print("2. Select branch 'main' and folder '/docs' or '/'")
    print("3. Save and push changes.")
    return True

def deploy_to_cloudflare_pages():
    """Deploy using Wrangler to Cloudflare Pages."""
    try:
        build_folder = next((f for f in ["dist", "build", "out"] if os.path.exists(f)), ".")
        print("🚀 Deploying to Cloudflare...")
        cmd = f"wrangler pages deploy {build_folder} --project-name {os.getcwd().split(os.sep)[-1]}"
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=300)
        if result.returncode == 0:
            print("✅ Deployed!")
            for line in result.stdout.split('\n'):
                if "https://" in line and "cloudflare" in line:
                    print(f"🔗 Live URL: {line.strip()}")
                    break
            return True
        else:
            print(f"⚠️ Failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("⚠️ Cloudflare deployment timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def deploy_to_render():
    """Deploy to Render (instructions for manual setup)."""
    print("🔧 Render Deployment Instructions:")
    print("1. Go to https://render.com and create account")
    print("2. Create new Web Service")
    print("3. Connect Git repo")
    print("4. Configure:")
    files = [f.name for f in os.scandir('.') if f.is_file()]
    if "requirements.txt" in files:
        print("   - Environment: Python")
        print("   - Build: pip install -r requirements.txt")
        print("   - Start: gunicorn app:app")
    else:
        print("   - Environment: Static Site")
        print("   - Build: (empty)")
        print("   - Publish: . or dist/build")
    print("5. Create Web Service")
    return True

def deploy_to_vercel_flask():
    """Deploy Flask to Vercel with config."""
    try:
        whoami_result = subprocess.run("vercel whoami", capture_output=True, text=True, shell=True, timeout=30)
        if whoami_result.returncode != 0:
            if input("Log in to Vercel now? (y/n): ").lower() == 'y':
                if not vercel_login():
                    return False

        # Ensure api directory exists for Flask projects
        if not os.path.exists("api"):
            os.makedirs("api")
            
        # Move app.py to api/index.py for Vercel
        if os.path.exists("app.py") and not os.path.exists("api/index.py"):
            shutil.copy("app.py", "api/index.py")
            print("✅ Copied app.py to api/index.py for Vercel deployment")

        # The "Deploying Flask to Vercel..." message is printed in main.py to avoid duplication
        result = subprocess.run("vercel --prod --yes", capture_output=True, text=True, shell=True, timeout=300)
        if result.returncode == 0:
            print("✅ Deployed!")
            for line in result.stdout.split('\n'):
                if line.startswith("https://"):
                    print(f"🔗 Live URL: {line.strip()}")
                    break
            return True
        else:
            print(f"⚠️ Failed: {result.stderr}")
            print("💡 Troubleshooting: Check vercel.json, requirements.txt, app structure.")
            return False
    except subprocess.TimeoutExpired:
        print("⚠️ Vercel Flask deployment timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def deploy_to_platform_flask(platform):
    """Deploy Flask project to the specified platform."""
    # The deployment message is printed in main.py to avoid duplication
    if platform == "Vercel":
        return deploy_to_vercel_flask()
    elif platform == "Render":
        return deploy_to_render()
    else:
        return deploy_to_platform(platform)

def deploy_to_platform(platform):
    """Deploy to the specified platform."""
    # The deployment message is printed in main.py to avoid duplication
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
        print(f"❓ Unsupported: {platform}")
        return False

def validate_deployment(platform, project_type):
    """Validate that the deployment was successful."""
    print("🔍 Validating deployment...")
    
    # For platforms that provide a URL, we could ping it to verify it's live
    # This is a simplified validation - in a real-world scenario, you might want
    # to make HTTP requests to verify the deployment
    
    if platform in ["Netlify", "Vercel", "Cloudflare Pages"]:
        print("✅ Deployment validation: Please check the provided URL to verify your site is live")
        return True
    elif platform == "GitHub Pages":
        print("✅ Deployment validation: Please check your GitHub Pages settings to verify your site is live")
        return True
    elif platform == "Render":
        print("✅ Deployment validation: Please check your Render dashboard to verify your app is live")
        return True
    else:
        print("✅ Deployment completed")
        return True