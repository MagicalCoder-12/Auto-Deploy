#!/usr/bin/env python3
"""Deployment module for Auto Deploy Agent"""

import subprocess
import os
import shutil
import sys
from config import PAID_PLATFORMS
from pathlib import Path

# Attempt to load .env from project root as a fallback so deploy functions
# work when the module is run/imported directly (in addition to main.py loading it).
try:
    from dotenv import load_dotenv
    _project_root = Path(__file__).resolve().parents[1]
    load_dotenv(dotenv_path=_project_root / ".env")
except Exception:
    # If python-dotenv isn't installed or load fails, continue silently;
    # main.py already attempts to load .env when available.
    pass

def check_paid_platform_confirmation(platform):
    """Check if platform is paid and ask for user confirmation."""
    if platform in PAID_PLATFORMS:
        print(f"\nNote: {platform} may require a payment method. Deployment may or may not succeed depending on the availability of free credits or trial resources.")
        
        while True:
            response = input("Would you like to proceed with this platform anyway? (yes/no): ").lower().strip()
            
            if response in ['yes', 'y', '1', 'true']:
                return True  # User confirmed, proceed
            elif response in ['no', 'n', '0', 'false']:
                return False  # User declined, need alternative
            else:
                print("Please respond with 'yes' or 'no'.")
    
    return True  # Not a paid platform, proceed normally

def vercel_login():
    """Guide user through Vercel login process."""
    print("Running 'vercel login'...")
    try:
        result = subprocess.run("vercel login", capture_output=False, text=True, encoding="utf-8", errors="replace", shell=True, timeout=120)
        if result.returncode == 0:
            print("Login successful!")
            return True
        else:
            print("Login failed. Try manually.")
            return False
    except subprocess.TimeoutExpired:
        print("Vercel login timed out")
        return False
    except Exception as e:
        print(f"Login error: {e}")
        return False

def get_netlify_site_id():
    """
    Dynamically detect Netlify site ID (priority order).
    
    Returns:
        Site ID string if found, None otherwise
        
    Priority:
    1. .netlify/state.json (source of truth - created by netlify init/link)
    2. netlify status command output
    3. NETLIFY_SITE_ID environment variable (fallback only)
    """
    # Priority 1: Read from .netlify/state.json (most recent, authoritative)
    netlify_state_path = ".netlify/state.json"
    if os.path.exists(netlify_state_path):
        try:
            import json
            with open(netlify_state_path, 'r') as f:
                state = json.load(f)
                # Navigate nested structure: state → siteInfo → id
                if 'siteInfo' in state and 'id' in state['siteInfo']:
                    site_id = state['siteInfo']['id']
                    if site_id:
                        return site_id
        except Exception:
            pass  # Continue to fallback
    
    # Priority 2: Get from netlify status command (current linked site)
    try:
        # Run netlify status and decode bytes explicitly to avoid platform-dependent
        # default decoders (Windows cp1252) which can raise UnicodeDecodeError.
        result = subprocess.run(
            ["netlify", "status"],
            capture_output=True,
            text=False,
            shell=False,
            timeout=10
        )
        if result.returncode == 0:
            stdout = result.stdout
            if isinstance(stdout, (bytes, bytearray)):
                stdout = stdout.decode('utf-8', errors='replace')
            else:
                stdout = str(stdout)

            # Look for "Site ID: xxxxx" or similar patterns
            for line in stdout.splitlines():
                if 'site id' in line.lower() or 'site-id' in line.lower():
                    parts = line.split(':', 1)
                    if len(parts) > 1:
                        site_id = parts[1].strip()
                        if site_id:
                            return site_id
    except Exception:
        pass  # Continue to fallback
    
    # Priority 3: Fallback to environment variable (last resort)
    site_id = os.getenv("NETLIFY_SITE_ID")
    if site_id:
        return site_id
    
    return None

def verify_netlify_initialization():
    """
    Verify that Netlify is initialized for the project.
    
    Returns:
        True if initialized (.netlify/state.json exists or site ID is detectable)
        False otherwise
    """
    # Check for .netlify/state.json (created by netlify init/link)
    if os.path.exists(".netlify/state.json"):
        return True
    
    # Check if we can get a site ID
    if get_netlify_site_id():
        return True
    
    return False

def update_netlify_site_id_runtime(site_id):
    """
    Update NETLIFY_SITE_ID in runtime environment (os.environ).
    
    This updates the in-memory environment without modifying .env file.
    Called after user completes netlify init to use the actual linked site.
    """
    if site_id:
        os.environ['NETLIFY_SITE_ID'] = site_id

def netlify_init_gate():
    """
    Gate function to ensure Netlify initialization before deployment.
    
    If already initialized:
    - Silent, non-interactive
    - Read site ID from .netlify/state.json
    - Return True immediately
    
    If NOT initialized:
    - Print clear step-by-step instructions
    - Wait for user to press ENTER
    - Verify and re-detect site ID
    - Update runtime environment
    - Return True/False based on verification
    """
    # Check if Netlify is already initialized
    if verify_netlify_initialization():
        # Already initialized - silent mode
        detected_site_id = get_netlify_site_id()
        if detected_site_id:
            # Update runtime environment with detected site ID
            update_netlify_site_id_runtime(detected_site_id)
            return True
        return False
    
    # Netlify not initialized - print instructions and wait for user
    print("\n" + "="*75)
    print("NETLIFY INITIALIZATION REQUIRED - ONE-TIME SETUP")
    print("="*75)
    print("\nBefore deployment, you need to initialize Netlify for this project.")
    print("This is a ONE-TIME setup. Follow these steps:\n")
    
    print("STEP 1: Log in to Netlify")
    print("  Run in your terminal:")
    print("    netlify login\n")
    print("  This will open your browser to authenticate with Netlify.\n")
    
    print("STEP 2: Link your project to Netlify")
    print("  Run one of the following commands:\n")
    print("  Option A (Recommended - automatic setup):")
    print("    netlify init\n")
    print("  Option B (Link to existing Netlify site):")
    print("    netlify link\n")
    
    print("STEP 3: Configure build settings (if using 'netlify init')")
    print("  - When prompted, select your build command")
    print("    (press Enter for default: 'npm run build')")
    print("  - Select your publish directory")
    print("    (usually 'dist', 'build', or 'public')")
    print("  - A .netlify/state.json file will be created\n")
    
    print("="*75)
    print("After completing the above steps, press ENTER to continue with deployment...")
    print("="*75)
    
    # Wait for user to press ENTER
    input()
    
    # Verify initialization and re-detect site ID
    print("\n⏳ Verifying Netlify initialization...")
    if not verify_netlify_initialization():
        print("✗ Netlify initialization verification failed.\n")
        print("Troubleshooting - Please check:")
        print("  1. Did you run 'netlify login' successfully?")
        print("  2. Did you run 'netlify init' or 'netlify link'?")
        print("  3. Is .netlify/state.json present in your project root?")
        print("  4. Is NETLIFY_SITE_ID set in your .env file?\n")
        print("Please complete the initialization steps and try deployment again.")
        return False
    
    # Re-detect actual site ID from .netlify/state.json or netlify status
    detected_site_id = get_netlify_site_id()
    if detected_site_id:
        print(f"✓ Netlify initialization verified!")
        print(f"  Site ID: {detected_site_id}")
        
        # Update runtime environment with the ACTUAL site ID
        update_netlify_site_id_runtime(detected_site_id)
        
        print("  Proceeding with automated deployment...\n")
        return True
    else:
        print("✗ Could not detect Netlify site ID.\n")
        print("Troubleshooting:")
        print("  - Ensure .netlify/state.json was created during 'netlify init'")
        print("  - Or set NETLIFY_SITE_ID in your .env file")
        return False

def deploy_to_netlify():
    """Deploy to Netlify after verifying initialization."""
    import subprocess
    import os

    try:
        # Gate: Ensure Netlify is initialized (silent if already done, asks only if needed)
        if not netlify_init_gate():
            print("Deployment aborted: Netlify not properly initialized.")
            return False
        
        print("Deploying to Netlify...")

        # Get site ID dynamically (detects from .netlify/state.json, then netlify status, then env var)
        netlify_site = get_netlify_site_id()
        netlify_token = os.getenv("NETLIFY_AUTH_TOKEN")
        
        if not netlify_site or not netlify_token:
            if not netlify_site:
                print("✗ Missing NETLIFY_SITE_ID.")
                print("  Could not detect from .netlify/state.json or netlify status.")
                print("  Ensure 'netlify init' or 'netlify link' was completed.")
            if not netlify_token:
                print("✗ Missing NETLIFY_AUTH_TOKEN.")
                print("  Set it in your .env file: NETLIFY_AUTH_TOKEN=your_token")
            return False

        cmd = (
            f"netlify deploy --prod "
            f"--site {netlify_site} "
            f"--auth {netlify_token} "
            f"--message \"Auto deploy\""
        )

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=True,
            timeout=300
        )

        if result.returncode == 0:
            print("Deployed! 🚀")
            for line in result.stdout.splitlines():
                if "Live URL" in line or "Website URL" in line:
                    print(line)
            
            # Run netlify status to confirm deployment state
            print("\nVerifying deployment status...")
            try:
                status_result = subprocess.run(["netlify", "status"], capture_output=True, text=False, shell=False, timeout=10)
                if status_result.returncode == 0:
                    out = status_result.stdout
                    if isinstance(out, (bytes, bytearray)):
                        out = out.decode('utf-8', errors='replace')
                    else:
                        out = str(out)
                    print(out)
            except Exception:
                pass  # If status check fails, deployment was still successful
            
            return True
        else:
            print("Deploy failed ❌")
            print(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("Netlify deployment timed out ⏱️")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def deploy_to_vercel():
    """Deploy using Vercel CLI."""
    try:
        whoami_result = subprocess.run("vercel whoami", capture_output=True, text=True, encoding="utf-8", errors="replace", shell=True, timeout=30)
        if whoami_result.returncode != 0:
            if input("Log in to Vercel now? (y/n): ").lower() == 'y':
                if not vercel_login():
                    return False

        # The "Deploying to Vercel..." message is printed in main.py to avoid duplication
        result = subprocess.run("vercel --prod --yes", capture_output=True, text=True, encoding="utf-8", errors="replace", shell=True, timeout=300)
        if result.returncode == 0:
            print("Deployed!")
            for line in result.stdout.split('\n'):
                if line.startswith("https://"):
                    print(f"Live URL: {line.strip()}")
                    break
            return True
        else:
            print(f"Failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("Vercel deployment timed out")
        return False
    except Exception as e:
        print(f"Error: {e}")
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
            print(f"Moved {dist_folder} to docs/")
    else:
        print("No build folder found. Using current dir.")

    print("\nFollow these to complete GitHub Pages setup:")
    print("1. Go to repo Settings > Pages")
    print("2. Select branch 'main' and folder '/docs' or '/'")
    print("3. Save and push changes.")
    return True

def deploy_to_cloudflare_pages():
    """Deploy using Wrangler to Cloudflare Pages."""
    try:
        build_folder = next((f for f in ["dist", "build", "out"] if os.path.exists(f)), ".")
        print("Deploying to Cloudflare...")
            cmd = f"wrangler pages deploy {build_folder} --project-name {os.getcwd().split(os.sep)[-1]}"
            result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", shell=True, timeout=300)
        if result.returncode == 0:
            print("Deployed!")
            for line in result.stdout.split('\n'):
                if "https://" in line and "cloudflare" in line:
                    print(f"Live URL: {line.strip()}")
                    break
            return True
        else:
            print(f"Failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("Cloudflare deployment timed out")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def deploy_to_render():
    """Deploy to Render (instructions for manual setup)."""
    print("Render Deployment Instructions:")
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
        whoami_result = subprocess.run("vercel whoami", capture_output=True, text=True, encoding="utf-8", errors="replace", shell=True, timeout=30)
        if whoami_result.returncode != 0:
            if input("Log in to Vercel now? (y/n): ").lower() == 'y':
                if not vercel_login():
                    return False

        # Ensure api directory exists for Flask projects
        if not os.path.exists("api"):
            os.makedirs("api")
            
        # Check if app.py exists and create proper api/index.py
        if os.path.exists("app.py") and not os.path.exists("api/index.py"):
            with open("api/index.py", "w") as f:
                f.write("# Vercel entry point for Flask app\n")
                f.write("from app import app\n\n")
                f.write("# Expose the Flask app as 'application' for Vercel\n")
                f.write("application = app\n")
            print("Created api/index.py for Vercel deployment")
        elif not os.path.exists("app.py") and not os.path.exists("api/index.py"):
            # Create a basic Flask app if neither exists
            with open("api/index.py", "w") as f:
                f.write("# Vercel entry point for Flask app\n")
                f.write("from flask import Flask\n\n")
                f.write("app = Flask(__name__)\n\n")
                f.write("@app.route('/')\n")
                f.write("def home():\n")
                f.write("    return '<h1>Hello from Flask on Vercel!</h1>'\n\n")
                f.write("# Expose the Flask app as 'application' for Vercel\n")
                f.write("application = app\n")
            print("Created basic Flask app in api/index.py for Vercel deployment")

        # The "Deploying Flask to Vercel..." message is printed in main.py to avoid duplication
        result = subprocess.run("vercel --prod --yes", capture_output=True, text=True, encoding="utf-8", errors="replace", shell=True, timeout=300)
        if result.returncode == 0:
            print("Deployed!")
            for line in result.stdout.split('\n'):
                if line.startswith("https://"):
                    print(f"Live URL: {line.strip()}")
                    break
            return True
        else:
            print(f"Failed: {result.stderr}")
            print("Troubleshooting: Check vercel.json, requirements.txt, app structure.")
            return False
    except subprocess.TimeoutExpired:
        print("Vercel Flask deployment timed out")
        return False
    except Exception as e:
        print(f"Error: {e}")
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
        print(f"Unsupported: {platform}")
        return False

def validate_deployment(platform, project_type):
    """Validate that the deployment was successful."""
    print("Validating deployment...")
    
    # For platforms that provide a URL, we could ping it to verify it's live
    # This is a simplified validation - in a real-world scenario, you might want
    # to make HTTP requests to verify the deployment
    
    if platform in ["Netlify", "Vercel", "Cloudflare Pages"]:
        print("Deployment validation: Please check the provided URL to verify your site is live")
        return True
    elif platform == "GitHub Pages":
        print("Deployment validation: Please check your GitHub Pages settings to verify your site is live")
        return True
    elif platform == "Render":
        print("Deployment validation: Please check your Render dashboard to verify your app is live")
        return True
    else:
        print("Deployment completed")
        return True