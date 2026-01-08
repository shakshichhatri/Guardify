# Guardify Web Dashboard Guide

## Overview
The Guardify Web Dashboard provides a real-time view of your bot's moderation statistics and activity across all servers.

## Starting the Dashboard

1. **Install Dependencies** (if not already done):
   ```bash
   pip install Flask
   ```

2. **Run the Dashboard**:
   ```bash
   python web_dashboard.py
   ```

3. **Access the Dashboard**:
   - Open your browser and navigate to: `http://localhost:5000`
   - Or access from another device on your network: `http://YOUR_IP:5000`

## Dashboard Features

### Main Page (`/`)
- Landing page with bot information
- Quick navigation to dashboard

### Dashboard (`/dashboard`)
- **Real-time Statistics**:
  - Total abuse cases detected
  - Severity breakdown (Low/Medium/High)
  - Unique users monitored
  - Active servers count
  
- **Recent Activity Feed**:
  - Latest 10 abuse detections
  - Message content and analysis
  - Timestamp and user information

- **Warning Statistics**:
  - Top 10 warned users
  - Warning counts per user
  - Last warning timestamps

### API Endpoint (`/api/stats`)
Returns JSON data with:
- Complete statistics
- Warning information
- Recent cases

Example response:
```json
{
  "stats": {
    "total_cases": 45,
    "severity_breakdown": {
      "low": 20,
      "medium": 15,
      "high": 10
    },
    "unique_users": 12,
    "unique_guilds": 3,
    "recent_cases": [...]
  },
  "warnings": [...]
}
```

## Discord Integration

### Setting Up Log Channel

Use the `/setlog` command in your Discord server:

```
/setlog #mod-logs
```

This will configure the bot to send all moderation logs to the specified channel.

### What Gets Logged

The bot automatically logs:
- ✅ Auto-moderation actions
- ✅ Warnings issued
- ✅ Kicks and bans
- ✅ Timeouts
- ✅ Abuse detections

### Log Format

Each log entry includes:
- Action taken
- Target user
- Moderator (if applicable)
- Reason
- Timestamp
- Additional context (warnings count, severity, etc.)

## Configuration

### Port Change
To change the dashboard port, edit `web_dashboard.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change 5000 to your desired port
```

### Log Directory
The dashboard reads from the `forensics_logs` directory by default. To change:
```python
LOGS_DIR = "your_custom_directory"  # Edit this line in web_dashboard.py
```

## Troubleshooting

### Dashboard Won't Start
- Ensure Flask is installed: `pip install Flask`
- Check if port 5000 is already in use
- Verify templates folder exists with HTML files

### No Data Showing
- Ensure the bot has been running and detecting abuse
- Check that `forensics_logs/abuse_evidence.jsonl` exists
- Verify warnings.json is present in forensics_logs

### Can't Access from Other Devices
- Check firewall settings
- Ensure you're using the correct IP address
- Verify the device is on the same network

## Production Deployment

⚠️ **Important**: The built-in Flask server is for development only.

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_dashboard:app
```

Or use Waitress (Windows-friendly):

```bash
pip install waitress
waitress-serve --port=5000 web_dashboard:app
```

## Security Notes

- The dashboard currently has no authentication
- Only expose it on trusted networks
- Consider adding authentication for production use
- Don't expose sensitive data publicly

## Auto-Refresh

The dashboard automatically refreshes statistics every 30 seconds to show the latest data without manual page reloads.
