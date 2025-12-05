# How to Redeploy on Vercel

## Option 1: Automatic Redeployment (Already Happening)

When you push to GitHub, Vercel automatically redeploys. Since we just pushed, check your Vercel dashboard - a new deployment should be in progress or already completed.

## Option 2: Manual Redeploy via Vercel Dashboard

1. Go to your Vercel dashboard: https://vercel.com/dashboard
2. Click on your project: `backend-real-estate-api`
3. Go to the "Deployments" tab
4. Find the latest deployment (should show your latest commit)
5. Click the "..." menu (three dots) on the deployment
6. Select "Redeploy"

## Option 3: Manual Redeploy via Vercel CLI

If you have Vercel CLI installed:

```bash
# Make sure you're logged in
vercel login

# Link to your project (if not already linked)
vercel link

# Redeploy to production
vercel --prod
```

## Option 4: Trigger via New Commit

If you want to force a redeploy, you can make a small change and push:

```bash
# Make a small change (like updating README or adding a comment)
echo "# Latest deployment" >> DEPLOYMENT.md

# Commit and push
git add .
git commit -m "Trigger redeploy"
git push
```

## Check Deployment Status

After any of the above, you can:
1. Check the Vercel dashboard for deployment status
2. Wait 1-2 minutes for the deployment to complete
3. Test your API endpoints again

## Verify Latest Commit is Deployed

Check that the deployment shows commit: `660f055 Fix vercel.json: remove rewrites, let Vercel auto-detect FastAPI`

