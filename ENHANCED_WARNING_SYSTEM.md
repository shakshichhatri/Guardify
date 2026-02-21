# 🛡️ Guardify Enhanced Warning & Auto-Mute System

## Overview

The Guardify bot has been enhanced with an **advanced multilingual content detection system** and an **automatic warning & mute system**. The system automatically detects offensive content in both **English and Hindi**, issues warnings, and auto-mutes users after 5 warnings.

---

## 🎯 Key Features

### 1. **Advanced Multilingual Content Detection**
- ✅ Detects offensive content in **English and Hindi**
- ✅ Identifies **hate speech, threats, harassment, discrimination**
- ✅ Detects **offensive slangs, profanity, and harmful content**
- ✅ Uses multiple detection methods:
  - **Better-Profanity Library** - Industry-standard profanity detection
  - **Keyword Matching** - Custom offensive word lists (English & Hindi)
  - **Pattern Matching** - Regex patterns for threats and hate speech
  - **Sentiment Analysis** - Contextual analysis using TextBlob

### 2. **Automatic Warning System**
- ✅ **Automatic warnings** when users post offensive content
- ✅ Warnings are **persistent** and stored in the system
- ✅ Users can see their warning count (**X/5**)
- ✅ After **5 warnings**, user is **automatically muted for 10 minutes**
- ✅ Warnings are tracked **per-guild** (different servers have separate warning counts)

### 3. **Message Deletion**
- ✅ Messages with offensive content are **automatically deleted**
- ✅ No manual intervention needed

### 4. **Automatic Muting**
- ✅ After 5 warnings, user is **automatically muted** for **10 minutes**
- ✅ A **"Muted" role** is automatically created and assigned
- ✅ Muted users **cannot send messages or speak in voice channels**
- ✅ **Automatic unmuting** after 10 minutes (no manual action needed)
- ✅ Mute status is **persistent** across bot restarts

### 5. **Notifications**
- ✅ **Channel notification** when content is detected and removed
- ✅ **DM notification** to the user explaining the violation
- ✅ Clear warning count display

---

## 📊 Content Detection Categories

### English Categories
- **HATE_SPEECH** - Racist, discriminatory, or hateful content
- **THREAT_VIOLENCE** - Threats, violence encouragement, suicide encouragement
- **DISCRIMINATION** - Derogatory terms based on identity
- **HARASSMENT** - Bullying, personal attacks
- **PROFANITY** - Offensive language and vulgar words
- **SLANG_OFFENSIVE** - Offensive slang and leetspeak variations

### Hindi Categories (Gaali)
- **HATE_SPEECH** - Communal, discriminatory content
- **THREATS** - "Mar dunga", "Chalbazo", violence threats
- **SEVERE_INSULTS** - "Harami", "Kamina", "Chutiya", etc.
- **HARASSMENT** - Personal attacks and bullying

---

## 🔧 Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Required libraries:
- `better-profanity>=0.7.0` - Profanity detection
- `profanityfilter>=2.0.6` - Additional filtering
- `langdetect>=1.0.9` - Language detection
- `transformers>=4.30.0` - AI model support
- `torch>=2.0.0` - ML framework
- Other existing dependencies

### 2. Bot Permissions Required
Ensure your bot has these permissions:
- ✅ **Manage Messages** - Delete offensive messages
- ✅ **Moderate Members** - Timeout/mute users
- ✅ **Manage Roles** - Create and assign mute role
- ✅ **Send Messages** - Send notifications
- ✅ **Embed Links** - Send embedded notifications

### 3. Server Setup
1. Create a "Muted" role (or let the bot create it automatically)
2. The bot will use `!setmuterole @role` if you have a custom mute role
3. Ensure the bot's role is **above** the muted role in the hierarchy

---

## 📋 Commands

### Checking Warnings
```
!warnings @user
```
Shows all warnings and mute status for a user in the current server.

### Manual Warning
```
!warn @user [reason]
```
Manually add a warning to a user (moderator only).

### Clear Warnings
```
!clearwarnings @user
```
Clear all warnings for a user (administrator only).

### Manual Mute
```
!forcemute @user [minutes] [reason]
```
Manually mute a user for specified minutes (default: 10 minutes).

### Manual Unmute
```
!unmute @user
```
Manually unmute a user.

### Warning Statistics
```
!warningstats
```
View warning system statistics for the current server.

### Set Mute Role
```
!setmuterole @role
```
Set a custom mute role for your server (administrator only).

---

## 📁 Data Storage

All warning and mute data is stored persistently in the `forensics_logs/` directory:

```
forensics_logs/
├── user_warnings.json      # All user warnings (per-guild)
├── user_mutes.json         # Active and inactive mutes
├── mute_roles.json         # Mute role configuration per guild
├── abuse_evidence.jsonl    # Evidence of all detected content
├── activity_logs.jsonl     # General activity logs
├── warnings.json           # Legacy warning format (for compatibility)
└── abuse_evidence.csv      # CSV export of abuse cases
```

---

## 🚀 How It Works

### Flow Diagram

```
User sends message
      ↓
Content Detector (Multilingual)
      ├─→ Better-Profanity Check
      ├─→ Keyword Matching (EN/HI)
      └─→ Pattern Matching (Threats)
      ↓
Is Offensive?
      ├─→ NO → Process normally
      └─→ YES
           ↓
        Delete Message
           ↓
        Add Warning (Warning Manager)
           ↓
        Warning Count < 5?
           ├─→ YES → Send warning notification
           └─→ NO (5 or more)
                ↓
             Create Mute Record
                ↓
             Apply Discord Timeout
                ↓
             Assign Mute Role
                ↓
             Schedule Auto-Unmute (10 minutes)
                ↓
             After 10 minutes → Auto-unmute
```

---

## 🎨 Warning Notification Examples

### First Warning
```
⚠️ Offensive Content Removed
Your message violated community guidelines.

Category: PROFANITY
Severity: LOW
Warnings: 1/5

You will be muted after 4 more warning(s)
```

### After 5 Warnings (Auto-Mute)
```
⚠️ Offensive Content Removed
Your message violated community guidelines.

Category: HATE_SPEECH
Severity: CRITICAL
Warnings: 5/5

🔇 AUTO-MUTE
Muted for 10 minutes (reached 5 warnings)
```

### DM Notification
```
⚠️ Community Guidelines Violation
Your message in [Server Name] was removed.

Detected Content: THREAT_VIOLENCE
Severity: HIGH
Warnings: 4/5

Appeal: Contact server moderators if you believe this is an error.
```

---

## 🛠️ Configuration

### Automatic Mute Duration
To change the auto-mute duration (currently 10 minutes), edit `bot.py`:
```python
await message.author.timeout(timedelta(minutes=10), ...)  # Change 10 to desired minutes
```

### Warning Threshold
To change the warning threshold (currently 5), search in `bot.py`:
```python
if warning_count >= 5:  # Change 5 to desired threshold
```

### Language Support
Currently supports: **English** and **Hindi**

To add more languages, extend `content_detector.py`:
1. Add language-specific keyword lists
2. Update `detect_language()` to recognize the language
3. Add patterns for the language

---

## 📈 Monitoring & Statistics

### View Statistics
```
!stats           # Overall abuse detection stats
!warningstats    # Warning system stats for current server
!history @user   # View abuse history for a user
```

### Data Analysis
All data is stored in JSON format and can be analyzed:
- `user_warnings.json` - Track warning patterns
- `user_mutes.json` - Monitor mute effectiveness
- `abuse_evidence.jsonl` - Analyze detected content types

---

## ⚙️ Troubleshooting

### Mute role not being assigned
- Ensure bot has "Manage Roles" permission
- Check that bot's role is above the muted role in hierarchy
- Use `!setmuterole @CustomRole` to set a custom mute role

### Not detecting certain offensive words
- Update the keyword lists in `content_detector.py`
- Add to `offensive_keywords_en` or `offensive_keywords_hi`
- The system uses multiple detection methods, so it's hard to evade

### Warnings not persisting
- Check that `forensics_logs/` directory exists and is writable
- Verify `user_warnings.json` file exists and has valid JSON
- Check bot logs for any JSON parsing errors

### Auto-unmute not working
- Verify bot has "Moderate Members" permission
- Check if the unmute task is properly scheduled
- Look for task errors in bot console output

---

## 🔐 Privacy & Data

- ⚠️ **All offensive content is logged** for moderation purposes
- 📁 Data is stored locally (not sent to external services)
- 🔏 Access restricted to server moderators/administrators
- ✅ Complies with Discord's Terms of Service

---

## 📞 Support & Enhancement

### Adding More Offensive Words
Edit `content_detector.py` and update:
- `self.offensive_keywords_en` for English
- `self.offensive_keywords_hi` for Hindi

### Adding New Detection Methods
Modify `analyze_content()` method in `HindiEnglishContentDetector` class to add:
- ML-based detection
- Custom API calls
- External service integration

### Testing Detection
Use the command:
```
!scan [text to analyze]
```

---

## 📝 Logs & Debugging

Enable detailed logging by checking console output:
```
[MESSAGE SCAN] User: 'message...' | Offensive: True | Category: HATE_SPEECH
[OFFENSIVE CONTENT DETECTED] ...
[WARNING ADDED] User now has 3/5 warnings
[AUTO-MUTE] User muted for 10 minutes (5 warnings)
[AUTO-UNMUTE] User has been unmuted
```

---

## 🎯 Best Practices

1. **Regular Review** - Check warning statistics weekly
2. **Role Management** - Ensure mute role hierarchy is correct
3. **Appeals** - Establish an appeal process for users
4. **Clear Rules** - Communicate community guidelines clearly
5. **Monitor Logs** - Review forensics logs for patterns
6. **Update Lists** - Keep offensive word lists current

---

## 🌍 Multilingual Expansion

Current support: **English 🇬🇧 + Hindi 🇮🇳**

To add more languages (e.g., Spanish, French, etc.):
1. Add language-specific keyword lists in `content_detector.py`
2. Update language detection patterns
3. Add regex patterns for language-specific threats
4. Test extensively before deployment

---

## 📊 Severity Levels

- **MINIMAL** (0.0-0.3) - Mild language
- **LOW** (0.3-0.5) - Offensive slangs
- **MEDIUM** (0.5-0.7) - Harassment, bullying
- **HIGH** (0.7-0.85) - Hate speech, discrimination
- **CRITICAL** (0.85-1.0) - Threats, violence encouragement

---

**Created:** February 2026  
**Version:** 2.0 (Enhanced with Multilingual Support)  
**Status:** Production Ready ✅
