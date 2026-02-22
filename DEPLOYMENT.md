# Deployment Guide - My Weather App

This guide explains how to deploy the My Weather app to Render with PostgreSQL.

## Prerequisites

- GitHub account with the repository pushed
- Render account (free tier available at https://render.com)

## Option 1: Deploy Using render.yaml (Recommended)

This is the easiest method - Render will automatically configure everything.

### Steps:

1. **Sign up/Login to Render**
   - Go to https://render.com
   - Sign up or login with your GitHub account

2. **Create New Blueprint**
   - Click "New +" button
   - Select "Blueprint"
   - Connect your GitHub account if not already connected
   - Select the `my_weather` repository

3. **Deploy**
   - Render will detect the `render.yaml` file
   - It will automatically create:
     - A web service running your Flask app
     - A PostgreSQL database
     - Environment variables linking them together
   - Click "Apply" to start deployment
   - Wait 5-10 minutes for deployment to complete

4. **Access Your App**
   - Once deployed, Render provides a URL like: `https://my-weather-app.onrender.com`
   - Click the URL to view your live app!

## Option 2: Manual Deployment

If you prefer manual setup:

### Step 1: Create PostgreSQL Database

1. In Render dashboard, click "New +" → "PostgreSQL"
2. Name: `my-weather-db`
3. Database: `weather`
4. User: `weather_user`
5. Region: Choose closest to you
6. Plan: Free
7. Click "Create Database"
8. Copy the "Internal Database URL" (you'll need this)

### Step 2: Create Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `my-weather-app`
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

4. Add Environment Variable:
   - Key: `DATABASE_URL`
   - Value: Paste the Internal Database URL from Step 1

5. Click "Create Web Service"

### Step 3: Wait for Deployment

- Render will build and deploy your app
- First deployment takes 5-10 minutes
- You'll get a URL like `https://my-weather-app.onrender.com`

## Database Behavior

### Local Development (SQLite)
- Database file: `weather.db`
- Fast and simple
- Data persists between restarts

### Production (PostgreSQL on Render)
- Uses PostgreSQL database
- Data persists across deployments and restarts
- Shared across all app instances

## Important Notes

### Free Tier Limitations
- App spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds (cold start)
- 750 hours/month of uptime
- PostgreSQL database has 1 GB storage limit

### Upgrade Options
If you need better performance:
- **Starter Plan ($7/month)**: No spin-down, faster builds
- **Standard Plan ($25/month)**: More resources, better performance

## Monitoring

### View Logs
1. Go to Render dashboard
2. Click your web service
3. Click "Logs" tab
4. See real-time application logs

### Check Database
1. Click your PostgreSQL database
2. Click "Connect" → "External Connection"
3. Use provided credentials with psql or database client

## Updating Your App

1. **Make changes locally**
2. **Commit and push to GitHub**:
   ```bash
   git add .
   git commit -m "Update feature"
   git push
   ```
3. **Render auto-deploys** when you push to main branch
4. **Monitor deployment** in Render dashboard

## Troubleshooting

### Build Fails
- Check Render build logs for errors
- Verify `requirements.txt` is up to date
- Ensure `build.sh` is executable

### Database Connection Errors
- Verify DATABASE_URL environment variable is set
- Check PostgreSQL database is running
- Review connection string format

### App Not Loading
- Check Render logs for Python errors
- Verify gunicorn is installed in requirements.txt
- Ensure port binding is correct (Render provides PORT env var)

## Local Testing with PostgreSQL

To test PostgreSQL locally before deploying:

1. Install PostgreSQL locally
2. Create database:
   ```bash
   createdb weather
   ```
3. Set environment variable:
   ```bash
   export DATABASE_URL="postgresql://localhost/weather"
   ```
4. Run app:
   ```bash
   python app.py
   ```

## Support

- Render Documentation: https://render.com/docs
- Flask Documentation: https://flask.palletsprojects.com/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
