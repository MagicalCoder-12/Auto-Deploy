#!/bin/bash

echo "🚀 Auto Deploy Agent CLI"
echo "========================"
echo
echo "This script will run the deploy agent which will:"
echo "1. Detect your project type"
echo "2. Use AI (Ollama with Llama 3.1) to recommend the best hosting platform"
echo "3. Guide you through installation of required tools"
echo "4. Deploy your site (or provide deployment instructions)"
echo
read -p "Press Enter to continue..."
echo

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory to ensure we can find our modules
cd "$SCRIPT_DIR"

# Add the script directory to PYTHONPATH so modules can be found
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Run the main.py file which contains the modularized code
python3 main.py

# Check if the command was successful
if [ $? -ne 0 ]; then
    echo
    echo "❌ An error occurred while running the deploy agent."
    echo "Please make sure:"
    echo "1. Python is installed and accessible from the command line"
    echo "2. Required dependencies are installed (pip install -r requirements.txt)"
    echo "3. Ollama is installed and the llama3.1:8b model is pulled"
    echo
    echo "For more information, check the README.md file."
fi

echo
echo "Deployment process completed."
echo "Note: For some platforms (like GitHub Pages), you may need to"
echo "complete manual steps to finish deployment."
read -p "Press Enter to exit..."