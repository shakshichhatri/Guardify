# Guardify Bot Setup & Run Guide 🛡️

## ✅ Features Implemented

### 🤖 Auto-Moderation (Always Active)
- **Abusive Language Detection** - AI-powered sentiment analysis with keyword matching
- **Spam Detection** - Automatic timeout for 2 minutes
- **Excessive Caps Detection** - Auto-delete messages with >70% caps
- **Progressive Punishment** - 5 warnings = 10-minute timeout
- **Auto-Delete** - Removes rule-breaking messages instantly

### 📊 Comprehensive Activity Logging
All activities are automatically logged to `forensics_logs/`:
- **abuse_evidence.jsonl** - Abusive message detections
- **activity_logs.jsonl** - All bot activities (joins, leaves, edits, deletes, channel changes)
- **mod_actions.jsonl** - All moderator actions (kicks, bans, timeouts, warns)
- **warnings.json** - User warning tracking

### 🔧 Moderation Commands
- `!kick @user [reason]` - Kick member
- `!ban @user [reason]` - Ban member
- `!unban <user_id> [reason]` - Unban user
- `!timeout @user <minutes> [reason]` - Timeout member
- `!untimeout @user` - Remove timeout
- `!warn @user [reason]` - Warn member
- `!warnings @user` - Check warnings
- `!clearwarnings @user` - Clear warnings (Admin)
- `!clear [amount]` - Bulk delete messages
- `!slowmode <seconds>` - Set slowmode
- `!lock` / `!unlock` - Lock/unlock channels

### 📈 Analytics Commands
- `!scan <message>` - Manually scan text for abuse
- `!history @user` - View abuse history
- `!stats` - Detection statistics
- `!automod` - View/configure auto-mod settings
- `!serverinfo` - Server details
- `!userinfo [@user]` - User details

---

## 🚀 Quick Start Guide

### Step 1: Get Your Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name (e.g., "Guardify")
3. Go to the "Bot" tab on the left
4. Click "Reset Token" and copy your new bot token **immediately**
5. Enable these **Privileged Gateway Intents**:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent

### Step 2: Invite Bot to Your Server

1. In Developer Portal, go to "OAuth2" > "URL Generator"
2. Select these **Scopes**:
   - ✅ bot
   - ✅ applications.commands
3. Select these **Bot Permissions**:
   - ✅ Manage Roles
   - ✅ Kick Members
   - ✅ Ban Members
   - ✅ Manage Channels
   - ✅ Manage Messages
   - ✅ Read Messages/View Channels
   - ✅ Send Messages
   - ✅ Manage Webhooks
   - ✅ Read Message History
   - ✅ Moderate Members (for timeouts)
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

### Step 3: Configure the Bot

Update `config.json` with your bot token:

```json
{
  "bot_token": "YOUR_BOT_TOKEN_HERE",
  "command_prefix": "!",
  "log_directory": "forensics_logs",
  "discord_client_id": "YOUR_CLIENT_ID",
  "discord_client_secret": "YOUR_CLIENT_SECRET",
  "dashboard_url": "http://localhost:5000"
}
```

**OR** set environment variable (more secure):
```bash
set DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
```

### Step 4: Run the Bot

**Option A: Using the batch file (Windows)**
```bash
start_bot.bat
```

**Option B: Direct Python command**
```bash
D:/project/Guardify/.venv/Scripts/python.exe bot.py
```

**Option C: Using PowerShell**
```powershell
cd D:\project\Guardify
.\.venv\Scripts\python.exe bot.py
```

### Step 5: Verify Bot is Online

You should see:
```
Starting Discord bot...
Web server started for health checks
Guardify#1234 has connected to Discord!
Bot is active in 1 guilds
Auto-moderation enabled: Abuse detection, spam filter, caps filter
```

Test in your Discord server:
```
!help_guardify
```

---

## 🌐 Making Bot 24/7 Online

### Method 1: Render.com (FREE - Recommended)

1. **Create a Render account**: [https://render.com](https://render.com)

2. **Create a new Web Service**:
   - Click "New +" > "Web Service"
   - Connect your GitHub repository (or upload code)
   - Configure:
     - **Name**: guardify-bot
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python bot.py`
     - **Instance Type**: Free

3. **Set Environment Variables** in Render dashboard:
   - `DISCORD_BOT_TOKEN` = your bot token

4. **Deploy**: Click "Create Web Service"

The bot will stay online 24/7! The built-in Flask server keeps the service alive.

---

### Method 2: Railway.app (FREE)

1. **Create account**: [https://railway.app](https://railway.app)
2. **Create new project** > Deploy from GitHub
3. **Add environment variables**:
   - `DISCORD_BOT_TOKEN` = your token
4. Railway auto-detects the setup and deploys

---

### Method 3: Heroku (Paid)

1. Create Heroku account
2. Install Heroku CLI
3. Run:
```bash
heroku create guardify-bot
heroku config:set DISCORD_BOT_TOKEN=your_token
git push heroku main
```

The `Procfile` is already configured:
```
worker: python bot.py
```

---

### Method 4: VPS (DigitalOcean, AWS, etc.)

1. **Get a VPS** (Ubuntu recommended)
2. **Install Python 3.9+**:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

3. **Upload bot files** and install dependencies:
```bash
cd /home/guardify
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Run with systemd** (keeps bot running forever):

Create `/etc/systemd/system/guardify.service`:
```ini
[Unit]
Description=Guardify Discord Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/guardify
Environment="DISCORD_BOT_TOKEN=your_token"
ExecStart=/home/guardify/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable guardify
sudo systemctl start guardify
sudo systemctl status guardify
```

---

### Method 5: Keep Alive on Your PC (Windows)

Use **Task Scheduler** to restart bot if it crashes:

1. Open Task Scheduler
2. Create Basic Task
3. **Trigger**: At startup
4. **Action**: Start a program
   - Program: `D:\project\Guardify\.venv\Scripts\python.exe`
   - Arguments: `bot.py`
   - Start in: `D:\project\Guardify`
5. Enable "Run whether user is logged on or not"

**Note**: Your PC must stay on for 24/7 operation.

---

## 📊 Monitoring Logs

All activities are logged in real-time to:

### Activity Logs (`forensics_logs/activity_logs.jsonl`)
```json
{"activity_type": "member_join", "details": {...}, "timestamp": "2026-02-06T..."}
{"activity_type": "message_delete", "details": {...}, "timestamp": "2026-02-06T..."}
{"activity_type": "channel_create", "details": {...}, "timestamp": "2026-02-06T..."}
```

### Moderator Actions (`forensics_logs/mod_actions.jsonl`)
```json
{"action": "ban", "moderator_id": "...", "target_id": "...", "reason": "...", "timestamp": "..."}
{"action": "timeout", "moderator_id": "...", "target_id": "...", "reason": "...", "timestamp": "..."}
```

### Abuse Evidence (`forensics_logs/abuse_evidence.jsonl`)
```json
{"message_id": "...", "author_id": "...", "content": "...", "analysis": {...}, "timestamp": "..."}
```

### View Logs in Discord
Use these commands to monitor:
- `!stats` - Overall statistics
- `!history @user` - User's abuse history
- `!warnings @user` - User's warnings

---

## 🛠️ Troubleshooting

### Bot doesn't respond
1. ✅ Check bot token is correct
2. ✅ Verify bot has proper permissions in Discord
3. ✅ Ensure "Message Content Intent" is enabled in Developer Portal
4. ✅ Check bot role is above members' roles in server settings

### Auto-mod not working
1. ✅ Bot needs these permissions:
   - Manage Messages (to delete)
   - Moderate Members (to timeout)
2. ✅ Bot's role must be higher than target users
3. ✅ Admins/Moderators are exempt from auto-mod

### Logs not being created
- The bot automatically creates `forensics_logs/` directory
- Check file permissions on the directory
- Logs are created on first event

### Bot crashes
- Check the terminal output for error messages
- Most common issue: Invalid or expired bot token
- Verify all dependencies are installed: `pip install -r requirements.txt`

---

## 🔒 Security Best Practices

1. **Never share your bot token** - It's like a password
2. **Use environment variables** for tokens (not config.json in production)
3. **Regenerate token** if accidentally exposed
4. **Regular backups** of logs directory
5. **Review mod actions** periodically using logs

---

## 📞 Support

Your bot is now configured with:
- ✅ Full auto-moderation system
- ✅ Comprehensive logging of all activities
- ✅ Moderator action tracking
- ✅ Ready for 24/7 deployment

For issues or questions, check the logs in `forensics_logs/` directory.

---

## Quick Command Reference

```
🛡️ Auto-Moderation: Always Active
📊 Analysis: !scan, !history, !stats
🔨 Moderation: !kick, !ban, !timeout, !warn
🧹 Management: !clear, !slowmode, !lock
⚙️ Config: !automod
❓ Help: !help_guardify
```

**Bot is ready to protect your server 24/7!** 🚀
