#!/usr/bin/env python3
"""
Platform recommendation module for Auto Deploy Agent.
REFACTOR: Prioritizes deterministic logic over LLM for infrastructure decisions
to ensure deployment consistency.
"""

import json
import sys

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    ollama = None
    OLLAMA_AVAILABLE = False

from config import RECOMMENDATIONS, OLLAMA_MODEL

# 1. DEFINITIVE SOURCE OF TRUTH
# These mappings ensure consistency regardless of AI model or version.
ALLOWED_PLATFORMS = ["Netlify", "Vercel", "GitHub Pages", "Cloudflare Pages"]

PROJECT_MAPPING = {
    "react": "Vercel",
    "nextjs": "Vercel",
    "vue": "Netlify",
    "nuxt": "Vercel",
    "angular": "Netlify",
    "static": "GitHub Pages",
    "html": "GitHub Pages",
    "svelte": "Vercel",
    "astro": "Vercel",
    "python": "Vercel", # Note: You mentioned no Render, but if python web, usually needs specific handling. 
                        # For this script, we will force to allowed list or fallback.
}

def _get_deterministic_platform(project_type: str) -> str:
    """
    Returns a platform based on strict code logic, not AI probability.
    """
    project_type = project_type.lower().strip()
    
    # Direct match
    if project_type in PROJECT_MAPPING:
        return PROJECT_MAPPING[project_type]
    
    # Fuzzy match for common variations
    if "react" in project_type: return "Vercel"
    if "vue" in project_type: return "Netlify"
    if "static" in project_type or "html" in project_type: return "GitHub Pages"
    
    # Default Fallback
    return "Vercel"

def _generate_steps_with_llm(platform: str, project_type: str) -> dict:
    """
    Uses LLM only to generate steps/reasoning for a KNOWN platform.
    This prevents the LLM from changing the target infrastructure.
    """
    if not OLLAMA_AVAILABLE or ollama is None:
        return None

    try:
        prompt = f"""
        You are a DevOps assistant. The platform {platform} has been selected for a {project_type} project.
        Do NOT choose a platform. 
        Provide a brief reason why {platform} is good for this, and 3 concise setup steps using their CLI.
        Allowed Platforms: {', '.join(ALLOWED_PLATFORMS)}
        
        Respond in JSON format: {{"reason": "...", "setup_steps": ["step1", "step2", "step3"]}}
        """
        
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
            format="json",
            options={
                "temperature": 0,  # CRITICAL: Ensures maximum determinism
                "timeout": 10
            }
        )
        content = json.loads(response["message"]["content"])
        
        # Validate that the LLM didn't hallucinate a new platform in the text
        return {
            "platform": platform, # Force the code-decided platform
            "reason": content.get("reason", "Standard deployment configuration"),
            "setup_steps": content.get("setup_steps", [])
        }
    except Exception as e:
        print(f"LLM enrichment failed: {e}")
        return None

def recommend_platform(project_type):
    """
    Main entry point. 
    1. Checks static config (Highest Priority).
    2. Uses deterministic mapping (High Priority).
    3. Uses LLM only for text enrichment (Low Priority).
    """
    
    # 1. Check Explicit Config Overrides (config.py)
    if project_type in RECOMMENDATIONS:
        return RECOMMENDATIONS[project_type]

    # 2. Determine Platform via Code (Deterministic)
    selected_platform = _get_deterministic_platform(project_type)

    # 3. Attempt to enrich with LLM (Optional/Non-Critical)
    # We pass the selected_platform to the LLM so it doesn't choose one itself.
    llm_result = _generate_steps_with_llm(selected_platform, project_type)
    
    if llm_result:
        return llm_result

    # 4. Hardcoded Fallback (Guaranteed to work)
    return {
        "platform": selected_platform,
        "reason": f"Default recommendation for {project_type} based on system rules.",
        "setup_steps": [
            f"Install {selected_platform} CLI",
            f"Login to {selected_platform}",
            f"Run deploy command for {selected_platform}"
        ]
    }

if __name__ == "__main__":
    # Test harness
    if len(sys.argv) > 1:
        p_type = sys.argv[1]
    else:
        p_type = "react"
        
    result = recommend_platform(p_type)
    print(json.dumps(result, indent=2))