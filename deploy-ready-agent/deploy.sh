#!/bin/bash

echo "🚀 Auto Deploy Agent CLI"
echo "========================"
echo
echo "This script will run the deploy agent which will:"
echo "1. Detect your project type"
echo "2. Recommend the best hosting platform"
echo "3. Guide you through installation of required tools"
echo "4. Deploy your site"
echo
read -p "Press Enter to continue..."
echo
python3 deploy_agent.py
echo
echo "Deployment process completed."
read -p "Press Enter to exit..."