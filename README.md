# Deploy Agent Test Suite

This repository contains several test projects designed to showcase the capabilities of the [deploy_agent.py](file:///D:/programs/Python/Ollama/deploy_agent.py) script. Each project represents a different web project type that the deploy agent can detect and recommend deployment platforms for.

## Test Projects

### 1. Static HTML Project ([test-project/](file:///D:/programs/Python/Ollama/test-project/))
A simple static HTML website with basic styling.

**Project Type:** Static HTML
**Detection Method:** Presence of `index.html` file

### 2. React Project ([react-test-project/](file:///D:/programs/Python/Ollama/react-test-project/))
A minimal React project configuration.

**Project Type:** React
**Detection Method:** Presence of `react` in dependencies in `package.json`

### 3. Vite Project ([vite-test-project/](file:///D:/programs/Python/Ollama/vite-test-project/))
A minimal Vite project configuration.

**Project Type:** Vite
**Detection Method:** Presence of `vite` in devDependencies in `package.json`

### 4. Python Flask Project ([flask-test-project/](file:///D:/programs/Python/Ollama/flask-test-project/))
A minimal Flask web application.

**Project Type:** Python Flask
**Detection Method:** Presence of `requirements.txt` file

## How to Test

1. Navigate to any of the test project directories:
   ```bash
   cd test-project
   # or
   cd react-test-project
   # or
   cd vite-test-project
   # or
   cd flask-test-project
   ```

2. Run the deploy agent:
   ```bash
   python ../deploy_agent.py
   ```

3. The script will:
   - Detect the project type
   - Use Llama 3.1 (via Ollama) to recommend the best free hosting platform
   - Provide setup instructions
   - Guide you through the deployment process

## Requirements

- Python 3.x
- Ollama with Llama 3.1 model (`ollama pull llama3.1:8b`)
- Node.js and npm (for projects that require it)
- Appropriate CLIs for deployment platforms (the script will guide you through installation)

## Project Detection Logic

The deploy agent uses the following logic to detect project types:

1. **Next.js**: `package.json` contains `next` in dependencies
2. **Vite**: `package.json` contains `vite` in devDependencies
3. **React**: `package.json` contains `react` in dependencies
4. **Static**: Presence of `index.html` file
5. **Python Flask**: Presence of `requirements.txt` file

For each detected project type, the agent uses Llama 3.1 to recommend the most suitable free hosting platform from options including Netlify, Vercel, GitHub Pages, Cloudflare Pages, and Render.