#!/usr/bin/env python3
"""Configuration constants for Auto Deploy Agent"""

from pathlib import Path

PROJECT_DIR = Path.cwd()

# Default Ollama model to use
OLLAMA_MODEL = "llama3.1:8b"  # This will be updated based on user selection

# Platform recommendations mapping (fallback when Ollama is not available)
RECOMMENDATIONS = {
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
        "platform": "Vercel",
        "reason": "Vercel provides excellent support for Python web applications with easy deployment",
        "setup_steps": [
            "Install Vercel CLI: npm install -g vercel",
            "Login to Vercel: vercel login",
            "Deploy: vercel --prod"
        ]
    },
}

# List of platforms that may require payment
PAID_PLATFORMS = ["Fly.io", "Heroku", "Railway", "AWS", "GCP", "Azure", "DigitalOcean"]

# CLI tool mapping
CLI_MAP = {
    "Netlify": {"cmd": "netlify", "install": "npm install -g netlify-cli", "auto_install": True},
    "Vercel": {"cmd": "vercel", "install": "npm install -g vercel", "auto_install": True},
    "Cloudflare Pages": {"cmd": "wrangler", "install": "npm install -g wrangler", "auto_install": True},
    "GitHub Pages": {"cmd": "git", "install": "https://git-scm.com/downloads", "auto_install": False},

}