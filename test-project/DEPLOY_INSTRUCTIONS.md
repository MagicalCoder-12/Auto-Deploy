# Deployment Instructions

You can run the deploy agent in several ways:

## Method 1: Direct Execution (Recommended)
Simply run the deploy agent directly from this directory:

```bash
# On Windows (Command Prompt)
python deploy_agent.py

# On Windows (PowerShell)
python deploy_agent.py

# On macOS/Linux
python3 deploy_agent.py
```

## Method 2: Using Batch File (Windows)
Double-click the [deploy.bat](file:///D:/programs/Python/Ollama/test-project/deploy.bat) file or run it from the command prompt:

```cmd
deploy.bat
```

## Method 3: Using PowerShell Script (Windows)
Run the PowerShell script:

```powershell
.\deploy.ps1
```

## Method 4: Using Shell Script (macOS/Linux)
Make the script executable and run it:

```bash
chmod +x deploy.sh
./deploy.sh
```

## Method 5: From Parent Directory
You can still run it from the parent directory as before:

```bash
python ../deploy_agent.py
```

## How It Works

The deploy agent will:
1. Automatically detect your project type
2. Recommend the best hosting platform using AI
3. Guide you through installing required tools
4. Build your project if necessary
5. Deploy to the recommended platform

## Requirements

- Python 3.x
- Ollama with Llama 3.1 model (`ollama pull llama3.1:8b`)
- Node.js and npm (for JavaScript projects)
- Platform-specific CLIs (the agent will guide you through installation)

## Troubleshooting

If you encounter issues:

1. **Script is stuck waiting for input**: 
   - Open a NEW terminal
   - Run the installation command shown
   - Wait for completion
   - Return and press Enter

2. **"npm not found" errors**:
   - Install Node.js from https://nodejs.org/
   - Restart your terminal
   - Verify with `npm --version`

3. **CLI tools not found**:
   - Install the required CLI (Netlify, Vercel, etc.)
   - Restart your terminal
   - Verify installation with `--version` command

4. **Authentication issues**:
   - The agent will prompt you to log in
   - Follow the browser-based authentication
   - Return to the terminal after authenticating

For detailed troubleshooting, see [TROUBLESHOOTING.md](file:///D:/programs/Python/Ollama/test-project/TROUBLESHOOTING.md).