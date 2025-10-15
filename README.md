# Auto Deploy Agent CLI

A command-line tool that automatically detects, builds, and deploys web projects to the most suitable hosting platform using AI-powered recommendations.

## Features

- 🔍 **Automatic Project Detection**: Identifies project types (Next.js, Vite, React, Flask, static sites)
- 🤖 **AI-Powered Platform Recommendation**: Uses Ollama with Llama 3.1 model to suggest the best hosting platform
- 🚀 **One-Command Deployment**: Deploys your project with a single command
- 🛠️ **Automatic CLI Installation**: Guides you through installing required CLIs
- 📦 **Dependency Management**: Automatically installs project dependencies
- 🔧 **Build Automation**: Handles project building when necessary

## Prerequisites

1. **Ollama**: Install Ollama from https://ollama.com/ and pull the Llama 3.1 model:
   ```bash
   ollama pull llama3.1:8b
   ```

2. **Python**: Python 3.6 or higher

3. **Platform-specific requirements**:
   - For Node.js projects: Node.js and npm
   - For Python projects: Python and pip

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
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install Ollama from https://ollama.com/ if not already installed
5. Pull the Llama 3.1 model:
   ```bash
   ollama pull llama3.1:8b
   ```

## Usage

1. Navigate to your web project directory
2. Run the deploy agent:
   ```bash
   python deploy_agent.py
   ```

The tool will:
1. Detect your project type
2. Use Ollama with Llama 3.1 to recommend the best hosting platform
3. Guide you through CLI installation if needed
4. Build your project if necessary
5. Deploy your project or provide deployment instructions

## How It Works

1. **Detection**: The tool scans your project directory to identify the project type based on files like `package.json`, `requirements.txt`, or `index.html`.

2. **AI Recommendation**: Uses Ollama with the Llama 3.1 model to analyze your project and recommend the most suitable hosting platform with personalized setup steps.

3. **Setup**: It guides you through installing any required CLIs.

4. **Build**: If your project requires building (Next.js, Vite, React), it will automatically run the build process.

5. **Deploy**: 
   - For platforms with CLI support (Vercel, Netlify, Cloudflare Pages), it performs automated deployment
   - For platforms requiring manual steps (GitHub Pages, Render), it provides detailed deployment instructions

## Project-Specific Configurations

### Flask Projects

For Flask projects, the tool automatically creates a `vercel.json` configuration file if deploying to Vercel, ensuring proper deployment.

## Deployment Types

### Automated Deployment (Vercel, Netlify, Cloudflare Pages)
These platforms have CLI tools that allow for fully automated deployment. The agent will:
1. Check authentication
2. Initialize the project
3. Deploy to the platform
4. Provide the live URL

### Manual Deployment (GitHub Pages, Render)
These platforms require manual steps to complete deployment:
- GitHub Pages: Requires pushing code to GitHub and enabling Pages in settings
- Render: Requires creating an account and connecting your Git repository

The agent provides detailed step-by-step instructions for completing these manual deployments.

## Troubleshooting

If you encounter issues:

1. Ensure Ollama is installed and the llama3.1:8b model is pulled
2. Ensure all required CLIs are installed and accessible
3. Check your internet connection
4. Verify you're logged in to your chosen platform
5. Make sure your project builds locally before deploying

For Flask projects deployed to Vercel, ensure:
- Your Flask app exposes an `application` variable
- `gunicorn` is included in your `requirements.txt`
- Your project structure matches Vercel's expectations