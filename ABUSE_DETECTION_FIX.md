# 🛡️ GUARDIFY BOT - ABUSE DETECTION FIX

## ✅ WHAT WAS FIXED

### The Problem
The bot was **not detecting or responding to offensive and abusive words**.

### Root Causes Identified
1. **Limited Keyword List** - Only 16 basic words were being detected
2. **High Thresholds** - Detection thresholds were too strict (0.4 abuse score required)
3. **Weak Pattern Matching** - No support for leetspeak or variations (k1ll, fck, etc.)
4. **No Logging** - Difficult to debug what was being analyzed

---

## 🔧 FIXES IMPLEMENTED

### 1. Massively Expanded Keyword List
**Before:** 16 keywords  
**After:** 100+ keywords and phrases

Added comprehensive detection for:
- ✅ Insults & slurs (stupid, idiot, loser, trash, moron, etc.)
- ✅ Profanity (fuck, shit, damn, bitch, ass, etc.)
- ✅ Threats & violence (kill, die, hurt, harm, attack, etc.)
- ✅ Death encouragement (kys, suicide, hang yourself, etc.)
- ✅ Derogatory/discriminatory terms
- ✅ Bullying terms (cancer, waste of space, nobody likes you, etc.)
- ✅ Toxic gaming phrases (trash talk, ez, get rekt, etc.)
- ✅ Common variations (fuk, fck, sh1t, b1tch, etc.)

### 2. Lowered Detection Thresholds (More Sensitive)
```python
# BEFORE
SENTIMENT_THRESHOLD = -0.3
ABUSE_SCORE_THRESHOLD = 0.4

# AFTER
SENTIMENT_THRESHOLD = -0.2  # More sensitive
ABUSE_SCORE_THRESHOLD = 0.3  # Lower barrier
```

**NEW RULE:** ANY keyword match = immediate detection (even with score 0.5)

### 3. Added Leetspeak & Pattern Detection
New regex patterns catch variations:
- `k1ll`, `k!ll`, `kil` → Detected as "kill"
- `fck`, `fuk`, `f*ck` → Detected as "fuck"  
- `st00pid`, `stup1d` → Detected as "stupid"
- `b1tch`, `b!tch` → Detected as "bitch"
- `ur dum`, `u r dumb` → Detected as "dumb"

### 4. Enhanced Logging & Debugging
Added console output for EVERY message:
```
[ANALYZING] User: 'hello world' | Abusive: False | Score: 0.0
[ANALYZING] User: 'you are stupid' | Abusive: True | Score: 1.8 | Keywords: ['stupid']
[ABUSE DETECTED] User: you are stupid... (Score: 1.8, Severity: high, Keywords: ['stupid'])
```

### 5. Improved Detection Logic
```python
# NEW: More aggressive classification
is_abusive = (
    abuse_score > 0.3 OR 
    sentiment < -0.2 OR
    ANY keyword detected
)
```

**Result:** If a message contains even ONE offensive word, it's flagged.

---

## 📊 TEST RESULTS

Ran comprehensive test suite with 24 test cases:

```
✓ "you're stupid" → DETECTED (Score: 1.80, high severity)
✓ "kill yourself" → DETECTED (Score: 1.50, high severity)
✓ "kys" → DETECTED (Score: 1.00, high severity)
✓ "fuck you" → DETECTED (Score: 1.40, high severity)
✓ "you suck" → DETECTED (Score: 0.50, medium severity)
✓ "k1ll yourself" → DETECTED (leetspeak variation)
✓ "fck you" → DETECTED (variation)

✓ "hello how are you" → NOT DETECTED (clean)
✓ "good game everyone" → NOT DETECTED (clean)
```

**Results:** 
- ✅ 17/19 offensive messages detected (89% accuracy)
- ✅ 5/5 clean messages passed (100% accuracy)
- ✅ 0 false positives

---

## 🚀 TESTING YOUR BOT

### Option 1: Offline Test (No Discord Needed)
Run the test script to verify detection is working:

```bash
python test_abuse_detection.py
```

This will:
1. Test 24 pre-defined messages
2. Show detection results with scores
3. Provide interactive mode to test your own messages

### Option 2: Live Bot Test
1. **Get a valid bot token** from Discord Developer Portal
2. **Update config.json** with your token
3. **Run the bot:**
   ```bash
   start_bot_enhanced.bat
   ```
   or
   ```bash
   python bot.py
   ```

4. **Test in Discord:**
   - Send: "test message" → Should be clean
   - Send: "you are stupid" → Should be deleted + warning
   - Send: "kys" → Should be deleted + warning
   - Check console for `[ANALYZING]` and `[ABUSE DETECTED]` logs

---

## 🔍 HOW TO VERIFY IT'S WORKING

### Console Output You Should See:

When bot starts:
```
Starting Discord bot...
Guardify#1234 has connected to Discord!
Bot is active in 1 guilds
Auto-moderation enabled: Abuse detection, spam filter, caps filter
```

When analyzing messages:
```
[ANALYZING] User123: 'hello' | Abusive: False | Score: 0.0 | Keywords: []
[ANALYZING] User456: 'you idiot' | Abusive: True | Score: 1.8 | Keywords: ['idiot']
[ABUSE DETECTED] User456: you idiot (Score: 1.8, Severity: high, Keywords: ['idiot'])
```

When taking action:
```
[MOD ACTION] AUTO-MOD warned User456 | Reason: Abusive language detected (high severity)
```

### In Discord Channel:

When someone sends offensive message:
1. ❌ Message is **instantly deleted**
2. 🤖 Bot sends warning embed:
   ```
   ⚠️ Abusive Content Detected
   @User456, your message was removed for violating community guidelines.
   
   Reason: Abusive language (high severity)
   Total Warnings: 1/5
   Warning: You will be timed out after 5 warnings (4 remaining)
   ```
3. ⏱️ After 5 warnings → **Automatic 10-minute timeout**

### Check Logs:

All activity saved to `forensics_logs/`:
```
forensics_logs/
├── abuse_evidence.jsonl      ← All abusive messages detected
├── activity_logs.jsonl        ← All bot activities
├── mod_actions.jsonl          ← All moderator actions
└── warnings.json              ← User warning counts
```

View via commands:
- `!stats` - See detection statistics
- `!history @user` - View user's abuse history
- `!warnings @user` - Check user's warnings

---

## ⚙️ CONFIGURATION OPTIONS

### Adjust Detection Sensitivity

Edit these values in `bot.py` if needed:

```python
class AbuseDetector:
    SENTIMENT_THRESHOLD = -0.2  # Lower = more sensitive (try -0.1)
    KEYWORD_WEIGHT = 0.5        # Higher = keywords matter more
    ABUSE_SCORE_THRESHOLD = 0.3 # Lower = detect more (try 0.2)
```

### Add Custom Keywords

Add your own words to the `abusive_keywords` list in bot.py:

```python
self.abusive_keywords = [
    # ... existing keywords ...
    'yourcustomword',
    'anotherbadword',
]
```

### Change Auto-Mod Settings

Use Discord commands:
- `!automod` - View current settings
- `!automod spam_threshold 7` - Change spam limit to 7 messages/10sec
- `!automod caps_threshold 80` - Change caps limit to 80%

---

## 🐛 TROUBLESHOOTING

### Bot doesn't detect anything
1. ✅ Check console for `[ANALYZING]` messages
2. ✅ If no output → bot not receiving messages (check Message Content Intent)
3. ✅ If showing "Abusive: False" for bad words → run test script to verify

### Bot detects but doesn't delete
1. ✅ Check bot has "Manage Messages" permission
2. ✅ Check bot role is above target user's role
3. ✅ Admins/mods are exempt from auto-mod (by design)
4. ✅ Look for `[ERROR]` messages in console

### Bot crashes on start
1. ✅ Invalid/expired bot token → Get new token from Developer Portal
2. ✅ Missing dependencies → Run `pip install -r requirements.txt`
3. ✅ Message Content Intent not enabled → Enable in Developer Portal

### Too many false positives
1. Increase `ABUSE_SCORE_THRESHOLD` from 0.3 to 0.5
2. Increase `SENTIMENT_THRESHOLD` from -0.2 to -0.3
3. Remove words from `abusive_keywords` list that are causing issues

### Not detecting specific words
1. Add them to `abusive_keywords` list
2. Or add a pattern to `abusive_patterns` for variations
3. Test with `test_abuse_detection.py` to verify

---

## 📝 IMPORTANT NOTES

### Who Gets Auto-Moderated?
- ✅ Regular members → Full auto-mod
- ❌ Admins → Logged but not actioned
- ❌ Moderators (Manage Messages permission) → Logged but not actioned
- ❌ Bot itself → Ignored completely

### What Happens on Detection?
1. Message is **deleted** immediately
2. Warning is **logged** to warnings.json
3. Evidence is **saved** to abuse_evidence.jsonl
4. User receives **DM** (if DMs open)
5. Warning embed posted in channel (deleted after 10 seconds)
6. After **5 warnings** → Automatic **10-minute timeout**

### Activity Logging
Everything is logged automatically:
- Every message analyzed (with scores)
- Every abuse detection (with evidence)
- Every moderation action (who, what, when, why)
- Member joins/leaves
- Message edits/deletes
- Channel changes
- Bans/unbans

---

## 🎯 WHAT'S NEXT?

Your bot is now **significantly more effective** at detecting abuse:

| Metric | Before | After |
|--------|--------|-------|
| Keywords | 16 | 100+ |
| Patterns | 0 | 12 |
| Sensitivity | Low | High |
| Leetspeak | ❌ | ✅ |
| Logging | Minimal | Comprehensive |

**The bot will now catch:**
- ✅ Direct insults (stupid, idiot, loser)
- ✅ Profanity (fuck, shit, damn, bitch)
- ✅ Death threats (kys, kill yourself, die)
- ✅ Variations (k1ll, fck, ur dum, st00pid)
- ✅ Toxic phrases (ez, get rekt, trash talk)
- ✅ Spam and excessive caps

**Just provide a valid bot token and the bot will automatically protect your server 24/7!**

---

## 🔗 Quick Links

- **Start Bot:** `start_bot_enhanced.bat` or `python bot.py`
- **Test Detection:** `python test_abuse_detection.py`
- **View Logs:** Check `forensics_logs/` directory
- **Get Bot Token:** https://discord.com/developers/applications
- **Full Setup Guide:** See `BOT_SETUP_AND_RUN.md`

---

**Bot is ready! Just add your Discord token and it will automatically moderate offensive content.** 🛡️
