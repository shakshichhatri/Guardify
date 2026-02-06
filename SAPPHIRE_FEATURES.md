# 🛡️ GUARDIFY - SAPPHIRE-LIKE DISCORD BOT

## ✨ TRANSFORMATION COMPLETE!

Your bot has been transformed into a **Sapphire-like Discord bot** with advanced moderation, welcome systems, verification, anti-raid protection, and comprehensive logging!

---

## 🎯 NEW SAPPHIRE-LIKE FEATURES

### 📢 **Welcome & Goodbye System**
- Customizable welcome messages when members join
- Customizable goodbye messages when members leave
- Supports variables: `{user}`, `{server}`, `{count}`
- Embeds with member avatars
- Member count tracking

**Setup:**
```
!setwelcome #welcome-channel
!welcomemsg Welcome {user} to {server}! You're member #{count}! 🎉
!goodbyemsg Goodbye {user}! We'll miss you! 👋
```

---

### ✅ **Verification System**
- New members receive "Unverified" role
- Can only access verification channel
- Type `!verify` to get verified
- Automatically get "Verified" role with full access
- Prevents raids and ensures real members

**Setup:**
```
!setupverify
```

Then configure channel permissions so Unverified role can only see verification channel.

---

### 🔒 **Anti-Raid Protection**
- Automatically detects mass join events
- Alerts admins when multiple accounts join rapidly
- Configurable sensitivity (default: 5 joins/10 seconds)
- Detects new accounts (< 7 days old)
- Raid mode alerts in log channel

**Setup:**
```
!antiraid on
!raidthreshold 5
!setlog #logs
```

---

### 📋 **Advanced Logging System**
Two separate log channels:

**General Logs:**
- Member joins (with account age alerts)
- Member leaves (with role info)
- Message edits and deletes
- Channel creates/deletes
- Anti-raid alerts
- Bot startup

**Mod Logs:**
- All moderation actions
- Kicks, bans, unbans
- Mutes, timeouts, warnings
- Who did what, when, and why

**Setup:**
```
!setlog #general-logs
!setmodlog #mod-logs
```

---

### 🎭 **Auto-Role System**
- Automatically assign role to new members
- Perfect for giving basic access roles
- Easy enable/disable

**Setup:**
```
!autorole @Member
!autorole none  (to disable)
```

---

### 👤 **Enhanced Moderation**

**New Commands:**
- `!mute @user [minutes] [reason]` - Mute member (default 10min)
- `!unmute @user` - Unmute member
- `!purge 50 @user` - Delete messages from specific user
- `!nick @user NewName` - Change nickname
- `!role @user @role` - Add/remove roles quickly

---

### ⚙️ **Server Configuration**

**Interactive Setup Wizard:**
```
!setup
```
Shows all available configuration options with examples.

**View Current Config:**
```
!config
```
Shows your server's current settings for:
- Welcome/goodbye system
- Log channels
- Verification status
- Anti-raid status
- Auto-role

---

## 🚀 QUICK START GUIDE

### Step 1: Basic Setup
```bash
!setup                    # View setup wizard
!setwelcome #welcome      # Set welcome channel
!setlog #logs             # Set log channel
!setmodlog #mod-logs      # Set mod action logs
```

### Step 2: Welcome Messages
```bash
!welcomemsg Welcome {user} to {server}! We're happy to have you here! 🎉
!goodbyemsg Goodbye {user}! Thanks for being part of our community! 👋
```

### Step 3: Security Features
```bash
!antiraid on              # Enable anti-raid protection
!setupverify              # Enable verification system (optional)
!autorole @Member         # Give new members a role automatically
```

### Step 4: Test Everything
- Join the server with an alt account
- Check welcome message appears
- Check logs are being recorded
- Try verification if enabled

---

## 📝 COMPLETE COMMAND LIST

### 🔧 Server Setup (Admin Only)
| Command | Description |
|---------|-------------|
| `!setup` | Interactive setup wizard |
| `!config` | View current configuration |
| `!setwelcome #channel` | Set welcome/goodbye channel |
| `!welcomemsg <message>` | Set welcome message |
| `!goodbyemsg <message>` | Set goodbye message |
| `!setlog #channel` | Set general log channel |
| `!setmodlog #channel` | Set mod action log channel |

### ✅ Verification System
| Command | Description |
|---------|-------------|
| `!setupverify` | Enable verification system |
| `!verify` | Verify yourself (users command) |

### 🎭 Role Management
| Command | Description |
|---------|-------------|
| `!autorole @role` | Set auto-role for new members |
| `!autorole none` | Disable auto-role |
| `!role @user @role` | Add/remove role from user |
| `!nick @user <name>` | Change user's nickname |

### 🔒 Anti-Raid Protection
| Command | Description |
|---------|-------------|
| `!antiraid on/off` | Toggle anti-raid protection |
| `!raidthreshold <number>` | Set detection sensitivity (joins/10s) |

### 🔨 Moderation Commands
| Command | Description |
|---------|-------------|
| `!kick @user [reason]` | Kick member from server |
| `!ban @user [reason]` | Ban member from server |
| `!unban <user_id> [reason]` | Unban user |
| `!mute @user [minutes] [reason]` | Mute member (default 10min) |
| `!unmute @user` | Unmute member |
| `!timeout @user <min> [reason]` | Timeout member |
| `!untimeout @user` | Remove timeout |
| `!warn @user [reason]` | Warn member |
| `!warnings @user` | Check user's warnings |
| `!clearwarnings @user` | Clear all warnings (Admin) |

### 🧹 Channel Management
| Command | Description |
|---------|-------------|
| `!purge <amount> [@user]` | Delete messages (optionally from specific user) |
| `!clear [amount]` | Bulk delete messages |
| `!slowmode <seconds>` | Set slowmode (0 to disable) |
| `!lock` | Lock channel |
| `!unlock` | Unlock channel |

### 📊 Information & Stats
| Command | Description |
|---------|-------------|
| `!scan <message>` | Manually scan text for abuse |
| `!history @user` | View user's abuse history |
| `!stats` | View detection statistics |
| `!serverinfo` | Display server information |
| `!userinfo [@user]` | Display user information |
| `!automod` | View/configure auto-mod settings |

### 📖 Help
| Command | Description |
|---------|-------------|
| `!help_guardify` | Show all commands |
| `!setup` | Show setup wizard |

---

## 🤖 AUTO-MODERATION (Always Active)

The bot automatically:
- ✅ Detects and removes abusive language (100+ keywords)
- ✅ Prevents spam (auto-timeout 2 minutes)
- ✅ Removes excessive caps messages
- ✅ Warns users automatically
- ✅ Timeouts users after 5 warnings (10 minutes)
- ✅ Logs all abuse detections
- ✅ Sends DMs to users who violate rules

**Admins and moderators are exempt from auto-moderation.**

---

## 📊 LOGGING FEATURES

### General Activity Logs
All activities automatically logged to `forensics_logs/activity_logs.jsonl`:
- Bot startup
- Member joins (with account age)
- Member leaves (with roles)
- Message edits and deletes
- Channel creates and deletes
- Member bans and unbans
- Anti-raid alerts

### Moderator Action Logs
All mod actions logged to `forensics_logs/mod_actions.jsonl`:
- Who performed the action
- Who was affected
- What action was taken
- Why (reason provided)
- When (timestamp)

### Abuse Evidence
All abuse detections logged to `forensics_logs/abuse_evidence.jsonl`:
- Message content
- Abuse score and severity
- Keywords detected
- User information
- Timestamp

### Discord Channel Logs
If you set up log channels with `!setlog` and `!setmodlog`, the bot will also send formatted embeds to Discord channels for real-time monitoring.

---

## 🎨 CUSTOMIZATION

### Welcome Message Variables
Use these in your welcome/goodbye messages:
- `{user}` - Mentions the user (@User)
- `{server}` - Server name
- `{count}` - Total member count

**Example:**
```
!welcomemsg Welcome {user} to **{server}**! You are member #{count}! 🎉
```

**Result:**
> Welcome @NewUser to **My Awesome Server**! You are member #150! 🎉

---

## 🔐 PERMISSIONS REQUIRED

Make sure the bot has these permissions:

**Essential:**
- ✅ Manage Roles
- ✅ Kick Members
- ✅ Ban Members
- ✅ Moderate Members (for timeouts)
- ✅ Manage Channels
- ✅ Manage Messages
- ✅ Read Messages/View Channels
- ✅ Send Messages
- ✅ Embed Links
- ✅ Read Message History

**Optional:**
- ✅ Manage Nicknames
- ✅ Manage Webhooks

**Bot Role Position:**
- Bot's role must be ABOVE the roles of members you want to moderate
- Bot's role must be BELOW your admin roles (for safety)

---

## ⚙️ BOT STATUS & ACTIVITY

The bot shows dynamic status:
```
Watching {server_count} servers | !help_guardify
```

When online, you'll see:
```
🛡️  Guardify#1234 is now ONLINE!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Active in 5 servers
👥 Protecting 1,234 members
🤖 Auto-moderation: ENABLED
🔒 Anti-raid protection: ENABLED
📝 Activity logging: ENABLED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🐛 TROUBLESHOOTING

### Bot doesn't send welcome messages
1. ✅ Set welcome channel: `!setwelcome #channel`
2. ✅ Check bot can send messages in that channel
3. ✅ Check bot has "Embed Links" permission

### Verification not working
1. ✅ Run `!setupverify` to create roles
2. ✅ Manually configure channel permissions:
   - Unverified role: Can only see #verification channel
   - Verified role: Can see all other channels
3. ✅ Make sure bot's role is above Unverified/Verified roles

### Anti-raid alerts not showing
1. ✅ Enable anti-raid: `!antiraid on`
2. ✅ Set log channel: `!setlog #logs`
3. ✅ Test with multiple accounts joining quickly

### Logs not being saved
- Logs are always saved to `forensics_logs/` directory
- For Discord channel logs, you must set channels with `!setlog` and `!setmodlog`

---

## 📊 FEATURE COMPARISON

| Feature | Guardify | Sapphire Bot |
|---------|----------|--------------|
| Welcome System | ✅ | ✅ |
| Goodbye Messages | ✅ | ✅ |
| Verification | ✅ | ✅ |
| Anti-Raid | ✅ | ✅ |
| Auto-Role | ✅ | ✅ |
| Moderation Commands | ✅ | ✅ |
| Logging System | ✅ | ✅ |
| Abuse Detection | ✅ (AI-powered) | ❌ |
| Spam Protection | ✅ | ✅ |
| Auto-Warnings | ✅ | ✅ |
| Configuration Commands | ✅ | ✅ |
| Setup Wizard | ✅ | ✅ |

---

## 🚀 RUNNING THE BOT

### Option 1: Quick Start
```bash
python bot.py
```

### Option 2: Using Batch File
```bash
start_bot_enhanced.bat
```

### Option 3: With Valid Token
Make sure your `config.json` has a valid bot token:
```json
{
  "bot_token": "YOUR_ACTUAL_BOT_TOKEN_HERE"
}
```

Get your token from:
https://discord.com/developers/applications

**IMPORTANT:** Enable these Privileged Gateway Intents:
- ✅ Server Members Intent
- ✅ Message Content Intent
- ✅ Presence Intent

---

## 🌐 DEPLOYING 24/7

The bot is ready for 24/7 deployment on:
- **Render.com** (FREE)
- **Railway.app** (FREE)
- **Heroku** (Paid)
- **VPS** (DigitalOcean, AWS, etc.)

See `BOT_SETUP_AND_RUN.md` for detailed deployment instructions.

---

## 📞 SUPPORT

For help:
1. Type `!help_guardify` in Discord
2. Type `!setup` for configuration wizard
3. Type `!config` to see current settings
4. Check `forensics_logs/` for activity logs

---

**Your bot is now a powerful Sapphire-like moderation bot!** 🎉

Just add your bot token and run it to start protecting your server with:
- ✅ Welcome/goodbye system
- ✅ Verification system
- ✅ Anti-raid protection
- ✅ Advanced logging
- ✅ AI-powered abuse detection
- ✅ Comprehensive moderation tools

**Use `!setup` to configure everything interactively!**
