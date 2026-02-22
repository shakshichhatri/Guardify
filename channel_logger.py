"""
Logging System - Send all bot actions to a dedicated Discord channel
Tracks warnings, mutes, detections, and system events
"""

import discord
from discord.ext import commands
from typing import Dict, Optional
from datetime import datetime
import json
import os


class ChannelLogger:
    """Logs bot actions to a dedicated Discord channel"""
    
    def __init__(self, log_dir: str = "forensics_logs"):
        self.log_dir = log_dir
        self.config_file = os.path.join(log_dir, "logging_config.json")
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """Load logging configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def save_config(self):
        """Save logging configuration"""
        os.makedirs(self.log_dir, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def set_log_channel(self, guild_id: str, channel_id: str) -> bool:
        """Set the logging channel for a guild"""
        self.config[guild_id] = {
            "log_channel_id": channel_id,
            "created_at": datetime.utcnow().isoformat(),
            "enabled": True
        }
        self.save_config()
        return True
    
    def get_log_channel_id(self, guild_id: str) -> Optional[str]:
        """Get the log channel ID for a guild"""
        if guild_id in self.config:
            return self.config[guild_id].get("log_channel_id")
        return None
    
    def is_logging_enabled(self, guild_id: str) -> bool:
        """Check if logging is enabled for a guild"""
        if guild_id in self.config:
            return self.config[guild_id].get("enabled", False)
        return False
    
    def disable_logging(self, guild_id: str) -> bool:
        """Disable logging for a guild"""
        if guild_id in self.config:
            self.config[guild_id]["enabled"] = False
            self.save_config()
            return True
        return False
    
    def enable_logging(self, guild_id: str) -> bool:
        """Enable logging for a guild"""
        if guild_id in self.config:
            self.config[guild_id]["enabled"] = True
            self.save_config()
            return True
        return False
    
    async def log_message(self, guild: discord.Guild, title: str, description: str, 
                         color: discord.Color = None, fields: Dict = None):
        """Send a log message to the logging channel"""
        try:
            guild_id = str(guild.id)
            
            if not self.is_logging_enabled(guild_id):
                return False
            
            channel_id = self.get_log_channel_id(guild_id)
            if not channel_id:
                return False
            
            channel = guild.get_channel(int(channel_id))
            if not channel:
                return False
            
            # Create embed
            embed = discord.Embed(
                title=title,
                description=description,
                color=color or discord.Color.blue(),
                timestamp=datetime.utcnow()
            )
            
            # Add fields if provided
            if fields:
                for field_name, field_value in fields.items():
                    embed.add_field(name=field_name, value=field_value, inline=True)
            
            embed.set_footer(text="Guardify Logging System")
            
            # Send to channel (keep message, don't delete)
            await channel.send(embed=embed)
            return True
        
        except Exception as e:
            print(f"[ERROR] Failed to log message: {e}")
            return False
    
    async def log_warning(self, guild: discord.Guild, member: discord.Member, 
                         warning_count: int, reason: str, severity: str):
        """Log a warning to the channel"""
        fields = {
            "👤 User": f"{member.mention} ({member.id})",
            "⚠️ Warning #": f"{warning_count}/5",
            "📝 Reason": reason[:200],
            "🔴 Severity": severity.upper(),
            "⏰ Time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        
        emoji = "⚠️" if warning_count < 5 else "🚫"
        color = discord.Color.orange() if warning_count < 5 else discord.Color.red()
        
        await self.log_message(
            guild,
            f"{emoji} Warning Issued",
            f"User {member.mention} received a warning.",
            color=color,
            fields=fields
        )
    
    async def log_mute(self, guild: discord.Guild, member: discord.Member, 
                      duration: int, reason: str):
        """Log a mute action"""
        fields = {
            "👤 User": f"{member.mention} ({member.id})",
            "⏱️ Duration": f"{duration} minutes",
            "📝 Reason": reason[:200],
            "⏰ Time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        
        await self.log_message(
            guild,
            "🔇 User Muted",
            f"{member.mention} has been muted.",
            color=discord.Color.red(),
            fields=fields
        )
    
    async def log_unmute(self, guild: discord.Guild, member: discord.Member):
        """Log an unmute action"""
        fields = {
            "👤 User": f"{member.mention} ({member.id})",
            "⏰ Time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        
        await self.log_message(
            guild,
            "🔊 User Unmuted",
            f"{member.mention} has been unmuted.",
            color=discord.Color.green(),
            fields=fields
        )
    
    async def log_detection(self, guild: discord.Guild, member: discord.Member, 
                           content: str, category: str, severity: str, detected_items: list):
        """Log content detection"""
        detected_str = ", ".join(detected_items[:3]) if detected_items else "N/A"
        
        fields = {
            "👤 User": f"{member.mention} ({member.id})",
            "🔍 Category": category.upper(),
            "🔴 Severity": severity.upper(),
            "🚨 Detected": detected_str,
            "📝 Content": f"```{content[:100]}...```" if len(content) > 100 else f"```{content}```",
            "⏰ Time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        
        await self.log_message(
            guild,
            f"🚨 {category.upper()} Detected",
            f"Offensive content detected from {member.mention}.",
            color=discord.Color.dark_red(),
            fields=fields
        )
    
    async def log_clearwarnings(self, guild: discord.Guild, member: discord.Member, 
                               moderator: discord.Member):
        """Log warnings cleared"""
        fields = {
            "👤 User": f"{member.mention} ({member.id})",
            "👮 Moderator": f"{moderator.mention} ({moderator.id})",
            "⏰ Time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        
        await self.log_message(
            guild,
            "✅ Warnings Cleared",
            f"All warnings for {member.mention} have been cleared.",
            color=discord.Color.green(),
            fields=fields
        )
    
    async def log_system_event(self, guild: discord.Guild, event_type: str, 
                              message: str, details: Dict = None):
        """Log system events"""
        fields = details or {}
        fields["⏰ Time"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        await self.log_message(
            guild,
            f"⚙️ {event_type}",
            message,
            color=discord.Color.greyple(),
            fields=fields
        )


# Singleton instance
_logger_instance = None

def get_channel_logger() -> ChannelLogger:
    """Get or create singleton instance"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = ChannelLogger()
    return _logger_instance
