#!/usr/bin/env python3
"""Model selection module for Auto Deploy Agent"""

import sys

# Global variable to store the selected model
_SELECTED_MODEL = None

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    ollama = None
    OLLAMA_AVAILABLE = False

def get_available_models():
    """Get list of available Ollama models from the system."""
    if not OLLAMA_AVAILABLE:
        print("❌ Ollama is not installed or not available.")
        return []
    
    try:
        # List available models from Ollama
        response = ollama.list()
        models = response.get('models', [])
        model_names = [model.model for model in models]
        return model_names
    except Exception as e:
        print(f"❌ Error getting Ollama models: {e}")
        return []

def select_model_gui():
    """Display a GUI-like menu for selecting an Ollama model."""
    if not OLLAMA_AVAILABLE:
        print("❌ Ollama is not installed. Please install it first with 'pip install ollama'.")
        return "llama3.1:8b"  # fallback to default
    
    models = get_available_models()
    
    if not models:
        print("⚠️  No Ollama models found. Make sure Ollama is running and models are pulled.")
        print("   You can pull a model with: ollama pull llama3.1:8b")
        return input("Enter model name to use (default: llama3.1:8b): ").strip() or "llama3.1:8b"
    
    print("\n🎯 Available Ollama Models:")
    print("=" * 40)
    
    for i, model in enumerate(models, 1):
        print(f"{i:2d}. {model}")
    
    print(f"{len(models) + 1:2d}. Enter custom model name")
    print("=" * 40)
    
    while True:
        try:
            choice = input(f"\nSelect a model (1-{len(models) + 1}): ").strip()
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(models):
                selected_model = models[choice_num - 1]
                print(f"✅ Selected model: {selected_model}")
                return selected_model
            elif choice_num == len(models) + 1:
                custom_model = input("Enter custom model name: ").strip()
                if custom_model:
                    print(f"✅ Selected custom model: {custom_model}")
                    return custom_model
                else:
                    print("❌ Invalid input. Please enter a model name.")
            else:
                print(f"❌ Invalid selection. Please enter a number between 1 and {len(models) + 1}.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\n⚠️  Operation cancelled by user. Using default model: llama3.1:8b")
            return "llama3.1:8b"

def get_model_name():
    """Get the model name to use, with option to select from available models."""
    global _SELECTED_MODEL
    
    # If model has already been selected, return it
    if _SELECTED_MODEL is not None:
        return _SELECTED_MODEL
    
    # Check if we should use a default model or allow selection
    use_default = input("Do you want to select an Ollama model? (Y/n): ").strip().lower()
    
    if use_default in ['n', 'no']:
        _SELECTED_MODEL = "llama3.1:8b"  # default model
    else:
        _SELECTED_MODEL = select_model_gui()
    
    return _SELECTED_MODEL

if __name__ == "__main__":
    # Test the model selector
    selected_model = get_model_name()
    print(f"\nUsing model: {selected_model}")