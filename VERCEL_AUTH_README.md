# Vercel Authentication Helper

This script helps you authenticate with Vercel for deployment purposes.

## Usage

1. **Check authentication status and login if needed**:
   ```bash
   python vercel_auth.py
   ```
   or
   ```bash
   python vercel_auth.py login
   ```

2. **Logout from Vercel**:
   ```bash
   python vercel_auth.py logout
   ```

## What it does

1. **Checks if Vercel CLI is installed**
2. **Verifies your authentication status**
3. **Guides you through the login process if needed**
4. **Handles the browser-based authentication flow**

## How it works

When you run the script:

1. It first checks if the Vercel CLI is installed
2. Then it checks if you're already logged in
3. If not logged in, it will:
   - Prompt you to continue with login
   - Run `vercel login` which opens a browser window
   - Guide you through the authentication process

## Manual Authentication

If you prefer to authenticate manually, you can:

1. Run `vercel login` directly in your terminal
2. Follow the browser-based authentication flow
3. Verify your login with `vercel whoami`

## Troubleshooting

**If login fails**:
- Make sure you have a stable internet connection
- Check that the Vercel CLI is properly installed (`vercel --version`)
- Try running `vercel login` directly in your terminal

**If you're still having issues**:
- You can deploy manually through the Vercel dashboard
- Make sure your project is on GitHub/GitLab for easy import