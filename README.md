# Guardify 🛡️

**AI-Enabled Social Media Forensics Investigation for Detecting and Preventing Digital Abuse**

## Overview

Guardify is an academic research tool and Discord moderation bot that uses **dual AI sentiment analysis** (TextBlob + VADER) to detect digital abuse in real-time. Designed for researchers, educators, and community moderators, it provides forensics-grade evidence collection with SHA-256 integrity verification and CSV export for data analysis.

## 🎓 Academic Features

### 🤖 Dual AI Detection System
- **TextBlob**: Pattern-based sentiment analysis
- **VADER**: Social media-optimized sentiment analyzer
- Combined sentiment scoring for improved accuracy
- Real-time monitoring of all Discord messages
- Multi-level severity classification (High, Medium, Low)

### 🔐 Forensics-Grade Evidence Collection
- **SHA-256 hashing** for evidence integrity verification
- **CSV export** for Excel, pandas, and statistical analysis
- **JSONL format** for detailed forensics logs
- Comprehensive metadata including timestamps, sentiment scores, and user data
- User interaction network tracking for pattern analysis

### 🛡️ Prevention & Early Intervention
- **Severity-based prevention tips** and guidance
- Evidence-based intervention strategies
- Crisis resource integration
- Automatic alerts for high-risk situations
- Progressive warning system

### 📊 Data Analysis & Research
- **CSV export** compatible with Excel, pandas, R, SPSS
- Statistical analysis capabilities
- Network analysis of user interactions
- Timeline tracking for longitudinal studies
- Perfect for cyberbullying research and data science projects

### 🔧 Professional Moderation Tools
- **15 slash commands** for comprehensive moderation
- Auto-moderation with configurable sensitivity
- Welcome messages and log channels
- Warning system with history tracking
- Web dashboard with OAuth2 authentication

## Installation

### Prerequisites
- Python 3.8 or higher
- Discord Bot Token (from Discord Developer Portal)
- Discord.py library with message content intent enabled

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/shakshichhatri/Guardify.git
   cd Guardify
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

Modify thresholds in the `AbuseDetector` class in `bot.py`:

```python
# Class-level constants at the top of AbuseDetector
SENTIMENT_THRESHOLD = -0.3  # More negative = stricter
KEYWORD_WEIGHT = 0.4        # Higher = keywords matter more
ABUSE_SCORE_THRESHOLD = 0.4 # Minimum score to classify as abusive
```

## 📊 Quick Command Reference

| Command | Purpose | Permission Required |
|---------|---------|---------------------|
| `/scan <message>` | Analyze specific message | Manage Messages |
| `/warn @user <reason>` | Warn a user | Manage Messages |
| `/kick @user <reason>` | Kick a user | Kick Members |
| `/ban @user <reason>` | Ban a user | Ban Members |
| `/timeout @user <duration>` | Timeout a user | Moderate Members |
| `/purge <amount>` | Delete messages | Manage Messages |
| `/history @user` | View user's warnings | Manage Messages |
| `/warnings` | View all warnings | Manage Messages |
| `/removewarn @user <warn_id>` | Remove specific warning | Manage Messages |
| `/clearwarnings @user` | Clear all warnings | Administrator |
| `/stats` | View abuse statistics | Manage Messages |
| `/export` | Export forensics data (CSV) | Administrator |
| `/prevention` | Prevention tips & resources | Manage Messages |
| `/automod <enable/disable>` | Toggle auto-moderation | Manage Server |
| `/setlog <#channel>` | Set log channel | Administrator |
| `/setwelcome <#channel>` | Set welcome channel | Administrator |

## 🎓 Academic Research

### For Researchers
Guardify provides forensics-grade data for academic research:

- **CSV Export**: `/export` command provides structured data
- **Dual AI Scores**: Both TextBlob and VADER sentiment scores
- **Integrity Verification**: SHA-256 hashes for evidence validation
- **Network Analysis**: User interaction tracking across servers
- **Longitudinal Studies**: Timestamp-based timeline analysis

### Sample Research Applications
- Cyberbullying detection and prevention studies
- Social media safety research
- Machine learning training datasets
- Educational intervention effectiveness
- Community moderation best practices

### Data Fields Available
```csv
evidence_id, timestamp, guild_id, guild_name, user_id, username,
channel_id, message_content, severity, textblob_sentiment,
vader_sentiment, combined_sentiment, content_hash
```

See [`ACADEMIC_FEATURES.md`](ACADEMIC_FEATURES.md) for detailed documentation.

## 🔐 Security & Privacy

- Bot token should never be committed to version control
- Forensics logs contain sensitive data - store securely
- Only authorized moderators can use detection commands
- Evidence logs should comply with your privacy policy
- SHA-256 hashing ensures evidence integrity
- Consider data retention policies for forensics logs

## ⚠️ Limitations

- Sentiment analysis accuracy depends on context and sarcasm detection
- Keyword lists need regular updates
- False positives may occur with nuanced language
- Does not detect image-based abuse
- Requires message content intent (privacy implications)
- AI models trained primarily on English text

## 🚀 Future Enhancements

- ✅ ~~Dual AI sentiment analysis~~ (Implemented)
- ✅ ~~CSV export for data analysis~~ (Implemented)
- ✅ ~~SHA-256 integrity verification~~ (Implemented)
- ✅ ~~Prevention tips and guidance~~ (Implemented)
- [ ] Timeline visualization (matplotlib)
- [ ] User network graphs
- [ ] Multi-language support
- [ ] Image/attachment analysis
- [ ] Automated PDF reports
- [ ] Custom ML model training

## 📞 Crisis Resources

If you or someone you know is experiencing a crisis:

- **988 Suicide & Crisis Lifeline**: Call/text 988 or visit [988lifeline.org](https://988lifeline.org)
- **Crisis Text Line**: Text HOME to 741741
- **Cyberbullying Research Center**: [cyberbullying.org](https://cyberbullying.org)
- **StopBullying.gov**: [stopbullying.gov](https://www.stopbullying.gov)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Areas for Contribution
- Additional AI models for detection
- Visualization features (matplotlib/seaborn)
- Multi-language support
- Documentation improvements
- Test coverage expansion

## 📚 Documentation

- **[Academic Features](ACADEMIC_FEATURES.md)** - Detailed research features
- **[Quick Start Guide](QUICKSTART.md)** - Get started quickly
- **[Setup Guide](SETUP.md)** - Complete setup instructions
- **[OAuth Setup](OAUTH_SETUP.md)** - Dashboard authentication
- **[Project Summary](PROJECT_SUMMARY.md)** - Complete feature list
- **[Web Dashboard Guide](WEB_DASHBOARD_GUIDE.md)** - Dashboard usage

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
