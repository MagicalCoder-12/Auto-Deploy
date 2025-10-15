# Flask Example Project

This is a simple Flask project that can be used to test the Auto Deploy Agent CLI.

## Project Structure

- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `api/` - Vercel serverless function directory
- `vercel.json` - Vercel deployment configuration

## How to Test

1. Navigate to this directory
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app locally:
   ```
   python app.py
   ```
4. To test with the Auto Deploy Agent CLI, run the deploy agent from this directory

## Deployment

This project is configured to work with Vercel out of the box. The `vercel.json` file tells Vercel how to deploy the application properly.