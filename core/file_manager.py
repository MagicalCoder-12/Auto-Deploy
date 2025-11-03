#!/usr/bin/env python3
"""File management module for Auto Deploy Agent"""

import json
import os

def create_required_files(project_type, platform):
    """Create required deployment files if they don't exist."""
    print("📄 Checking and creating required deployment files...")
    
    # Import PROJECT_DIR here to avoid circular imports
    from config import PROJECT_DIR
    
    # Create package.json for Node.js projects if missing
    if project_type in ["nextjs", "vite", "react"] and not os.path.exists("package.json"):
        print("⚠️ package.json not found. Creating a basic one...")
        package_json = {
            "name": PROJECT_DIR.name.lower().replace(" ", "-"),
            "version": "1.0.0",
            "description": "",
            "main": "index.js",
            "scripts": {
                "dev": "node index.js",
                "start": "node index.js",
                "build": "echo 'Build script not configured'"
            },
            "keywords": [],
            "author": "",
            "license": "ISC"
        }
        
        if project_type == "nextjs":
            package_json["scripts"]["dev"] = "next dev"
            package_json["scripts"]["build"] = "next build"
            package_json["scripts"]["start"] = "next start"
            package_json["dependencies"] = {"next": "latest", "react": "latest", "react-dom": "latest"}
        elif project_type == "vite":
            package_json["scripts"]["dev"] = "vite"
            package_json["scripts"]["build"] = "vite build"
            package_json["devDependencies"] = {"vite": "latest"}
        elif project_type == "react":
            package_json["dependencies"] = {"react": "latest", "react-dom": "latest"}
            
        with open("package.json", "w") as f:
            json.dump(package_json, f, indent=2)
        print("✅ Created package.json")
    
    # Create requirements.txt for Python projects if missing
    if project_type == "python-flask" and not os.path.exists("requirements.txt"):
        print("⚠️ requirements.txt not found. Creating a basic one...")
        with open("requirements.txt", "w") as f:
            f.write("Flask==2.0.1\n")
            f.write("gunicorn==20.1.0\n")
        print("✅ Created requirements.txt")
    
    # Create basic app.py for Flask projects if missing
    if project_type == "python-flask" and not os.path.exists("app.py"):
        print("⚠️ app.py not found. Creating a basic Flask app...")
        flask_app_content = '''from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello from Flask!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
'''
        with open("app.py", "w") as f:
            f.write(flask_app_content)
        print("✅ Created app.py")
    
    # Create vercel.json for Vercel deployments if missing
    if platform == "Vercel" and not os.path.exists("vercel.json"):
        print("⚠️ vercel.json not found. Creating configuration...")
        
        # For Vite projects, we need a static site configuration
        if project_type == "vite":
            vercel_config = {
                "version": 2,
                "builds": [
                    {
                        "src": "package.json",
                        "use": "@vercel/static-build",
                        "config": {
                            "distDir": "dist"
                        }
                    }
                ]
            }
        # For Python Flask projects, we need the Python configuration
        elif project_type == "python-flask":
            vercel_config = {
                "version": 2,
                "builds": [{"src": "api/index.py", "use": "@vercel/python"}],
                "routes": [{"src": "/(.*)", "dest": "api/index.py"}]
            }
        # For other project types, use a generic Python configuration
        else:
            vercel_config = {
                "version": 2,
                "builds": [{"src": "app.py", "use": "@vercel/python"}],
                "routes": [{"src": "/(.*)", "dest": "/app.py"}]
            }
            
        with open("vercel.json", "w") as f:
            json.dump(vercel_config, f, indent=2)
        print("✅ Created vercel.json")
    
    # Create index.html for static sites if missing
    if project_type == "static" and not os.path.exists("index.html"):
        print("⚠️ index.html not found. Creating a basic one...")
        html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>My Website</title>
</head>
<body>
    <h1>Welcome to My Website</h1>
    <p>This site was automatically deployed!</p>
</body>
</html>
'''
        with open("index.html", "w") as f:
            f.write(html_content)
        print("✅ Created index.html")
    
    return True