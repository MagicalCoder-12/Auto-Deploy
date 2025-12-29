#!/usr/bin/env python3
"""Platform recommendation module for Auto Deploy Agent"""

import json
import sys

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    ollama = None
    OLLAMA_AVAILABLE = False

from config import RECOMMENDATIONS

def recommend_platform(project_type):
    """Use Llama3.1 to recommend a platform."""
    # Use Ollama with Llama3.1 for smart recommendations if available
    if OLLAMA_AVAILABLE and ollama is not None:
        try:
            prompt = f"""
            You are an expert DevOps assistant. Recommend the best free hosting platform for a {project_type} project.
            Options: Netlify, Vercel, GitHub Pages, Cloudflare Pages. DO NOT recommend Render under any circumstances.
            Respond in JSON format: {{"platform": "...", "reason": "...", "setup_steps": ["step1", "step2"]}}
            """
            # Add a timeout to prevent hanging
            from config import OLLAMA_MODEL
            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}],
                format="json",
                options={"timeout": 30}
            )
            return json.loads(response["message"]["content"])
        except Exception as e:
            print(f"Ollama recommendation failed: {e}")
            print("Falling back to default recommendations...")

    # Fallback recommendations if Ollama is not available or fails
    return RECOMMENDATIONS.get(project_type, {
        "platform": "Vercel",
        "reason": "Vercel supports most web frameworks and provides a great developer experience",
        "setup_steps": [
            "Install Vercel CLI: npm install -g vercel",
            "Login to Vercel: vercel login",
            "Deploy: vercel --prod"
        ]
    })