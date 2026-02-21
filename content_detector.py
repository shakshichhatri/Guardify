"""
Advanced Content Detector - Multilingual Support (English & Hindi)
Detects offensive slangs, hate speech, threats, and sensitive words
Using AI extensions and multiple detection methods
"""

import re
from typing import Dict, List, Tuple
from datetime import datetime
import json
import os

try:
    from better_profanity import profanity
    BETTER_PROFANITY_AVAILABLE = True
except ImportError:
    BETTER_PROFANITY_AVAILABLE = False

try:
    from langdetect import detect, LangDetectException
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False


class HindiEnglishContentDetector:
    """Advanced multilingual content detector for English and Hindi"""
    
    def __init__(self):
        # Initialize better-profanity
        if BETTER_PROFANITY_AVAILABLE:
            profanity.load_censor_words()
        
        # Extended offensive word lists - ENGLISH
        self.offensive_keywords_en = {
            # Hate speech & Discrimination
            'hate', 'racist', 'racism', 'sexist', 'sexism', 'homophobic', 'transphobic',
            'bigot', 'bigotry', 'supremacist', 'fascist', 'terrorist', 'terrorism',
            'kill', 'kill all', 'massacre', 'genocide', 'ethnic cleansing',
            
            # Threats & Violence
            'hurt', 'harm', 'attack', 'beat', 'punch', 'kick', 'stab', 'shoot', 'murder',
            'suicide', 'kys', 'kms', 'hang', 'drink bleach', 'die', 'neck yourself', 
            'rope yourself', 'end yourself', 'unalive yourself', 'get cancer', 'get aids',
            'jump off', 'go die', 'kill yourself', 'delete yourself',
            
            # Severe insults & Derogatory terms
            'n-word', 'n***a', 'n***er', 'f-word', 'f****t', 'f*g', 'queer', 'faggot',
            'tranny', 'trannies', 'dyke', 'chink', 'spic', 'wetback', 'cracker', 'honky',
            'gook', 'ape', 'monkey', 'rag head', 'towelhead',
            
            # Bullying & Toxicity
            'cancer', 'tumor', 'disease', 'waste of space', 'nobody likes you',
            'everyone hates you', 'useless', 'failure', 'embarrassment', 'joke',
            'clown', 'braindead', 'brainless', 'retard', 'retarded', 'moron',
            'idiot', 'stupid', 'dumb', 'dumbass', 'dummy', 'loser', 'trash', 
            'garbage', 'worthless', 'pathetic', 'disgusting',
            
            # Sexual harassment & Vulgar terms
            'whore', 'slut', 'thot', 'hoe', 'prostitute', 'hooker', 'porn', 'rape',
            'sexually assault', 'sexual harass', 'grope', 'molest',
            
            # Profanity (core words)
            'fuck', 'shit', 'crap', 'damn', 'hell', 'bastard', 'bitch', 'ass',
            'asshole', 'prick', 'dick', 'cock', 'pussy', 'cunt', 'twat',
            'motherfucker', 'wtf', 'stfu', 'shut up',
            
            # Variants & Leetspeak (common variations)
            'fuk', 'fck', 'sh1t', 'b1tch', 'a$$', 'a55', 'fvck', 'phuck', 'shtty',
            'suck', 'sucks', 'noob', 'n00b', 'scrub', 'bot', 'trash player',
            
            # Toxic gaming/online terms
            'ez', 'get rekt', 'trash talk', 'git gud', 'cope', 'seethe', 'mald',
            'ratio', 'cry about it', 'cope harder', 'simp', 'incel', 'neckbeard',
            'virgin', 'your mom', 'yo mama', 'your sister', 'deez nuts',
        }
        
        # Extended offensive word lists - HINDI
        self.offensive_keywords_hi = {
            # Gaali (Abusive words) - Hindi
            'gaali', 'gali', 'besharam', 'badmash', 'nalayak', 'kamina', 'harami',
            'pagal', 'budhu', 'bewakoof', 'murkh', 'chakku', 'chutiya', 'bhosdi',
            'bc', 'bh*nchod', 'lund', 'lauda', 'jhant', 'randi', 'raandi', 'rand',
            'kutia', 'kutiya', 'suar', 'soor', 'chakla', 'chakli', 'kutti',
            
            # Threats & Violence - Hindi
            'mardunga', 'mar dunga', 'pitayi', 'chalbazo', 'chot parunga', 'maar',
            'maar dunga', 'peetu', 'pakad le', 'aag lagadi', 'todo', 'toda', 'tordunga',
            'tori', 'kaat', 'kaatdunga', 'stab', 'chhura', 'talvaar', 'banduk',
            'goli', 'dhakka', 'ghusa', 'hatya', 'hatyakand',
            
            # Severe insults
            'maachod', 'behya', 'apamaan', 'badnaam', 'sharam', 'lalach', 'shudr',
            'neech', 'neechta', 'ghatiya', 'nindya', 'ninda', 'beizzat', 'izzat',
            'mati', 'tuhmat', 'ilzaam', 'gunah',
            
            # Discriminatory (caste/religion) - Hindi
            'dohit', 'dhobhi', 'chandal', 'pariya', 'bhangiya', 'teli', 'kumhar',
            'mali', 'kayasth', 'brahmin', 'kshatriya', 'vaishya', 'shudra',
            'mleccha', 'yavana', 'barbarae', 'videshi',
            
            # Suicidal threats - Hindi
            'sui kara', 'jaan de', 'mar ja', 'jeevan sambhal', 'atmahatya', 'suicide',
            'phansi', 'zalim', 'bura hai', 'buraa', 'atyachaar', 'bhag ja', 'katl',
            
            # Toxic behavior - Hindi
            'jhooth', 'jhoota', 'chugal', 'bakwas', 'bakanwas', 'faltu', 'bekaar',
            'adayit', 'adayi', 'galat', 'galti', 'paapi', 'paap', 'papi',
        }
        
        # Detect patterns for threats and violence
        self.threat_patterns = [
            r'\b(i\'?ll|will|gonna|gon[na]+|imma|imma gonna)\s+(kill|hurt|harm|beat|punch|stab|shoot)\b',
            r'\b(kill|hurt|harm|beat|punch|stab|shoot)\s+(yourself|yourself|urself|u|yourself)\b',
            r'\b(go\s+)?die\b', 
            r'\b(neck|rope|hang|drink\s+bleach|jump\s+off)\s+(yourself|urself)\b',
            r'\bkys\b|\bkms\b',
            r'\b(death\s+)?threat',
            r'\b(commit|attempt|do)\s+(suicide|atmahatya)',
            r'💀|☠️|🔪|🔫|⚰️',  # Death/violence emojis
        ]
        
        # Hate speech patterns
        self.hate_patterns = [
            r'\b(f+[au]ck\s+)?all\s+\w+\b',  # "fuck all [group]"
            r'\b\w+s?\s+(are|r)\s+(trash|garbage|cancer|disease|subhuman|animals?|pigs?|rats?)\b',
            r'\b(hate|despise)\s+\w+(s?)\b',
            r'\b\[banned word\]\s+lives\s+(don\'?t|do\s+not)\s+matter\b',
            r'(white|black|brown|yellow|red)\s+(genocide|replacement|supremacy)',
        ]
        
        # Weighted severity scoring
        self.severity_weights = {
            'threat_violence': 1.0,      # Most severe
            'hate_speech': 0.9,
            'discrimination': 0.85,
            'harassment': 0.7,
            'profanity': 0.4,
            'slang_offensive': 0.5,
        }
    
    def detect_language(self, text: str) -> str:
        """Detect if text is in Hindi or English"""
        if not LANGDETECT_AVAILABLE:
            # Fallback: check for Hindi unicode patterns
            hindi_pattern = re.compile(r'[\u0900-\u097F]')
            if hindi_pattern.search(text):
                return 'hi'
            return 'en'
        
        try:
            lang = detect(text)
            if lang in ['hi', 'en']:
                return lang
            # Check for Hindi characters as backup
            hindi_pattern = re.compile(r'[\u0900-\u097F]')
            if hindi_pattern.search(text):
                return 'hi'
            return 'en'
        except LangDetectException:
            return 'en'  # Default to English on detection failure
    
    def check_better_profanity(self, text: str) -> Tuple[bool, List[str]]:
        """Use better-profanity library for detection"""
        if not BETTER_PROFANITY_AVAILABLE:
            return False, []
        
        try:
            if profanity.contains_profanity(text):
                detected = []
                words = text.lower().split()
                for word in words:
                    if profanity.contains_profanity(word):
                        detected.append(word.strip('.,!?;:'))
                return True, detected[:5]  # Return up to 5 detected words
        except Exception as e:
            print(f"[ERROR] Better profanity check failed: {e}")
        
        return False, []
    
    def check_keyword_match(self, text: str, lang: str) -> Tuple[bool, List[str], str]:
        """Check for keyword matches with language-specific lists"""
        text_lower = text.lower()
        
        # Select keyword list based on language
        keywords = self.offensive_keywords_hi if lang == 'hi' else self.offensive_keywords_en
        
        detected = []
        category = 'profanity'
        
        for keyword in keywords:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text_lower):
                detected.append(keyword)
        
        # Determine category based on keywords
        threat_keywords = {'kill', 'harm', 'hurt', 'attack', 'suicide', 'kys', 'die',
                          'mar', 'mardunga', 'mar dunga', 'pitayi', 'chalbazo'}
        hate_keywords = {'racist', 'racism', 'hate', 'bigot', 'supremacist', 'terrorist',
                        'discrimination', 'discriminate'}
        
        if any(k in detected for k in threat_keywords):
            category = 'threat_violence'
        elif any(k in detected for k in hate_keywords):
            category = 'hate_speech'
        elif any(keyword in ['n***er', 'f****t', 'chink', 'spic'] for k in detected):
            category = 'discrimination'
        elif any(k in ['besharam', 'badmash', 'harami', 'chutiya'] for k in detected):
            category = 'harassment'
        
        return len(detected) > 0, detected[:5], category
    
    def check_pattern_match(self, text: str) -> Tuple[bool, List[str], str]:
        """Check for dangerous patterns (threats, hate speech)"""
        text_lower = text.lower()
        detected_patterns = []
        category = 'profanity'
        
        # Check threat patterns
        for pattern in self.threat_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                detected_patterns.append('Threat or suicide encouragement detected')
                category = 'threat_violence'
                break
        
        # Check hate speech patterns
        if category != 'threat_violence':  # Don't override threat detection
            for pattern in self.hate_patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    detected_patterns.append('Hate speech pattern detected')
                    category = 'hate_speech'
                    break
        
        return len(detected_patterns) > 0, detected_patterns, category
    
    def analyze_content(self, text: str) -> Dict:
        """
        Comprehensive content analysis
        
        Returns:
            Dict with detection results, severity, category, and detected content
        """
        # Language detection
        detected_lang = self.detect_language(text)
        
        # Method 1: Better Profanity check
        profanity_detected, profanity_words = self.check_better_profanity(text)
        
        # Method 2: Keyword matching
        keyword_detected, keyword_matches, keyword_category = self.check_keyword_match(text, detected_lang)
        
        # Method 3: Pattern matching for threats and hate speech
        pattern_detected, pattern_matches, pattern_category = self.check_pattern_match(text)
        
        # Determine if content is offensive
        is_offensive = profanity_detected or keyword_detected or pattern_detected
        
        # Determine category and severity
        category = 'clean'
        severity_score = 0.0
        
        if pattern_detected:
            category = pattern_category
            severity_score = self.severity_weights.get(category, 0.5)
        elif keyword_detected:
            category = keyword_category
            severity_score = self.severity_weights.get(category, 0.5)
        elif profanity_detected:
            category = 'profanity'
            severity_score = self.severity_weights.get('profanity', 0.4)
        
        # Collect all detected offensive content
        all_detected = list(set(profanity_words + keyword_matches + pattern_matches))
        
        return {
            "is_offensive": is_offensive,
            "severity": severity_score,
            "category": category,
            "language": detected_lang,
            "detected_content": all_detected[:5],  # Top 5 detected items
            "profanity_words": profanity_words[:3],
            "pattern_matches": pattern_matches,
            "methods_triggered": [
                "better_profanity" if profanity_detected else None,
                "keyword_matching" if keyword_detected else None,
                "pattern_matching" if pattern_detected else None,
            ],
            "timestamp": datetime.utcnow().isoformat(),
            "confidence": min(0.95, (len(all_detected) / 5) * 0.95),  # Confidence score
        }
    
    def get_severity_level(self, severity_score: float) -> str:
        """Convert severity score to level"""
        if severity_score >= 0.85:
            return "CRITICAL"
        elif severity_score >= 0.7:
            return "HIGH"
        elif severity_score >= 0.5:
            return "MEDIUM"
        elif severity_score >= 0.3:
            return "LOW"
        else:
            return "MINIMAL"


# Singleton instance
_detector_instance = None

def get_content_detector() -> HindiEnglishContentDetector:
    """Get or create singleton instance of content detector"""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = HindiEnglishContentDetector()
    return _detector_instance
