# Guardify Deployment Guide - Render.com (FREE 24/7 Hosting)

## Why Render.com?
- ✅ **100% Free** - No credit card required
- ✅ **Always Online** - 24/7 uptime
- ✅ **Auto-Restart** - Automatically restarts if bot crashes
- ✅ **Easy Setup** - Deploy in 5 minutes
- ✅ **GitHub Integration** - Auto-deploy on push

## Step-by-Step Deployment

### 1. Prepare Your Repository

First, push your Guardify code to GitHub if you haven't already:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit for Guardify bot"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/Guardify.git
git branch -M main
git push -u origin main
```

### 2. Sign Up for Render.com

1. Go to [Render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with your GitHub account (recommended)
4. Authorize Render to access your repositories

### 3. Deploy Your Bot

1. **Click "New +" button** in the Render dashboard
2. **Select "Web Service"**
3. **Connect your Guardify repository**
   - If you don't see it, click "Configure account" and grant access
4. **Configure the service:**
   - **Name**: `guardify-bot` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Branch**: `main` (or your default branch)
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python -m textblob.download_corpora
     ```
   - **Start Command**: 
     ```bash
     python bot.py
     ```
   - **Plan**: Select **"Free"** (most important!)

5. **Add Environment Variables:**
   - Click "Advanced" or scroll down to "Environment Variables"
   - Add new variable:
     - **Key**: `DISCORD_BOT_TOKEN`
     - **Value**: `your_actual_bot_token_here` (paste your Discord bot token)

6. **Click "Create Web Service"**

### 4. Wait for Deployment

- Render will build and deploy your bot (takes 2-5 minutes)
- Watch the logs to see progress
- When you see "Logged in as [YourBotName]" - it's online! 🎉

### 5. Verify Your Bot is Online

1. Go to your Discord server
2. Check if your bot shows as "Online"
3. Try a command like `/help` to test

## Important Notes

### Free Tier Limitations
- Render's free tier may "spin down" after 15 minutes of inactivity
- To keep it active 24/7, you can:
  1. Use Render's paid plan ($7/month for always-on)
  2. Use the keep-alive solution below (free)

### Keep-Alive Solution (Optional)

If the bot spins down, add this to your `bot.py`:

```python
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Guardify Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
```

Then add to your `main()` function:
```python
keep_alive()  # Add this before bot.run(token)
```

And use a service like [UptimeRobot](https://uptimerobot.com) (free) to ping your Render URL every 5 minutes.

## Troubleshooting

### Bot Won't Start
- **Check logs** in Render dashboard
- Verify `DISCORD_BOT_TOKEN` is set correctly
- Ensure "Message Content Intent" is enabled in Discord Developer Portal

### Bot Goes Offline
- Check Render dashboard for errors
- Verify you're on the free plan (not a trial that expired)
- Check Discord bot token hasn't been regenerated

### Build Fails
- Ensure `requirements.txt` is in root directory
- Check Python version compatibility
- Review build logs for specific errors

## Alternative Free Options

If Render doesn't work for you:

1. **Railway.app** - $5 free credit monthly
2. **Fly.io** - Free tier with 3 shared VMs
3. **Oracle Cloud** - Always free tier (more complex setup)

## Monitoring Your Bot

- **Render Dashboard**: Shows logs, CPU, memory usage
- **Discord**: Bot status (online/offline)
- **Logs**: Check `forensics_logs/` directory is being created

## Updating Your Bot

When you push changes to GitHub:
1. Render automatically detects the push
2. Rebuilds and redeploys your bot
3. Bot restarts with new code (downtime: ~2 minutes)

Or manually redeploy:
1. Go to Render dashboard
2. Click your service
3. Click "Manual Deploy" → "Deploy latest commit"

## Support

- **Render Docs**: https://render.com/docs
- **Discord.py Docs**: https://discordpy.readthedocs.io/
- **Guardify Issues**: Create an issue on GitHub

---

**Your bot will now be online 24/7 for FREE! 🎉**
