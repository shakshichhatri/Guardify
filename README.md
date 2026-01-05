# Respect Ranger 🛡️

AI-enabled Discord bot for social media forensics to detect and prevent digital abuse.

## Overview

Respect Ranger is a Python-based Discord bot that uses sentiment analysis and keyword detection to identify abusive content in real-time. The bot automatically logs evidence for digital forensics, helping server moderators maintain a safe and respectful community environment.

## Features

### 🤖 Automatic Abuse Detection
- Real-time monitoring of all Discord messages
- Sentiment analysis using TextBlob NLP library
- Keyword-based detection for common abusive terms
- Multi-level severity classification (Low, Medium, High)

### 📊 Forensics Logging
- Comprehensive evidence collection in JSONL format
- Stores message content, author details, timestamps, and analysis results
- Enables investigation and pattern analysis
- User abuse history tracking

### 🔧 Moderator Commands
- `!scan <message>` - Manually analyze a message for abusive content
- `!history @user [limit]` - View abuse history for a specific user
- `!stats` - Display overall abuse detection statistics
- `!help_ranger` - Show available commands and usage

## Installation

### Prerequisites
- Python 3.8 or higher
- Discord Bot Token (from Discord Developer Portal)
- Discord.py library with message content intent enabled

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/shakshichhatri/respect-ranger-.git
   cd respect-ranger-
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download TextBlob corpora** (required for sentiment analysis)
   ```bash
   python -m textblob.download_corpora
   ```

4. **Configure the bot**
   
   Option A: Using environment variable (recommended)
   ```bash
   export DISCORD_BOT_TOKEN="your_bot_token_here"
   ```
   
   Option B: Using config file
   ```bash
   cp config.json.example config.json
   # Edit config.json and add your bot token
   ```

5. **Run the bot**
   ```bash
   python bot.py
   ```

## Creating a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Enable these Privileged Gateway Intents:
   - Message Content Intent
   - Server Members Intent
5. Copy the bot token (keep it secure!)
6. Go to "OAuth2" > "URL Generator"
7. Select scopes: `bot`
8. Select permissions: `Read Messages/View Channels`, `Send Messages`, `Manage Messages`, `Read Message History`
9. Use the generated URL to invite the bot to your server

## Usage

### Automatic Detection
The bot automatically monitors all messages in channels it has access to. When abusive content is detected:
- The message is analyzed for sentiment and keywords
- Evidence is logged to `forensics_logs/abuse_evidence.jsonl`
- Console output shows detection details

### Manual Commands

**Scan a message:**
```
!scan This is a test message to analyze
```

**View user history:**
```
!history @username 5
```

**View statistics:**
```
!stats
```

**Get help:**
```
!help_ranger
```

## How It Works

### Abuse Detection Algorithm

1. **Sentiment Analysis**: Uses TextBlob to calculate message sentiment polarity (-1 to +1)
2. **Keyword Detection**: Scans for known abusive keywords/phrases
3. **Score Calculation**: Combines sentiment and keyword matches
4. **Classification**: Determines if message is abusive and assigns severity level

### Severity Levels

- 🟢 **Low**: Abuse score 0.4-0.5
- 🟡 **Medium**: Abuse score 0.5-0.8
- 🔴 **High**: Abuse score > 0.8

### Forensics Data Structure

Each logged evidence entry includes:
```json
{
  "message_id": "unique_message_id",
  "author_id": "user_id",
  "author_name": "username",
  "channel_id": "channel_id",
  "guild_name": "server_name",
  "content": "message_content",
  "created_at": "timestamp",
  "analysis": {
    "is_abusive": true,
    "abuse_score": 0.75,
    "sentiment": -0.6,
    "detected_keywords": ["keyword1", "keyword2"],
    "severity": "medium"
  },
  "logged_at": "timestamp"
}
```

## Permissions Required

The bot requires the following Discord permissions:
- Read Messages/View Channels
- Send Messages
- Manage Messages (for moderator commands)
- Read Message History

## Customization

### Adding Custom Keywords

Edit the `abusive_keywords` list in the `AbuseDetector` class in `bot.py`:

```python
self.abusive_keywords = [
    'hate', 'kill', 'stupid', # ... add your keywords
]
```

### Adjusting Sensitivity

Modify thresholds in the `AbuseDetector` class:

```python
self.sentiment_threshold = -0.3  # More negative = stricter
self.keyword_weight = 0.4        # Higher = keywords matter more
```

## Security & Privacy

- Bot token should never be committed to version control
- Forensics logs contain sensitive data - store securely
- Only authorized moderators can use detection commands
- Evidence logs should comply with your privacy policy
- Consider data retention policies for forensics logs

## Limitations

- Sentiment analysis accuracy depends on context and sarcasm detection
- Keyword lists need regular updates
- False positives may occur
- Does not detect image-based abuse
- Requires message content intent (privacy implications)

## Future Enhancements

- Machine learning-based classification
- Multi-language support
- Image/attachment analysis
- Integration with moderation actions
- Web dashboard for forensics review
- Export reports in various formats

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Disclaimer

This bot is provided as-is for educational and community safety purposes. Users are responsible for:
- Complying with Discord's Terms of Service
- Following local laws regarding data collection and privacy
- Implementing appropriate data protection measures
- Using the bot responsibly and ethically

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
