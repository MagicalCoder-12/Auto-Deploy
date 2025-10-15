# Auto Deploy Agent CLI

A command-line tool that automatically detects, builds, and deploys web projects to the most suitable hosting platform.

## Features

- 🔍 **Automatic Project Detection**: Identifies project types (Next.js, Vite, React, Flask, static sites)
- 🤖 **Smart Platform Recommendation**: Suggests the best hosting platform for your project
- 🚀 **One-Command Deployment**: Deploys your project with a single command
- 🛠️ **Automatic CLI Installation**: Guides you through installing required CLIs
- 📦 **Dependency Management**: Automatically installs project dependencies
- 🔧 **Build Automation**: Handles project building when necessary

## Supported Project Types

- Next.js
- Vite
- React
- Flask (Python)
- Static HTML/CSS/JS sites

## Supported Platforms

- Vercel
- Netlify
- GitHub Pages
- Cloudflare Pages
- Render

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Navigate to your web project directory
2. Run the deploy agent:
   ```bash
   python deploy_agent.py
   ```

The tool will:
1. Detect your project type
2. Recommend the best hosting platform
3. Guide you through CLI installation if needed
4. Build your project if necessary
5. Deploy your project

## How It Works

1. **Detection**: The tool scans your project directory to identify the project type based on files like `package.json`, `requirements.txt`, or `index.html`.

2. **Recommendation**: Based on your project type, it recommends the most suitable hosting platform.

3. **Setup**: It guides you through installing any required CLIs.

4. **Build**: If your project requires building (Next.js, Vite, React), it will automatically run the build process.

5. **Deploy**: It deploys your project to the recommended platform using the appropriate CLI commands.

## Project-Specific Configurations

### Flask Projects

For Flask projects, the tool automatically creates a `vercel.json` configuration file if deploying to Vercel, ensuring proper deployment.

## Troubleshooting

If you encounter issues:

1. Ensure all required CLIs are installed and accessible
2. Check your internet connection
3. Verify you're logged in to your chosen platform
4. Make sure your project builds locally before deploying

For Flask projects deployed to Vercel, ensure:
- Your Flask app exposes an `application` variable
- `gunicorn` is included in your `requirements.txt`
- Your project structure matches Vercel's expectations