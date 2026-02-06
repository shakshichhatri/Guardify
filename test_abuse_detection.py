"""
Test script to verify abuse detection is working correctly.
Run this to test the detection without needing a live Discord bot.
"""

import sys
from bot import AbuseDetector

def test_abuse_detection():
    """Test the abuse detector with various messages."""
    
    detector = AbuseDetector()
    
    print("=" * 70)
    print("TESTING GUARDIFY ABUSE DETECTION SYSTEM")
    print("=" * 70)
    print()
    
    # Test cases
    test_messages = [
        # Should be detected as abusive
        "you're stupid",
        "kill yourself",
        "you are an idiot",
        "shut up loser",
        "kys",
        "you're trash",
        "go die",
        "fucking idiot",
        "you suck",
        "dumb ass",
        "fuck you",
        "stupid bitch",
        "worthless piece of trash",
        "you're a moron",
        "pathetic loser",
        
        # Leetspeak variations
        "k1ll yourself",
        "fck you",
        "ur dum",
        "st00pid",
        
        # Should NOT be detected
        "hello how are you",
        "that's a nice picture",
        "good game everyone",
        "thanks for helping",
        "I love this server",
    ]
    
    detected_count = 0
    false_negatives = []
    false_positives = []
    
    for i, message in enumerate(test_messages, 1):
        result = detector.analyze_message(message)
        
        is_abusive = result['is_abusive']
        score = result['abuse_score']
        keywords = result['detected_keywords']
        severity = result['severity']
        
        # Determine expected result (first 19 should be abusive, last 5 should not)
        expected_abusive = i <= 19
        
        status = "✓" if is_abusive == expected_abusive else "✗"
        color = "DETECTED" if is_abusive else "CLEAN"
        
        print(f"{status} Test {i:2d} [{color:8s}] Score: {score:4.2f} | Severity: {severity:6s}")
        print(f"   Message: '{message}'")
        if keywords:
            print(f"   Keywords: {', '.join(keywords[:3])}")
        print()
        
        if is_abusive:
            detected_count += 1
            if not expected_abusive:
                false_positives.append(message)
        elif expected_abusive:
            false_negatives.append(message)
    
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print(f"Total Tests: {len(test_messages)}")
    print(f"Detected as Abusive: {detected_count}")
    print(f"Expected Detection: 19")
    print()
    
    if false_negatives:
        print(f"⚠️  FALSE NEGATIVES ({len(false_negatives)}) - Should detect but didn't:")
        for msg in false_negatives:
            print(f"   - '{msg}'")
        print()
    
    if false_positives:
        print(f"⚠️  FALSE POSITIVES ({len(false_positives)}) - Wrongly detected:")
        for msg in false_positives:
            print(f"   - '{msg}'")
        print()
    
    if not false_negatives and not false_positives:
        print("✅ ALL TESTS PASSED! Abuse detection is working correctly.")
    else:
        print(f"⚠️  {len(false_negatives) + len(false_positives)} tests failed.")
    
    print()
    print("=" * 70)
    
    # Interactive test
    print("\n📝 INTERACTIVE TEST MODE")
    print("Type messages to test (or 'quit' to exit):\n")
    
    while True:
        try:
            user_input = input("Test message: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            if not user_input:
                continue
            
            result = detector.analyze_message(user_input)
            
            if result['is_abusive']:
                print(f"  🚨 ABUSIVE DETECTED!")
                print(f"     Score: {result['abuse_score']}")
                print(f"     Severity: {result['severity']}")
                print(f"     Keywords: {', '.join(result['detected_keywords'][:5])}")
            else:
                print(f"  ✅ Clean message")
                print(f"     Score: {result['abuse_score']}")
            print()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"  Error: {e}\n")
    
    print("\nTest complete!")

if __name__ == "__main__":
    test_abuse_detection()
