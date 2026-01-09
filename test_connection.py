"""
Test bot connection to verify setup
"""
import discord
import os
import json

# Load token
token = os.getenv('DISCORD_BOT_TOKEN')
if not token:
    config_file = 'config.json'
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            token = config.get('bot_token')

if not token:
    print("ERROR: No bot token found!")
    print("Please set DISCORD_BOT_TOKEN environment variable or create config.json")
    exit(1)

print(f"Token found: {token[:20]}...")

# Setup intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

# Create simple bot
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Bot logged in as {client.user}')
    print(f'✅ Bot is in {len(client.guilds)} servers')
    print('✅ Bot is ONLINE and running!')
    print('Press Ctrl+C to stop')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f'Message from {message.author}: {message.content[:50]}')

print("Starting bot...")
try:
    client.run(token)
except Exception as e:
    print(f"ERROR: {e}")
    print("\nPossible issues:")
    print("1. Invalid bot token")
    print("2. Message Content Intent not enabled in Discord Developer Portal")
    print("3. Bot not invited to any servers")
