# Deploy Your Billionaire Tracker in 5 Minutes! 🚀

This guide will help you deploy your application to **Render.com** with a free PostgreSQL database.

## Prerequisites

- A GitHub account
- A Render.com account (free - sign up at https://render.com)

---

## Option 1: One-Click Deploy with Render (EASIEST) ⚡

### Step 1: Push to GitHub

If you haven't already pushed your code to GitHub:

```bash
# If this is already on GitHub, skip to Step 2
git remote add github https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push github claude/download-billionaire-list-011CUV3GJA62hx6X9C6bpu9U
```

### Step 2: Deploy to Render

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com/

2. **Click "New +"** → **"Blueprint"**

3. **Connect Your GitHub Repository**
   - Authorize Render to access your GitHub
   - Select your repository: `anara71/Basics`
   - Select branch: `claude/download-billionaire-list-011CUV3GJA62hx6X9C6bpu9U`

4. **Deploy!**
   - Render will automatically detect the `render.yaml` file
   - It will create:
     - A web service (your Flask app)
     - A PostgreSQL database
   - Click "Apply"

5. **Wait for Deployment** (3-5 minutes)
   - Render will build and deploy your application
   - You'll get a live URL like: `https://billionaire-tracker.onrender.com`

6. **Initialize the Database**
   - Once deployed, open the web service shell
   - Run: `python download_billionaires.py`
   - This populates your database with billionaire data

### Step 3: Access Your App! 🎉

Your app is now live at: `https://your-app-name.onrender.com`

---

## Option 2: Manual Render Deploy (Alternative)

If the blueprint doesn't work, follow these steps:

### A. Create PostgreSQL Database

1. Go to Render Dashboard → **"New +"** → **"PostgreSQL"**
2. Settings:
   - **Name**: `billionaire-tracker-db`
   - **Database**: `billionaire_tracker`
   - **Region**: Oregon (Free)
   - **Plan**: Free
3. Click **"Create Database"**
4. Copy the **Internal Database URL** (starts with `postgres://`)

### B. Create Web Service

1. Go to Render Dashboard → **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Settings:
   - **Name**: `billionaire-tracker`
   - **Region**: Oregon (Free)
   - **Branch**: `claude/download-billionaire-list-011CUV3GJA62hx6X9C6bpu9U`
   - **Root Directory**: (leave empty)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

4. **Add Environment Variables**:
   Click "Advanced" → "Add Environment Variable"

   ```
   SECRET_KEY = (click "Generate" button)
   JWT_SECRET_KEY = (click "Generate" button)
   DATABASE_URL = (paste the Internal Database URL from step A)
   ```

5. Click **"Create Web Service"**

### C. Initialize Database

1. Wait for deployment to complete (3-5 minutes)
2. Go to your web service → **"Shell"** tab
3. Run these commands:
   ```bash
   python download_billionaires.py
   ```

### D. Done! 🎉

Your app is live at the URL shown in the Render dashboard!

---

## Option 3: Deploy to Railway.app (Also Very Easy) 🚂

### Step 1: Go to Railway

1. Visit: https://railway.app
2. Sign in with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**

### Step 2: Select Your Repository

1. Choose: `anara71/Basics`
2. Select branch: `claude/download-billionaire-list-011CUV3GJA62hx6X9C6bpu9U`

### Step 3: Add PostgreSQL

1. Click **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway automatically sets the `DATABASE_URL` environment variable

### Step 4: Configure Environment Variables

1. Click on your web service
2. Go to **"Variables"** tab
3. Add:
   ```
   SECRET_KEY = (generate a random string)
   JWT_SECRET_KEY = (generate a random string)
   ```

   Generate random keys:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

### Step 5: Deploy

1. Railway auto-detects Python and starts building
2. Go to **"Settings"** → Set **Start Command**: `gunicorn app:app`
3. Wait for deployment (2-3 minutes)

### Step 6: Initialize Database

1. Open the web service terminal
2. Run: `python download_billionaires.py`

### Done! 🎉

Your app is live! Railway provides you with a URL.

---

## Option 4: Deploy to Heroku (Classic) 📦

### Step 1: Install Heroku CLI

```bash
# Install from: https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login and Create App

```bash
heroku login
heroku create billionaire-tracker-yourname
```

### Step 3: Add PostgreSQL

```bash
heroku addons:create heroku-postgresql:mini
```

### Step 4: Deploy

```bash
git push heroku claude/download-billionaire-list-011CUV3GJA62hx6X9C6bpu9U:main
```

### Step 5: Set Environment Variables

```bash
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
heroku config:set JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
```

### Step 6: Initialize Database

```bash
heroku run python download_billionaires.py
```

### Step 7: Open App

```bash
heroku open
```

---

## Troubleshooting

### Build Fails

- Check that `requirements.txt` is in the root directory
- Verify Python version in `runtime.txt`

### Database Connection Issues

- Make sure `DATABASE_URL` environment variable is set
- Check that the database URL starts with `postgresql://` (not `postgres://`)

### App Crashes on Startup

- Check logs in Render/Railway/Heroku dashboard
- Verify all environment variables are set
- Make sure gunicorn is in `requirements.txt`

### No Billionaires Showing

- Run the initialization script: `python download_billionaires.py`

---

## After Deployment

### Access Your App

Visit your app URL and:
1. **Register** a new account
2. **Browse** billionaires
3. **Track** relationships
4. **Manage** your network

### Update Billionaire Data

To refresh the billionaire data periodically:

1. Go to your platform's shell/terminal
2. Run: `python download_billionaires.py`

Or set up a scheduled job:
- **Render**: Use Cron Jobs
- **Railway**: Use Scheduled Jobs
- **Heroku**: Use Heroku Scheduler

---

## Security Checklist ✅

Before going live, ensure:

- ✅ `SECRET_KEY` is set to a random value
- ✅ `JWT_SECRET_KEY` is set to a random value
- ✅ Using PostgreSQL (not SQLite)
- ✅ HTTPS is enabled (automatic on Render/Railway/Heroku)
- ✅ Environment variables are not committed to git

---

## Cost

All platforms mentioned have **FREE TIERS**:

- **Render**: Free tier includes 750 hours/month
- **Railway**: $5 free credit monthly
- **Heroku**: Free tier (with some limitations)

Your billionaire tracker app will run **completely free** on any of these platforms!

---

## Support

If you encounter issues:

1. Check the deployment logs in your platform's dashboard
2. Verify environment variables are set correctly
3. Check database connectivity
4. Review DEPLOYMENT.md for detailed troubleshooting

---

**Ready to deploy? Choose a platform above and follow the steps!** 🚀

**Recommended: Start with Render.com (Option 1) - it's the easiest!**
