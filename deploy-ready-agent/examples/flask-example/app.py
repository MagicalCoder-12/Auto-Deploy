from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Flask Test Project</h1><p>This is a simple Flask project for testing the deploy agent.</p>'

# Vercel requires the app to be exposed as `application`
application = app

if __name__ == '__main__':
    # Use the PORT environment variable if provided (for Vercel)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)