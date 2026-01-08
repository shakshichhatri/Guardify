"""
Guardify - AI-Enabled Social Media Forensics Investigation
Detecting and Preventing Digital Abuse through Advanced AI Moderation

Project: AI-Enabled Social Media Forensics Investigation for Detecting and Preventing Digital Abuse
Purpose: Empowers users to collect evidence, detect harmful content, and prevent escalation
         through AI-powered analysis and comprehensive forensics logging.
"""

import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime, timedelta, timezone
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import hashlib
import pandas as pd
import re
from typing import Dict, List, Optional
import asyncio
from collections import defaultdict
import csv


class AbuseDetector:
    """
    AI-Powered Abuse Detection System
    
    Uses dual sentiment analysis (TextBlob + VADER) for improved accuracy
    in detecting harmful content, cyberbullying, and online harassment.
    Implements forensics-grade evidence collection methodology.
    """
    
    SENTIMENT_THRESHOLD = -0.3
    VADER_THRESHOLD = -0.5
    KEYWORD_WEIGHT = 0.4
    ABUSE_SCORE_THRESHOLD = 0.4
    
    def __init__(self):
        self.abusive_keywords = [
            'hate', 'kill', 'stupid', 'idiot', 'loser', 'trash',
            'worthless', 'pathetic', 'disgusting', 'die', 'kys',
            'retard', 'moron', 'dumb', 'ugly', 'fat', 'nazi',
            'fuck', 'shit', 'bitch', 'ass', 'damn', 'suicide',
            'hurt yourself', 'nobody likes you', 'waste of space'
        ]
        self.spam_tracker = defaultdict(list)
        self.vader = SentimentIntensityAnalyzer()
        
        # Prevention tips database
        self.prevention_tips = {
            'high': [
                "🚨 Severe abuse detected. Document evidence and contact authorities if needed.",
                "⚠️ High-risk content identified. Consider implementing cooling-off period.",
                "📞 Critical situation. Reach out to mental health resources if affected."
            ],
            'medium': [
                "⚠️ Potentially harmful language detected. Monitor situation closely.",
                "📋 Recommend reviewing community guidelines with involved parties.",
                "🛡️ Enable auto-moderation to prevent escalation."
            ],
            'low': [
                "💡 Mild concern detected. Consider gentle reminder about respectful communication.",
                "📚 Educational opportunity - share resources about positive online behavior.",
                "👀 Keep monitoring - early intervention prevents escalation."
            ]
        }
        
    def analyze_message(self, content: str) -> Dict:
        """
        Dual AI Sentiment Analysis for Abuse Detection
        
        Combines TextBlob (pattern-based) and VADER (lexicon-based) for
        comprehensive analysis. Returns forensics-grade evidence data.
        """
        content_lower = content.lower()
        
        # TextBlob sentiment analysis
        blob = TextBlob(content)
        textblob_sentiment = blob.sentiment.polarity
        
        # VADER sentiment analysis (better for social media)
        vader_scores = self.vader.polarity_scores(content)
        vader_compound = vader_scores['compound']
        
        # Keyword detection with pattern matching
        detected_keywords = []
        for keyword in self.abusive_keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, content_lower):
                detected_keywords.append(keyword)
        
        # Combined abuse score calculation
        keyword_score = len(detected_keywords) * self.KEYWORD_WEIGHT
        textblob_score = abs(min(textblob_sentiment, 0))
        vader_score = abs(min(vader_compound, 0))
        
        # Weighted average of both sentiment analyzers
        combined_sentiment = (textblob_sentiment + vader_compound) / 2
        abuse_score = keyword_score + (textblob_score + vader_score) / 2
        
        # Determine if abusive
        is_abusive = (abuse_score > self.ABUSE_SCORE_THRESHOLD or 
                     textblob_sentiment < self.SENTIMENT_THRESHOLD or
                     vader_compound < self.VADER_THRESHOLD)
        
        # Severity classification
        severity = "low"
        if abuse_score > 0.8 or vader_compound < -0.7:
            severity = "high"
        elif abuse_score > 0.5 or vader_compound < -0.4:
            severity = "medium"
        
        # Get prevention tip
        prevention_tip = self.get_prevention_tip(severity)
        
        return {
            "is_abusive": is_abusive,
            "abuse_score": round(abuse_score, 3),
            "textblob_sentiment": round(textblob_sentiment, 3),
            "vader_sentiment": round(vader_compound, 3),
            "combined_sentiment": round(combined_sentiment, 3),
            "vader_details": vader_scores,
            "detected_keywords": detected_keywords,
            "severity": severity,
            "prevention_tip": prevention_tip,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "content_hash": hashlib.sha256(content.encode()).hexdigest()[:16]
        }
    
    def get_prevention_tip(self, severity: str) -> str:
        """Get appropriate prevention tip based on severity."""
        import random
        return random.choice(self.prevention_tips.get(severity, self.prevention_tips['low']))
    
    def check_spam(self, user_id: int, message_time: datetime) -> bool:
        """Check if user is spamming."""
        self.spam_tracker[user_id].append(message_time)
        
        # Keep only messages from last 5 seconds
        cutoff = message_time - timedelta(seconds=5)
        self.spam_tracker[user_id] = [t for t in self.spam_tracker[user_id] if t > cutoff]
        
        # If more than 5 messages in 5 seconds, it's spam
        return len(self.spam_tracker[user_id]) > 5


class ForensicsLogger:
    """
    Forensics-Grade Evidence Collection and Management
    
    Implements comprehensive logging with data integrity verification (SHA-256),
    CSV export for analysis, and prevention guidance integration.
    Designed for academic research and legal documentation purposes.
    """
    
    def __init__(self, log_dir: str = "forensics_logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, "abuse_evidence.jsonl")
        self.csv_file = os.path.join(log_dir, "abuse_evidence.csv")
        self.warnings_file = os.path.join(log_dir, "warnings.json")
        self.interactions_file = os.path.join(log_dir, "user_interactions.json")
        self.load_warnings()
        self.user_interactions = defaultdict(list)  # Track user interaction network
        
    def load_warnings(self):
        """Load warning counts from file."""
        if os.path.exists(self.warnings_file):
            with open(self.warnings_file, 'r') as f:
                self.warnings = json.load(f)
        else:
            self.warnings = {}
    
    def save_warnings(self):
        """Save warning counts to file."""
        with open(self.warnings_file, 'w') as f:
            json.dump(self.warnings, f, indent=2)
    
    def add_warning(self, user_id: str, guild_id: str, reason: str) -> int:
        """Add a warning for a user."""
        key = f"{guild_id}:{user_id}"
        if key not in self.warnings:
            self.warnings[key] = []
        
        self.warnings[key].append({
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.save_warnings()
        return len(self.warnings[key])
    
    def get_warnings(self, user_id: str, guild_id: str) -> List[Dict]:
        """Get warnings for a user."""
        key = f"{guild_id}:{user_id}"
        return self.warnings.get(key, [])
    
    def remove_warning(self, user_id: str, guild_id: str, index: int) -> bool:
        """Remove a specific warning by index."""
        key = f"{guild_id}:{user_id}"
        if key in self.warnings and 0 <= index < len(self.warnings[key]):
            self.warnings[key].pop(index)
            if len(self.warnings[key]) == 0:
                del self.warnings[key]
            self.save_warnings()
            return True
        return False
    
    def clear_warnings(self, user_id: str, guild_id: str):
        """Clear warnings for a user."""
        key = f"{guild_id}:{user_id}"
        if key in self.warnings:
            del self.warnings[key]
            self.save_warnings()
        
    def log_evidence(self, message: discord.Message, analysis: Dict) -> None:
        """
        Log forensics evidence with data integrity verification.
        
        Creates both JSONL and CSV records for research analysis.
        Includes SHA-256 hash for evidence verification and chain of custody.
        """
        # Create evidence record with data integrity
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
            "logged_at": datetime.now(timezone.utc).isoformat(),
            "evidence_hash": analysis.get('content_hash', hashlib.sha256(message.content.encode()).hexdigest()[:16])
        }
        
        # Log to JSONL (for detailed records)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evidence, ensure_ascii=False) + '\n')
        
        # Log to CSV (for visualization and analysis)
        self.log_to_csv(evidence)
        
        # Track user interactions for network analysis
        if message.guild:
            self.track_interaction(str(message.author.id), str(message.guild.id))
    
    def log_to_csv(self, evidence: Dict) -> None:
        """Export evidence to CSV for analysis in Excel/pandas."""
        file_exists = os.path.exists(self.csv_file)
        
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
            fieldnames = [
                'timestamp', 'message_id', 'author_id', 'author_name',
                'guild_name', 'channel_name', 'content', 'severity',
                'abuse_score', 'textblob_sentiment', 'vader_sentiment',
                'keywords', 'prevention_tip', 'evidence_hash'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            analysis = evidence.get('analysis', {})
            writer.writerow({
                'timestamp': evidence.get('created_at', ''),
                'message_id': evidence.get('message_id', ''),
                'author_id': evidence.get('author_id', ''),
                'author_name': evidence.get('author_name', ''),
                'guild_name': evidence.get('guild_name', ''),
                'channel_name': evidence.get('channel_name', ''),
                'content': evidence.get('content', '')[:500],  # Truncate for CSV
                'severity': analysis.get('severity', ''),
                'abuse_score': analysis.get('abuse_score', ''),
                'textblob_sentiment': analysis.get('textblob_sentiment', ''),
                'vader_sentiment': analysis.get('vader_sentiment', ''),
                'keywords': ','.join(analysis.get('detected_keywords', [])),
                'prevention_tip': analysis.get('prevention_tip', ''),
                'evidence_hash': evidence.get('evidence_hash', '')
            })
    
    def track_interaction(self, user_id: str, guild_id: str) -> None:
        """Track user interactions for network visualization."""
        key = f"{guild_id}:{user_id}"
        self.user_interactions[key].append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'guild_id': guild_id
        })
    
    def get_user_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Retrieve abuse history for a specific user."""
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
        """Get statistics about logged abuse cases."""
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


class Guardify(commands.Bot):
    """Main bot class with enhanced moderation features."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.abuse_detector = AbuseDetector()
        self.forensics_logger = ForensicsLogger()
        self.auto_mod_enabled = {}  # Guild-specific auto-mod settings
        self.log_channels = {}  # Guild-specific log channels
        self.welcome_channels = {}  # Guild-specific welcome channels
        self.welcome_messages = {}  # Guild-specific welcome messages
        self.load_log_channels()
        self.load_welcome_config()
        
    def load_log_channels(self):
        """Load log channels from file."""
        log_file = 'forensics_logs/log_channels.json'
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                self.log_channels = json.load(f)
    
    def save_log_channels(self):
        """Save log channels to file."""
        os.makedirs('forensics_logs', exist_ok=True)
        with open('forensics_logs/log_channels.json', 'w') as f:
            json.dump(self.log_channels, f, indent=2)
    
    def load_welcome_config(self):
        """Load welcome configuration from file."""
        welcome_file = 'forensics_logs/welcome_config.json'
        if os.path.exists(welcome_file):
            with open(welcome_file, 'r') as f:
                config = json.load(f)
                self.welcome_channels = config.get('channels', {})
                self.welcome_messages = config.get('messages', {})
    
    def save_welcome_config(self):
        """Save welcome configuration to file."""
        os.makedirs('forensics_logs', exist_ok=True)
        with open('forensics_logs/welcome_config.json', 'w') as f:
            json.dump({
                'channels': self.welcome_channels,
                'messages': self.welcome_messages
            }, f, indent=2)
    
    async def log_to_channel(self, guild_id: int, embed: discord.Embed):
        """Send log message to configured log channel."""
        channel_id = self.log_channels.get(str(guild_id))
        if channel_id:
            try:
                channel = self.get_channel(int(channel_id))
                if channel:
                    await channel.send(embed=embed)
            except Exception as e:
                print(f"Failed to send log to channel: {e}")
    
    async def setup_hook(self):
        """Setup hook for slash commands."""
        try:
            synced = await self.tree.sync()
            print(f"✅ Synced {len(synced)} slash commands")
        except Exception as e:
            print(f"❌ Failed to sync commands: {e}")
        
    async def on_ready(self):
        """Called when the bot is ready."""
        print(f'╔════════════════════════════════════════╗')
        print(f'║   🛡️  GUARDIFY BOT ONLINE 🛡️           ║')
        print(f'╠════════════════════════════════════════╣')
        print(f'║  Bot: {self.user.name:<28} ║')
        print(f'║  ID: {str(self.user.id):<29} ║')
        print(f'║  Servers: {len(self.guilds):<27} ║')
        print(f'╚════════════════════════════════════════╝')
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="for abuse | !help"
            )
        )
        
    async def on_guild_join(self, guild):
        """Send welcome message when bot joins a server."""
        # Find the first text channel bot can send messages in
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title="🛡️ Thanks for adding Guardify!",
                    description="I'm here to keep your server safe and friendly.",
                    color=discord.Color.blue()
                )
                embed.add_field(
                    name="🚀 Getting Started",
                    value="• Use `/help` to see all commands\n"
                          "• I automatically detect abusive messages\n"
                          "• Use `/automod enable` to activate auto-moderation",
                    inline=False
                )
                embed.add_field(
                    name="🔧 Setup Permissions",
                    value="Make sure I have these permissions:\n"
                          "• Manage Messages (to delete abusive content)\n"
                          "• Kick Members (for moderation actions)\n"
                          "• Ban Members (for severe violations)\n"
                          "• Timeout Members (to mute users)",
                    inline=False
                )
                embed.set_footer(text="Need help? Use /support")
                
                try:
                    await channel.send(embed=embed)
                except:
                    pass
                break
    
    async def on_member_join(self, member: discord.Member):
        """Send welcome message when a member joins the server."""
        guild_id = str(member.guild.id)
        
        # Check if welcome is configured for this guild
        if guild_id not in self.welcome_channels:
            return
        
        channel_id = self.welcome_channels[guild_id]
        channel = self.get_channel(int(channel_id))
        
        if not channel:
            return
        
        # Get custom message or use default
        custom_message = self.welcome_messages.get(guild_id, "")
        
        # Replace placeholders
        if custom_message:
            message_text = custom_message.replace("{user}", member.mention)
            message_text = message_text.replace("{server}", member.guild.name)
            message_text = message_text.replace("{count}", str(member.guild.member_count))
        else:
            message_text = f"Welcome to **{member.guild.name}**, {member.mention}! 🎉\nYou are member #{member.guild.member_count}!"
        
        # Create welcome embed
        embed = discord.Embed(
            title="👋 Welcome!",
            description=message_text,
            color=discord.Color.green(),
            timestamp=datetime.now(timezone.utc)
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Member #{member.guild.member_count}")
        
        try:
            await channel.send(embed=embed)
        except Exception as e:
            print(f"Failed to send welcome message: {e}")
        
    async def on_message(self, message: discord.Message):
        """Process every message for abuse detection."""
        if message.author == self.user or message.author.bot:
            return
        
        # Check for spam
        if message.guild and self.abuse_detector.check_spam(message.author.id, message.created_at):
            if self.auto_mod_enabled.get(message.guild.id, False):
                try:
                    await message.delete()
                    await message.channel.send(
                        f"⚠️ {message.author.mention}, please slow down! (Spam detected)",
                        delete_after=5
                    )
                except:
                    pass
        
        # Analyze message
        analysis = self.abuse_detector.analyze_message(message.content)
        
        # Log and handle if abusive
        if analysis['is_abusive']:
            self.forensics_logger.log_evidence(message, analysis)
            
            # Auto-moderation if enabled
            if message.guild and self.auto_mod_enabled.get(message.guild.id, False):
                await self.handle_abusive_message(message, analysis)
        
        await self.process_commands(message)
    
    async def handle_abusive_message(self, message: discord.Message, analysis: Dict):
        """Handle abusive message with appropriate action."""
        try:
            # Delete the message
            await message.delete()
            
            # Add warning
            warning_count = self.forensics_logger.add_warning(
                str(message.author.id),
                str(message.guild.id),
                f"Abusive language (Severity: {analysis['severity']})"
            )
            
            # Create warning embed
            embed = discord.Embed(
                title="⚠️ Warning Issued",
                description=f"{message.author.mention}, your message was removed for violating server rules.",
                color=discord.Color.orange()
            )
            embed.add_field(name="Reason", value="Abusive/Inappropriate Language", inline=False)
            embed.add_field(name="Warnings", value=f"{warning_count}/3", inline=True)
            embed.add_field(name="Severity", value=analysis['severity'].upper(), inline=True)
            
            # Take action based on warning count
            if warning_count >= 3:
                try:
                    await message.author.timeout(timedelta(hours=1), reason="3 warnings for abusive behavior")
                    embed.add_field(name="Action", value="⏱️ Timed out for 1 hour", inline=False)
                except:
                    pass
            elif warning_count >= 2:
                embed.set_footer(text="⚠️ Next warning will result in a timeout")
            
            await message.channel.send(embed=embed, delete_after=10)
            
            # Send log to log channel
            log_embed = discord.Embed(
                title="🚨 Auto-Moderation Action",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            log_embed.add_field(name="User", value=f"{message.author.mention} ({message.author})", inline=True)
            log_embed.add_field(name="Channel", value=message.channel.mention, inline=True)
            log_embed.add_field(name="Warnings", value=f"{warning_count}/3", inline=True)
            log_embed.add_field(name="Message", value=message.content[:1000], inline=False)
            log_embed.add_field(name="Severity", value=analysis['severity'].upper(), inline=True)
            log_embed.add_field(name="Score", value=str(analysis['abuse_score']), inline=True)
            if analysis.get('detected_keywords'):
                log_embed.add_field(name="Keywords", value=", ".join(analysis['detected_keywords']), inline=False)
            
            await self.log_to_channel(message.guild.id, log_embed)
            
        except Exception as e:
            print(f"Error handling abusive message: {e}")


# Setup bot
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = Guardify(command_prefix='!', intents=intents)


# ============= MODERATION COMMANDS =============

@bot.hybrid_command(name='warn', description='Warn a user for violating rules')
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    """Warn a user."""
    if member.bot:
        await ctx.send("❌ Cannot warn bots!", ephemeral=True)
        return
    
    warning_count = bot.forensics_logger.add_warning(
        str(member.id),
        str(ctx.guild.id),
        reason
    )
    
    embed = discord.Embed(
        title="⚠️ User Warned",
        color=discord.Color.orange(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="User", value=member.mention, inline=True)
    embed.add_field(name="Warned by", value=ctx.author.mention, inline=True)
    embed.add_field(name="Total Warnings", value=f"{warning_count}/3", inline=True)
    embed.add_field(name="Reason", value=reason, inline=False)
    
    await ctx.send(embed=embed)
    
    # Log to channel
    log_embed = discord.Embed(
        title="⚠️ User Warned",
        color=discord.Color.orange(),
        timestamp=datetime.utcnow()
    )
    log_embed.add_field(name="User", value=f"{member.mention} ({member})", inline=True)
    log_embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
    log_embed.add_field(name="Warnings", value=f"{warning_count}/3", inline=True)
    log_embed.add_field(name="Reason", value=reason, inline=False)
    await bot.log_to_channel(ctx.guild.id, log_embed)
    
    # Try to DM the user
    try:
        dm_embed = discord.Embed(
            title=f"⚠️ Warning from {ctx.guild.name}",
            description=f"You have been warned by a moderator.",
            color=discord.Color.orange()
        )
        dm_embed.add_field(name="Reason", value=reason)
        dm_embed.add_field(name="Warnings", value=f"{warning_count}/3")
        await member.send(embed=dm_embed)
    except:
        pass


@bot.hybrid_command(name='warnings', description='View warnings for a user')
@commands.has_permissions(manage_messages=True)
async def warnings(ctx, member: discord.Member):
    """View warnings for a user."""
    warns = bot.forensics_logger.get_warnings(str(member.id), str(ctx.guild.id))
    
    embed = discord.Embed(
        title=f"⚠️ Warnings for {member.name}",
        color=discord.Color.orange()
    )
    
    if not warns:
        embed.description = "No warnings found."
    else:
        embed.description = f"Total warnings: {len(warns)}"
        for i, warn in enumerate(warns[-5:], 1):
            embed.add_field(
                name=f"Warning #{i}",
                value=f"**Reason:** {warn['reason']}\n**Date:** {warn['timestamp'][:10]}",
                inline=False
            )
    
    await ctx.send(embed=embed)


@bot.hybrid_command(name='removewarn', description='Remove a specific warning from a user')
@commands.has_permissions(manage_messages=True)
async def removewarn(ctx, member: discord.Member, warning_number: int):
    """Remove a specific warning by number (1-based index)."""
    warns = bot.forensics_logger.get_warnings(str(member.id), str(ctx.guild.id))
    
    if not warns:
        await ctx.send(f"❌ {member.mention} has no warnings!", ephemeral=True)
        return
    
    if warning_number < 1 or warning_number > len(warns):
        await ctx.send(f"❌ Invalid warning number! {member.mention} has {len(warns)} warning(s).", ephemeral=True)
        return
    
    # Remove warning (convert to 0-based index)
    success = bot.forensics_logger.remove_warning(str(member.id), str(ctx.guild.id), warning_number - 1)
    
    if success:
        remaining = len(bot.forensics_logger.get_warnings(str(member.id), str(ctx.guild.id)))
        embed = discord.Embed(
            title="✅ Warning Removed",
            description=f"Removed warning #{warning_number} from {member.mention}\nRemaining warnings: {remaining}",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"Removed by {ctx.author}")
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"❌ Failed to remove warning!", ephemeral=True)


@bot.hybrid_command(name='clearwarnings', description='Clear all warnings for a user')
@commands.has_permissions(administrator=True)
async def clearwarnings(ctx, member: discord.Member):
    """Clear warnings for a user."""
    bot.forensics_logger.clear_warnings(str(member.id), str(ctx.guild.id))
    
    embed = discord.Embed(
        title="✅ Warnings Cleared",
        description=f"All warnings have been cleared for {member.mention}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)


@bot.hybrid_command(name='kick', description='Kick a user from the server')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    """Kick a user."""
    if member.top_role >= ctx.author.top_role:
        await ctx.send("❌ You cannot kick this user!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="👢 User Kicked",
        color=discord.Color.red(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="User", value=f"{member.mention} ({member})", inline=True)
    embed.add_field(name="Kicked by", value=ctx.author.mention, inline=True)
    embed.add_field(name="Reason", value=reason, inline=False)
    
    try:
        # Try to DM user
        dm_embed = discord.Embed(
            title=f"Kicked from {ctx.guild.name}",
            description=f"You have been kicked by a moderator.",
            color=discord.Color.red()
        )
        dm_embed.add_field(name="Reason", value=reason)
        await member.send(embed=dm_embed)
    except:
        pass
    
    await member.kick(reason=reason)
    await ctx.send(embed=embed)
    
    # Log to channel
    await bot.log_to_channel(ctx.guild.id, embed)


@bot.hybrid_command(name='ban', description='Ban a user from the server')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    """Ban a user."""
    if member.top_role >= ctx.author.top_role:
        await ctx.send("❌ You cannot ban this user!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🔨 User Banned",
        color=discord.Color.dark_red(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="User", value=f"{member.mention} ({member})", inline=True)
    embed.add_field(name="Banned by", value=ctx.author.mention, inline=True)
    embed.add_field(name="Reason", value=reason, inline=False)
    
    try:
        dm_embed = discord.Embed(
            title=f"Banned from {ctx.guild.name}",
            description=f"You have been permanently banned.",
            color=discord.Color.dark_red()
        )
        dm_embed.add_field(name="Reason", value=reason)
        await member.send(embed=dm_embed)
    except:
        pass
    
    await member.ban(reason=reason, delete_message_days=1)
    await ctx.send(embed=embed)
    
    # Log to channel
    await bot.log_to_channel(ctx.guild.id, embed)


@bot.hybrid_command(name='timeout', description='Timeout a user')
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, duration: int, *, reason: str = "No reason provided"):
    """Timeout a user (duration in minutes)."""
    if member.top_role >= ctx.author.top_role:
        await ctx.send("❌ You cannot timeout this user!", ephemeral=True)
        return
    
    await member.timeout(timedelta(minutes=duration), reason=reason)
    
    embed = discord.Embed(
        title="⏱️ User Timed Out",
        color=discord.Color.orange(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="User", value=member.mention, inline=True)
    embed.add_field(name="Duration", value=f"{duration} minutes", inline=True)
    embed.add_field(name="Reason", value=reason, inline=False)
    
    await ctx.send(embed=embed)
    
    # Log to channel
    await bot.log_to_channel(ctx.guild.id, embed)


@bot.hybrid_command(name='purge', description='Delete multiple messages')
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    """Delete multiple messages."""
    if amount < 1 or amount > 100:
        await ctx.send("❌ Please specify a number between 1 and 100!", ephemeral=True)
        return
    
    deleted = await ctx.channel.purge(limit=amount + 1)
    
    embed = discord.Embed(
        title="🗑️ Messages Deleted",
        description=f"Deleted {len(deleted)-1} messages",
        color=discord.Color.green()
    )
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(3)
    await msg.delete()


# ============= ABUSE DETECTION COMMANDS =============

@bot.hybrid_command(name='scan', description='Scan a message for abusive content')
@commands.has_permissions(manage_messages=True)
async def scan(ctx, *, text: str):
    """Manually scan a message."""
    analysis = bot.abuse_detector.analyze_message(text)
    
    embed = discord.Embed(
        title="🔍 Abuse Detection Analysis",
        color=discord.Color.red() if analysis['is_abusive'] else discord.Color.green()
    )
    
    embed.add_field(name="Abusive", value="✅ Yes" if analysis['is_abusive'] else "❌ No", inline=True)
    embed.add_field(name="Severity", value=analysis['severity'].upper(), inline=True)
    embed.add_field(name="Score", value=f"{analysis['abuse_score']}/1.0", inline=True)
    embed.add_field(name="Sentiment", value=str(analysis['sentiment']), inline=True)
    
    if analysis['detected_keywords']:
        embed.add_field(
            name="Detected Keywords",
            value=", ".join(analysis['detected_keywords']),
            inline=False
        )
    
    await ctx.send(embed=embed)


@bot.hybrid_command(name='history', description='View abuse history for a user')
@commands.has_permissions(manage_messages=True)
async def history(ctx, user: discord.User, limit: int = 5):
    """View abuse history for a user."""
    records = bot.forensics_logger.get_user_history(str(user.id), limit)
    
    if not records:
        embed = discord.Embed(
            title="📋 Clean Record",
            description=f"{user.mention} has no abuse records",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(
        title=f"📋 Abuse History - {user.name}",
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


@bot.hybrid_command(name='stats', description='View moderation statistics')
@commands.has_permissions(manage_messages=True)
async def stats(ctx):
    """View statistics."""
    stats = bot.forensics_logger.get_statistics()
    
    embed = discord.Embed(
        title="📊 Guardify Statistics",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(name="📝 Total Cases", value=str(stats.get('total_cases', 0)), inline=True)
    embed.add_field(name="👥 Unique Users", value=str(stats.get('unique_users', 0)), inline=True)
    embed.add_field(name="🏰 Servers", value=str(stats.get('unique_guilds', 0)), inline=True)
    
    severity = stats.get('severity_breakdown', {})
    embed.add_field(
        name="⚠️ Severity Breakdown",
        value=f"🟢 Low: {severity.get('low', 0)}\n"
              f"🟡 Medium: {severity.get('medium', 0)}\n"
              f"🔴 High: {severity.get('high', 0)}",
        inline=False
    )
    
    await ctx.send(embed=embed)


@bot.hybrid_command(name='export', description='Export forensics data for analysis')
@commands.has_permissions(administrator=True)
async def export_data(ctx):
    """
    Export evidence data in CSV format for analysis.
    
    Perfect for importing into Excel, pandas, or data visualization tools.
    """
    csv_path = bot.forensics_logger.csv_file
    
    if not os.path.exists(csv_path):
        await ctx.send("❌ No evidence data available to export.", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="📊 Forensics Data Export",
        description="Evidence data ready for analysis",
        color=discord.Color.blue()
    )
    
    # Get file size
    file_size = os.path.getsize(csv_path) / 1024  # KB
    
    embed.add_field(name="Format", value="CSV (Comma-Separated Values)", inline=True)
    embed.add_field(name="File Size", value=f"{file_size:.2f} KB", inline=True)
    embed.add_field(
        name="📈 Compatible With",
        value="• Microsoft Excel\n• Google Sheets\n• Python pandas\n• Matplotlib\n• Data visualization tools",
        inline=False
    )
    embed.add_field(
        name="🔐 Data Integrity",
        value="Each record includes SHA-256 hash for verification",
        inline=False
    )
    
    await ctx.send(embed=embed)
    await ctx.send(file=discord.File(csv_path, filename="guardify_evidence_export.csv"))


@bot.hybrid_command(name='prevention', description='Get prevention tips and guidance')
@commands.has_permissions(manage_messages=True)
async def prevention_tips(ctx):
    """
    Display comprehensive prevention tips and resources.
    
    Helps educators and moderators prevent escalation of harmful behavior.
    """
    embed = discord.Embed(
        title="🛡️ Abuse Prevention Guide",
        description="Evidence-based strategies for preventing online harassment",
        color=discord.Color.blue(),
        timestamp=datetime.now(timezone.utc)
    )
    
    embed.add_field(
        name="🚨 High-Risk Situations",
        value="• Document all evidence immediately\n"
              "• Contact appropriate authorities\n"
              "• Provide mental health resources\n"
              "• Implement immediate cooling-off period\n"
              "• Notify parents/guardians if minors involved",
        inline=False
    )
    
    embed.add_field(
        name="⚠️ Medium-Risk Prevention",
        value="• Review community guidelines together\n"
              "• Enable auto-moderation features\n"
              "• Increase monitoring frequency\n"
              "• Provide educational resources\n"
              "• Schedule conflict resolution session",
        inline=False
    )
    
    embed.add_field(
        name="💡 Low-Risk Best Practices",
        value="• Gentle reminders about respectful communication\n"
              "• Share positive behavior examples\n"
              "• Encourage empathy and understanding\n"
              "• Monitor for pattern changes\n"
              "• Foster inclusive community culture",
        inline=False
    )
    
    embed.add_field(
        name="📚 Resources",
        value="• [Cyberbullying Research Center](https://cyberbullying.org)\n"
              "• [National Suicide Prevention Lifeline](https://988lifeline.org)\n"
              "• [Crisis Text Line](https://www.crisistextline.org)\n"
              "• [StopBullying.gov](https://www.stopbullying.gov)",
        inline=False
    )
    
    embed.add_field(
        name="🔧 Guardify Tools",
        value="`/scan` - Analyze specific messages\n"
              "`/automod enable` - Automatic detection\n"
              "`/setlog` - Configure logging\n"
              "`/export` - Export data for analysis",
        inline=False
    )
    
    embed.set_footer(text="Early intervention prevents escalation")
    
    await ctx.send(embed=embed)


@bot.hybrid_command(name='setwelcome', description='Set welcome channel and message')
@commands.has_permissions(administrator=True)
async def setwelcome(ctx, channel: discord.TextChannel = None, *, message: str = None):
    """Set or clear the welcome channel and custom message.
    
    Placeholders:
    {user} - Mentions the new member
    {server} - Server name
    {count} - Member count
    """
    if channel is None:
        # Clear welcome
        if str(ctx.guild.id) in bot.welcome_channels:
            del bot.welcome_channels[str(ctx.guild.id)]
            if str(ctx.guild.id) in bot.welcome_messages:
                del bot.welcome_messages[str(ctx.guild.id)]
            bot.save_welcome_config()
            await ctx.send("✅ Welcome messages disabled.", ephemeral=True)
        else:
            await ctx.send("❌ Welcome messages are not currently enabled.", ephemeral=True)
    else:
        # Set welcome channel
        bot.welcome_channels[str(ctx.guild.id)] = str(channel.id)
        
        # Set custom message if provided
        if message:
            bot.welcome_messages[str(ctx.guild.id)] = message
        
        bot.save_welcome_config()
        
        embed = discord.Embed(
            title="✅ Welcome Messages Enabled",
            description=f"New members will be welcomed in {channel.mention}",
            color=discord.Color.green()
        )
        
        if message:
            embed.add_field(
                name="📝 Custom Message",
                value=message,
                inline=False
            )
        else:
            embed.add_field(
                name="📝 Message",
                value="Using default welcome message",
                inline=False
            )
        
        embed.add_field(
            name="💡 Placeholders",
            value="`{user}` - Mention member\n"
                  "`{server}` - Server name\n"
                  "`{count}` - Member count",
            inline=False
        )
        embed.add_field(
            name="🔧 Example",
            value="`/setwelcome #general Welcome {user} to {server}! You are member #{count}!`",
            inline=False
        )
        
        await ctx.send(embed=embed)

@bot.hybrid_command(name='setlog', description='Set the channel for moderation logs')
@commands.has_permissions(administrator=True)
async def setlog(ctx, channel: discord.TextChannel = None):
    """Set or clear the log channel."""
    if channel is None:
        # Clear log channel
        if str(ctx.guild.id) in bot.log_channels:
            del bot.log_channels[str(ctx.guild.id)]
            bot.save_log_channels()
            await ctx.send("✅ Log channel cleared. Moderation logs will no longer be posted.", ephemeral=True)
        else:
            await ctx.send("❌ No log channel is currently set.", ephemeral=True)
    else:
        # Set log channel
        bot.log_channels[str(ctx.guild.id)] = str(channel.id)
        bot.save_log_channels()
        
        embed = discord.Embed(
            title="✅ Log Channel Set",
            description=f"Moderation logs will now be posted to {channel.mention}",
            color=discord.Color.green()
        )
        embed.add_field(
            name="📋 What Gets Logged",
            value="• Auto-moderation actions\n"
                  "• Warnings issued\n"
                  "• Kicks and bans\n"
                  "• Timeouts\n"
                  "• Abuse detections",
            inline=False
        )
        await ctx.send(embed=embed)


@bot.hybrid_command(name='automod', description='Enable/disable auto-moderation')
@commands.has_permissions(administrator=True)
async def automod(ctx, action: str):
    """Enable or disable auto-moderation."""
    if action.lower() not in ['enable', 'disable']:
        await ctx.send("❌ Use: `/automod enable` or `/automod disable`", ephemeral=True)
        return
    
    bot.auto_mod_enabled[ctx.guild.id] = (action.lower() == 'enable')
    
    embed = discord.Embed(
        title="🛡️ Auto-Moderation " + ("Enabled" if action.lower() == 'enable' else "Disabled"),
        description="Auto-moderation will " + ("now automatically delete abusive messages and issue warnings." if action.lower() == 'enable' else "no longer automatically take action."),
        color=discord.Color.green() if action.lower() == 'enable' else discord.Color.red()
    )
    
    await ctx.send(embed=embed)


@bot.command(name='sync')
@commands.is_owner()
async def sync(ctx):
    """Manually sync slash commands (Owner only)."""
    try:
        synced = await bot.tree.sync()
        await ctx.send(f"✅ Synced {len(synced)} commands!")
    except Exception as e:
        await ctx.send(f"❌ Failed to sync: {e}")


@bot.hybrid_command(name='bothelp', description='Show all available commands')
async def help_command(ctx):
    """Show help."""
    embed = discord.Embed(
        title="🛡️ Guardify Help",
        description="Advanced Discord Moderation Bot",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🛡️ Moderation Commands",
        value="`/warn` - Warn a user\n"
              "`/kick` - Kick a user\n"
              "`/ban` - Ban a user\n"
              "`/timeout` - Timeout a user\n"
              "`/purge` - Delete messages\n"
              "`/removewarn` - Remove a specific warning",
        inline=False
    )
    
    embed.add_field(
        name="🔍 Detection Commands",
        value="`/scan` - Scan a message\n"
              "`/history` - View abuse history\n"
              "`/stats` - View statistics\n"
              "`/warnings` - View user warnings\n"
              "`/clearwarnings` - Clear all warnings",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Settings",
        value="`/automod enable/disable` - Toggle auto-moderation\n"
              "`/setlog #channel` - Set moderation log channel\n"
              "`/setwelcome #channel [message]` - Set welcome messages",
        inline=False
    )
    
    embed.add_field(
        name="🤖 Auto Features",
        value="• Automatic abuse detection\n"
              "• Spam prevention\n"
              "• Welcome messages\n"
              "• Forensics logging",
        inline=False
    )
    
    embed.set_footer(text="Use /command for detailed help on each command")
    
    await ctx.send(embed=embed)


def main():
    """Main entry point."""
    token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not token:
        config_file = 'config.json'
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                token = config.get('bot_token')
    
    if not token:
        print("ERROR: Discord bot token not found!")
        return
    
    bot.run(token)


if __name__ == "__main__":
    main()
