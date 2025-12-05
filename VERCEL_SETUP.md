# Vercel CLI Setup Guide

## Step 1: Login to Vercel

Run this command in your terminal:

```bash
vercel login
```

This will open a browser window for you to authenticate with your Vercel account.

## Step 2: Link to Existing Project

After logging in, link your local project to the existing Vercel project:

```bash
vercel link
```

You'll be prompted to:
1. Select your Vercel account/team: **Gerard's projects**
2. Select the project: **backend-real-estate-api**
3. Select the directory: **./** (current directory)
4. Override settings: **No** (keep existing settings)

## Step 3: Deploy Commands

Once linked, you can use:

```bash
# Deploy to preview (creates a preview URL)
vercel

# Deploy to production
vercel --prod

# View deployment logs
vercel logs

# View project info
vercel inspect

# List all deployments
vercel list
```

## Step 4: Environment Variables

You can also manage environment variables via CLI:

```bash
# List environment variables
vercel env ls

# Add environment variable
vercel env add GEMINI_API_KEY

# Pull environment variables locally (creates .env.local)
vercel env pull .env.local
```

## Quick Commands

```bash
# Login
vercel login

# Link project
vercel link

# Deploy to production
vercel --prod

# Check status
vercel inspect
```

