# 🛡️ GUARDIFY - SAPPHIRE-LIKE BOT - QUICK REFERENCE

## ⚡ ESSENTIAL COMMANDS

### First-Time Setup
```
!setup              # Interactive setup wizard (shows all options)
!config             # View current server configuration
```

### Welcome System
```
!setwelcome #channel                  # Set welcome/goodbye channel
!welcomemsg Welcome {user} to {server}! 🎉   # Custom welcome
!goodbyemsg Goodbye {user}! 👋        # Custom goodbye
```

### Logging
```
!setlog #logs            # General activity logs
!setmodlog #mod-logs     # Moderation action logs
```

### Security
```
!antiraid on             # Enable anti-raid protection
!raidthreshold 5         # Alert after 5 joins in 10 seconds
!setupverify             # Enable verification system
!verify                  # Users type this to verify
```

### Auto-Role
```
!autorole @RoleName      # Auto-assign role to new members
!autorole none           # Disable auto-role
```

### Moderation
```
!mute @user 10 reason    # Mute for 10 minutes
!purge 50 @user          # Delete 50 messages from user
!nick @user NewName      # Change nickname
!role @user @role        # Add/remove role
!warn @user reason       # Warn user
```

### Info
```
!help_guardify           # Show all commands
!serverinfo              # Server details
!stats                   # Abuse detection stats
```

---

## 📊 MESSAGE VARIABLES

Use in welcome/goodbye messages:
- `{user}` → @mentions the user
- `{server}` → Server name
- `{count}` → Total member count

Example:
```
!welcomemsg Welcome {user}! You're member #{count} of {server}! 🎉
```

---

## 🔧 COMPLETE COMMAND LIST

| Category | Commands |
|----------|----------|
| **Setup** | setup, config, setwelcome, setlog, setmodlog |
| **Messages** | welcomemsg, goodbyemsg |
| **Verification** | setupverify, verify |
| **Security** | antiraid, raidthreshold |
| **Roles** | autorole, role, nick |
| **Moderation** | kick, ban, unban, mute, unmute, timeout, warn, purge |
| **Channel** | clear, slowmode, lock, unlock |
| **Info** | scan, history, stats, warnings, serverinfo, userinfo |
| **Help** | help_guardify, automod |

---

## 🤖 AUTO-MODERATION (Always Active)

- ✅ Detects 100+ offensive words
- ✅ Blocks spam (auto-timeout 2min)
- ✅ Removes excessive caps
- ✅ Auto-warns violators
- ✅ Timeouts after 5 warnings (10min)
- ✅ Logs everything to forensics_logs/

*Admins & moderators are exempt*

---

## 📋 WHAT GETS LOGGED

### General Logs (`!setlog #channel`)
- Member joins (with account age alerts)
- Member leaves
- Message edits/deletes
- Anti-raid alerts

### Mod Logs (`!setmodlog #channel`)
- All kicks, bans, unbans
- All mutes, timeouts, warns
- Who did it, when, and why

### Forensics Logs (Local Files)
- `activity_logs.jsonl` - All activities
- `mod_actions.jsonl` - All mod actions
- `abuse_evidence.jsonl` - All abuse detections
- `warnings.json` - Warning tracking
- `guild_configs.json` - Server settings

---

## ⚙️ PERMISSIONS NEEDED

Make sure bot has:
- ✅ Manage Roles
- ✅ Kick Members
- ✅ Ban Members
- ✅ Moderate Members
- ✅ Manage Messages
- ✅ Send Messages
- ✅ Embed Links

**Bot role must be ABOVE roles it moderates!**

---

## 🚀 TO START BOT

1. Get token from https://discord.com/developers/applications
2. Enable **Message Content Intent** (critical!)
3. Update `config.json` with token
4. Run: `python bot.py`

---

## ✨ SAPPHIRE-LIKE FEATURES

✅ Welcome/goodbye messages  
✅ Verification system  
✅ Anti-raid protection  
✅ Advanced logging  
✅ Auto-role assignment  
✅ Setup wizard  
✅ Per-server configs  
✅ Enhanced moderation  
✅ Professional embeds  

**PLUS: AI-powered abuse detection!**

---

## 📞 QUICK HELP

- Type `!help_guardify` in Discord
- Type `!setup` for setup wizard
- Read `SAPPHIRE_FEATURES.md` for full guide
- Check `forensics_logs/` for activity logs

---

**Your bot is ready to protect your server like Sapphire bot!** 🎉
