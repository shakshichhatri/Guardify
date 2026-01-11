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
    
    # Configurable thresholds
    SENTIMENT_THRESHOLD = -0.3  # Negative sentiment threshold
    KEYWORD_WEIGHT = 0.4
    ABUSE_SCORE_THRESHOLD = 0.4  # Minimum score to classify as abusive
    
    def __init__(self):
        # List of abusive keywords/phrases (expandable)
        self.abusive_keywords = [
            'hate', 'kill', 'stupid', 'idiot', 'loser', 'trash',
            'worthless', 'pathetic', 'disgusting', 'die', 'kys',
            'retard', 'moron', 'dumb', 'ugly', 'fat', 'nazi'
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
        
        # Keyword detection with word boundary matching to avoid false positives
        detected_keywords = []
        for keyword in self.abusive_keywords:
            # Use word boundaries to match whole words only
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, content_lower):
                detected_keywords.append(keyword)
        
        # Calculate abuse score
        keyword_score = len(detected_keywords) * self.KEYWORD_WEIGHT
        sentiment_score = abs(min(sentiment, 0))
        
        abuse_score = keyword_score + sentiment_score
        
        # Classification
        is_abusive = abuse_score > self.ABUSE_SCORE_THRESHOLD or sentiment < self.SENTIMENT_THRESHOLD
        
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


@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    """
    Kick a member from the server.
    Usage: !kick @user [reason]
    """
    try:
        await member.kick(reason=f"{reason} | Kicked by {ctx.author}")
        embed = discord.Embed(
            title="Member Kicked",
            description=f"{member.mention} has been kicked from the server.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
        await ctx.send(embed=embed)
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
        embed = discord.Embed(
            title="Member Banned",
            description=f"{member.mention} has been banned from the server.",
            color=discord.Color.red()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
        await ctx.send(embed=embed)
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
        embed = discord.Embed(
            title="Member Unbanned",
            description=f"{user.mention} has been unbanned from the server.",
            color=discord.Color.green()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
        await ctx.send(embed=embed)
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
        embed = discord.Embed(
            title="Member Timed Out",
            description=f"{member.mention} has been timed out for {duration} minutes.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
        await ctx.send(embed=embed)
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
        title="Guardify - Help",
        description="AI-enabled Discord bot for detecting and preventing digital abuse",
        color=discord.Color.purple()
    )
    
    embed.add_field(
        name="🤖 Automatic Detection",
        value="The bot automatically monitors all messages for abusive content and logs evidence.",
        inline=False
    )
    
    embed.add_field(
        name="📋 Abuse Detection",
        value="`!scan <message>` - Manually scan text\n`!history @user` - View abuse history\n`!stats` - Detection statistics",
        inline=False
    )
    
    embed.add_field(
        name="🔨 Moderation",
        value="`!kick @user [reason]` - Kick member\n`!ban @user [reason]` - Ban member\n`!unban <id> [reason]` - Unban user\n`!timeout @user <min> [reason]` - Timeout member\n`!untimeout @user` - Remove timeout",
        inline=False
    )
    
    embed.add_field(
        name="⚠️ Warnings",
        value="`!warn @user [reason]` - Warn member\n`!warnings @user` - Check warnings",
        inline=False
    )
    
    embed.add_field(
        name="🧹 Channel Management",
        value="`!clear [amount]` - Delete messages\n`!slowmode <sec>` - Set slowmode\n`!lock` - Lock channel\n`!unlock` - Unlock channel",
        inline=False
    )
    
    embed.add_field(
        name="📊 Information",
        value="`!serverinfo` - Server details\n`!userinfo [@user]` - User details",
        inline=False
    )
    
    embed.set_footer(text="Use !help_guardify to see this message again")
    
    await ctx.send(embed=embed)


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
