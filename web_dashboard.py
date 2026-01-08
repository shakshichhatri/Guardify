"""
Guardify Web Dashboard
Simple web interface for viewing bot statistics and logs
"""

from flask import Flask, render_template, jsonify, session, redirect, url_for, request
import json
import os
from datetime import datetime
from collections import Counter
import requests
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

LOGS_DIR = "forensics_logs"

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)
    DISCORD_CLIENT_ID = config.get('discord_client_id')
    DISCORD_CLIENT_SECRET = config.get('discord_client_secret')
    DASHBOARD_URL = config.get('dashboard_url', 'http://localhost:5000')

DISCORD_API_BASE = 'https://discord.com/api/v10'
OAUTH2_REDIRECT_URI = f'{DASHBOARD_URL}/callback'


def login_required(f):
    """Decorator to require Discord login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def get_user_guilds():
    """Get guilds the logged-in user is in."""
    if 'access_token' not in session:
        return []
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    response = requests.get(f'{DISCORD_API_BASE}/users/@me/guilds', headers=headers)
    if response.status_code == 200:
        return response.json()
    return []


def get_statistics(guild_id=None):
    """Get bot statistics from logs."""
    log_file = os.path.join(LOGS_DIR, "abuse_evidence.jsonl")
    
    if not os.path.exists(log_file):
        return {
            "total_cases": 0,
            "severity_breakdown": {"low": 0, "medium": 0, "high": 0},
            "unique_users": 0,
            "unique_guilds": 0,
            "recent_cases": []
        }
    
    cases = []
    users = set()
    guilds = set()
    severity_count = {"low": 0, "medium": 0, "high": 0}
    
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                record = json.loads(line)
                
                # Filter by guild if specified
                if guild_id and str(record.get('guild_id')) != str(guild_id):
                    continue
                
                cases.append(record)
                users.add(record.get('author_id'))
                if record.get('guild_id'):
                    guilds.add(record.get('guild_id'))
                
                severity = record.get('analysis', {}).get('severity', 'low')
                severity_count[severity] += 1
            except:
                continue
    
    # Get 10 most recent cases
    recent_cases = sorted(cases, key=lambda x: x.get('logged_at', ''), reverse=True)[:10]
    
    return {
        "total_cases": len(cases),
        "severity_breakdown": severity_count,
        "unique_users": len(users),
        "unique_guilds": len(guilds),
        "recent_cases": recent_cases
    }


def get_warnings(guild_id=None):
    """Get warning statistics."""
    warnings_file = os.path.join(LOGS_DIR, "warnings.json")
    
    if not os.path.exists(warnings_file):
        return []
    
    with open(warnings_file, 'r') as f:
        warnings = json.load(f)
    
    warning_list = []
    for key, warns in warnings.items():
        g_id, user_id = key.split(':')
        
        # Filter by guild if specified
        if guild_id and str(g_id) != str(guild_id):
            continue
        
        warning_list.append({
            "user_id": user_id,
            "guild_id": g_id,
            "count": len(warns),
            "last_warning": warns[-1]['timestamp'] if warns else None
        })
    
    return sorted(warning_list, key=lambda x: x['count'], reverse=True)


@app.route('/')
def index():
    """Landing page."""
    user = session.get('user')
    return render_template('index.html', user=user)


@app.route('/login')
def login():
    """Redirect to Discord OAuth2."""
    oauth_url = (
        f'https://discord.com/api/oauth2/authorize'
        f'?client_id={DISCORD_CLIENT_ID}'
        f'&redirect_uri={OAUTH2_REDIRECT_URI}'
        f'&response_type=code'
        f'&scope=identify%20guilds'
    )
    return redirect(oauth_url)


@app.route('/callback')
def callback():
    """Handle OAuth2 callback."""
    code = request.args.get('code')
    
    if not code:
        return redirect(url_for('index'))
    
    # Exchange code for access token
    data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': OAUTH2_REDIRECT_URI
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(f'{DISCORD_API_BASE}/oauth2/token', data=data, headers=headers)
    
    if response.status_code != 200:
        return redirect(url_for('index'))
    
    token_data = response.json()
    session['access_token'] = token_data['access_token']
    
    # Get user info
    headers = {
        'Authorization': f"Bearer {token_data['access_token']}"
    }
    
    user_response = requests.get(f'{DISCORD_API_BASE}/users/@me', headers=headers)
    
    if user_response.status_code == 200:
        session['user'] = user_response.json()
    
    return redirect(url_for('guilds'))


@app.route('/logout')
def logout():
    """Logout user."""
    session.clear()
    return redirect(url_for('index'))


@app.route('/guilds')
@login_required
def guilds():
    """Show list of guilds user can access."""
    user_guilds = get_user_guilds()
    return render_template('guilds.html', guilds=user_guilds, user=session.get('user'))


@app.route('/dashboard')
@app.route('/dashboard/<guild_id>')
@login_required
def dashboard(guild_id=None):
    """Main dashboard page."""
    if guild_id:
        # Verify user has access to this guild
        user_guilds = get_user_guilds()
        guild_ids = [str(g['id']) for g in user_guilds]
        
        if str(guild_id) not in guild_ids:
            return "Access denied", 403
        
        # Get guild name
        guild_name = next((g['name'] for g in user_guilds if str(g['id']) == str(guild_id)), 'Unknown')
        return render_template('dashboard_new.html', guild_id=guild_id, guild_name=guild_name, user=session.get('user'))
    
    return render_template('dashboard_new.html', user=session.get('user'))


@app.route('/api/stats')
@app.route('/api/stats/<guild_id>')
def api_stats(guild_id=None):
    """API endpoint for statistics."""
    # If guild_id provided and user logged in, verify access
    if guild_id and 'user' in session:
        user_guilds = get_user_guilds()
        guild_ids = [str(g['id']) for g in user_guilds]
        
        if str(guild_id) not in guild_ids:
            return jsonify({"error": "Access denied"}), 403
    
    stats = get_statistics(guild_id)
    warnings = get_warnings(guild_id)
    
    return jsonify({
        "stats": stats,
        "warnings": warnings[:10]  # Top 10 warned users
    })


if __name__ == '__main__':
    # Create templates folder
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
