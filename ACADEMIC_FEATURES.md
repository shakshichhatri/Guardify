# Guardify - Academic Research Features

## AI-Enabled Social Media Forensics Investigation for Detecting and Preventing Digital Abuse

This document outlines the academic research features implemented in Guardify to align with the project proposal.

---

## 🤖 Dual AI Sentiment Analysis

### Overview
Guardify uses **two complementary AI systems** for improved detection accuracy:

1. **TextBlob** - Polarity-based sentiment analysis
2. **VADER (Valence Aware Dictionary and sEntiment Reasoner)** - Social media-optimized sentiment analyzer

### How It Works

```python
# Each message is analyzed by both AI systems
textblob_sentiment = blob.sentiment.polarity  # -1.0 to +1.0
vader_scores = self.vader.polarity_scores(content)
combined_sentiment = (textblob_sentiment + vader_compound) / 2
```

### Output Fields
- `textblob_sentiment`: TextBlob polarity score
- `vader_sentiment`: VADER compound score
- `combined_sentiment`: Average of both scores
- `vader_details`: Breakdown (positive, neutral, negative, compound)

### Why Dual AI?
- **TextBlob**: Better for general language sentiment
- **VADER**: Specifically tuned for social media (emojis, slang, caps)
- **Combined**: More robust and accurate detection

---

## 🔐 Evidence Integrity Verification

### SHA-256 Hashing
Every piece of evidence includes a **cryptographic hash** for integrity verification.

```python
# Each logged evidence includes:
"content_hash": hashlib.sha256(content.encode()).hexdigest()[:16]
```

### Benefits
- **Tamper Detection**: Verify evidence hasn't been altered
- **Chain of Custody**: Maintain forensic integrity
- **Legal Compliance**: Meet academic and legal standards

### Usage
```
Original Message: "You're such an idiot"
SHA-256 Hash: 7a8f9d3e2b1c4a5d
```

If the message is altered, the hash won't match - proving tampering.

---

## 📊 CSV Export for Data Analysis

### Export Format
All forensics data is automatically exported to CSV format for analysis.

**File**: `forensics_logs/abuse_evidence.csv`

### CSV Columns
| Column | Description |
|--------|-------------|
| evidence_id | Unique identifier |
| timestamp | When incident occurred |
| guild_id | Server ID |
| guild_name | Server name |
| user_id | User ID who sent message |
| username | Username |
| channel_id | Channel ID |
| message_content | The harmful content |
| severity | high/medium/low |
| textblob_sentiment | TextBlob score |
| vader_sentiment | VADER score |
| combined_sentiment | Average score |
| content_hash | SHA-256 hash |

### Compatible With
- ✅ Microsoft Excel
- ✅ Google Sheets
- ✅ Python pandas
- ✅ R programming
- ✅ SPSS, Tableau, Power BI

### Analysis Examples

**Python pandas:**
```python
import pandas as pd

# Load evidence data
df = pd.read_csv('forensics_logs/abuse_evidence.csv')

# Analyze severity distribution
severity_counts = df['severity'].value_counts()

# Find most toxic users
toxic_users = df.groupby('username')['combined_sentiment'].mean()

# Time series analysis
df['timestamp'] = pd.to_datetime(df['timestamp'])
daily_incidents = df.groupby(df['timestamp'].dt.date).size()
```

**Excel:**
- Import CSV → Data → From Text/CSV
- Create pivot tables for analysis
- Generate charts and graphs

---

## 🛡️ Prevention Tips & Early Intervention

### Severity-Based Guidance

Guardify provides **contextual prevention tips** based on abuse severity:

#### High-Risk Situations (combined_sentiment < -0.5)
- 📞 Contact appropriate authorities immediately
- 🆘 Provide mental health resources
- 📝 Document all evidence thoroughly
- 👨‍👩‍👧 Notify parents/guardians if minors involved
- ⏸️ Implement cooling-off period

#### Medium-Risk Prevention (-0.5 to -0.2)
- 📋 Review community guidelines
- 🤖 Enable auto-moderation features
- 📊 Increase monitoring frequency
- 📚 Provide educational resources
- 🤝 Schedule conflict resolution

#### Low-Risk Best Practices (-0.2 to 0)
- 💬 Gentle reminders about respect
- ✨ Share positive examples
- ❤️ Encourage empathy
- 👀 Monitor for pattern changes
- 🌟 Foster inclusive culture

### Access Prevention Guide
```
/prevention - Display comprehensive prevention tips
```

---

## 📈 Network Analysis & User Interactions

### Interaction Tracking
Guardify tracks user interactions for network analysis:

```python
# Automatically logged:
user_interactions = {
    "user_123": ["guild_1", "guild_2"],
    "user_456": ["guild_1", "guild_3"]
}
```

### Use Cases
- Identify multi-server abuse patterns
- Detect coordinated harassment
- Visualize social networks
- Track repeat offenders

**File**: `forensics_logs/user_interactions.json`

---

## 📊 Data Export Commands

### `/export` - Export Forensics Data
Exports all evidence in CSV format for analysis.

**Features:**
- ✅ CSV format for Excel/pandas
- ✅ Includes all metadata
- ✅ SHA-256 integrity verification
- ✅ Ready for statistical analysis

**Example:**
```
/export
```

Returns: `guardify_evidence_export.csv` file

---

## 📚 Research Applications

### Academic Use Cases

#### 1. **Cyberbullying Research**
- Analyze sentiment patterns over time
- Study effectiveness of interventions
- Compare detection algorithms

#### 2. **Social Media Safety**
- Identify risk factors for abuse
- Develop prevention strategies
- Test moderation approaches

#### 3. **Educational Settings**
- Monitor student interactions
- Early detection of bullying
- Evidence for disciplinary action

#### 4. **Data Science Projects**
- Machine learning training data
- Sentiment analysis benchmarks
- Network analysis studies

### Sample Research Questions
- ✅ What times of day see highest abuse rates?
- ✅ Which keywords correlate with severe abuse?
- ✅ How effective is auto-moderation?
- ✅ Do warnings reduce repeat offenses?
- ✅ What intervention strategies work best?

---

## 🔧 Technical Implementation

### AI Models Used
1. **TextBlob 0.17.0+**
   - Pattern-based sentiment analysis
   - Polarity: -1 (negative) to +1 (positive)
   - Subjectivity scoring

2. **VADER 3.3.2+**
   - Lexicon and rule-based sentiment
   - Social media optimized
   - Emoji/emoticon aware
   - Handles slang and abbreviations

### Data Integrity
- **Algorithm**: SHA-256 cryptographic hashing
- **Implementation**: `hashlib.sha256(content.encode()).hexdigest()`
- **Purpose**: Tamper detection and forensic integrity

### Export Formats
- **JSONL**: Detailed logs with full metadata
- **CSV**: Structured data for analysis
- **JSON**: Configuration and tracking data

---

## 📖 Commands Reference

| Command | Purpose | Permission |
|---------|---------|------------|
| `/scan` | Analyze specific message for abuse | Manage Messages |
| `/export` | Export evidence data (CSV) | Administrator |
| `/prevention` | View prevention tips & resources | Manage Messages |
| `/stats` | View server abuse statistics | Manage Messages |
| `/automod enable` | Enable automatic detection | Manage Server |
| `/setlog` | Configure log channel | Administrator |

---

## 🎓 Citation & Attribution

If you use Guardify in academic research, please cite:

```
Project: AI-Enabled Social Media Forensics Investigation for Detecting and 
         Preventing Digital Abuse
Tool: Guardify Discord Moderation Bot
Features: Dual AI sentiment analysis (TextBlob + VADER), forensics logging,
          CSV export, SHA-256 integrity verification
```

---

## 📞 Resources & Support

### Crisis Resources
- **988 Suicide & Crisis Lifeline**: 988 or [988lifeline.org](https://988lifeline.org)
- **Crisis Text Line**: Text HOME to 741741
- **Cyberbullying Research Center**: [cyberbullying.org](https://cyberbullying.org)
- **StopBullying.gov**: [stopbullying.gov](https://www.stopbullying.gov)

### Technical Documentation
- See `PROJECT_SUMMARY.md` for complete bot features
- See `README.md` for setup instructions
- See `QUICKSTART.md` for quick start guide

---

## 🚀 Future Enhancements

### Planned Features
- [ ] Timeline visualization (matplotlib)
- [ ] User network graphs
- [ ] Automated PDF reports
- [ ] Statistical analysis dashboard
- [ ] Pattern detection alerts
- [ ] Multi-language support
- [ ] Custom ML model training

---

**Last Updated**: 2024
**Version**: 2.0 (Academic Research Edition)
