# Troubleshooting Guide

This guide helps you resolve common issues with the deploy agent.

## Common Issues and Solutions

### 1. Script is stuck waiting for input

**Problem**: The deploy agent shows a message like "Press Enter after installing..." and doesn't continue.

**Solution**: 
1. Open a NEW terminal/command prompt
2. Run the installation command shown in the message
3. Wait for the installation to complete
4. Return to the original terminal and press Enter

### 2. "npm not found" or "node not found" errors

**Problem**: The deploy agent reports that Node.js or npm is not installed.

**Solution**:
1. Download and install Node.js from https://nodejs.org/
2. Restart your terminal/command prompt
3. Verify installation by running:
   ```bash
   node --version
   npm --version
   ```
4. Run the deploy agent again

### 3. "Netlify CLI not found" error

**Problem**: The deploy agent can't find the Netlify CLI.

**Solution**:
1. Install the Netlify CLI:
   ```bash
   npm install -g netlify-cli
   ```
2. Verify installation:
   ```bash
   netlify --version
   ```
3. Run the deploy agent again

### 4. "Vercel CLI not found" error

**Problem**: The deploy agent can't find the Vercel CLI.

**Solution**:
1. Install the Vercel CLI:
   ```bash
   npm install -g vercel
   ```
2. Verify installation:
   ```bash
   vercel --version
   ```
3. Run the deploy agent again

### 5. Authentication required

**Problem**: Platforms like Vercel or Netlify require authentication.

**Solution**:
1. The deploy agent will prompt you to log in
2. Choose "y" to proceed with authentication
3. Follow the browser-based authentication flow
4. Return to the terminal after authenticating

### 6. Deployment fails after authentication

**Problem**: Deployment still fails even after installing CLI tools and authenticating.

**Solution**:
1. Try running the deployment command manually:
   ```bash
   # For Netlify
   netlify deploy --prod
   
   # For Vercel
   vercel --prod --yes
   ```
2. Check the error message for specific details
3. Make sure you have an internet connection

## Platform-Specific Troubleshooting

### Netlify Issues

1. **Login issues**:
   ```bash
   netlify login
   ```

2. **Manual deployment**:
   ```bash
   netlify deploy --prod
   ```

### Vercel Issues

1. **Login issues**:
   ```bash
   vercel login
   ```

2. **Check authentication**:
   ```bash
   vercel whoami
   ```

### GitHub Pages Issues

1. Make sure your project is on GitHub
2. Check repository settings → Pages
3. Ensure the correct branch and folder are selected

## General Tips

1. **Always use a fresh terminal** after installing new tools
2. **Check your internet connection** before deploying
3. **Read error messages carefully** - they often contain specific solutions
4. **Verify tool installation** with `--version` commands
5. **Restart the deploy agent** after fixing issues

## Manual Deployment

If the automated deployment continues to fail, you can deploy manually:

1. **Netlify**: 
   - Go to https://netlify.com
   - Create an account
   - Drag and drop your site folder to deploy

2. **Vercel**:
   - Go to https://vercel.com
   - Create an account
   - Import your Git repository or upload your site

3. **GitHub Pages**:
   - Push your site to a GitHub repository
   - Go to repository Settings → Pages
   - Select your source and save

## Need More Help?

1. Check the platform's official documentation
2. Verify all requirements are installed
3. Try running the deploy agent again
4. Contact support for the specific platform if issues persist