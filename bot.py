"""
Respect Ranger Discord Bot
AI-enabled bot for detecting and logging abusive content in Discord messages.
"""

import discord
from discord.ext import commands
import json
import os
from datetime import datetime, timedelta
from textblob import TextBlob
import re
from typing import Dict, List, Optional
from threading import Thread
from flask import Flask


class AbuseDetector:
    """Detects abusive content using sentiment analysis and keyword matching."""
    
    # Configurable thresholds - MADE MORE SENSITIVE
    SENTIMENT_THRESHOLD = -0.2  # Negative sentiment threshold (lowered for sensitivity)
    KEYWORD_WEIGHT = 0.5
    ABUSE_SCORE_THRESHOLD = 0.3  # Minimum score to classify as abusive (lowered)
    
    def __init__(self):
        # Comprehensive list of abusive keywords/phrases
        self.abusive_keywords = [
            # Insults & Slurs
            'hate', 'kill', 'stupid', 'idiot', 'loser', 'trash', 'garbage',
            'worthless', 'pathetic', 'disgusting', 'die', 'kys', 'kms',
            'retard', 'retarded', 'moron', 'dumb', 'dumbass', 'dummy',
            'ugly', 'fat', 'fatty', 'nazi', 'pig', 'scum', 'filth',
            'shit', 'crap', 'damn', 'hell', 'bastard', 'bitch',
            'ass', 'asshole', 'fuck', 'fucking', 'fucked', 'fucker',
            'motherfucker', 'wtf', 'stfu', 'shut up',
            
            # Threats & Violence
            'hurt', 'harm', 'attack', 'beat', 'punch', 'kick',
            'stab', 'shoot', 'murder', 'suicide', 'hang yourself',
            'jump off', 'kll', 'k1ll', 'd1e', 'unalive',
            
            # Derogatory Terms
            'n***a', 'n***er', 'f****t', 'f*g', 'gay' 'queer',
            'tranny', 'dyke', 'chink', 'spic', 'wetback',
            'cracker', 'honky', 'gook', 'savage', 'ape',
            
            # Bullying Terms
            'cancer', 'tumor', 'disease', 'waste of space',
            'nobody likes you', 'everyone hates you', 'useless',
            'failure', 'embarrassment', 'joke', 'clown',
            'braindead', 'brainless', 'no brain',
            
            # Common Variations & Leetspeak
            'fuk', 'fck', 'sh1t', 'b1tch', 'a$$', 'a55',
            'fvck', 'phuck', 'shtty', 'sucks', 'suck',
            'noob', 'n00b', 'scrub', 'bot', 'trash player',
            
            # Toxic Phrases
            'go die', 'kill yourself', 'end yourself', 'rope yourself',
            'get cancer', 'get aids', 'neck yourself', 'off yourself',
            'delete yourself', 'uninstall life', 'your mom', 'yo mama',
            'ez', 'get rekt', 'trash talk', 'git gud', 'cope',
            'seethe', 'mald', 'ratio', 'cry about it', 'cope harder',
            
            # Additional Offensive Terms
            'simp', 'incel', 'neckbeard', 'virgin', 'whore',
            'slut', 'thot', 'hoe', 'prostitute', 'hooker',
            'cunt', 'twat', 'prick', 'dick', 'cock',
            'balls', 'deez nuts', 'ligma', 'bofa',
            
            # Discriminatory
            'racist', 'sexist', 'homophobic', 'transphobic',
            'bigot', 'supremacist', 'fascist', 'terrorist'
        ]
        
        # Patterns for detecting leetspeak and variations
        self.abusive_patterns = [
            (r'k+[i1!]l+', 'kill variations'),
            (r'f+[u*]+c+k+', 'fuck variations'),
            (r's+h+[i1!]+t+', 'shit variations'),
            (r'b+[i1!]+t+c+h+', 'bitch variations'),
            (r'n+[i1!]+g+', 'n-word variations'),
            (r'f+[a@]+g+', 'slur variations'),
            (r'st[u*0]+p[i1!]+d+', 'stupid variations'),
            (r'd[u*0]+m+b*', 'dumb variations'),
            (r'[i1!]+d+[i1!]+[o0]+t+', 'idiot variations'),
            (r'go+ d+[i1!]+e+', 'death threats'),
            (r'kys+', 'suicide encouragement'),
            (r'u+r+ d+[u0]+m+', 'ur dumb variations'),
        ]
        
    def analyze_message(self, content: str) -> Dict:
        """
        Analyze message for abusive content.
        
        Returns:
            Dict containing abuse score, sentiment, detected keywords, and classification
        """
        content_lower = content.lower()
        
        # Sentiment analysis using TextBlob
        blob = TextBlob(content)
        sentiment = blob.sentiment.polarity
        
        # Keyword detection with word boundary matching
        detected_keywords = []
        for keyword in self.abusive_keywords:
            # Use word boundaries to match whole words only
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, content_lower):
                detected_keywords.append(keyword)
        
        # Pattern detection for leetspeak and variations
        detected_patterns = []
        for pattern, description in self.abusive_patterns:
            if re.search(pattern, content_lower, re.IGNORECASE):
                detected_patterns.append(description)
                detected_keywords.append(description)  # Count patterns as keywords too
        
        # Calculate abuse score
        keyword_score = len(detected_keywords) * self.KEYWORD_WEIGHT
        sentiment_score = abs(min(sentiment, 0))
        
        abuse_score = keyword_score + sentiment_score
        
        # Classification - More aggressive detection
        is_abusive = (
            abuse_score > self.ABUSE_SCORE_THRESHOLD or 
            sentiment < self.SENTIMENT_THRESHOLD or
            len(detected_keywords) > 0  # ANY keyword match = abusive
        )
        
        severity = "low"
        if abuse_score > 0.8 or len(detected_keywords) >= 3:
            severity = "high"
        elif abuse_score > 0.4 or len(detected_keywords) >= 2:
            severity = "medium"
        
        return {
            "is_abusive": is_abusive,
            "abuse_score": round(abuse_score, 3),
            "sentiment": round(sentiment, 3),
            "detected_keywords": detected_keywords[:5],  # Limit display
            "detected_patterns": detected_patterns,
            "severity": severity,
            "timestamp": datetime.utcnow().isoformat()
        }


class ForensicsLogger:
    """Logs evidence of abusive messages for digital forensics."""
    
    def __init__(self, log_dir: str = "forensics_logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, "abuse_evidence.jsonl")
        self.activity_log_file = os.path.join(log_dir, "activity_logs.jsonl")
        self.mod_actions_file = os.path.join(log_dir, "mod_actions.jsonl")
        
    def log_evidence(self, message: discord.Message, analysis: Dict) -> None:
        """
        Log evidence of abusive message.
        
        Args:
            message: Discord message object
            analysis: Analysis results from AbuseDetector
        """
        evidence = {
            "message_id": str(message.id),
            "author_id": str(message.author.id),
            "author_name": str(message.author),
            "channel_id": str(message.channel.id),
            "channel_name": str(message.channel) if hasattr(message.channel, 'name') else "DM",
            "guild_id": str(message.guild.id) if message.guild else None,
            "guild_name": str(message.guild.name) if message.guild else None,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
            "analysis": analysis,
            "logged_at": datetime.utcnow().isoformat()
        }
        
        # Append to JSONL file (one JSON object per line)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evidence, ensure_ascii=False) + '\n')
    
    def log_activity(self, activity_type: str, details: Dict) -> None:
        """
        Log general bot activities.
        
        Args:
            activity_type: Type of activity (e.g., 'message_delete', 'member_join', 'channel_update')
            details: Dictionary containing activity details
        """
        log_entry = {
            "activity_type": activity_type,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        with open(self.activity_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def log_mod_action(self, action: str, moderator: discord.User, target: discord.User, 
                       reason: str, guild_id: str) -> None:
        """
        Log moderator actions.
        
        Args:
            action: Type of moderation action
            moderator: User who performed the action
            target: User affected by the action
            reason: Reason for the action
            guild_id: Server ID where action occurred
        """
        log_entry = {
            "action": action,
            "moderator_id": str(moderator.id),
            "moderator_name": str(moderator),
            "target_id": str(target.id),
            "target_name": str(target),
            "reason": reason,
            "guild_id": guild_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        with open(self.mod_actions_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def get_user_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Retrieve abuse history for a specific user.
        
        Args:
            user_id: Discord user ID
            limit: Maximum number of records to return
            
        Returns:
            List of evidence records for the user
        """
        if not os.path.exists(self.log_file):
            return []
        
        records = []
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    record = json.loads(line)
                    if record.get('author_id') == user_id:
                        records.append(record)
                        if len(records) >= limit:
                            break
                except json.JSONDecodeError:
                    continue
        
        return records
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about logged abuse cases.
        
        Returns:
            Dictionary with statistics
        """
        if not os.path.exists(self.log_file):
            return {"total_cases": 0}
        
        stats = {
            "total_cases": 0,
            "severity_breakdown": {"low": 0, "medium": 0, "high": 0},
            "unique_users": set(),
            "unique_guilds": set()
        }
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    record = json.loads(line)
                    stats["total_cases"] += 1
                    
                    severity = record.get("analysis", {}).get("severity", "low")
                    stats["severity_breakdown"][severity] = stats["severity_breakdown"].get(severity, 0) + 1
                    
                    stats["unique_users"].add(record.get("author_id"))
                    if record.get("guild_id"):
                        stats["unique_guilds"].add(record.get("guild_id"))
                except json.JSONDecodeError:
                    continue
        
        stats["unique_users"] = len(stats["unique_users"])
        stats["unique_guilds"] = len(stats["unique_guilds"])
        
        return stats


class RespectRanger(commands.Bot):
    """Main bot class for Guardify - Sapphire-like Discord Bot."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.abuse_detector = AbuseDetector()
        self.forensics_logger = ForensicsLogger()
        
        # Auto-mod settings
        self.spam_threshold = 5  # messages per 10 seconds
        self.caps_threshold = 0.7  # 70% caps in message
        self.user_messages = {}  # Track message timestamps for spam detection
        
        # Server configurations (saved per guild)
        self.guild_configs = self.load_guild_configs()
        
        # Anti-raid protection
        self.join_tracking = {}  # Track recent joins per guild
        self.raid_mode = {}  # Track if guild is in raid mode
        
        # Verification system
        self.pending_verifications = {}  # Users awaiting verification
    
    def load_guild_configs(self) -> Dict:
        """Load guild-specific configurations."""
        config_file = 'guild_configs.json'
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_guild_configs(self):
        """Save guild configurations."""
        with open('guild_configs.json', 'w') as f:
            json.dump(self.guild_configs, f, indent=2)
    
    def get_guild_config(self, guild_id: str) -> Dict:
        """Get config for specific guild with defaults."""
        if guild_id not in self.guild_configs:
            self.guild_configs[guild_id] = {
                'welcome_channel': None,
                'welcome_message': 'Welcome {user} to {server}! 🎉',
                'goodbye_message': 'Goodbye {user}! We\'ll miss you. 👋',
                'log_channel': None,
                'mod_log_channel': None,
                'verification_enabled': False,
                'verification_role': None,
                'verified_role': None,
                'mute_role': None,
                'autorole': None,
                'anti_raid': True,
                'raid_threshold': 5,  # joins per 10 seconds
            }
            self.save_guild_configs()
        return self.guild_configs[guild_id]
    
    async def on_ready(self):
        """Called when the bot is ready."""
        print('=' * 60)
        print(f'🛡️  {self.user} is now ONLINE!')
        print('=' * 60)
        print(f'📊 Active in {len(self.guilds)} servers')
        print(f'👥 Protecting {sum(g.member_count for g in self.guilds)} members')
        print(f'🤖 Auto-moderation: ENABLED')
        print(f'🔒 Anti-raid protection: ENABLED')
        print(f'📝 Activity logging: ENABLED')
        print('=' * 60)
        
        # Set bot activity status
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(self.guilds)} servers | !help_guardify"
        )
        await self.change_presence(activity=activity, status=discord.Status.online)
        
        # Log bot startup
        self.forensics_logger.log_activity("bot_startup", {
            "bot_name": str(self.user),
            "guild_count": len(self.guilds),
            "guilds": [{"id": str(g.id), "name": g.name} for g in self.guilds]
        })
    
    async def on_member_join(self, member: discord.Member):
        """Handle member joins with welcome, auto-role, verification, and anti-raid."""
        guild_id = str(member.guild.id)
        config = self.get_guild_config(guild_id)
        
        # Log join
        self.forensics_logger.log_activity("member_join", {
            "user_id": str(member.id),
            "user_name": str(member),
            "guild_id": guild_id,
            "guild_name": member.guild.name,
            "account_created": member.created_at.isoformat(),
            "account_age_days": (datetime.utcnow() - member.created_at).days
        })
        print(f"[MEMBER JOIN] {member} joined {member.guild.name}")
        
        # Anti-raid detection
        if config.get('anti_raid', True):
            now = datetime.utcnow()
            if guild_id not in self.join_tracking:
                self.join_tracking[guild_id] = []
            
            # Clean old joins (older than 10 seconds)
            self.join_tracking[guild_id] = [
                join_time for join_time in self.join_tracking[guild_id]
                if (now - join_time).total_seconds() < 10
            ]
            
            self.join_tracking[guild_id].append(now)
            
            # Check for raid (multiple joins in short time)
            raid_threshold = config.get('raid_threshold', 5)
            if len(self.join_tracking[guild_id]) > raid_threshold:
                if not self.raid_mode.get(guild_id, False):
                    self.raid_mode[guild_id] = True
                    print(f"[RAID DETECTED] {member.guild.name} - {len(self.join_tracking[guild_id])} joins in 10s")
                    
                    # Alert in log channel
                    if config.get('log_channel'):
                        try:
                            log_channel = member.guild.get_channel(int(config['log_channel']))
                            if log_channel:
                                embed = discord.Embed(
                                    title="🚨 RAID DETECTED",
                                    description=f"Unusual join activity detected: {len(self.join_tracking[guild_id])} members joined in 10 seconds.",
                                    color=discord.Color.red()
                                )
                                embed.add_field(name="Recommendation", value="Consider enabling verification or locking the server.", inline=False)
                                await log_channel.send(embed=embed)
                        except:
                            pass
        
        # Check account age (new accounts might be suspicious)
        account_age = (datetime.utcnow() - member.created_at).days
        if account_age < 7 and config.get('log_channel'):
            try:
                log_channel = member.guild.get_channel(int(config['log_channel']))
                if log_channel:
                    embed = discord.Embed(
                        title="⚠️ New Account Alert",
                        description=f"{member.mention} joined with a new account.",
                        color=discord.Color.orange()
                    )
                    embed.add_field(name="Account Age", value=f"{account_age} days", inline=True)
                    embed.add_field(name="Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
                    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                    await log_channel.send(embed=embed)
            except:
                pass
        
        # Auto-role assignment
        if config.get('autorole'):
            try:
                role = member.guild.get_role(int(config['autorole']))
                if role:
                    await member.add_roles(role, reason="Auto-role on join")
            except:
                pass
        
        # Verification system
        if config.get('verification_enabled') and config.get('verification_role'):
            try:
                verify_role = member.guild.get_role(int(config['verification_role']))
                if verify_role:
                    await member.add_roles(verify_role, reason="Pending verification")
                    self.pending_verifications[str(member.id)] = {
                        'guild_id': guild_id,
                        'joined_at': datetime.utcnow().isoformat()
                    }
                    
                    # DM verification instructions
                    try:
                        embed = discord.Embed(
                            title=f"Welcome to {member.guild.name}! 🛡️",
                            description="Please verify yourself to access the server.",
                            color=discord.Color.blue()
                        )
                        embed.add_field(name="How to Verify", value="Type `!verify` in the verification channel or DM me.", inline=False)
                        await member.send(embed=embed)
                    except:
                        pass
            except Exception as e:
                print(f"[ERROR] Verification failed: {e}")
        
        # Send welcome message
        if config.get('welcome_channel'):
            try:
                channel = member.guild.get_channel(int(config['welcome_channel']))
                if channel:
                    message = config.get('welcome_message', 'Welcome {user} to {server}! 🎉')
                    message = message.replace('{user}', member.mention)
                    message = message.replace('{server}', member.guild.name)
                    message = message.replace('{count}', str(member.guild.member_count))
                    
                    embed = discord.Embed(
                        description=message,
                        color=discord.Color.green()
                    )
                    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                    embed.set_footer(text=f"Member #{member.guild.member_count}")
                    await channel.send(embed=embed)
            except Exception as e:
                print(f"[ERROR] Welcome message failed: {e}")
    
    async def on_member_remove(self, member: discord.Member):
        """Handle member leave with goodbye message and logging."""
        guild_id = str(member.guild.id)
        config = self.get_guild_config(guild_id)
        
        # Log leave
        self.forensics_logger.log_activity("member_leave", {
            "user_id": str(member.id),
            "user_name": str(member),
            "guild_id": guild_id,
            "guild_name": member.guild.name,
            "roles": [str(role.name) for role in member.roles if role.name != "@everyone"]
        })
        print(f"[MEMBER LEAVE] {member} left {member.guild.name}")
        
        # Send goodbye message
        if config.get('welcome_channel'):
            try:
                channel = member.guild.get_channel(int(config['welcome_channel']))
                if channel:
                    message = config.get('goodbye_message', 'Goodbye {user}! We\'ll miss you. 👋')
                    message = message.replace('{user}', str(member))
                    message = message.replace('{server}', member.guild.name)
                    
                    embed = discord.Embed(
                        description=message,
                        color=discord.Color.red()
                    )
                    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                    await channel.send(embed=embed)
            except Exception as e:
                print(f"[ERROR] Goodbye message failed: {e}")
        
        # Remove from verification tracking if pending
        if str(member.id) in self.pending_verifications:
            del self.pending_verifications[str(member.id)]
    
    async def on_message_delete(self, message: discord.Message):
        """Log when a message is deleted."""
        if message.author == self.user or not message.guild:
            return
        
        self.forensics_logger.log_activity("message_delete", {
            "message_id": str(message.id),
            "author_id": str(message.author.id),
            "author_name": str(message.author),
            "channel_id": str(message.channel.id),
            "channel_name": str(message.channel),
            "guild_id": str(message.guild.id),
            "content": message.content[:500]
        })
    
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        """Log when a message is edited."""
        if before.author == self.user or not before.guild or before.content == after.content:
            return
        
        self.forensics_logger.log_activity("message_edit", {
            "message_id": str(before.id),
            "author_id": str(before.author.id),
            "author_name": str(before.author),
            "channel_id": str(before.channel.id),
            "guild_id": str(before.guild.id),
            "before_content": before.content[:500],
            "after_content": after.content[:500]
        })
    
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        """Log when a channel is created."""
        self.forensics_logger.log_activity("channel_create", {
            "channel_id": str(channel.id),
            "channel_name": str(channel),
            "channel_type": str(channel.type),
            "guild_id": str(channel.guild.id)
        })
    
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        """Log when a channel is deleted."""
        self.forensics_logger.log_activity("channel_delete", {
            "channel_id": str(channel.id),
            "channel_name": str(channel),
            "guild_id": str(channel.guild.id)
        })
    
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        """Log when a member is banned."""
        self.forensics_logger.log_activity("member_ban", {
            "user_id": str(user.id),
            "user_name": str(user),
            "guild_id": str(guild.id),
            "guild_name": guild.name
        })
        print(f"[BAN] {user} was banned from {guild.name}")
    
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        """Log when a member is unbanned."""
        self.forensics_logger.log_activity("member_unban", {
            "user_id": str(user.id),
            "user_name": str(user),
            "guild_id": str(guild.id),
            "guild_name": guild.name
        })
        print(f"[UNBAN] {user} was unbanned from {guild.name}")
    
    def check_spam(self, user_id: int) -> bool:
        """Check if user is spamming."""
        now = datetime.utcnow()
        if user_id not in self.user_messages:
            self.user_messages[user_id] = []
        
        # Clean old messages (older than 10 seconds)
        self.user_messages[user_id] = [
            msg_time for msg_time in self.user_messages[user_id]
            if (now - msg_time).total_seconds() < 10
        ]
        
        # Add current message
        self.user_messages[user_id].append(now)
        
        # Check if spam (more than threshold messages in 10 seconds)
        return len(self.user_messages[user_id]) > self.spam_threshold
    
    def check_excessive_caps(self, content: str) -> bool:
        """Check if message has excessive caps."""
        if len(content) < 10:
            return False
        letters = [c for c in content if c.isalpha()]
        if not letters:
            return False
        caps_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
        return caps_ratio > self.caps_threshold
        
    async def on_message(self, message: discord.Message):
        """Process every message for abuse detection and auto-moderation."""
        # Ignore bot's own messages
        if message.author == self.user:
            return
        
        # Ignore DMs
        if not message.guild:
            return
        
        # IMPORTANT: Analyze ALL messages first
        analysis = self.abuse_detector.analyze_message(message.content)
        
        # Debug logging - print EVERY message analysis
        if len(message.content.strip()) > 0:
            print(f"[ANALYZING] {message.author}: '{message.content[:50]}' | Abusive: {analysis['is_abusive']} | Score: {analysis['abuse_score']} | Keywords: {analysis['detected_keywords']}")
        
        # Check for commands first - but still apply auto-mod after
        # (Commands will be processed at the end)
        
        # Check for spam
        if self.check_spam(message.author.id):
            try:
                await message.delete()
                embed = discord.Embed(
                    title="🚫 Spam Detected",
                    description=f"{message.author.mention}, please slow down! Don't spam messages.",
                    color=discord.Color.red()
                )
                warning_msg = await message.channel.send(embed=embed)
                await warning_msg.delete(delay=5)
                
                # Timeout for 2 minutes for spamming
                await message.author.timeout(timedelta(minutes=2), reason="Auto-mod: Spamming")
                print(f"[SPAM] {message.author} timed out for spamming")
                return
            except Exception as e:
                print(f"[ERROR] Spam action failed: {e}")
        
        # Check for excessive caps
        if self.check_excessive_caps(message.content):
            try:
                await message.delete()
                embed = discord.Embed(
                    title="🔠 Excessive Caps",
                    description=f"{message.author.mention}, please don't use excessive CAPS LOCK.",
                    color=discord.Color.orange()
                )
                warning_msg = await message.channel.send(embed=embed)
                await warning_msg.delete(delay=5)
                return
            except Exception as e:
                print(f"[ERROR] Caps filter action failed: {e}")
        
        # Auto-moderation for abusive content (analysis already done above)
        if analysis['is_abusive']:
            self.forensics_logger.log_evidence(message, analysis)
            print(f"[ABUSE DETECTED] {message.author}: {message.content[:50]}... "
                  f"(Score: {analysis['abuse_score']}, Severity: {analysis['severity']}, Keywords: {analysis['detected_keywords']})")
            
            try:
                # Delete the abusive message
                await message.delete()
                
                # Load warnings
                warnings_file = os.path.join(self.forensics_logger.log_dir, "warnings.json")
                warnings = {}
                if os.path.exists(warnings_file):
                    with open(warnings_file, 'r') as f:
                        warnings = json.load(f)
                
                # Add automatic warning
                user_id = str(message.author.id)
                if user_id not in warnings:
                    warnings[user_id] = []
                
                warnings[user_id].append({
                    "warned_by": "AUTO-MOD",
                    "warned_by_name": "Guardify Auto-Moderation",
                    "reason": f"Abusive language detected ({analysis['severity']} severity)",
                    "message_content": message.content[:100],
                    "timestamp": datetime.utcnow().isoformat()
                })
                
                # Save warnings
                with open(warnings_file, 'w') as f:
                    json.dump(warnings, f, indent=2)
                
                warning_count = len(warnings[user_id])
                
                # Send warning message in channel
                embed = discord.Embed(
                    title="⚠️ Abusive Content Detected",
                    description=f"{message.author.mention}, your message was removed for violating community guidelines.",
                    color=discord.Color.orange()
                )
                embed.add_field(name="Reason", value=f"Abusive language ({analysis['severity']} severity)", inline=False)
                embed.add_field(name="Total Warnings", value=f"{warning_count}/5", inline=True)
                
                # Auto-timeout after 5 warnings
                if warning_count >= 5:
                    try:
                        await message.author.timeout(timedelta(minutes=10), reason="Auto-mod: 5 warnings reached")
                        embed.add_field(name="Action Taken", value="🔇 Timed out for 10 minutes (5 warnings)", inline=False)
                        embed.color = discord.Color.red()
                    except discord.Forbidden:
                        embed.add_field(name="Note", value="⚠️ Unable to timeout user (insufficient permissions)", inline=False)
                else:
                    embed.add_field(name="Warning", value=f"You will be timed out after 5 warnings ({5-warning_count} remaining)", inline=False)
                
                warning_msg = await message.channel.send(embed=embed)
                # Delete warning message after 10 seconds
                await warning_msg.delete(delay=10)
                
                # Try to DM the user
                try:
                    dm_embed = discord.Embed(
                        title="⚠️ Community Guidelines Violation",
                        description=f"Your message in {message.guild.name} was removed.",
                        color=discord.Color.red()
                    )
                    dm_embed.add_field(name="Message", value=message.content[:500], inline=False)
                    dm_embed.add_field(name="Reason", value=f"Abusive language detected", inline=False)
                    dm_embed.add_field(name="Warnings", value=f"{warning_count}/5", inline=False)
                    if warning_count >= 5:
                        dm_embed.add_field(name="Action", value="Timed out for 10 minutes", inline=False)
                    await message.author.send(embed=dm_embed)
                except:
                    pass  # User has DMs disabled
                    
            except discord.Forbidden:
                print(f"[ERROR] Cannot delete message or timeout user - missing permissions")
            except Exception as e:
                print(f"[ERROR] Auto-mod failed: {e}")
        
        # Process commands
        await self.process_commands(message)


# Setup bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = RespectRanger(command_prefix='!', intents=intents)


@bot.command(name='scan')
@commands.has_permissions(manage_messages=True)
async def scan_message(ctx, *, text: str):
    """
    Manually scan a message for abusive content.
    Usage: !scan <message text>
    """
    analysis = bot.abuse_detector.analyze_message(text)
    
    embed = discord.Embed(
        title="Abuse Detection Analysis",
        color=discord.Color.red() if analysis['is_abusive'] else discord.Color.green()
    )
    
    embed.add_field(name="Abusive", value=str(analysis['is_abusive']), inline=True)
    embed.add_field(name="Severity", value=analysis['severity'].upper(), inline=True)
    embed.add_field(name="Abuse Score", value=str(analysis['abuse_score']), inline=True)
    embed.add_field(name="Sentiment", value=str(analysis['sentiment']), inline=True)
    
    if analysis['detected_keywords']:
        embed.add_field(
            name="Detected Keywords",
            value=", ".join(analysis['detected_keywords']),
            inline=False
        )
    
    await ctx.send(embed=embed)


@bot.command(name='history')
@commands.has_permissions(manage_messages=True)
async def user_history(ctx, user: discord.User, limit: int = 5):
    """
    View abuse history for a user.
    Usage: !history @user [limit]
    """
    records = bot.forensics_logger.get_user_history(str(user.id), limit)
    
    if not records:
        await ctx.send(f"No abuse records found for {user.mention}")
        return
    
    embed = discord.Embed(
        title=f"Abuse History for {user.name}",
        description=f"Showing {len(records)} most recent cases",
        color=discord.Color.orange()
    )
    
    for i, record in enumerate(records[:limit], 1):
        analysis = record.get('analysis', {})
        embed.add_field(
            name=f"Case #{i} - {analysis.get('severity', 'N/A').upper()}",
            value=f"**Message:** {record.get('content', 'N/A')[:100]}...\n"
                  f"**Score:** {analysis.get('abuse_score', 'N/A')}\n"
                  f"**Date:** {record.get('created_at', 'N/A')[:10]}",
            inline=False
        )
    
    await ctx.send(embed=embed)


@bot.command(name='stats')
@commands.has_permissions(manage_messages=True)
async def statistics(ctx):
    """
    View abuse detection statistics.
    Usage: !stats
    """
    stats = bot.forensics_logger.get_statistics()
    
    embed = discord.Embed(
        title="Abuse Detection Statistics",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="Total Cases", value=str(stats.get('total_cases', 0)), inline=True)
    embed.add_field(name="Unique Users", value=str(stats.get('unique_users', 0)), inline=True)
    embed.add_field(name="Unique Servers", value=str(stats.get('unique_guilds', 0)), inline=True)
    
    severity = stats.get('severity_breakdown', {})
    embed.add_field(
        name="Severity Breakdown",
        value=f"🟢 Low: {severity.get('low', 0)}\n"
              f"🟡 Medium: {severity.get('medium', 0)}\n"
              f"🔴 High: {severity.get('high', 0)}",
        inline=False
    )
    
    await ctx.send(embed=embed)


@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    """
    Kick a member from the server.
    Usage: !kick @user [reason]
    """
    try:
        await member.kick(reason=f"{reason} | Kicked by {ctx.author}")
        
        # Log the action
        bot.forensics_logger.log_mod_action("kick", ctx.author, member, reason, str(ctx.guild.id))
        
        embed = discord.Embed(
            title="Member Kicked",
            description=f"{member.mention} has been kicked from the server.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
        await ctx.send(embed=embed)
        print(f"[MOD ACTION] {ctx.author} kicked {member} | Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to kick this member!")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    """
    Ban a member from the server.
    Usage: !ban @user [reason]
    """
    try:
        await member.ban(reason=f"{reason} | Banned by {ctx.author}", delete_message_days=1)
        
        # Log the action
        bot.forensics_logger.log_mod_action("ban", ctx.author, member, reason, str(ctx.guild.id))
        
        embed = discord.Embed(
            title="Member Banned",
            description=f"{member.mention} has been banned from the server.",
            color=discord.Color.red()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
        await ctx.send(embed=embed)
        print(f"[MOD ACTION] {ctx.author} banned {member} | Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to ban this member!")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='unban')
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int, *, reason: str = "No reason provided"):
    """
    Unban a user from the server.
    Usage: !unban <user_id> [reason]
    """
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=f"{reason} | Unbanned by {ctx.author}")
        
        # Log the action
        bot.forensics_logger.log_mod_action("unban", ctx.author, user, reason, str(ctx.guild.id))
        
        embed = discord.Embed(
            title="Member Unbanned",
            description=f"{user.mention} has been unbanned from the server.",
            color=discord.Color.green()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
        await ctx.send(embed=embed)
        print(f"[MOD ACTION] {ctx.author} unbanned {user} | Reason: {reason}")
    except discord.NotFound:
        await ctx.send("❌ User not found or not banned!")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='timeout')
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, duration: int, *, reason: str = "No reason provided"):
    """
    Timeout a member (mute) for specified minutes.
    Usage: !timeout @user <minutes> [reason]
    """
    try:
        await member.timeout(timedelta(minutes=duration), reason=f"{reason} | Timeout by {ctx.author}")
        
        # Log the action
        bot.forensics_logger.log_mod_action("timeout", ctx.author, member, f"{duration}min - {reason}", str(ctx.guild.id))
        
        embed = discord.Embed(
            title="Member Timed Out",
            description=f"{member.mention} has been timed out for {duration} minutes.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
        await ctx.send(embed=embed)
        print(f"[MOD ACTION] {ctx.author} timed out {member} for {duration}min | Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to timeout this member!")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='untimeout')
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, member: discord.Member):
    """
    Remove timeout from a member.
    Usage: !untimeout @user
    """
    try:
        await member.timeout(None, reason=f"Timeout removed by {ctx.author}")
        embed = discord.Embed(
            title="Timeout Removed",
            description=f"{member.mention} can now speak again.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='warn')
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    """
    Warn a member.
    Usage: !warn @user [reason]
    """
    warnings_file = os.path.join(bot.forensics_logger.log_dir, "warnings.json")
    
    # Load existing warnings
    warnings = {}
    if os.path.exists(warnings_file):
        with open(warnings_file, 'r') as f:
            warnings = json.load(f)
    
    # Add warning
    user_id = str(member.id)
    if user_id not in warnings:
        warnings[user_id] = []
    
    warnings[user_id].append({
        "warned_by": str(ctx.author.id),
        "warned_by_name": str(ctx.author),
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    # Save warnings
    with open(warnings_file, 'w') as f:
        json.dump(warnings, f, indent=2)
    
    # Log the action
    bot.forensics_logger.log_mod_action("warn", ctx.author, member, reason, str(ctx.guild.id))
    print(f"[MOD ACTION] {ctx.author} warned {member} | Reason: {reason}")
    
    # Send warning message
    embed = discord.Embed(
        title="Member Warned",
        description=f"{member.mention} has been warned.",
        color=discord.Color.gold()
    )
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.add_field(name="Total Warnings", value=str(len(warnings[user_id])), inline=False)
    embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
    await ctx.send(embed=embed)
    
    # Try to DM the user
    try:
        dm_embed = discord.Embed(
            title="⚠️ Warning",
            description=f"You have been warned in {ctx.guild.name}",
            color=discord.Color.gold()
        )
        dm_embed.add_field(name="Reason", value=reason, inline=False)
        await member.send(embed=dm_embed)
    except:
        pass


@bot.command(name='automod')
@commands.has_permissions(administrator=True)
async def automod_settings(ctx, setting: str = None, value: str = None):
    """
    View or configure auto-moderation settings.
    Usage: !automod [setting] [value]
    Settings: spam_threshold, caps_threshold
    """
    if setting is None:
        embed = discord.Embed(
            title="🛡️ Auto-Moderation Settings",
            description="Current auto-moderation configuration",
            color=discord.Color.blue()
        )
        embed.add_field(name="Spam Threshold", value=f"{bot.spam_threshold} messages per 10 seconds", inline=False)
        embed.add_field(name="Caps Threshold", value=f"{int(bot.caps_threshold * 100)}% caps in message", inline=False)
        embed.add_field(name="Auto-Delete", value="✅ Enabled for abusive content, spam, excessive caps", inline=False)
        embed.add_field(name="Auto-Warn", value="✅ Enabled for abusive content", inline=False)
        embed.add_field(name="Auto-Timeout", value="✅ After 5 warnings (10 minutes) or spam (2 minutes)", inline=False)
        embed.set_footer(text="Use !automod <setting> <value> to change")
        await ctx.send(embed=embed)
    else:
        if setting == "spam_threshold" and value:
            try:
                bot.spam_threshold = int(value)
                await ctx.send(f"✅ Spam threshold set to {value} messages per 10 seconds")
            except:
                await ctx.send("❌ Invalid value. Use a number (e.g., !automod spam_threshold 5)")
        elif setting == "caps_threshold" and value:
            try:
                bot.caps_threshold = int(value) / 100
                await ctx.send(f"✅ Caps threshold set to {value}%")
            except:
                await ctx.send("❌ Invalid value. Use a percentage (e.g., !automod caps_threshold 70)")
        else:
            await ctx.send("❌ Unknown setting. Available: spam_threshold, caps_threshold")


@bot.command(name='clearwarnings')
@commands.has_permissions(administrator=True)
async def clear_warnings(ctx, member: discord.Member):
    """
    Clear all warnings for a member.
    Usage: !clearwarnings @user
    """
    warnings_file = os.path.join(bot.forensics_logger.log_dir, "warnings.json")
    
    if not os.path.exists(warnings_file):
        await ctx.send(f"{member.mention} has no warnings to clear.")
        return
    
    with open(warnings_file, 'r') as f:
        warnings_data = json.load(f)
    
    user_id = str(member.id)
    if user_id in warnings_data:
        del warnings_data[user_id]
        with open(warnings_file, 'w') as f:
            json.dump(warnings_data, f, indent=2)
        await ctx.send(f"✅ Cleared all warnings for {member.mention}")
    else:
        await ctx.send(f"{member.mention} has no warnings to clear.")


@bot.command(name='warnings')
@commands.has_permissions(manage_messages=True)
async def warnings(ctx, member: discord.Member):
    """
    Check warnings for a member.
    Usage: !warnings @user
    """
    warnings_file = os.path.join(bot.forensics_logger.log_dir, "warnings.json")
    
    if not os.path.exists(warnings_file):
        await ctx.send(f"{member.mention} has no warnings.")
        return
    
    with open(warnings_file, 'r') as f:
        warnings_data = json.load(f)
    
    user_id = str(member.id)
    user_warnings = warnings_data.get(user_id, [])
    
    if not user_warnings:
        await ctx.send(f"{member.mention} has no warnings.")
        return
    
    embed = discord.Embed(
        title=f"Warnings for {member}",
        description=f"Total warnings: {len(user_warnings)}",
        color=discord.Color.gold()
    )
    
    for i, warning in enumerate(user_warnings[-5:], 1):  # Show last 5
        embed.add_field(
            name=f"Warning #{i}",
            value=f"**Reason:** {warning['reason']}\n**By:** {warning['warned_by_name']}\n**Date:** {warning['timestamp'][:10]}",
            inline=False
        )
    
    await ctx.send(embed=embed)


@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    """
    Delete multiple messages.
    Usage: !clear [amount] (default: 10, max: 100)
    """
    if amount > 100:
        amount = 100
    
    try:
        deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include command message
        msg = await ctx.send(f"✅ Deleted {len(deleted) - 1} messages.")
        await msg.delete(delay=3)
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to delete messages!")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='slowmode')
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int = 0):
    """
    Set slowmode delay in channel.
    Usage: !slowmode <seconds> (0 to disable, max: 21600)
    """
    if seconds > 21600:
        seconds = 21600
    
    try:
        await ctx.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await ctx.send("✅ Slowmode disabled.")
        else:
            await ctx.send(f"✅ Slowmode set to {seconds} seconds.")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='lock')
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    """
    Lock the current channel (prevent @everyone from sending messages).
    Usage: !lock
    """
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed = discord.Embed(
            title="🔒 Channel Locked",
            description=f"{ctx.channel.mention} has been locked.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='unlock')
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    """
    Unlock the current channel.
    Usage: !unlock
    """
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=None)
        embed = discord.Embed(
            title="🔓 Channel Unlocked",
            description=f"{ctx.channel.mention} has been unlocked.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='serverinfo')
async def serverinfo(ctx):
    """
    Display server information.
    Usage: !serverinfo
    """
    guild = ctx.guild
    embed = discord.Embed(
        title=f"📊 {guild.name}",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Server ID", value=guild.id, inline=True)
    await ctx.send(embed=embed)


@bot.command(name='userinfo')
async def userinfo(ctx, member: discord.Member = None):
    """
    Display user information.
    Usage: !userinfo [@user]
    """
    member = member or ctx.author
    embed = discord.Embed(
        title=f"👤 {member}",
        color=member.color
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Nickname", value=member.nick or "None", inline=True)
    embed.add_field(name="Status", value=str(member.status).title(), inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Roles", value=f"{len(member.roles) - 1}", inline=True)
    await ctx.send(embed=embed)


@bot.command(name='help_guardify')
async def help_command(ctx):
    """
    Show bot help and available commands.
    Usage: !help_guardify
    """
    embed = discord.Embed(
        title="Guardify - Complete Command Guide",
        description="Sapphire-like Discord bot with advanced moderation\nUse `!setup` for server configuration wizard",
        color=discord.Color.purple()
    )
    
    embed.add_field(
        name="🔧 Server Setup (Admin)",
        value="`!setup` - Setup wizard\n`!config` - View config\n`!setwelcome #channel` - Welcome channel\n`!setlog #channel` - Log channel",
        inline=False
    )
    
    embed.add_field(
        name="📢 Welcome & Messages",
        value="`!welcomemsg <text>` - Set welcome message\n`!goodbyemsg <text>` - Set goodbye message",
        inline=False
    )
    
    embed.add_field(
        name="✅ Verification & Roles",
        value="`!setupverify` - Enable verification\n`!verify` - Verify yourself\n`!autorole @role` - Set auto-role",
        inline=False
    )
    
    embed.add_field(
        name="🔒 Anti-Raid",
        value="`!antiraid on/off` - Toggle protection\n`!raidthreshold <n>` - Set sensitivity",
        inline=False
    )
    
    embed.add_field(
        name="🤖 Auto-Moderation (Active)",
        value="✅ Abusive language detection\n✅ Spam protection\n✅ Caps filter\n✅ Auto-warnings & timeouts",
        inline=False
    )
    
    embed.add_field(
        name="🔨 Moderation",
        value="`!kick` `!ban` `!unban` `!mute` `!unmute`\n`!timeout` `!warn` `!purge` `!nick` `!role`",
        inline=False
    )
    
    embed.add_field(
        name="🧹 Channel Tools",
        value="`!clear` `!slowmode` `!lock` `!unlock`",
        inline=False
    )
    
    embed.add_field(
        name="📊 Info & Stats",
        value="`!scan` `!history` `!stats` `!warnings`\n`!serverinfo` `!userinfo` `!automod`",
        inline=False
    )
    
    embed.set_footer(text="Guardify • Protecting your server 24/7")
    
    await ctx.send(embed=embed)


# ==================== SAPPHIRE-LIKE FEATURES ====================

@bot.command(name='setup')
@commands.has_permissions(administrator=True)
async def setup_server(ctx):
    """
    Interactive server setup wizard (Sapphire-style).
    Usage: !setup
    """
    embed = discord.Embed(
        title="🛡️ Guardify Server Setup Wizard",
        description="Let's configure your server! Use the commands below to set up features.",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="📢 Welcome System",
        value="`!setwelcome #channel` - Set welcome/goodbye channel\n"
              "`!welcomemsg <message>` - Customize welcome message\n"
              "`!goodbyemsg <message>` - Customize goodbye message",
        inline=False
    )
    
    embed.add_field(
        name="📋 Logging",
        value="`!setlog #channel` - Set general log channel\n"
              "`!setmodlog #channel` - Set mod action log channel",
        inline=False
    )
    
    embed.add_field(
        name="✅ Verification System",
        value="`!setupverify` - Enable verification system\n"
              "`!verify` - Verify a member (users use this)",
        inline=False
    )
    
    embed.add_field(
        name="🎭 Auto-Role",
        value="`!autorole @role` - Set role to give on join\n"
              "`!autorole none` - Disable auto-role",
        inline=False
    )
    
    embed.add_field(
        name="🔒 Anti-Raid",
        value="`!antiraid <on/off>` - Toggle anti-raid protection\n"
              "`!raidthreshold <number>` - Set raid detection sensitivity",
        inline=False
    )
    
    embed.add_field(
        name="Variables",
        value="`{user}` - Mentions user\n`{server}` - Server name\n`{count}` - Member count",
        inline=False
    )
    
    await ctx.send(embed=embed)


@bot.command(name='setwelcome')
@commands.has_permissions(administrator=True)
async def set_welcome_channel(ctx, channel: discord.TextChannel):
    """Set welcome/goodbye message channel."""
    guild_id = str(ctx.guild.id)
    config = bot.get_guild_config(guild_id)
    config['welcome_channel'] = str(channel.id)
    bot.save_guild_configs()
    await ctx.send(f"✅ Welcome channel set to {channel.mention}")


@bot.command(name='welcomemsg')
@commands.has_permissions(administrator=True)
async def set_welcome_message(ctx, *, message: str):
    """Set custom welcome message."""
    guild_id = str(ctx.guild.id)
    config = bot.get_guild_config(guild_id)
    config['welcome_message'] = message
    bot.save_guild_configs()
    
    preview = message.replace('{user}', ctx.author.mention).replace('{server}', ctx.guild.name).replace('{count}', str(ctx.guild.member_count))
    embed = discord.Embed(title="✅ Welcome Message Updated", description="Preview:", color=discord.Color.green())
    embed.add_field(name="Message", value=preview, inline=False)
    await ctx.send(embed=embed)


@bot.command(name='goodbyemsg')
@commands.has_permissions(administrator=True)
async def set_goodbye_message(ctx, *, message: str):
    """Set custom goodbye message."""
    guild_id = str(ctx.guild.id)
    config = bot.get_guild_config(guild_id)
    config['goodbye_message'] = message
    bot.save_guild_configs()
    await ctx.send(f"✅ Goodbye message updated!")


@bot.command(name='setlog')
@commands.has_permissions(administrator=True)
async def set_log_channel(ctx, channel: discord.TextChannel):
    """Set general log channel."""
    guild_id = str(ctx.guild.id)
    config = bot.get_guild_config(guild_id)
    config['log_channel'] = str(channel.id)
    bot.save_guild_configs()
    
    embed = discord.Embed(title="✅ Log Channel Set", description=f"General logs will be sent to {channel.mention}", color=discord.Color.blue())
    embed.add_field(name="What gets logged?", value="• Member joins (with account age check)\n• Member leaves\n• Message edits/deletes\n• Anti-raid alerts", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='setmodlog')
@commands.has_permissions(administrator=True)
async def set_modlog_channel(ctx, channel: discord.TextChannel):
    """Set moderator action log channel."""
    guild_id = str(ctx.guild.id)
    config = bot.get_guild_config(guild_id)
    config['mod_log_channel'] = str(channel.id)
    bot.save_guild_configs()
    await ctx.send(f"✅ Mod log channel set to {channel.mention}\nAll kicks, bans, warnings, and timeouts will be logged here.")


@bot.command(name='setupverify')
@commands.has_permissions(administrator=True)
async def setup_verification(ctx):
    """Set up verification system."""
    guild_id = str(ctx.guild.id)
    config = bot.get_guild_config(guild_id)
    
    verify_role = discord.utils.get(ctx.guild.roles, name="Unverified")
    if not verify_role:
        verify_role = await ctx.guild.create_role(name="Unverified", color=discord.Color.light_gray(), reason="Verification system setup")
    
    verified_role = discord.utils.get(ctx.guild.roles, name="Verified")
    if not verified_role:
        verified_role = await ctx.guild.create_role(name="Verified", color=discord.Color.green(), reason="Verification system setup")
    
    config['verification_enabled'] = True
    config['verification_role'] = str(verify_role.id)
    config['verified_role'] = str(verified_role.id)
    bot.save_guild_configs()
    
    embed = discord.Embed(title="✅ Verification System Enabled", description="New members will need to verify before accessing the server.", color=discord.Color.green())
    embed.add_field(name="Unverified Role", value=verify_role.mention, inline=True)
    embed.add_field(name="Verified Role", value=verified_role.mention, inline=True)
    embed.add_field(name="⚠️ Important", value="Make sure to configure channel permissions so Unverified members can only see a verification channel!", inline=False)
    embed.add_field(name="How Members Verify", value="New members type `!verify` in the verification channel or DM the bot.", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='verify')
async def verify_member(ctx):
    """Verify yourself to access the server."""
    guild = ctx.guild if ctx.guild else None
    
    if not guild:
        user_id = str(ctx.author.id)
        if user_id in bot.pending_verifications:
            guild_id = bot.pending_verifications[user_id]['guild_id']
            guild = bot.get_guild(int(guild_id))
        else:
            await ctx.send("❌ You don't have any pending verifications.")
            return
    
    guild_id = str(guild.id)
    config = bot.get_guild_config(guild_id)
    
    if not config.get('verification_enabled'):
        await ctx.send("❌ Verification is not enabled on this server.")
        return
    
    member = guild.get_member(ctx.author.id)
    if not member:
        await ctx.send("❌ You're not in the server.")
        return
    
    verify_role = guild.get_role(int(config['verification_role'])) if config.get('verification_role') else None
    verified_role = guild.get_role(int(config['verified_role'])) if config.get('verified_role') else None
    
    if verify_role in member.roles:
        try:
            await member.remove_roles(verify_role, reason="User verified")
            if verified_role:
                await member.add_roles(verified_role, reason="User verified")
            
            if str(ctx.author.id) in bot.pending_verifications:
                del bot.pending_verifications[str(ctx.author.id)]
            
            embed = discord.Embed(title="✅ Verification Successful!", description=f"Welcome to {guild.name}! You now have access to all channels.", color=discord.Color.green())
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")
    else:
        await ctx.send("❌ You're already verified or don't need verification!")


@bot.command(name='autorole')
@commands.has_permissions(administrator=True)
async def set_autorole(ctx, role: discord.Role = None):
    """Set role to automatically give to new members."""
    guild_id = str(ctx.guild.id)
    config = bot.get_guild_config(guild_id)
    
    if role:
        config['autorole'] = str(role.id)
        bot.save_guild_configs()
        await ctx.send(f"✅ Auto-role set to {role.mention}. New members will automatically receive this role.")
    else:
        config['autorole'] = None
        bot.save_guild_configs()
        await ctx.send("✅ Auto-role disabled.")


@bot.command(name='antiraid')
@commands.has_permissions(administrator=True)
async def toggle_antiraid(ctx, status: str):
    """Toggle anti-raid protection."""
    guild_id = str(ctx.guild.id)
    config = bot.get_guild_config(guild_id)
    
    if status.lower() in ['on', 'enable', 'true']:
        config['anti_raid'] = True
        bot.save_guild_configs()
        await ctx.send("✅ Anti-raid protection ENABLED. The bot will alert you if multiple accounts join rapidly.")
    elif status.lower() in ['off', 'disable', 'false']:
        config['anti_raid'] = False
        bot.save_guild_configs()
        bot.raid_mode[guild_id] = False
        await ctx.send("✅ Anti-raid protection DISABLED.")
    else:
        await ctx.send("❌ Usage: `!antiraid on` or `!antiraid off`")


@bot.command(name='raidthreshold')
@commands.has_permissions(administrator=True)
async def set_raid_threshold(ctx, number: int):
    """Set how many joins in 10 seconds triggers raid alert."""
    guild_id = str(ctx.guild.id)
    config = bot.get_guild_config(guild_id)
    
    if number < 3:
        await ctx.send("❌ Threshold must be at least 3.")
        return
    
    config['raid_threshold'] = number
    bot.save_guild_configs()
    await ctx.send(f"✅ Raid threshold set to {number} joins per 10 seconds.")


@bot.command(name='mute')
@commands.has_permissions(moderate_members=True)
async def mute_member(ctx, member: discord.Member, duration: int = None, *, reason: str = "No reason provided"):
    """Mute a member."""
    if duration is None:
        duration = 10
    
    try:
        await member.timeout(timedelta(minutes=duration), reason=f"{reason} | Muted by {ctx.author}")
        bot.forensics_logger.log_mod_action("mute", ctx.author, member, f"{duration}min - {reason}", str(ctx.guild.id))
        
        embed = discord.Embed(title="🔇 Member Muted", description=f"{member.mention} has been muted for {duration} minutes.", color=discord.Color.orange())
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
        await ctx.send(embed=embed)
        print(f"[MOD ACTION] {ctx.author} muted {member} for {duration}min | Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to mute this member!")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='unmute')
@commands.has_permissions(moderate_members=True)
async def unmute_member(ctx, member: discord.Member):
    """Unmute a member."""
    try:
        await member.timeout(None, reason=f"Unmuted by {ctx.author}")
        embed = discord.Embed(title="🔊 Member Unmuted", description=f"{member.mention} can now speak again.", color=discord.Color.green())
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='purge')
@commands.has_permissions(manage_messages=True)
async def purge_messages(ctx, amount: int, member: discord.Member = None):
    """Bulk delete messages."""
    if amount > 100:
        amount = 100
    
    try:
        if member:
            deleted = await ctx.channel.purge(limit=amount + 1, check=lambda m: m.author == member)
            msg = await ctx.send(f"✅ Deleted {len(deleted) - 1} messages from {member.mention}.")
        else:
            deleted = await ctx.channel.purge(limit=amount + 1)
            msg = await ctx.send(f"✅ Deleted {len(deleted) - 1} messages.")
        await msg.delete(delay=3)
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to delete messages!")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='nick')
@commands.has_permissions(manage_nicknames=True)
async def change_nickname(ctx, member: discord.Member, *, nickname: str = None):
    """Change a member's nickname."""
    try:
        await member.edit(nick=nickname, reason=f"Changed by {ctx.author}")
        if nickname:
            await ctx.send(f"✅ Changed nickname of {member.mention} to **{nickname}**")
        else:
            await ctx.send(f"✅ Reset nickname of {member.mention}")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to change this member's nickname!")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='role')
@commands.has_permissions(manage_roles=True)
async def manage_role(ctx, member: discord.Member, role: discord.Role):
    """Add or remove a role from a member."""
    try:
        if role in member.roles:
            await member.remove_roles(role, reason=f"Removed by {ctx.author}")
            await ctx.send(f"✅ Removed {role.mention} from {member.mention}")
        else:
            await member.add_roles(role, reason=f"Added by {ctx.author}")
            await ctx.send(f"✅ Added {role.mention} to {member.mention}")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to manage this role!")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='config')
@commands.has_permissions(administrator=True)
async def view_config(ctx):
    """View current server configuration."""
    guild_id = str(ctx.guild.id)
    config = bot.get_guild_config(guild_id)
    
    embed = discord.Embed(title=f"⚙️ {ctx.guild.name} Configuration", color=discord.Color.blue())
    
    welcome_ch = ctx.guild.get_channel(int(config['welcome_channel'])) if config.get('welcome_channel') else None
    embed.add_field(name="📢 Welcome System", value=f"Channel: {welcome_ch.mention if welcome_ch else 'Not set'}\nMessage: `{config.get('welcome_message', 'Default')[:50]}...`", inline=False)
    
    log_ch = ctx.guild.get_channel(int(config['log_channel'])) if config.get('log_channel') else None
    modlog_ch = ctx.guild.get_channel(int(config['mod_log_channel'])) if config.get('mod_log_channel') else None
    embed.add_field(name="📋 Logging", value=f"General Log: {log_ch.mention if log_ch else 'Not set'}\nMod Log: {modlog_ch.mention if modlog_ch else 'Not set'}", inline=False)
    
    verify_enabled = "✅ Enabled" if config.get('verification_enabled') else "❌ Disabled"
    embed.add_field(name="✅ Verification", value=verify_enabled, inline=True)
    
    antiraid_status = "✅ Enabled" if config.get('anti_raid', True) else "❌ Disabled"
    raid_threshold = config.get('raid_threshold', 5)
    embed.add_field(name="🔒 Anti-Raid", value=f"{antiraid_status} ({raid_threshold} joins/10s)", inline=True)
    
    autorole = ctx.guild.get_role(int(config['autorole'])) if config.get('autorole') else None
    embed.add_field(name="🎭 Auto-Role", value=autorole.mention if autorole else "Not set", inline=True)
    
    embed.set_footer(text="Use !setup for configuration help")
    await ctx.send(embed=embed)


# ==================== END SAPPHIRE-LIKE FEATURES ====================


# Simple web server for Render.com (keeps service alive)
app = Flask('')

@app.route('/')
def home():
    return "Guardify Bot is online! 🛡️"

@app.route('/health')
def health():
    return {"status": "online", "bot": str(bot.user) if bot.is_ready() else "connecting"}

def run_web_server():
    """Run Flask web server in background thread."""
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def main():
    """Main entry point for the bot."""
    # Load bot token from environment variable or config file
    token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not token:
        # Try loading from config file
        config_file = 'config.json'
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                token = config.get('bot_token')
    
    if not token:
        print("ERROR: Discord bot token not found!")
        print("Please set DISCORD_BOT_TOKEN environment variable or add it to config.json")
        return
    
    # Start web server in background (for Render.com)
    try:
        server_thread = Thread(target=run_web_server)
        server_thread.daemon = True
        server_thread.start()
        print("Web server started for health checks")
    except Exception as e:
        print(f"Warning: Could not start web server: {e}")
    
    # Run the bot
    try:
        print("Starting Discord bot...")
        bot.run(token)
    except Exception as e:
        print(f"ERROR: Bot failed to start: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
