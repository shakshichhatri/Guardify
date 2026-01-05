"""
Respect Ranger Discord Bot
AI-enabled bot for detecting and logging abusive content in Discord messages.
"""

import discord
from discord.ext import commands
import json
import os
from datetime import datetime
from textblob import TextBlob
import re
from typing import Dict, List, Optional


class AbuseDetector:
    """Detects abusive content using sentiment analysis and keyword matching."""
    
    def __init__(self):
        # List of abusive keywords/phrases (expandable)
        self.abusive_keywords = [
            'hate', 'kill', 'stupid', 'idiot', 'loser', 'trash',
            'worthless', 'pathetic', 'disgusting', 'die', 'kys',
            'retard', 'moron', 'dumb', 'ugly', 'fat', 'nazi'
        ]
        
        # Severity thresholds
        self.sentiment_threshold = -0.3  # Negative sentiment threshold
        self.keyword_weight = 0.4
        
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
        
        # Keyword detection
        detected_keywords = [
            keyword for keyword in self.abusive_keywords 
            if keyword in content_lower
        ]
        
        # Calculate abuse score
        keyword_score = len(detected_keywords) * self.keyword_weight
        sentiment_score = abs(min(sentiment, 0))
        
        abuse_score = keyword_score + sentiment_score
        
        # Classification
        is_abusive = abuse_score > 0.4 or sentiment < self.sentiment_threshold
        
        severity = "low"
        if abuse_score > 0.8:
            severity = "high"
        elif abuse_score > 0.5:
            severity = "medium"
        
        return {
            "is_abusive": is_abusive,
            "abuse_score": round(abuse_score, 3),
            "sentiment": round(sentiment, 3),
            "detected_keywords": detected_keywords,
            "severity": severity,
            "timestamp": datetime.utcnow().isoformat()
        }


class ForensicsLogger:
    """Logs evidence of abusive messages for digital forensics."""
    
    def __init__(self, log_dir: str = "forensics_logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, "abuse_evidence.jsonl")
        
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
    """Main bot class for Respect Ranger."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.abuse_detector = AbuseDetector()
        self.forensics_logger = ForensicsLogger()
        
    async def on_ready(self):
        """Called when the bot is ready."""
        print(f'{self.user} has connected to Discord!')
        print(f'Bot is active in {len(self.guilds)} guilds')
        
    async def on_message(self, message: discord.Message):
        """Process every message for abuse detection."""
        # Ignore bot's own messages
        if message.author == self.user:
            return
        
        # Analyze message
        analysis = self.abuse_detector.analyze_message(message.content)
        
        # Log if abusive
        if analysis['is_abusive']:
            self.forensics_logger.log_evidence(message, analysis)
            print(f"[ABUSE DETECTED] {message.author}: {message.content[:50]}... "
                  f"(Score: {analysis['abuse_score']}, Severity: {analysis['severity']})")
        
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


@bot.command(name='help_ranger')
async def help_command(ctx):
    """
    Show bot help and available commands.
    Usage: !help_ranger
    """
    embed = discord.Embed(
        title="Respect Ranger - Help",
        description="AI-enabled Discord bot for detecting and preventing digital abuse",
        color=discord.Color.purple()
    )
    
    embed.add_field(
        name="🤖 Automatic Detection",
        value="The bot automatically monitors all messages for abusive content and logs evidence.",
        inline=False
    )
    
    embed.add_field(
        name="!scan <message>",
        value="Manually scan a message for abusive content (Requires: Manage Messages)",
        inline=False
    )
    
    embed.add_field(
        name="!history @user [limit]",
        value="View abuse history for a specific user (Requires: Manage Messages)",
        inline=False
    )
    
    embed.add_field(
        name="!stats",
        value="View overall abuse detection statistics (Requires: Manage Messages)",
        inline=False
    )
    
    embed.add_field(
        name="!help_ranger",
        value="Show this help message",
        inline=False
    )
    
    await ctx.send(embed=embed)


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
    
    # Run the bot
    bot.run(token)


if __name__ == "__main__":
    main()
