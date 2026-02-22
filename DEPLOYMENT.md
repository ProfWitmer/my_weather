# Deployment Guide - My Weather App

This guide explains how to deploy the My Weather app to **PythonAnywhere** (truly free tier, no expiration).

## Why PythonAnywhere?

✅ **Actually Free Forever** - No expiration, no credit card required
✅ **Persistent SQLite** - Your database won't disappear
✅ **Simple Setup** - Designed specifically for Python web apps
✅ **No Complicated Configuration** - Works great with Flask

## Prerequisites

- GitHub account with the repository pushed
- PythonAnywhere account (free at https://www.pythonanywhere.com)

## Deployment Steps (FREE Forever)

### Step 1: Create PythonAnywhere Account

1. Go to https://www.pythonanywhere.com
2. Click **"Pricing & signup"** → **"Create a Beginner account"**
3. Choose a username (this becomes part of your URL: `username.pythonanywhere.com`)
4. Fill in email and password
5. Click "Register"
6. Verify your email

### Step 2: Clone Your Repository

1. **Open Bash Console**
   - From PythonAnywhere dashboard, click "Consoles" tab
   - Click "Bash" to open a new console

2. **Clone your repository**:
   ```bash
   git clone https://github.com/ProfWitmer/my_weather.git
   cd my_weather
   ```

3. **Create virtual environment**:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 myweather
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize database**:
   ```bash
   python database.py
   ```

### Step 3: Create Web App

1. **Go to Web tab**
   - Click "Web" in the top menu
   - Click "Add a new web app"

2. **Configure Web App**
   - Click "Next" (for free domain)
   - Select "Manual configuration" (NOT Flask)
   - Choose **Python 3.10**
   - Click "Next"

### Step 4: Configure WSGI File

1. **Edit WSGI configuration**
   - On the Web tab, find "Code" section
   - Click on the WSGI configuration file link (e.g., `/var/www/username_pythonanywhere_com_wsgi.py`)

2. **Replace entire file contents** with:
   ```python
   import sys
   import os

   # Add your project directory to the sys.path
   project_home = '/home/username/my_weather'  # REPLACE 'username' with your PythonAnywhere username
   if project_home not in sys.path:
       sys.path.insert(0, project_home)

   # Set environment variables
   os.environ['DATABASE_URL'] = ''  # Empty = use SQLite

   # Import Flask app
   from app import app as application
   ```

3. **Important**: Replace `username` with your actual PythonAnywhere username
4. Click "Save"

### Step 5: Configure Virtualenv

1. **Still on Web tab**, find "Virtualenv" section
2. **Enter virtualenv path**:
   ```
   /home/username/.virtualenvs/myweather
   ```
   (Replace `username` with your PythonAnywhere username)
3. The path should turn blue/green when correct

### Step 6: Set Working Directory

1. **On Web tab**, find "Code" section
2. **Working directory**: `/home/username/my_weather`
   (Replace `username` with your actual username)

### Step 7: Reload and Test

1. **Scroll to top of Web tab**
2. Click the big green **"Reload"** button
3. Click your app URL: `https://username.pythonanywhere.com`
4. Your weather app should load! 🎉

## Testing Your Deployment

1. Search for a location: "New York" or "90210"
2. Save some locations
3. Check weather displays correctly
4. Close browser and come back - saved locations should persist!

## Free Tier Features

✅ **What you get FREE forever:**
- One web app at `username.pythonanywhere.com`
- HTTPS included
- Persistent file storage (SQLite database stays)
- 512 MB disk space
- No expiration date
- No credit card required

⚠️ **Free tier limitations:**
- One web app only
- Can't use custom domain with HTTPS (paid feature)
- Limited CPU seconds per day
- Must access your app at least once every 3 months or it gets disabled (but not deleted)
- Some Python packages may not be available (all of ours work fine)

## Updating Your App

When you make changes:

1. **SSH into PythonAnywhere console** (or use web console)
2. **Navigate to project**:
   ```bash
   cd ~/my_weather
   workon myweather  # Activate virtualenv
   ```

3. **Pull latest changes**:
   ```bash
   git pull origin main
   ```

4. **Install any new dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Reload web app**:
   - Go to Web tab
   - Click "Reload" button
   - Or use command line:
     ```bash
     touch /var/www/username_pythonanywhere_com_wsgi.py
     ```

## Viewing Logs

1. **Go to Web tab**
2. **Scroll to "Log files" section**
3. **View logs**:
   - **Error log**: Shows Python errors and exceptions
   - **Server log**: Shows HTTP requests
   - **Access log**: Shows all requests to your app

Click any log file to view it in browser.

## Troubleshooting

### App Shows "Something went wrong"

**Check error log**:
1. Web tab → Log files → Error log
2. Look for Python exceptions
3. Common issues:
   - Wrong virtualenv path
   - Wrong project path in WSGI file
   - Missing dependencies

**Solution**:
- Verify paths in WSGI file match your username
- Check virtualenv path is correct
- Run `pip install -r requirements.txt` again

### "Could not find platform independent libraries"

**Solution**: Recreate virtualenv with correct Python version:
```bash
mkvirtualenv --python=/usr/bin/python3.10 myweather
pip install -r requirements.txt
```

### Database Not Persisting

**Check**: Make sure `DATABASE_URL` is empty or not set in WSGI file
- Empty `DATABASE_URL` = uses SQLite
- SQLite file location: `/home/username/my_weather/weather.db`

**Solution**:
```bash
cd ~/my_weather
python database.py  # Reinitialize if needed
```

### Geocoding/Weather API Errors

**Problem**: External API calls may fail due to network restrictions

**Solution**:
- Free tier can access most APIs
- If blocked, upgrade to paid tier
- Check error logs for specific API errors

### Module Not Found Errors

**Solution**:
1. Make sure virtualenv is activated: `workon myweather`
2. Install missing package: `pip install package-name`
3. Reload web app

### Static Files Not Loading

**Solution**:
1. Go to Web tab → Static files section
2. Add static file mapping:
   - URL: `/static/`
   - Directory: `/home/username/my_weather/static/`

## Managing Your Database

### View Database Contents

```bash
cd ~/my_weather
sqlite3 weather.db

# Inside sqlite3:
.tables                    # List tables
SELECT * FROM locations;   # View locations
.quit                      # Exit
```

### Backup Database

```bash
cd ~/my_weather
cp weather.db weather.db.backup
```

### Reset Database

```bash
cd ~/my_weather
rm weather.db
python database.py
```

## Performance Tips

1. **Keep app active**: Visit your app regularly (at least every 3 months)
2. **Optimize queries**: Database queries should be fast with SQLite
3. **Monitor CPU usage**: Free tier has daily CPU limits - check dashboard
4. **Use caching**: App already caches weather data for 10 minutes

## Upgrade Options (Optional)

If you need more features:

- **Hacker Plan ($5/month)**:
  - More CPU seconds
  - More disk space (1 GB)
  - Custom domain support
  - No "must visit every 3 months" requirement

## Comparison: PythonAnywhere vs Render

| Feature | PythonAnywhere Free | Render Free |
|---------|-------------------|-------------|
| **Cost** | Free forever | Free for 1 month |
| **Database** | SQLite (persistent) | PostgreSQL (expires) |
| **Expiration** | Never (just visit every 3 months) | 30 days |
| **Setup** | Easy | Complex |
| **Custom Domain** | No (paid) | Yes |
| **Cold Start** | No | Yes (15min timeout) |

## Additional Resources

- **PythonAnywhere Help**: https://help.pythonanywhere.com/
- **Flask Tutorial**: https://help.pythonanywhere.com/pages/Flask/
- **Forums**: https://www.pythonanywhere.com/forums/
- **Your Dashboard**: https://www.pythonanywhere.com/user/username/

## Quick Reference

### Important Paths (replace 'username' with yours)
- **Project**: `/home/username/my_weather`
- **Virtualenv**: `/home/username/.virtualenvs/myweather`
- **WSGI file**: `/var/www/username_pythonanywhere_com_wsgi.py`
- **Database**: `/home/username/my_weather/weather.db`

### Common Commands
```bash
# Activate virtualenv
workon myweather

# Update code
cd ~/my_weather
git pull origin main

# Install dependencies
pip install -r requirements.txt

# Reload app
touch /var/www/username_pythonanywhere_com_wsgi.py
```

### Your App URL
`https://username.pythonanywhere.com` (replace with your username)

---

**Ready to deploy?** Follow Steps 1-7 above. Total time: ~15-20 minutes for first deployment.

**Best part**: It's FREE FOREVER with persistent storage! 🎉
