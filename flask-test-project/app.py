from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Flask Test Project</h1><p>This is a simple Flask project for testing the deploy_agent.py script.</p>'

if __name__ == '__main__':
    app.run(debug=True)