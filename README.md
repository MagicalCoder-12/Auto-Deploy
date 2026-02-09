# Auto Deploy Agent CLI

A command-line tool that automatically detects, builds, and deploys web projects to the most suitable hosting platform using AI-powered recommendations.

## Preview

[![Preview](preview.png)](https://auto-deploy-website-roeqwymq8-magicalcoder-12s-projects.vercel.app)

Click to watch a video demo of how to use this project

## Features

- 🔍 **Automatic Project Detection**: Identifies project types (Next.js, Vite, React, Flask, static sites)
- 🤖 **AI-Powered Platform Recommendation**: Uses Ollama with Llama 3.1 model to suggest the best hosting platform
- 🚀 **One-Command Deployment**: Deploys your project with a single command
- 🛠️ **Automatic CLI Installation**: Guides you through installing required CLIs
- 📦 **Dependency Management**: Automatically installs project dependencies
- 🔧 **Build Automation**: Handles project building when necessary
- 📁 **Modular Architecture**: Code is organized into separate modules for easier maintenance

## Prerequisites

1. **Ollama**: Install Ollama from https://ollama.com/ and pull the Llama 3.1 model:
   ```bash
   ollama pull llama3.1:8b
   ```

2. **Python**: Python 3.6 or higher

3. **Git**: Required for deployment to platforms that use Git-based deployment (GitHub Pages, Render)

## Supported Project Types

- Next.js
- Vite
- React
- Flask (Python)
- Static HTML/CSS/JS sites

## Supported Platforms

- Vercel (automated deployment)
- Netlify (automated deployment)
- GitHub Pages (manual deployment instructions)
- Cloudflare Pages (automated deployment)
- Render (manual deployment instructions)

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Install dependencies using the modern PEP 517 build system:
   ```bash
   pip install .
   ```
   This will install the package and make the `deploy-agent` command available globally.

4. Verify installation:
   ```bash
   deploy-agent
   ```

5. Ensure Ollama is installed from https://ollama.com/ and pull the Llama 3.1 model:
   ```bash
   ollama pull llama3.1:8b
   ```

### Alternative: Run without installation
If you prefer not to install the package globally, you can run directly from the project directory without installation:

```bash
# Run with Python
python main.py
```

or use the provided scripts from the project root:
- **Windows**: `deploy.bat`
- **macOS/Linux**: `./deploy.sh`

**Note:** When running without installation, the Auto Deploy directory must be in your project's root for proper functionality.

## Platform CLI Installation Commands

If you prefer to manually install the required CLIs for each platform, you can use the following commands:

### Vercel
```bash
npm install -g vercel
```

### Netlify
```bash
npm install -g netlify-cli
```

### Cloudflare Pages
```bash
npm install -g wrangler
```

### GitHub Pages and Render
These platforms use Git for deployment, so you need to have Git installed:
```bash
# For Windows: Download from https://git-scm.com/downloads
# For macOS (with Homebrew):
brew install git
# For Ubuntu/Debian:
sudo apt install git
# For CentOS/RHEL:
sudo yum install git
```

## Usage

You can run the Auto Deploy Agent in several ways:

### Method 1: Using the provided scripts (Recommended)
From the project directory, run:
- **Windows**: `deploy.bat`
- **macOS/Linux**: `./deploy.sh`

### Method 2: Using the installed CLI command
If you installed the package with `pip install .`, you can run:
```bash
deploy-agent
```

### Method 3: Direct Python execution
From the project directory, run:
```bash
python main.py
```

The tool will:
1. Detect your project type
2. Use Ollama with Llama 3.1 to recommend the best hosting platform
3. Guide you through CLI installation if needed
4. Build your project if necessary
5. Deploy your project or provide deployment instructions

## Modular Architecture

The code has been restructured into a modular architecture for better maintainability:

```
Auto Deploy/
├── core/                      # Core functionality modules
│   ├── detector.py            # Project detection logic
│   ├── recommender.py         # Platform recommendation logic
│   ├── model_selector.py      # Ollama model selection
│   ├── cli_manager.py         # CLI tool management
│   ├── git_handler.py         # Git operations
│   ├── builder.py             # Build processes
│   ├── deployer.py            # Deployment functions
│   ├── file_manager.py        # File creation and management
│   └── __init__.py
├── utils/                     # Utility functions
│   └── helpers.py
├── auto_deploy_agent_cli/     # CLI package
│   ├── deploy_agent.py        # CLI entry point
│   └── __init__.py
├── config.py                  # Configuration constants
├── main.py                    # Main entry point
├── deploy.bat                 # Windows deployment script
├── deploy.sh                  # macOS/Linux deployment script
└── pyproject.toml             # Project metadata and dependencies
```

## How It Works

1. **Detection**: Scans your project to identify the type based on files like `package.json`, `requirements.txt`, or `index.html`
2. **AI Recommendation**: Uses Ollama with Llama 3.1 to recommend the best hosting platform with setup steps
3. **CLI Setup**: Guides you through installing required platform CLIs
4. **Build**: Automatically builds your project if needed (Next.js, Vite, React, etc.)
5. **Deploy**: Either automates deployment (Vercel, Netlify, Cloudflare Pages) or provides step-by-step instructions (GitHub Pages, Render)

## Flask-Specific Configuration

For Flask projects deployed to Vercel, the tool automatically creates a `vercel.json` configuration file. Ensure:
- Your Flask app exports an `application` variable
- `gunicorn` is in your `requirements.txt`
- Your project structure matches Vercel's expectations

## Deployment Types

**Automated Deployment** (Vercel, Netlify, Cloudflare Pages):
- The agent automatically handles authentication, initialization, and deployment
- Provides the live URL upon successful deployment

**Manual Deployment** (GitHub Pages, Render):
- GitHub Pages: Push code to GitHub and enable Pages in repository settings
- Render: Create account, connect your Git repository, and configure build settings
- The agent provides detailed step-by-step instructions for each platform

## Troubleshooting

**Common issues:**
- **Ollama not running**: Ensure Ollama is installed and the `llama3.1:8b` model is pulled
- **CLI tools not found**: Install required CLIs (Vercel, Netlify, Wrangler) using the commands in the Platform CLI Installation section
- **Deployment failure**: Check internet connection, verify you're logged in to your platform, and ensure your project builds locally
- **Flask to Vercel**: Make sure `gunicorn` is in `requirements.txt` and your app exports an `application` variable
