# Deployment Guide: FastAPI to Vercel

This guide will walk you through deploying your FastAPI application to Vercel via GitHub.

**Note:** Only the FastAPI backend is deployed to Vercel. The Streamlit frontend in the `frontend/` folder is for local testing only and is excluded from deployment.

## Prerequisites

- GitHub account
- Vercel account (sign up at [vercel.com](https://vercel.com))
- Git installed on your machine

## Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface

1. Go to [github.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name your repository (e.g., `backend-real-estate-api`)
5. Choose visibility (Public or Private)
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

### Option B: Using GitHub CLI

```bash
gh repo create backend-real-estate-api --public
```

## Step 2: Initialize Git and Push to GitHub

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: FastAPI Real Estate API"

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/backend-real-estate-api.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard

1. Go to [vercel.com](https://vercel.com) and sign in (or sign up)
2. Click "Add New..." → "Project"
3. Click "Import Git Repository"
4. Select your GitHub repository (`backend-real-estate-api`)
5. Vercel will automatically detect FastAPI:
   - Framework Preset: FastAPI (auto-detected)
   - Root Directory: `./` (leave as default)
   - Build Command: Leave empty (or set to `pip install -r requirements.txt`)
   - Output Directory: Leave empty
   - Install Command: `pip install -r requirements.txt`

6. **Add Environment Variables:**
   - Click "Environment Variables"
   - Add: `GEMINI_API_KEY` = `your_actual_api_key_here`
   - Make sure it's set for Production, Preview, and Development

7. Click "Deploy"
8. Wait for deployment to complete (usually 1-2 minutes)

### Option B: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project directory
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? (select your account)
# - Link to existing project? N
# - Project name: backend-real-estate-api
# - Directory: ./
# - Override settings? N

# Add environment variable
vercel env add GEMINI_API_KEY

# Deploy to production
vercel --prod
```

## Step 4: Verify Deployment

1. After deployment, Vercel will provide you with a URL like:
   `https://your-project-name.vercel.app`

2. Test your endpoints:
   ```bash
   # Health check
   curl https://your-project-name.vercel.app/health

   # Find apartment
   curl -X POST https://your-project-name.vercel.app/tool/find-apartment \
     -H "Content-Type: application/json" \
     -d '{"query": "I need a 2 bedroom apartment in Miami"}'
   ```

3. Visit the API docs at:
   `https://your-project-name.vercel.app/docs`

## Step 5: Continuous Deployment

Once connected to GitHub, Vercel will automatically:
- Deploy every push to `main` branch to production
- Create preview deployments for pull requests
- Rebuild on every commit

## Important Notes

### Environment Variables

Make sure to add `GEMINI_API_KEY` in Vercel:
1. Go to your project in Vercel dashboard
2. Settings → Environment Variables
3. Add `GEMINI_API_KEY` with your actual API key
4. Select all environments (Production, Preview, Development)
5. Redeploy if needed

### File Structure for Vercel

Vercel automatically detects FastAPI if:
- `app.py`, `index.py`, or `server.py` exists in root
- Or specified in `pyproject.toml`

Our project uses `app.py` in the root, which is automatically detected.

### Limitations

- Function size limit: 250MB (all dependencies must fit)
- Cold starts: First request may be slower
- Timeout: 10 seconds on Hobby plan, 60 seconds on Pro

## Troubleshooting

### Build Fails
- Check that all dependencies in `requirements.txt` are compatible
- Verify Python version compatibility
- Check build logs in Vercel dashboard

### Module Not Found
- Ensure all directories (`services/`, `models/`, `utils/`) are committed to Git
- Check that `__init__.py` files exist in all Python packages

### API Key Not Working
- Verify environment variable is set in Vercel
- Check that variable name matches exactly: `GEMINI_API_KEY`
- Redeploy after adding environment variables

## Useful Commands

```bash
# View deployment logs
vercel logs

# View environment variables
vercel env ls

# Pull environment variables locally
vercel env pull .env.local

# Deploy preview
vercel

# Deploy production
vercel --prod
```

## Next Steps

- Set up custom domain (optional)
- Configure CORS if needed for specific domains
- Set up monitoring and alerts
- Configure webhooks for CI/CD

## Resources

- [Vercel FastAPI Documentation](https://vercel.com/docs/frameworks/backend/fastapi)
- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [Vercel CLI Documentation](https://vercel.com/docs/cli)

