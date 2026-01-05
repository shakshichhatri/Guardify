"""
Example usage scenarios for Respect Ranger Discord Bot
Demonstrates various use cases and API interactions
"""

from bot import AbuseDetector, ForensicsLogger
from datetime import datetime
import json


def example_basic_detection():
    """Example 1: Basic abuse detection."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Abuse Detection")
    print("=" * 60 + "\n")
    
    detector = AbuseDetector()
    
    # Analyze a message
    message = "You are so stupid and worthless"
    result = detector.analyze_message(message)
    
    print(f"Message: '{message}'")
    print(f"\nAnalysis Results:")
    print(f"  Is Abusive: {result['is_abusive']}")
    print(f"  Abuse Score: {result['abuse_score']}")
    print(f"  Sentiment: {result['sentiment']}")
    print(f"  Severity: {result['severity']}")
    print(f"  Keywords: {result['detected_keywords']}")
    print()


def example_custom_thresholds():
    """Example 2: Customizing detection thresholds."""
    print("=" * 60)
    print("EXAMPLE 2: Custom Sensitivity Thresholds")
    print("=" * 60 + "\n")
    
    # Create detector with custom thresholds
    detector = AbuseDetector()
    
    # Show current thresholds
    print("Current Configuration:")
    print(f"  Sentiment Threshold: {detector.SENTIMENT_THRESHOLD}")
    print(f"  Keyword Weight: {detector.KEYWORD_WEIGHT}")
    print(f"  Abuse Score Threshold: {detector.ABUSE_SCORE_THRESHOLD}")
    
    # You can modify class constants for stricter/looser detection
    # For stricter detection:
    # AbuseDetector.ABUSE_SCORE_THRESHOLD = 0.3
    # For looser detection:
    # AbuseDetector.ABUSE_SCORE_THRESHOLD = 0.6
    
    print()


def example_forensics_workflow():
    """Example 3: Complete forensics workflow."""
    print("=" * 60)
    print("EXAMPLE 3: Forensics Logging Workflow")
    print("=" * 60 + "\n")
    
    # Initialize components
    detector = AbuseDetector()
    logger = ForensicsLogger(log_dir="example_logs")
    
    # Mock message class
    class Message:
        def __init__(self, content, author_id, author_name):
            self.id = 12345
            self.content = content
            self.created_at = datetime.now()
            
            class Author:
                def __init__(self, uid, name):
                    self.id = uid
                    self.name = name
                def __str__(self):
                    return self.name
            
            class Channel:
                def __init__(self):
                    self.id = 111
                    self.name = "general"
                def __str__(self):
                    return "general"
            
            class Guild:
                def __init__(self):
                    self.id = 999
                    self.name = "Example Server"
            
            self.author = Author(author_id, author_name)
            self.channel = Channel()
            self.guild = Guild()
    
    # Simulate message processing
    messages = [
        ("Hello everyone!", 101, "GoodUser"),
        ("You are an idiot", 102, "BadUser"),
        ("Have a nice day!", 101, "GoodUser"),
    ]
    
    print("Processing messages:\n")
    for content, author_id, author_name in messages:
        msg = Message(content, author_id, author_name)
        analysis = detector.analyze_message(content)
        
        print(f"Message: '{content}' by {author_name}")
        print(f"  Abusive: {analysis['is_abusive']}")
        
        if analysis['is_abusive']:
            logger.log_evidence(msg, analysis)
            print(f"  ⚠️ LOGGED TO FORENSICS")
        
        print()
    
    # Check statistics
    stats = logger.get_statistics()
    print(f"Total cases logged: {stats['total_cases']}")
    print(f"Unique users flagged: {stats['unique_users']}")
    print()


def example_batch_analysis():
    """Example 4: Batch message analysis."""
    print("=" * 60)
    print("EXAMPLE 4: Batch Message Analysis")
    print("=" * 60 + "\n")
    
    detector = AbuseDetector()
    
    messages = [
        "Great job team!",
        "This is terrible",
        "You stupid idiot",
        "Thanks for your help",
        "I hate this pathetic situation",
    ]
    
    results = []
    for msg in messages:
        analysis = detector.analyze_message(msg)
        results.append({
            'message': msg,
            'abusive': analysis['is_abusive'],
            'score': analysis['abuse_score']
        })
    
    # Sort by abuse score
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print("Messages ranked by abuse score:\n")
    for i, r in enumerate(results, 1):
        status = "🔴 ABUSIVE" if r['abusive'] else "🟢 CLEAN"
        print(f"{i}. {status} (Score: {r['score']:.2f})")
        print(f"   '{r['message']}'")
        print()


def example_user_tracking():
    """Example 5: Track user behavior over time."""
    print("=" * 60)
    print("EXAMPLE 5: User Behavior Tracking")
    print("=" * 60 + "\n")
    
    detector = AbuseDetector()
    logger = ForensicsLogger(log_dir="example_logs")
    
    # Mock user
    class Message:
        def __init__(self, content, msg_id):
            self.id = msg_id
            self.content = content
            self.created_at = datetime.now()
            
            class Author:
                id = 5555
                name = "TrackedUser"
                def __str__(self):
                    return "TrackedUser#1234"
            
            class Channel:
                id = 111
                name = "chat"
                def __str__(self):
                    return "chat"
            
            class Guild:
                id = 999
                name = "Test Server"
            
            self.author = Author()
            self.channel = Channel()
            self.guild = Guild()
    
    # Simulate user messages over time
    user_messages = [
        "You are worthless",
        "This is stupid",
        "You pathetic loser",
    ]
    
    print("Tracking user 'TrackedUser#1234':\n")
    for i, content in enumerate(user_messages, 1):
        msg = Message(content, 1000 + i)
        analysis = detector.analyze_message(content)
        
        if analysis['is_abusive']:
            logger.log_evidence(msg, analysis)
            print(f"Incident #{i}:")
            print(f"  Message: '{content}'")
            print(f"  Severity: {analysis['severity'].upper()}")
    
    # Retrieve user history
    history = logger.get_user_history('5555')
    print(f"\nTotal violations: {len(history)}")
    
    # Calculate patterns
    if history:
        avg_score = sum(h['analysis']['abuse_score'] for h in history) / len(history)
        print(f"Average abuse score: {avg_score:.2f}")
        
        severities = [h['analysis']['severity'] for h in history]
        print(f"Severity distribution: {dict((s, severities.count(s)) for s in set(severities))}")
    
    print()


def example_integration_with_discord():
    """Example 6: How to integrate with Discord bot."""
    print("=" * 60)
    print("EXAMPLE 6: Discord Bot Integration Pattern")
    print("=" * 60 + "\n")
    
    print("Integration pattern in your Discord bot:\n")
    
    code_example = '''
# In your Discord bot code:

from bot import AbuseDetector, ForensicsLogger

# Initialize in your bot class
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!')
        self.detector = AbuseDetector()
        self.logger = ForensicsLogger()
    
    async def on_message(self, message):
        # Skip bot messages
        if message.author.bot:
            return
        
        # Analyze the message
        analysis = self.detector.analyze_message(message.content)
        
        # If abusive, log and take action
        if analysis['is_abusive']:
            # Log evidence
            self.logger.log_evidence(message, analysis)
            
            # Optional: Alert moderators
            if analysis['severity'] == 'high':
                # Send alert to mod channel
                mod_channel = self.get_channel(MOD_CHANNEL_ID)
                await mod_channel.send(
                    f"⚠️ High severity abuse detected from {message.author.mention}"
                )
            
            # Optional: Take automatic action
            # await message.delete()
            # await message.author.timeout(duration=60)  # 1 min timeout
        
        # Continue processing commands
        await self.process_commands(message)
'''
    
    print(code_example)
    print()


def main():
    """Run all examples."""
    examples = [
        example_basic_detection,
        example_custom_thresholds,
        example_forensics_workflow,
        example_batch_analysis,
        example_user_tracking,
        example_integration_with_discord,
    ]
    
    for example in examples:
        example()
        input("Press Enter to continue to next example...")
        print("\n")
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
