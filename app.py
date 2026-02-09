from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello from Flask!</h1>'

# Expose the Flask app as 'application' for Vercel
application = app

if __name__ == '__main__':
    app.run(debug=True)
