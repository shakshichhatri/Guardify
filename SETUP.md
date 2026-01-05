# Quick Start Guide - Respect Ranger

## Step-by-Step Setup

### 1. Environment Setup

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download TextBlob corpora (required)
python -m textblob.download_corpora
```

### 2. Discord Bot Configuration

1. Visit the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and name it "Respect Ranger"
3. Navigate to the "Bot" section
4. Click "Add Bot"
5. Under "Privileged Gateway Intents", enable:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent
6. Click "Reset Token" and copy your bot token (save it securely!)

### 3. Bot Token Configuration

**Method 1: Environment Variable (Recommended)**
```bash
# On Windows (Command Prompt):
set DISCORD_BOT_TOKEN=your_token_here

# On Windows (PowerShell):
$env:DISCORD_BOT_TOKEN="your_token_here"

# On macOS/Linux:
export DISCORD_BOT_TOKEN="your_token_here"
```

**Method 2: Configuration File**
```bash
# Copy the example config
cp config.json.example config.json

# Edit config.json with your favorite editor
# Replace YOUR_DISCORD_BOT_TOKEN_HERE with your actual token
```

### 4. Invite Bot to Your Server

1. In Discord Developer Portal, go to "OAuth2" > "URL Generator"
2. Under "Scopes", select:
   - ✅ bot
3. Under "Bot Permissions", select:
   - ✅ Read Messages/View Channels
   - ✅ Send Messages
   - ✅ Manage Messages
   - ✅ Read Message History
   - ✅ Embed Links
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

### 5. Run the Bot

```bash
python bot.py
```

You should see:
```
RespectRanger#1234 has connected to Discord!
Bot is active in 1 guilds
```

## Testing the Bot

### Test Automatic Detection

Send these messages in any channel where the bot has access:

**Clean Message (should NOT be flagged):**
```
Hello everyone! Have a great day!
```

**Abusive Message (should be flagged):**
```
You are so stupid and worthless
```

Check the console output for detection logs.

### Test Commands

**1. Manual Scan:**
```
!scan You are amazing and wonderful
!scan This is stupid and pathetic
```

**2. View Help:**
```
!help_ranger
```

**3. View Statistics (requires Manage Messages permission):**
```
!stats
```

**4. View User History (requires Manage Messages permission):**
```
!history @username 5
```

## Verifying Installation

Run the test suite:
```bash
python -m pytest test_bot.py -v
```

Or using unittest:
```bash
python test_bot.py
```

All tests should pass ✅

## Checking Forensics Logs

After detecting abusive messages, check the logs:

```bash
# View the log file
cat forensics_logs/abuse_evidence.jsonl

# Or on Windows:
type forensics_logs\abuse_evidence.jsonl
```

Each line contains a JSON object with full evidence details.

## Troubleshooting

### Bot doesn't respond to commands
- Verify the bot has "Send Messages" permission
- Check that the command prefix is correct (default: `!`)
- Ensure the bot is online in your server

### "Message Content Intent" errors
- Enable "Message Content Intent" in Discord Developer Portal
- Restart the bot after enabling

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Download TextBlob corpora: `python -m textblob.download_corpora`

### Bot token errors
- Verify your token is correct
- Ensure there are no extra spaces in the token
- Check that environment variable is set or config.json exists

## Next Steps

- Customize the keyword list in `bot.py`
- Adjust sensitivity thresholds
- Set up automated backup of forensics logs
- Review and analyze collected data regularly

## Support

For issues or questions, please open an issue on GitHub:
https://github.com/shakshichhatri/respect-ranger-/issues
