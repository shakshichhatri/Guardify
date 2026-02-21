# 🚀 Enhanced Warning System - Quick Start Guide

## What's New?

Your Guardify bot now has **automatic offensive content detection** for **English and Hindi** with intelligent muting!

---

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Restart Bot
```bash
python bot.py
```

### Step 3: Done! ✅
The bot now automatically:
- 🔍 Detects offensive content
- ⚠️ Issues warnings automatically
- 🔇 Mutes users after 5 warnings
- 📤 Sends notifications

---

## Quick Command Reference

### Check a User's Warnings
```
!warnings @username
```

### Manually Warn Someone
```
!warn @username broke rule #2
```

### Mute Someone Manually
```
!forcemute @username 10 spamming
```

### Unmute Someone
```
!unmute @username
```

### View Stats
```
!warningstats
```

---

## 🎯 How It Works

1. **User posts offensive content**
   ↓
2. **Bot detects it** (English or Hindi)
   ↓
3. **Message deleted automatically**
   ↓
4. **Warning added** (1/5, 2/5, 3/5, 4/5...)
   ↓
5. **User notified** via channel + DM
   ↓
6. **After 5 warnings** → **Auto-muted for 10 minutes**
   ↓
7. **After 10 minutes** → **Auto-unmuted**

---

## What Gets Detected?

✅ Hate speech  
✅ Threats & violence encouragement  
✅ Harassment & bullying  
✅ Profanity & offensive slangs  
✅ Discriminatory language  
✅ Harmful content  

**In both English and Hindi!**

---

## Data Stored

All warnings are saved in:
- 📁 `forensics_logs/user_warnings.json`
- 📁 `forensics_logs/user_mutes.json`

**Persistent** - survives bot restarts!

---

## Bot Permissions Needed

Make sure your bot's Discord permissions include:
- ✅ Manage Messages (delete)
- ✅ Moderate Members (mute)
- ✅ Manage Roles (assign mute role)
- ✅ Send Messages
- ✅ Embed Links

---

## Common Tasks

### I want to see all warnings for a user
```
!warnings @username
```

### I want to forgive a user (clear warnings)
```
!clearwarnings @username
```

### I want to manually mute someone
```
!forcemute @username 30 reason
```

### I want to see overall statistics
```
!warningstats
```

### I want to use my own mute role
```
!setmuterole @CustomRole
```

---

## Editing Offensive Words

To add/remove offensive words:

1. Open `content_detector.py`
2. Find `self.offensive_keywords_en` (English) or `self.offensive_keywords_hi` (Hindi)
3. Add/remove words in the list
4. Save and restart bot

Example:
```python
self.offensive_keywords_en = {
    'hate', 'kill', 'stupid',  # These are detected
    'mynewword', 'badword',     # Add your custom words
    ...
}
```

---

## Troubleshooting

### Mute role not being created?
- Bot needs "Manage Roles" permission
- Bot's role must be above mute role in hierarchy

### Words not being detected?
- Check `content_detector.py` for the word list
- Use `!scan your text here` to test detection

### Warnings not saving?
- Check if `forensics_logs/` folder exists
- Verify bot can write to the folder

---

## Files Changed

New files:
- ✅ `content_detector.py` - Advanced multilingual detection
- ✅ `warning_system.py` - Warning & mute management
- ✅ `ENHANCED_WARNING_SYSTEM.md` - Full documentation

Updated files:
- 📝 `bot.py` - Enhanced message handler + new commands
- 📝 `requirements.txt` - New dependencies

---

## Support

Have questions? Check:
- 📖 `ENHANCED_WARNING_SYSTEM.md` for detailed docs
- 🔧 Bot console output for debug messages
- 📊 `forensics_logs/` directory for stored data

---

**Your bot is now enhanced! 🎉**

For detailed information, see `ENHANCED_WARNING_SYSTEM.md`
