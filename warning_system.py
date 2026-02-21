"""
Warning System & Mute Management Module
Handles persistent warning storage, tracking, and automatic muting
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import asyncio


class WarningManager:
    """Manages user warnings, tracking, and automatic muting"""
    
    def __init__(self, log_dir: str = "forensics_logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.warnings_file = os.path.join(log_dir, "user_warnings.json")
        self.mutes_file = os.path.join(log_dir, "user_mutes.json")
        
        # Load existing data
        self.warnings = self.load_warnings()
        self.active_mutes = self.load_mutes()
    
    def load_warnings(self) -> Dict:
        """Load warnings from persistent storage"""
        if os.path.exists(self.warnings_file):
            try:
                with open(self.warnings_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def save_warnings(self):
        """Save warnings to persistent storage"""
        with open(self.warnings_file, 'w') as f:
            json.dump(self.warnings, f, indent=2)
    
    def load_mutes(self) -> Dict:
        """Load active mutes from persistent storage"""
        if os.path.exists(self.mutes_file):
            try:
                with open(self.mutes_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def save_mutes(self):
        """Save mutes to persistent storage"""
        with open(self.mutes_file, 'w') as f:
            json.dump(self.active_mutes, f, indent=2)
    
    def add_warning(self, user_id: str, guild_id: str, reason: str, 
                   severity: str = "medium", content: str = "") -> int:
        """
        Add a warning to a user
        
        Args:
            user_id: Discord user ID
            guild_id: Guild ID where warning occurred
            reason: Reason for warning
            severity: Severity level (low, medium, high, critical)
            content: The offensive content
        
        Returns:
            Total warning count for the user in this guild
        """
        key = f"{guild_id}:{user_id}"
        
        if key not in self.warnings:
            self.warnings[key] = {
                "user_id": user_id,
                "guild_id": guild_id,
                "warnings": [],
                "created_at": datetime.utcnow().isoformat()
            }
        
        warning = {
            "id": len(self.warnings[key]["warnings"]) + 1,
            "reason": reason,
            "severity": severity,
            "content": content[:200],  # Limit content length
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.warnings[key]["warnings"].append(warning)
        self.save_warnings()
        
        return len(self.warnings[key]["warnings"])
    
    def get_warning_count(self, user_id: str, guild_id: str) -> int:
        """Get total warnings for a user in a guild"""
        key = f"{guild_id}:{user_id}"
        if key in self.warnings:
            return len(self.warnings[key]["warnings"])
        return 0
    
    def get_warnings(self, user_id: str, guild_id: str, limit: int = 10) -> List[Dict]:
        """Get warnings for a user in a guild"""
        key = f"{guild_id}:{user_id}"
        if key in self.warnings:
            return self.warnings[key]["warnings"][-limit:]
        return []
    
    def clear_warnings(self, user_id: str, guild_id: str) -> bool:
        """Clear all warnings for a user in a guild"""
        key = f"{guild_id}:{user_id}"
        if key in self.warnings:
            del self.warnings[key]
            self.save_warnings()
            return True
        return False
    
    def remove_warning(self, user_id: str, guild_id: str, warning_id: int) -> bool:
        """Remove a specific warning"""
        key = f"{guild_id}:{user_id}"
        if key in self.warnings:
            self.warnings[key]["warnings"] = [
                w for w in self.warnings[key]["warnings"] if w.get("id") != warning_id
            ]
            self.save_warnings()
            return True
        return False
    
    def create_mute(self, user_id: str, guild_id: str, duration_minutes: int = 10,
                   reason: str = "") -> Dict:
        """
        Create a mute record
        
        Args:
            user_id: Discord user ID
            guild_id: Guild ID
            duration_minutes: Duration of mute in minutes
            reason: Reason for mute
        
        Returns:
            Mute record with expiry time
        """
        mute_key = f"{guild_id}:{user_id}"
        
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        mute_record = {
            "user_id": user_id,
            "guild_id": guild_id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_minutes": duration_minutes,
            "reason": reason,
            "is_active": True,
            "mute_role_assigned": False
        }
        
        self.active_mutes[mute_key] = mute_record
        self.save_mutes()
        
        return mute_record
    
    def get_mute(self, user_id: str, guild_id: str) -> Optional[Dict]:
        """Get active mute record for a user"""
        mute_key = f"{guild_id}:{user_id}"
        
        if mute_key in self.active_mutes:
            mute = self.active_mutes[mute_key]
            
            # Check if mute has expired
            end_time = datetime.fromisoformat(mute["end_time"])
            if datetime.utcnow() > end_time:
                mute["is_active"] = False
                self.save_mutes()
                return None
            
            return mute
        
        return None
    
    def is_user_muted(self, user_id: str, guild_id: str) -> bool:
        """Check if user is currently muted"""
        return self.get_mute(user_id, guild_id) is not None
    
    def end_mute(self, user_id: str, guild_id: str) -> bool:
        """End a mute early"""
        mute_key = f"{guild_id}:{user_id}"
        
        if mute_key in self.active_mutes:
            self.active_mutes[mute_key]["is_active"] = False
            self.active_mutes[mute_key]["end_time"] = datetime.utcnow().isoformat()
            self.save_mutes()
            return True
        
        return False
    
    def mark_mute_role_assigned(self, user_id: str, guild_id: str) -> bool:
        """Mark that mute role has been assigned to user"""
        mute_key = f"{guild_id}:{user_id}"
        
        if mute_key in self.active_mutes:
            self.active_mutes[mute_key]["mute_role_assigned"] = True
            self.save_mutes()
            return True
        
        return False
    
    def get_expired_mutes(self) -> List[Dict]:
        """Get all mutes that have expired"""
        expired = []
        now = datetime.utcnow()
        
        for key, mute in self.active_mutes.items():
            if mute.get("is_active"):
                end_time = datetime.fromisoformat(mute["end_time"])
                if now > end_time:
                    expired.append(mute)
        
        return expired
    
    def get_statistics(self, guild_id: str = None) -> Dict:
        """Get warning and mute statistics"""
        stats = {
            "total_users_warned": 0,
            "total_warnings": 0,
            "total_active_mutes": 0,
            "severity_breakdown": {"low": 0, "medium": 0, "high": 0, "critical": 0},
            "guilds_affected": set()
        }
        
        for key, user_data in self.warnings.items():
            if guild_id and not key.startswith(guild_id):
                continue
                
            stats["total_users_warned"] += 1
            stats["guilds_affected"].add(user_data["guild_id"])
            
            for warning in user_data["warnings"]:
                stats["total_warnings"] += 1
                severity = warning.get("severity", "medium")
                stats["severity_breakdown"][severity] = stats["severity_breakdown"].get(severity, 0) + 1
        
        # Count active mutes
        now = datetime.utcnow()
        for mute in self.active_mutes.values():
            if mute.get("is_active"):
                end_time = datetime.fromisoformat(mute["end_time"])
                if now < end_time:
                    stats["total_active_mutes"] += 1
        
        stats["guilds_affected"] = len(stats["guilds_affected"])
        
        return stats
    
    def cleanup_expired_mutes(self):
        """Clean up expired mute records"""
        now = datetime.utcnow()
        expired_keys = []
        
        for key, mute in self.active_mutes.items():
            if mute.get("is_active"):
                end_time = datetime.fromisoformat(mute["end_time"])
                if now > end_time:
                    expired_keys.append(key)
        
        for key in expired_keys:
            del self.active_mutes[key]
        
        if expired_keys:
            self.save_mutes()
        
        return len(expired_keys)


class MuteRoleManager:
    """Manages mute roles and channel permissions"""
    
    def __init__(self, log_dir: str = "forensics_logs"):
        self.log_dir = log_dir
        self.role_config_file = os.path.join(log_dir, "mute_roles.json")
        self.role_config = self.load_role_config()
    
    def load_role_config(self) -> Dict:
        """Load mute role configuration"""
        if os.path.exists(self.role_config_file):
            try:
                with open(self.role_config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def save_role_config(self):
        """Save mute role configuration"""
        with open(self.role_config_file, 'w') as f:
            json.dump(self.role_config, f, indent=2)
    
    def set_mute_role(self, guild_id: str, role_id: str) -> bool:
        """Set the mute role for a guild"""
        self.role_config[guild_id] = {
            "mute_role_id": role_id,
            "created_at": datetime.utcnow().isoformat()
        }
        self.save_role_config()
        return True
    
    def get_mute_role(self, guild_id: str) -> Optional[str]:
        """Get the mute role ID for a guild"""
        if guild_id in self.role_config:
            return self.role_config[guild_id].get("mute_role_id")
        return None
    
    def has_mute_role(self, guild_id: str) -> bool:
        """Check if guild has a mute role configured"""
        return guild_id in self.role_config


# Singleton instances
_warning_manager = None
_mute_role_manager = None

def get_warning_manager() -> WarningManager:
    """Get or create singleton instance"""
    global _warning_manager
    if _warning_manager is None:
        _warning_manager = WarningManager()
    return _warning_manager

def get_mute_role_manager() -> MuteRoleManager:
    """Get or create singleton instance"""
    global _mute_role_manager
    if _mute_role_manager is None:
        _mute_role_manager = MuteRoleManager()
    return _mute_role_manager
