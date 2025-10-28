#!/usr/bin/env python3
"""Project detection module for Auto Deploy Agent"""

import json
import os
from pathlib import Path

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

from config import PROJECT_DIR

def detect_project_type():
    """Detect what kind of web project this is using Ollama with Llama3.1."""
    files = [f.name for f in PROJECT_DIR.iterdir() if f.is_file()]
    folders = [f.name for f in PROJECT_DIR.iterdir() if f.is_dir()]

    if OLLAMA_AVAILABLE:
        try:
            prompt = f"""
            You are an expert DevOps assistant. Based on these files: {', '.join(files)} and folders: {', '.join(folders)},
            detect the web project type. Possible types: nextjs, vite, react, static, python-flask, or unknown.
            Respond in JSON format: {{"type": "...", "reason": "..."}}.
            """
            response = ollama.chat(
                model="llama3.1:8b",  # Updated to use llama3.1:8b model
                messages=[{"role": "user", "content": prompt}],
                format="json"
            )
            result = json.loads(response["message"]["content"])
            print(f"🔍 Project detection reason: {result['reason']}")
            return result["type"]
        except Exception as e:
            print(f"⚠️ Ollama detection failed: {e}")
            print("Falling back to default detection...")

    # Fallback to original hardcoded detection
    if "package.json" in files:
        try:
            with open("package.json") as f:
                pkg = json.load(f)
            if "next" in pkg.get("dependencies", {}):
                return "nextjs"
            elif "vite" in pkg.get("devDependencies", {}):
                return "vite"
            elif "react" in pkg.get("dependencies", {}):
                return "react"
        except json.JSONDecodeError:
            pass

    if "index.html" in files:
        return "static"

    if "requirements.txt" in files:
        return "python-flask"

    return "unknown"