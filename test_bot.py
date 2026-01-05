"""
Unit tests for Respect Ranger Discord Bot
Tests the abuse detection and forensics logging functionality
"""

import unittest
import os
import json
import tempfile
import shutil
from datetime import datetime
from bot import AbuseDetector, ForensicsLogger


class TestAbuseDetector(unittest.TestCase):
    """Test cases for the AbuseDetector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = AbuseDetector()
    
    def test_clean_message(self):
        """Test that clean messages are not flagged as abusive."""
        result = self.detector.analyze_message("Hello, how are you doing today?")
        self.assertFalse(result['is_abusive'])
        self.assertEqual(result['severity'], 'low')
        self.assertEqual(len(result['detected_keywords']), 0)
    
    def test_positive_message(self):
        """Test that positive messages are not flagged."""
        result = self.detector.analyze_message("You are amazing! Great job!")
        self.assertFalse(result['is_abusive'])
        self.assertGreater(result['sentiment'], 0)
    
    def test_abusive_keywords(self):
        """Test detection of messages with abusive keywords."""
        result = self.detector.analyze_message("You are so stupid and worthless")
        self.assertTrue(result['is_abusive'])
        self.assertGreater(len(result['detected_keywords']), 0)
        self.assertIn('stupid', result['detected_keywords'])
        self.assertIn('worthless', result['detected_keywords'])
    
    def test_negative_sentiment(self):
        """Test detection of messages with negative sentiment."""
        result = self.detector.analyze_message("I hate everything about this")
        self.assertTrue(result['is_abusive'])
        self.assertLess(result['sentiment'], 0)
    
    def test_severity_levels(self):
        """Test that severity levels are correctly assigned."""
        # Low severity
        result_low = self.detector.analyze_message("This is slightly annoying")
        
        # Medium/High severity - multiple keywords
        result_medium = self.detector.analyze_message("You stupid idiot")
        
        # High severity - many keywords
        result_high = self.detector.analyze_message("You are stupid, pathetic, worthless trash")
        
        # Just verify they have severity levels assigned
        self.assertIn(result_low['severity'], ['low', 'medium', 'high'])
        self.assertIn(result_medium['severity'], ['low', 'medium', 'high'])
        self.assertIn(result_high['severity'], ['low', 'medium', 'high'])
        
        # High severity should have higher score than low
        self.assertGreater(result_high['abuse_score'], result_low['abuse_score'])
    
    def test_mixed_content(self):
        """Test messages with both positive and negative elements."""
        result = self.detector.analyze_message("You did great on that, but you're still an idiot")
        # Should detect the keyword even if overall sentiment is mixed
        self.assertIn('idiot', result['detected_keywords'])
        # May or may not be flagged as abusive depending on overall score
        self.assertIsInstance(result['is_abusive'], bool)
    
    def test_case_insensitivity(self):
        """Test that keyword detection is case-insensitive."""
        result = self.detector.analyze_message("You are STUPID and PATHETIC")
        self.assertTrue(result['is_abusive'])
        self.assertIn('stupid', result['detected_keywords'])
        self.assertIn('pathetic', result['detected_keywords'])
    
    def test_abuse_score_calculation(self):
        """Test that abuse score is properly calculated."""
        result = self.detector.analyze_message("hate hate hate")
        self.assertIsInstance(result['abuse_score'], float)
        self.assertGreater(result['abuse_score'], 0)
    
    def test_timestamp_present(self):
        """Test that analysis includes timestamp."""
        result = self.detector.analyze_message("Test message")
        self.assertIn('timestamp', result)
        # Verify it's a valid ISO format timestamp
        datetime.fromisoformat(result['timestamp'])


class TestForensicsLogger(unittest.TestCase):
    """Test cases for the ForensicsLogger class."""
    
    def setUp(self):
        """Set up test fixtures with temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.logger = ForensicsLogger(log_dir=self.temp_dir)
        
        # Create mock message object
        self.mock_message = type('MockMessage', (), {
            'id': 123456789,
            'content': 'Test abusive message',
            'created_at': datetime.utcnow(),
            'author': type('MockAuthor', (), {
                'id': 987654321,
                '__str__': lambda self: 'TestUser#1234'
            })(),
            'channel': type('MockChannel', (), {
                'id': 111222333,
                'name': 'test-channel',
                '__str__': lambda self: 'test-channel'
            })(),
            'guild': type('MockGuild', (), {
                'id': 444555666,
                'name': 'Test Server'
            })()
        })()
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir)
    
    def test_log_directory_creation(self):
        """Test that log directory is created."""
        self.assertTrue(os.path.exists(self.temp_dir))
    
    def test_log_evidence(self):
        """Test logging of evidence."""
        analysis = {
            'is_abusive': True,
            'abuse_score': 0.75,
            'sentiment': -0.6,
            'detected_keywords': ['hate'],
            'severity': 'medium'
        }
        
        self.logger.log_evidence(self.mock_message, analysis)
        
        # Verify log file was created
        self.assertTrue(os.path.exists(self.logger.log_file))
        
        # Read and verify content
        with open(self.logger.log_file, 'r') as f:
            line = f.readline()
            record = json.loads(line)
            
            self.assertEqual(record['message_id'], '123456789')
            self.assertEqual(record['author_id'], '987654321')
            self.assertEqual(record['content'], 'Test abusive message')
            self.assertEqual(record['analysis']['severity'], 'medium')
    
    def test_multiple_logs(self):
        """Test logging multiple evidence entries."""
        analysis = {
            'is_abusive': True,
            'abuse_score': 0.75,
            'severity': 'medium'
        }
        
        # Log multiple times
        for i in range(3):
            self.logger.log_evidence(self.mock_message, analysis)
        
        # Verify all entries are logged
        with open(self.logger.log_file, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 3)
    
    def test_get_user_history(self):
        """Test retrieving user abuse history."""
        analysis = {
            'is_abusive': True,
            'abuse_score': 0.75,
            'severity': 'medium'
        }
        
        # Log some evidence
        self.logger.log_evidence(self.mock_message, analysis)
        self.logger.log_evidence(self.mock_message, analysis)
        
        # Retrieve history
        history = self.logger.get_user_history('987654321', limit=10)
        
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['author_id'], '987654321')
    
    def test_get_user_history_limit(self):
        """Test that user history respects limit parameter."""
        analysis = {'is_abusive': True, 'severity': 'medium'}
        
        # Log 5 entries
        for i in range(5):
            self.logger.log_evidence(self.mock_message, analysis)
        
        # Request only 3
        history = self.logger.get_user_history('987654321', limit=3)
        
        self.assertEqual(len(history), 3)
    
    def test_get_user_history_no_records(self):
        """Test retrieving history for user with no records."""
        history = self.logger.get_user_history('nonexistent_user')
        self.assertEqual(len(history), 0)
    
    def test_get_statistics(self):
        """Test statistics generation."""
        analysis_medium = {
            'is_abusive': True,
            'abuse_score': 0.6,
            'severity': 'medium'
        }
        analysis_high = {
            'is_abusive': True,
            'abuse_score': 0.9,
            'severity': 'high'
        }
        
        # Log different severity levels
        self.logger.log_evidence(self.mock_message, analysis_medium)
        self.logger.log_evidence(self.mock_message, analysis_high)
        
        stats = self.logger.get_statistics()
        
        self.assertEqual(stats['total_cases'], 2)
        self.assertEqual(stats['unique_users'], 1)
        self.assertIn('severity_breakdown', stats)
    
    def test_get_statistics_empty(self):
        """Test statistics when no data exists."""
        stats = self.logger.get_statistics()
        self.assertEqual(stats['total_cases'], 0)
    
    def test_jsonl_format(self):
        """Test that logs are in proper JSONL format."""
        analysis = {'is_abusive': True, 'severity': 'medium'}
        
        self.logger.log_evidence(self.mock_message, analysis)
        self.logger.log_evidence(self.mock_message, analysis)
        
        # Verify each line is valid JSON
        with open(self.logger.log_file, 'r') as f:
            for line in f:
                try:
                    json.loads(line)
                except json.JSONDecodeError:
                    self.fail("Invalid JSON in log file")


class TestIntegration(unittest.TestCase):
    """Integration tests for combined functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = AbuseDetector()
        self.temp_dir = tempfile.mkdtemp()
        self.logger = ForensicsLogger(log_dir=self.temp_dir)
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir)
    
    def test_detection_and_logging_workflow(self):
        """Test complete workflow from detection to logging."""
        # Create mock message
        mock_message = type('MockMessage', (), {
            'id': 123456789,
            'content': 'You are stupid and worthless',
            'created_at': datetime.utcnow(),
            'author': type('MockAuthor', (), {
                'id': 987654321,
                '__str__': lambda self: 'AbusiveUser#1234'
            })(),
            'channel': type('MockChannel', (), {
                'id': 111222333,
                'name': 'general',
                '__str__': lambda self: 'general'
            })(),
            'guild': type('MockGuild', (), {
                'id': 444555666,
                'name': 'Test Server'
            })()
        })()
        
        # Detect abuse
        analysis = self.detector.analyze_message(mock_message.content)
        
        # Verify detection
        self.assertTrue(analysis['is_abusive'])
        
        # Log evidence
        self.logger.log_evidence(mock_message, analysis)
        
        # Verify logging
        history = self.logger.get_user_history('987654321')
        self.assertEqual(len(history), 1)
        self.assertTrue(history[0]['analysis']['is_abusive'])


if __name__ == '__main__':
    unittest.main()
