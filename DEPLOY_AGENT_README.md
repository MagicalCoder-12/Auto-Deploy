# Enhanced Deploy Agent

The enhanced deploy agent is a smart deployment tool that automatically detects your project type, recommends the best hosting platform using AI (Llama 3.1 via Ollama), and helps you deploy your site.

## Features

- **Automatic Project Detection**: Identifies project types including static HTML, React, Vite, Next.js, and Python Flask
- **AI-Powered Recommendations**: Uses Llama 3.1 to recommend the best hosting platform for your project
- **Multi-Platform Support**: Supports Netlify, Vercel, GitHub Pages, Cloudflare Pages, and Render
- **Automated Deployment**: Can automatically deploy to supported platforms
- **Step-by-Step Guidance**: Provides clear instructions for manual deployment when needed

## How It Works

1. **Project Detection**: The agent scans your project directory to identify the project type
2. **AI Recommendation**: Uses Llama 3.1 to recommend the best hosting platform
3. **Tool Installation**: Guides you through installing required CLIs
4. **Build Process**: Automatically builds your project if necessary
5. **Deployment**: Deploys your site to the recommended platform

## Supported Project Types

- Static HTML (`index.html` file)
- React (React in `package.json` dependencies)
- Vite (Vite in `package.json` devDependencies)
- Next.js (Next.js in `package.json` dependencies)
- Python Flask (`requirements.txt` file)

## Supported Platforms

- **Netlify**: Full automated deployment support
- **Vercel**: Full automated deployment support
- **GitHub Pages**: Instructions for manual setup
- **Cloudflare Pages**: Deployment using Wrangler CLI
- **Render**: Instructions for manual setup

## Usage

1. Navigate to your project directory:
   ```bash
   cd your-project-directory
   ```

2. Run the deploy agent:
   ```bash
   python path/to/deploy_agent.py
   ```

3. Follow the prompts to:
   - Install required CLIs
   - Build your project (if necessary)
   - Deploy to the recommended platform

## Requirements

- Python 3.x
- Ollama with Llama 3.1 model (`ollama pull llama3.1:8b`)
- Node.js and npm (for JavaScript projects)
- Platform-specific CLIs (the agent will guide you through installation)

## Enhancements Made

The enhanced deploy agent now includes:

1. **Full deployment support** for all major platforms
2. **Automatic project building** for JavaScript frameworks
3. **Improved error handling** and user feedback
4. **URL extraction** from deployment outputs when available
5. **Platform-specific deployment functions** with proper error handling

## Test Projects

This repository includes test projects for all supported project types:
- Static HTML project
- React project
- Vite project
- Python Flask project

Each test project can be used to verify the deploy agent functionality.