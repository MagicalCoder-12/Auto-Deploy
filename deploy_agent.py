#!/usr/bin/env python3
""" Auto Deploy Agent CLI - Automatically detect, build, and deploy web projects """

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
    """Detect what kind of web project this is using Ollama with Llama3.1."""
    files = [f.name for f in PROJECT_DIR.iterdir() if f.is_file()]
    folders = [f.name for f in PROJECT_DIR.iterdir() if f.is_dir()]

    if OLLAMA_AVAILABLE:
        try:
            prompt = f"""
            You are an expert DevOps assistant. Based on these files: {', '.join(files)} and folders: {', '.join(folders)},
            detect the web project type. Possible types: nextjs, vite, react, static, python-flask, or unknown.
            Respond in JSON format: {{"type": "...", "reason": "..."}}.
            """
            response = ollama.chat(
                model="llama3.1:8b",  # Updated to use llama3.1:8b model
                messages=[{"role": "user", "content": prompt}],
                format="json"
            )
            result = json.loads(response["message"]["content"])
            print(f"🔍 Project detection reason: {result['reason']}")
            return result["type"]
        except Exception as e:
            print(f"⚠️ Ollama detection failed: {e}")
            print("Falling back to default detection...")

    # Fallback to original hardcoded detection
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
        return "python-flask"

    return "unknown"

def recommend_platform(project_type):
    """Use Llama3.1 to recommend a platform."""
    # Use Ollama with Llama3.1 for smart recommendations if available
    if OLLAMA_AVAILABLE:
        try:
            prompt = f"""
            You are an expert DevOps assistant. Recommend the best free hosting platform for a {project_type} project.
            Options: Netlify, Vercel, GitHub Pages, Cloudflare Pages, Render.
            Respond in JSON format: {{"platform": "...", "reason": "...", "setup_steps": ["step1", "step2"]}}
            """
            response = ollama.chat(
                model="llama3.1:8b",  # Updated to use llama3.1:8b model
                messages=[{"role": "user", "content": prompt}],
                format="json"
            )
            return json.loads(response["message"]["content"])
        except Exception as e:
            print(f"⚠️ Ollama recommendation failed: {e}")
            print("Falling back to default recommendations...")

    # Fallback recommendations if Ollama is not available or fails
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

def check_cli_installed(cli_command):
    """Check if a CLI tool is installed by running --version."""
    try:
        result = subprocess.run(f"{cli_command} --version", capture_output=True, text=True, shell=True)
        return result.returncode == 0
    except Exception:
        return False

def install_cli(platform):
    """Check if CLI is available, ask permission to install if not."""
    cli_map = {
        "Netlify": {"cmd": "netlify", "install": "npm install -g netlify-cli", "auto_install": True},
        "Vercel": {"cmd": "vercel", "install": "npm install -g vercel", "auto_install": True},
        "Cloudflare Pages": {"cmd": "wrangler", "install": "npm install -g wrangler", "auto_install": True},
        "GitHub Pages": {"cmd": "git", "install": "https://git-scm.com/downloads", "auto_install": False},
        "Render": {"cmd": "git", "install": "https://git-scm.com/downloads", "auto_install": False}
    }
    cli_info = cli_map.get(platform)
    
    if not cli_info:
        print(f"✅ {platform} doesn't require a specific CLI.")
        return True

    if check_cli_installed(cli_info["cmd"]):
        print(f"✅ {cli_info['cmd']} is already installed.")
        return True

    print(f"⚠️ {cli_info['cmd']} not found.")
    
    if cli_info["auto_install"]:
        permission = input(f"Do you want me to install it automatically? (y/n): ")
        if permission.lower() == 'y':
            try:
                print(f"👉 Installing {cli_info['cmd']}...")
                result = subprocess.run(cli_info["install"], capture_output=True, text=True, shell=True)
                if result.returncode == 0:
                    print("✅ Installation successful!")
                    return True
                else:
                    print(f"⚠️ Installation failed: {result.stderr}")
                    return False
            except Exception as e:
                print(f"❌ Error installing: {e}")
                return False
        else:
            print(f"👉 Please install manually: {cli_info['install']}")
            print("After installation, restart your terminal and run this script again.")
            return False
    else:
        # Tools that require manual installation
        print(f"🔧 {cli_info['cmd']} requires manual installation.")
        print(f"👉 Please download and install from: {cli_info['install']}")
        print("👉 After installation, restart your terminal.")
        input("Press Enter after installing...")
        
        # Verify installation
        if check_cli_installed(cli_info["cmd"]):
            print(f"✅ {cli_info['cmd']} successfully installed!")
            return True
        else:
            print(f"⚠️ {cli_info['cmd']} still not found. Please verify installation.")
            return False

def check_and_install_git():
    """Check if git is installed, ask to install if not."""
    return install_cli("GitHub Pages")  # Reuse the installation logic

def create_gitignore(project_type):
    """Create a .gitignore file based on the project type."""
    gitignore_path = PROJECT_DIR / ".gitignore"
    
    if gitignore_path.exists():
        print("✅ .gitignore file already exists.")
        return True
    
    print("📄 Creating .gitignore file...")
    
    # Base gitignore content
    gitignore_content = """# Dependencies
node_modules/
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Directory for instrumented libs generated by jscoverage/JSCover
lib-cov

# Coverage directory used by tools like istanbul
coverage/
*.lcov

# nyc test coverage
.nyc_output

# Grunt intermediate storage (https://gruntjs.com/creating-plugins#storing-task-files)
.grunt

# Bower dependency directory (https://bower.io/)
bower_components

# node-waf configuration
.lock-wscript

# Compiled binary addons (https://nodejs.org/api/addons.html)
build/Release

# Dependency directories
jspm_packages/

# Snowpack dependency directory (https://snowpack.dev/)
web_modules/

# TypeScript cache
*.tsbuildinfo

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Microbundle cache
.rpt2_cache/
.rts2_cache_cjs/
.rts2_cache_es/
.rts2_cache_umd/

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env*

# parcel-bundler cache (https://parceljs.org/)
.cache
.parcel-cache

# Next.js build output
.next/
out/

# Nuxt.js build / generate output
.nuxt
dist/

# Gatsby files
.cache/
# Comment in the public line in if your project uses Gatsby and not Next.js
# https://nextjs.org/blog/next-9-1#public-directory-support
# public/

# vuepress build output
.vuepress/dist

# Serverless directories
.serverless/

# FuseBox cache
.fusebox/

# DynamoDB Local files
.dynamodb/

# TernJS port file
.tern-port

# Stores VSCode versions used for testing VSCode extensions
.vscode-test

# yarn v2
.yarn/cache
.yarn/unplugged
.yarn/build-state.yml
.yarn/install-state.gz
.pnp.*

"""
    
    # Add Python-specific ignores
    if project_type in ["python-flask"]:
        gitignore_content += """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/#use-with-ide
.pdm.toml

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env/
.venv/
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

"""
    
    try:
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content)
        print("✅ .gitignore file created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create .gitignore file: {e}")
        return False

def init_git_repo():
    """Initialize dir as git repo with user permission, and connect to remote."""
    if os.path.exists(".git"):
        print("✅ This directory is already a git repository.")
        # Check if remote exists
        try:
            result = subprocess.run("git remote get-url origin", capture_output=True, text=True, shell=True)
            if result.returncode == 0 and result.stdout.strip():
                print(f"🔗 Already connected to remote: {result.stdout.strip()}")
                return True
        except Exception:
            pass

    permission = input("Do you want me to initialize a git repository for this project? (y/n): ")
    if permission.lower() != 'y':
        return False

    try:
        print("🔧 Initializing git repo...")
        subprocess.run("git init", check=True, shell=True)
        
        # Create .gitignore file
        # We'll determine project type by checking existing files
        files = [f.name for f in PROJECT_DIR.iterdir() if f.is_file()]
        project_type = "unknown"
        if "package.json" in files:
            project_type = "node"
        elif "requirements.txt" in files:
            project_type = "python-flask"
        elif "index.html" in files:
            project_type = "static"
            
        create_gitignore(project_type)
        
        subprocess.run("git add .", check=True, shell=True)
        commit_msg = input("Enter commit message (default: 'Initial commit'): ") or "Initial commit"
        subprocess.run(f"git commit -m '{commit_msg}'", check=True, shell=True)

        # Ask for remote repository URL
        repo_url = input("Enter your remote Git repository URL (e.g., https://github.com/user/repo.git) or leave blank to skip: ").strip()
        if repo_url:
            subprocess.run(f"git remote add origin {repo_url}", check=True, shell=True)
            subprocess.run("git branch -M main", check=True, shell=True)
            push_permission = input("Do you want to push to the remote repository now? (y/n): ")
            if push_permission.lower() == 'y':
                print("🚀 Pushing to remote repository...")
                subprocess.run("git push -u origin main", check=True, shell=True)
                print("✅ Pushed to remote repository!")
        else:
            print("ℹ️  Skipped remote repository setup. You can add it later with 'git remote add origin <url>'")
            
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Git init failed: {e}")
        return False

def check_node_installed():
    """Check if Node.js and npm are installed and accessible."""
    try:
        node_result = subprocess.run("node --version", capture_output=True, text=True, shell=True)
        if node_result.returncode != 0:
            print("❌ Node.js not found.")
            return False
        print(f"✅ Node.js version: {node_result.stdout.strip()}")

        npm_result = subprocess.run("npm --version", capture_output=True, text=True, shell=True)
        if npm_result.returncode != 0:
            print("❌ npm not found.")
            return False
        print(f"✅ npm version: {npm_result.stdout.strip()}")
        return True
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
            print(f"⚠️ Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_required_files(project_type, platform):
    """Create required deployment files if they don't exist."""
    print("📄 Checking and creating required deployment files...")
    
    # Create package.json for Node.js projects if missing
    if project_type in ["nextjs", "vite", "react"] and not os.path.exists("package.json"):
        print("⚠️ package.json not found. Creating a basic one...")
        package_json = {
            "name": PROJECT_DIR.name.lower().replace(" ", "-"),
            "version": "1.0.0",
            "description": "",
            "main": "index.js",
            "scripts": {
                "dev": "node index.js",
                "start": "node index.js",
                "build": "echo 'Build script not configured'"
            },
            "keywords": [],
            "author": "",
            "license": "ISC"
        }
        
        if project_type == "nextjs":
            package_json["scripts"]["dev"] = "next dev"
            package_json["scripts"]["build"] = "next build"
            package_json["scripts"]["start"] = "next start"
            package_json["dependencies"] = {"next": "latest", "react": "latest", "react-dom": "latest"}
        elif project_type == "vite":
            package_json["scripts"]["dev"] = "vite"
            package_json["scripts"]["build"] = "vite build"
            package_json["devDependencies"] = {"vite": "latest"}
        elif project_type == "react":
            package_json["dependencies"] = {"react": "latest", "react-dom": "latest"}
            
        with open("package.json", "w") as f:
            json.dump(package_json, f, indent=2)
        print("✅ Created package.json")
    
    # Create requirements.txt for Python projects if missing
    if project_type == "python-flask" and not os.path.exists("requirements.txt"):
        print("⚠️ requirements.txt not found. Creating a basic one...")
        with open("requirements.txt", "w") as f:
            f.write("Flask==2.0.1\n")
            f.write("gunicorn==20.1.0\n")
        print("✅ Created requirements.txt")
    
    # Create basic app.py for Flask projects if missing
    if project_type == "python-flask" and not os.path.exists("app.py"):
        print("⚠️ app.py not found. Creating a basic Flask app...")
        flask_app_content = '''from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello from Flask!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
'''
        with open("app.py", "w") as f:
            f.write(flask_app_content)
        print("✅ Created app.py")
    
    # Create vercel.json for Vercel deployments if missing
    if platform == "Vercel" and not os.path.exists("vercel.json"):
        print("⚠️ vercel.json not found. Creating configuration...")
        vercel_config = {
            "version": 2,
            "builds": [{"src": "app.py", "use": "@vercel/python"}],
            "routes": [{"src": "/(.*)", "dest": "/app.py"}]
        }
        
        if project_type == "python-flask":
            vercel_config["builds"] = [{"src": "api/index.py", "use": "@vercel/python"}]
            vercel_config["routes"] = [{"src": "/(.*)", "dest": "api/index.py"}]
            
        with open("vercel.json", "w") as f:
            json.dump(vercel_config, f, indent=2)
        print("✅ Created vercel.json")
    
    # Create index.html for static sites if missing
    if project_type == "static" and not os.path.exists("index.html"):
        print("⚠️ index.html not found. Creating a basic one...")
        html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>My Website</title>
</head>
<body>
    <h1>Welcome to My Website</h1>
    <p>This site was automatically deployed!</p>
</body>
</html>
'''
        with open("index.html", "w") as f:
            f.write(html_content)
        print("✅ Created index.html")
    
    return True

def build_project(project_type):
    """Build the project if necessary."""
    print("🔨 Building project...")

    # Check if Node.js/npm are available first for JS projects
    if project_type in ["nextjs", "vite", "react"]:
        if not check_node_installed():
            print("⚠️ Node.js is required. Please install from https://nodejs.org/")
            retry = input("Check again after install? (y/n): ")
            if retry.lower() == 'y' and not check_node_installed():
                return False
            return False

        if not os.path.exists("node_modules"):
            if not install_dependencies():
                return False

        try:
            print("🔧 Running npm run build...")
            result = subprocess.run("npm run build", capture_output=True, text=True, cwd=PROJECT_DIR, shell=True)
            if result.returncode == 0:
                print("✅ Build successful!")
                return True
            else:
                print(f"⚠️ Build failed: {result.stderr}")
                if "missing script" in result.stderr.lower() or "missing script" in result.stdout.lower():
                    print("💡 No build script found. Proceeding without build.")
                    return True
                if "not recognized" in result.stderr.lower() or "command not found" in result.stderr.lower():
                    if input("Install dependencies now? (y/n): ").lower() == 'y':
                        if install_dependencies():
                            retry_result = subprocess.run("npm run build", capture_output=True, text=True, cwd=PROJECT_DIR, shell=True)
                            if retry_result.returncode == 0:
                                return True
                return False
        except Exception as e:
            print(f"❌ Build error: {e}")
            return False
    else:
        print("ℹ️ No build step required.")
        return True

def vercel_login():
    """Guide user through Vercel login process."""
    print("🔐 Running 'vercel login'...")
    try:
        result = subprocess.run("vercel login", capture_output=False, text=True, shell=True)
        if result.returncode == 0:
            print("✅ Login successful!")
            return True
        else:
            print("⚠️ Login failed. Try manually.")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False

def deploy_to_netlify():
    """Deploy using Netlify CLI."""
    try:
        print("🔧 Initializing Netlify...")
        init_result = subprocess.run("netlify init --manual", capture_output=True, text=True, shell=True)
        if init_result.returncode != 0:
            print(f"⚠️ Init failed: {init_result.stderr}")
            if input("Log in to Netlify now? (y/n): ").lower() == 'y':
                subprocess.run("netlify login", capture_output=True, text=True, shell=True)

        print("🚀 Deploying to Netlify...")
        result = subprocess.run("netlify deploy --prod", capture_output=True, text=True, shell=True)
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
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def deploy_to_vercel():
    """Deploy using Vercel CLI."""
    try:
        whoami_result = subprocess.run("vercel whoami", capture_output=True, text=True, shell=True)
        if whoami_result.returncode != 0:
            if input("Log in to Vercel now? (y/n): ").lower() == 'y':
                if not vercel_login():
                    return False

        print("🚀 Deploying to Vercel...")
        result = subprocess.run("vercel --prod --yes", capture_output=True, text=True, shell=True)
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
        cmd = f"wrangler pages deploy {build_folder} --project-name {PROJECT_DIR.name}"
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
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
    files = [f.name for f in PROJECT_DIR.iterdir() if f.is_file()]
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
        whoami_result = subprocess.run("vercel whoami", capture_output=True, text=True, shell=True)
        if whoami_result.returncode != 0:
            if input("Log in to Vercel now? (y/n): ").lower() == 'y':
                if not vercel_login():
                    return False

        # Ensure api directory exists for Flask projects
        if not os.path.exists("api"):
            os.makedirs("api")
            
        # Move app.py to api/index.py for Vercel
        if os.path.exists("app.py") and not os.path.exists("api/index.py"):
            import shutil
            shutil.copy("app.py", "api/index.py")
            print("✅ Copied app.py to api/index.py for Vercel deployment")

        print("🚀 Deploying Flask to Vercel...")
        result = subprocess.run("vercel --prod --yes", capture_output=True, text=True, shell=True)
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
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def deploy_to_platform_flask(platform):
    """Deploy Flask project to the specified platform."""
    print(f"🚀 Deploying Flask to {platform}...")
    if platform == "Vercel":
        return deploy_to_vercel_flask()
    elif platform == "Render":
        return deploy_to_render()
    else:
        return deploy_to_platform(platform)

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
        print(f"❓ Unsupported: {platform}")
        return False

def main():
    print("🚀 Welcome to the Auto Deploy Agent CLI!")
    print(f"Scanning project in: {PROJECT_DIR}")

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
    else:
        print(f"\n❌ Deployment failed.")
        print("Troubleshooting: Check CLI login, internet, project setup.")
        print("Try manual deploy via platform dashboard.")

if __name__ == "__main__":
    main()