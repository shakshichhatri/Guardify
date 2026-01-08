# Dashboard Authentication Setup - Quick Start

## ⚡ Quick Setup (3 Steps)

### 1️⃣ Get Your Client Secret
1. Go to https://discord.com/developers/applications
2. Select your **Guardify** app
3. Click **OAuth2** → **General**
4. Copy the **Client Secret** (click Reset Secret if needed)

### 2️⃣ Add Redirect URI
Still in OAuth2 section:
1. Scroll to **Redirects**
2. Click **Add Redirect**
3. Enter: `http://localhost:5000/callback`
4. Click **Save Changes**

### 3️⃣ Update Config
Edit `config.json` and replace `YOUR_CLIENT_SECRET_HERE`:
```json
{
  "discord_client_secret": "paste_your_actual_secret_here"
}
```

## ✅ That's It!

Restart the web dashboard:
```bash
python web_dashboard.py
```

Visit: http://localhost:5000

## 🎯 How to Use

1. **Visit Homepage** - Click "Login with Discord"
2. **Authorize** - Allow Guardify to see your servers
3. **Select Server** - Choose which server's dashboard to view
4. **View Stats** - See moderation data for that specific server

## 🔒 What Users See

- **Own Servers Only** - Users only see servers they're members of
- **Per-Server Stats** - Each server has separate statistics
- **Secure Sessions** - Login persists until logout/browser close

## 📝 Important Notes

- ⚠️ You MUST add the redirect URI in Discord Developer Portal
- ⚠️ Client Secret must be kept private (don't commit to GitHub)
- ✅ Each server gets its own isolated dashboard
- ✅ Users can only access servers they belong to
- ✅ No authentication needed to view bot info on homepage

## 🚀 Production Notes

When deploying publicly:
1. Change `dashboard_url` in config.json to your domain
2. Add production redirect URI: `https://yourdomain.com/callback`
3. Use HTTPS (required by Discord)
4. Use environment variables for secrets
