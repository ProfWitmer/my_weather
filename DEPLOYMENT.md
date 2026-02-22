# Deployment Guide - My Weather App

This guide explains how to deploy the My Weather app to Render with PostgreSQL using the **FREE tier**.

## Prerequisites

- GitHub account with the repository pushed
- Render account (free tier available at https://render.com)

## Deployment Steps (FREE Tier)

### Step 1: Create PostgreSQL Database (FREE)

1. **Sign up/Login to Render**
   - Go to https://render.com
   - Sign up or login with your GitHub account

2. **Create Database**
   - Click "New +" button → Select "PostgreSQL"
   - Configure:
     - **Name**: `my-weather-db`
     - **Database**: `weather`
     - **User**: `weather_user` (or leave default)
     - **Region**: Choose closest to you
     - **PostgreSQL Version**: 16 (or latest)
     - **Plan**: **Free**
   - Click "Create Database"
   - Wait ~2 minutes for database to provision

3. **Copy Database URL**
   - Once created, find "Internal Database URL" on the database page
   - Click the copy icon
   - **Save this URL** - you'll need it in Step 2

### Step 2: Create Web Service (FREE)

1. **Create Web Service**
   - Click "New +" → Select "Web Service"
   - Choose "Build and deploy from a Git repository"
   - Click "Next"

2. **Connect Repository**
   - Click "Connect account" if needed
   - Find and select your `my_weather` repository
   - Click "Connect"

3. **Configure Service**
   Fill in these settings:

   - **Name**: `my-weather-app` (or choose your own)
   - **Region**: Same as your database
   - **Branch**: `main`
   - **Runtime**: **Python 3**
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: **Free**

4. **Add Environment Variable**
   - Scroll to "Environment Variables" section
   - Click "Add Environment Variable"
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the Internal Database URL from Step 1
   - Click "Add"

5. **Deploy**
   - Click "Create Web Service"
   - Render will start building your app
   - First deployment takes ~5-10 minutes
   - Watch the logs to see progress

### Step 3: Access Your App

1. Once deployment succeeds (green checkmark), you'll see:
   - Your app URL: `https://my-weather-app-xxxx.onrender.com`
   - Click the URL to view your live app! 🎉

2. **Test the app**:
   - Search for a location (e.g., "New York" or "90210")
   - Save some locations
   - Verify weather displays correctly

## How It Works

### Local Development (SQLite)
- Database file: `weather.db`
- Fast and simple
- Data persists between restarts
- No DATABASE_URL environment variable needed

### Production (PostgreSQL on Render)
- Uses PostgreSQL database (set via DATABASE_URL)
- Data persists across deployments and restarts
- Survives app spin-downs
- Shared across all app instances

The app automatically detects which database to use based on the `DATABASE_URL` environment variable.

## Free Tier Limitations

⚠️ **Important to know:**

- **App spin-down**: Free web services spin down after 15 minutes of inactivity
- **Cold starts**: First request after spin-down takes 30-60 seconds to wake up
- **Monthly limits**: 750 hours/month of uptime (enough for 24/7 if you only have one service)
- **Database storage**: PostgreSQL free tier has 1 GB storage limit
- **Database expires**: Free PostgreSQL databases expire after 90 days (you'll get email warning)

### Upgrade Options (Optional)
If you need better performance:
- **Starter Plan ($7/month)**: No spin-down, always-on
- **Standard Plan ($25/month)**: More resources, better performance

## Automatic Deployments

Once set up, deployments are automatic:

1. **Make changes locally**
2. **Commit and push**:
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```
3. **Render auto-deploys** when you push to the `main` branch
4. **Monitor progress** in Render dashboard logs

## Monitoring Your App

### View Logs
1. Go to Render dashboard
2. Click your web service (`my-weather-app`)
3. Click "Logs" tab
4. See real-time application logs (useful for debugging)

### Check Database
1. Click your PostgreSQL database (`my-weather-db`)
2. View metrics: storage used, connections, etc.
3. Click "Connect" → "External Connection" to access with psql or database client

### Monitor Uptime
- Dashboard shows when app is active/sleeping
- Shows recent deployments and their status

## Troubleshooting

### Build Fails
**Problem**: Build fails with error messages

**Solutions**:
- Check Render build logs for specific errors
- Verify `requirements.txt` has all dependencies
- Ensure `build.sh` is executable (should be by default)
- Try manual build command: `pip install -r requirements.txt && python -c "from database import init_db; init_db()"`

### Database Connection Errors
**Problem**: App can't connect to database

**Solutions**:
- Verify `DATABASE_URL` environment variable is set correctly
- Check PostgreSQL database status (should be "Available")
- Copy the **Internal Database URL** (not External) from database page
- Restart web service after adding DATABASE_URL

### App Shows Error Page
**Problem**: 500 or other errors when accessing app

**Solutions**:
- Check Render logs for Python errors
- Verify database tables were created (check build logs)
- Test locally with PostgreSQL to reproduce
- Check that all required environment variables are set

### Geocoding Not Working
**Problem**: Location searches fail

**Solutions**:
- Check rate limiting - Nominatim allows 1 request/second
- Verify network access isn't blocked
- Check Render logs for specific API errors

### App Takes Long to Load
**Problem**: First request is very slow

**Solutions**:
- This is normal on free tier (cold start after spin-down)
- App wakes up in 30-60 seconds
- Consider upgrading to paid plan for always-on service
- Use a service like UptimeRobot to ping your app and keep it warm

## Local Testing with PostgreSQL (Optional)

To test PostgreSQL locally before deploying:

1. **Install PostgreSQL locally**:
   ```bash
   # macOS with Homebrew
   brew install postgresql@16
   brew services start postgresql@16

   # Ubuntu/Debian
   sudo apt-get install postgresql

   # Windows
   # Download from https://www.postgresql.org/download/windows/
   ```

2. **Create database**:
   ```bash
   createdb weather
   ```

3. **Set environment variable**:
   ```bash
   # macOS/Linux
   export DATABASE_URL="postgresql://localhost/weather"

   # Windows (PowerShell)
   $env:DATABASE_URL="postgresql://localhost/weather"
   ```

4. **Run app**:
   ```bash
   python app.py
   ```

5. **Test**, then unset to go back to SQLite:
   ```bash
   unset DATABASE_URL  # macOS/Linux
   Remove-Item Env:DATABASE_URL  # Windows PowerShell
   ```

## Additional Resources

- **Render Documentation**: https://render.com/docs
- **Render Free Tier Details**: https://render.com/docs/free
- **Flask Documentation**: https://flask.palletsprojects.com/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **Gunicorn Documentation**: https://docs.gunicorn.org/

## Quick Reference

### Key Files for Deployment
- `requirements.txt` - Python dependencies
- `build.sh` - Build script (installs deps, initializes DB)
- `database.py` - Database connection (auto-detects SQLite vs PostgreSQL)
- `config.py` - Configuration (reads DATABASE_URL)

### Environment Variables
- `DATABASE_URL` - PostgreSQL connection string (set in Render)
- `SECRET_KEY` - Flask secret key (optional, auto-generated if not set)

### Important URLs
- **Render Dashboard**: https://dashboard.render.com/
- **Your GitHub Repo**: https://github.com/ProfWitmer/my_weather
- **Live App**: (will be) https://my-weather-app-xxxx.onrender.com

---

**Ready to deploy?** Follow Steps 1-3 above. Total time: ~10-15 minutes for first deployment.
