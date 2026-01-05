"""
Demo script to showcase Respect Ranger bot functionality
This script demonstrates the abuse detection without requiring Discord connection
"""

from bot import AbuseDetector, ForensicsLogger
import json


def demo_abuse_detection():
    """Demonstrate the abuse detection capabilities."""
    print("=" * 60)
    print("RESPECT RANGER - ABUSE DETECTION DEMO")
    print("=" * 60)
    print()
    
    detector = AbuseDetector()
    
    # Test messages with different levels of abuse
    test_messages = [
        ("Hello everyone! Hope you're having a great day!", "Clean message"),
        ("That's an interesting perspective, thanks for sharing", "Positive message"),
        ("This is stupid", "Single keyword"),
        ("You are so stupid and worthless", "Multiple keywords"),
        ("I hate everything about this pathetic situation", "Negative sentiment"),
        ("You stupid, pathetic, worthless idiot", "High severity"),
        ("kys you disgusting trash", "Severe abuse"),
    ]
    
    print("Testing various messages:\n")
    
    for message, description in test_messages:
        print(f"📝 Message: '{message}'")
        print(f"   Description: {description}")
        
        result = detector.analyze_message(message)
        
        print(f"   🔍 Abusive: {'YES ⚠️' if result['is_abusive'] else 'NO ✅'}")
        print(f"   📊 Abuse Score: {result['abuse_score']}")
        print(f"   😊 Sentiment: {result['sentiment']}")
        print(f"   🚨 Severity: {result['severity'].upper()}")
        
        if result['detected_keywords']:
            print(f"   🔑 Keywords: {', '.join(result['detected_keywords'])}")
        
        print()


def demo_forensics_logging():
    """Demonstrate the forensics logging capabilities."""
    print("=" * 60)
    print("FORENSICS LOGGING DEMO")
    print("=" * 60)
    print()
    
    # Create a temporary logger
    logger = ForensicsLogger(log_dir="demo_logs")
    
    # Create mock message
    class MockMessage:
        def __init__(self, msg_id, author_id, author_name, content):
            from datetime import datetime
            self.id = msg_id
            self.content = content
            self.created_at = datetime.now()
            
            class MockAuthor:
                def __init__(self, uid, name):
                    self.id = uid
                    self.name = name
                def __str__(self):
                    return self.name
            
            class MockChannel:
                def __init__(self):
                    self.id = 123456
                    self.name = "general"
                def __str__(self):
                    return "general"
            
            class MockGuild:
                def __init__(self):
                    self.id = 999888
                    self.name = "Demo Server"
            
            self.author = MockAuthor(author_id, author_name)
            self.channel = MockChannel()
            self.guild = MockGuild()
    
    # Simulate logging some abusive messages
    detector = AbuseDetector()
    
    messages = [
        (1001, 5001, "User1#1234", "You are so stupid"),
        (1002, 5001, "User1#1234", "This is pathetic and worthless"),
        (1003, 5002, "User2#5678", "You idiot, go away"),
    ]
    
    print("Logging abusive messages...\n")
    
    for msg_id, author_id, author_name, content in messages:
        mock_msg = MockMessage(msg_id, author_id, author_name, content)
        analysis = detector.analyze_message(content)
        
        if analysis['is_abusive']:
            logger.log_evidence(mock_msg, analysis)
            print(f"✅ Logged: '{content}' by {author_name}")
            print(f"   Severity: {analysis['severity'].upper()}, Score: {analysis['abuse_score']}")
    
    print(f"\n📂 Evidence logged to: {logger.log_file}")
    
    # Display statistics
    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)
    
    stats = logger.get_statistics()
    print(f"Total Cases: {stats['total_cases']}")
    print(f"Unique Users: {stats['unique_users']}")
    print(f"Unique Servers: {stats['unique_guilds']}")
    print(f"\nSeverity Breakdown:")
    for severity, count in stats['severity_breakdown'].items():
        print(f"  {severity.capitalize()}: {count}")
    
    # Display user history
    print("\n" + "=" * 60)
    print("USER HISTORY EXAMPLE")
    print("=" * 60)
    
    history = logger.get_user_history('5001', limit=5)
    print(f"\nShowing history for User ID 5001 ({len(history)} records):\n")
    
    for i, record in enumerate(history, 1):
        print(f"Record #{i}:")
        print(f"  Message: {record['content']}")
        print(f"  Score: {record['analysis']['abuse_score']}")
        print(f"  Severity: {record['analysis']['severity'].upper()}")
        print()


def main():
    """Run the demo."""
    print("\n")
    demo_abuse_detection()
    print("\n")
    demo_forensics_logging()
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("\nTo use with Discord:")
    print("1. Set up your bot token in config.json or as environment variable")
    print("2. Run: python bot.py")
    print("3. The bot will automatically detect abuse in real-time!")
    print("\nFor more information, see README.md and SETUP.md")
    print()


if __name__ == "__main__":
    main()
