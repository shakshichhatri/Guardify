# OAuth2 Dashboard Setup Guide

## Getting Your Discord Client Secret

To enable Discord login for your web dashboard, you need to get your Client Secret from the Discord Developer Portal:

### Step 1: Access Developer Portal
1. Go to https://discord.com/developers/applications
2. Select your **Guardify** application (ID: 1458798335178707036)

### Step 2: Get Client Secret
1. Click on **OAuth2** in the left sidebar
2. Click on **General** under OAuth2
3. You'll see your **Client ID** (already in config.json)
4. Click **Reset Secret** to generate a new Client Secret (or copy the existing one if visible)
5. **IMPORTANT**: Copy this secret immediately - you won't be able to see it again!

### Step 3: Add Redirect URI
1. Still in the OAuth2 section, scroll down to **Redirects**
2. Click **Add Redirect**
3. Enter: `http://localhost:5000/callback`
4. Click **Save Changes**

**For Production**: Add your production URL too, e.g., `https://yourdomain.com/callback`

### Step 4: Update Configuration
1. Open `config.json` in your project
2. Replace `YOUR_CLIENT_SECRET_HERE` with the actual secret you copied
3. Save the file

Your config.json should look like:
```json
{
  "bot_token": "MTQ1ODc5ODMzNTE3ODcwNzAzNg...",
  "command_prefix": "!",
  "log_directory": "forensics_logs",
  "discord_client_id": "1458798335178707036",
  "discord_client_secret": "your_actual_secret_here",
  "dashboard_url": "http://localhost:5000"
}
```

### Step 5: Restart Web Dashboard
1. Stop the current web dashboard (Ctrl+C in terminal)
2. Run: `python web_dashboard.py`
3. Navigate to http://localhost:5000

## How It Works

### User Flow:
1. **Landing Page** (`/`) - User clicks "Login with Discord"
2. **Discord Authorization** - User authorizes your app to access their Discord info
3. **Callback** (`/callback`) - Discord redirects back with authorization code
4. **Token Exchange** - Your app exchanges code for access token
5. **Server Selection** (`/guilds`) - User sees list of their Discord servers
6. **Dashboard** (`/dashboard/<guild_id>`) - User views stats for specific server

### Features:
- ✅ **Discord OAuth2 Authentication** - Secure login via Discord
- ✅ **Per-Server Dashboards** - Each server has its own stats
- ✅ **Access Control** - Users can only view servers they're members of
- ✅ **Session Management** - Persistent login sessions
- ✅ **User Info Display** - Shows username and avatar
- ✅ **Guild Icons** - Displays server icons and names

### API Endpoints:
- `GET /` - Landing page (public)
- `GET /login` - Redirect to Discord OAuth2
- `GET /callback` - Handle OAuth2 callback
- `GET /logout` - Clear session
- `GET /guilds` - List user's servers (requires login)
- `GET /dashboard` - Global dashboard (requires login)
- `GET /dashboard/<guild_id>` - Server-specific dashboard (requires login + membership)
- `GET /api/stats` - Global stats API
- `GET /api/stats/<guild_id>` - Server-specific stats API

### Security Notes:
- Client Secret is server-side only (never exposed to browser)
- Access tokens stored in secure Flask sessions
- Guild access verified before showing data
- Sessions use cryptographically secure random keys

## Production Deployment

For production use:

1. **Update config.json**:
   ```json
   {
     "dashboard_url": "https://yourdomain.com"
   }
   ```

2. **Add Production Redirect URI** in Discord Developer Portal:
   - `https://yourdomain.com/callback`

3. **Use HTTPS**: Discord OAuth2 requires HTTPS in production

4. **Environment Variables** (recommended for secrets):
   ```bash
   export DISCORD_CLIENT_SECRET="your_secret"
   export FLASK_SECRET_KEY="your_random_key"
   ```

5. **Production Server**: Use Gunicorn or Waitress instead of Flask dev server

## Troubleshooting

### "Invalid OAuth2 Redirect URI"
- Make sure you added the exact redirect URI in Developer Portal
- Check that `dashboard_url` in config.json matches your actual URL

### "Access Denied" when viewing dashboard
- User must be a member of the server
- Bot must be in the server to have data

### "Invalid Client Secret"
- Verify the secret is correct in config.json
- Try resetting the secret in Developer Portal

### Session Expires Quickly
- Flask sessions last until browser closes by default
- Add `PERMANENT_SESSION_LIFETIME` to configure duration
