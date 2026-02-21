# 🧪 Testing Guide - Enhanced Warning & Mute System

## Pre-Testing Checklist

- [ ] New files installed: `content_detector.py`, `warning_system.py`
- [ ] `bot.py` updated with new commands
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Bot restarted
- [ ] Bot has permissions: Manage Messages, Moderate Members, Manage Roles
- [ ] Test server ready with test users

---

## 1. Content Detection Testing

### Test 1.1: English Profanity
```bash
User: !scan fuck this shit
Expected Output:
- is_offensive: TRUE
- category: PROFANITY
- severity: MEDIUM-HIGH
- detected_content: ['fuck', 'shit']
```

### Test 1.2: English Hate Speech
```bash
User: !scan I hate all [group] they are animals
Expected Output:
- is_offensive: TRUE
- category: HATE_SPEECH
- severity: HIGH
- detected_content: ['hate', 'animals']
```

### Test 1.3: English Threats
```bash
User: !scan I will kill you
Expected Output:
- is_offensive: TRUE
- category: THREAT_VIOLENCE
- severity: CRITICAL
- detected_content: ['kill']
```

### Test 1.4: Hindi Profanity (Gaali)
```bash
User: !scan तुम बहुत गंदे हो kamina harami
Expected Output:
- is_offensive: TRUE
- category: PROFANITY or HARASSMENT
- severity: MEDIUM-HIGH
- language: HINDI or MIXED
- detected_content: ['kamina', 'harami']
```

### Test 1.5: Hindi Threats
```bash
User: !scan तुम्हें मार दूंगा mar dunga
Expected Output:
- is_offensive: TRUE
- category: THREAT_VIOLENCE
- severity: CRITICAL
- language: HINDI
- detected_content: ['mar dunga']
```

### Test 1.6: False Positive Check
```bash
User: !scan This is great
Expected Output:
- is_offensive: FALSE
- category: CLEAN
- detected_content: []
```

### Test 1.7: Leetspeak Detection
```bash
User: !scan f*** sh1t h8 kkill
Expected Output:
- is_offensive: TRUE (should catch variations)
- category: PROFANITY
- detected_content: variations detected
```

---

## 2. Automatic Warning System Testing

### Test 2.1: First Offensive Message
```
1. User sends: "This is fucking stupid"
2. Expected:
   - Message deleted ✓
   - Warning notification sent ✓
   - DM sent to user ✓
   - Warning count: 1/5 ✓
3. Verify: !warnings @testuser
   Expected: Shows 1 warning
```

### Test 2.2: Multiple Warnings (2-4)
```
1. Repeat offensive message 3 more times
2. Expected:
   - Each message deleted ✓
   - Warnings accumulate 2/5, 3/5, 4/5 ✓
   - Notifications show warning count ✓
3. Verify: !warnings @testuser
   Expected: Shows 4 warnings
```

### Test 2.3: Auto-Mute at 5 Warnings
```
1. User sends 5th offensive message
2. Expected:
   - Message deleted ✓
   - Added 5th warning ✓
   - User gets timeout (muted) ✓
   - Mute role assigned ✓
   - Notification shows "AUTO-MUTE" ✓
   - DM shows mute status ✓
3. Verify: 
   - !warnings @testuser → Shows 5 warnings + mute status
   - Discord shows user as timed out
   - User has "Muted" role
```

### Test 2.4: Cannot Talk While Muted
```
1. Muted user tries to speak
2. Expected:
   - "You are timed out and cannot speak" error
   - Message not sent ✓
3. Verify in Discord UI
```

---

## 3. Automatic Unmute Testing

### Test 3.1: Auto-Unmute After 10 Minutes
```
1. User is muted (see Test 2.3)
2. Wait 10 minutes (or check logs)
3. Expected:
   - Timeout removed ✓
   - Mute role removed ✓
   - User can speak again ✓
   - Mute status updated in database ✓
4. Verify:
   - !warnings @testuser → Shows mute as "inactive"
   - User can send messages
```

### Test 3.2: Manual Unmute
```
1. User is muted
2. Admin runs: !unmute @testuser
3. Expected:
   - Timeout removed immediately ✓
   - Mute role removed ✓
   - User can speak again ✓
4. Verify: User can send messages
```

---

## 4. Mute Role Testing

### Test 4.1: Auto-Create Mute Role
```
1. First mute (if role doesn't exist)
2. Expected:
   - "Muted" role created ✓
   - Permissions set on role ✓
   - Role assigned to user ✓
3. Verify in Discord server roles
```

### Test 4.2: Custom Mute Role
```
1. Create custom role: "No Talk"
2. Admin runs: !setmuterole @NoTalk
3. Verify:
   - Command confirms ✓
   - Next mute uses custom role ✓
   - Role visible in !setmuterole settings
```

### Test 4.3: Channel Restrictions
```
1. Muted user with role assigned
2. Expected:
   - Cannot send messages in text channels ✓
   - Cannot speak in voice channels ✓
3. Verify:
   - Try sending message: "You do not have permission"
   - Try joining voice: Muted or permission denied
```

---

## 5. Data Persistence Testing

### Test 5.1: Warnings Survive Bot Restart
```
1. User has 3 warnings
2. Restart bot: python bot.py
3. Run: !warnings @testuser
4. Expected: Still shows 3 warnings ✓
5. Verify: forensics_logs/user_warnings.json contains data
```

### Test 5.2: Mute Status Survives Restart
```
1. User is muted with time remaining
2. Restart bot
3. Expected:
   - Mute still active ✓
   - User still cannot speak ✓
   - Auto-unmute still scheduled ✓
```

### Test 5.3: JSON File Format
```
1. Check forensics_logs/user_warnings.json
2. Expected format:
{
  "guild_id:user_id": {
    "user_id": "...",
    "guild_id": "...",
    "warnings": [
      {
        "id": 1,
        "reason": "...",
        "severity": "...",
        "timestamp": "..."
      }
    ]
  }
}
```

---

## 6. Command Testing

### Test 6.1: !warnings Command
```
!warnings @user
Expected: Shows all warnings + mute status
```

### Test 6.2: !warn Command (Manual)
```
!warn @user breaking rule 5
Expected: Warning added, count increases
```

### Test 6.3: !clearwarnings Command
```
!clearwarnings @user
Expected: All warnings cleared
Verify: !warnings @user shows 0 warnings
```

### Test 6.4: !forcemute Command
```
!forcemute @user 15 spamming
Expected: 
- User muted for 15 minutes
- Mute role assigned
- Auto-unmute scheduled
```

### Test 6.5: !unmute Command
```
!unmute @user
Expected:
- User unmuted immediately
- Mute role removed
- Can speak again
```

### Test 6.6: !warningstats Command
```
!warningstats
Expected: Shows statistics
- Total users warned
- Total warnings
- Active mutes
- Breakdown by severity
```

### Test 6.7: !setmuterole Command
```
!setmuterole @CustomRole
Expected: Role set as mute role for guild
Next mute will use this role
```

---

## 7. Permission Testing

### Test 7.1: Insufficient Permissions
```
Regular user runs: !clearwarnings @user
Expected: ❌ "You don't have permission"
```

### Test 7.2: Moderator Permissions
```
User with "Manage Messages" runs: !warn @user
Expected: ✅ Warning added
```

### Test 7.3: Administrator Permissions
```
User with "Administrator" runs: !clearwarnings @user
Expected: ✅ Warnings cleared
```

---

## 8. Multi-Guild Testing

### Test 8.1: Separate Warning Counts
```
1. User has 3 warnings in Guild1
2. Send 1 offensive message in Guild2
3. Expected:
   - Guild1: Still 3 warnings
   - Guild2: 1 warning
4. Verify: Check both servers
```

### Test 8.2: Separate Mute Roles
```
1. Guild1 uses "Muted" role
2. Guild2 uses "No Talk" role
3. Mute user in Guild1
4. Expected: "Muted" role assigned in Guild1
5. Mute user in Guild2
6. Expected: "No Talk" role assigned in Guild2
```

---

## 9. Edge Cases Testing

### Test 9.1: Rapid Messages
```
User sends 5 offensive messages rapidly
Expected: All deleted, warnings added (not skipped)
```

### Test 9.2: Mixed Languages
```
!scan fuck this is gandi baat
Expected: Detects both English and Hindi content
```

### Test 9.3: Very Long Message
```
Send 1000+ character offensive message
Expected: Processed correctly, no errors
```

### Test 9.4: Special Characters/Emojis
```
!scan f**k $h1†
Expected: Detects with special char handling
```

### Test 9.5: Already Muted User
```
Muted user sends offensive message
Expected: Tries to delete (fails silently) or handles gracefully
```

---

## 10. Logging & Debugging

### Check Log Files
```
forensics_logs/
├── user_warnings.json      ✓ Check for user data
├── user_mutes.json         ✓ Check for mute records
├── mute_roles.json         ✓ Check role assignments
├── abuse_evidence.jsonl    ✓ Check detected content
└── activity_logs.jsonl     ✓ Check system logs
```

### Console Output
```
[MESSAGE SCAN] Check for analysis output
[OFFENSIVE CONTENT DETECTED] Should show category
[WARNING ADDED] Should show warning count
[AUTO-MUTE] Should show when muting
[AUTO-UNMUTE] Should show when unmuting
```

---

## 11. Performance Testing

### Test 11.1: Message Processing Speed
```
Send message
Expected processing time: <100ms
Verify: No noticeable lag
```

### Test 11.2: Memory Usage
```
Run bot for 1 hour with normal traffic
Expected memory: Stable, no growth
```

### Test 11.3: Concurrent Users
```
Multiple users sending messages simultaneously
Expected: All processed correctly, no order issues
```

---

## 12. Recovery Testing

### Test 12.1: Bot Crash & Restart
```
1. Force stop bot (Ctrl+C)
2. Restart bot
3. Expected:
   - All data intact ✓
   - Active mutes still active ✓
   - No errors in console ✓
```

### Test 12.2: Corrupted JSON
```
1. Manually edit user_warnings.json to invalid JSON
2. Restart bot
3. Expected: Bot handles gracefully, logs error
```

---

## Testing Checklist

- [ ] All 12 test categories executed
- [ ] No critical errors
- [ ] All expected outputs matched
- [ ] Data persists correctly
- [ ] Mute system works end-to-end
- [ ] Commands are intuitive
- [ ] Notifications are clear
- [ ] Permissions enforced
- [ ] Multi-guild isolation works
- [ ] Performance acceptable

---

## Known Issues & Workarounds

### Issue 1: Mute role not created
**Cause:** Bot missing "Manage Roles" permission  
**Workaround:** Grant permission and restart

### Issue 2: Warning count seems wrong
**Cause:** Multiple guilds with same user  
**Verify:** Check `user_warnings.json` for guild_id:user_id format

### Issue 3: Auto-unmute not working
**Cause:** Bot went offline before task executed  
**Workaround:** Manually unmute with `!unmute @user`

---

## Success Criteria

All tests pass if:
- ✅ Content detected correctly
- ✅ Warnings issued automatically
- ✅ Messages deleted
- ✅ Muted after 5 warnings
- ✅ Role assigned
- ✅ Auto-unmuted after 10 minutes
- ✅ Data persists
- ✅ Commands work
- ✅ Permissions enforced
- ✅ No errors in logs

---

**Testing Date:** _______________  
**Tester:** _______________  
**Status:** PASS / FAIL  
**Notes:** _______________
