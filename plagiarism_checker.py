import sqlite3
from difflib import SequenceMatcher
from datetime import datetime
import re
import textstat

def normalize_text(text):
    # Keep only letters and join them into words without gaps
    words = re.findall(r'[a-zA-Z]+', text)
    normalized = ' '.join(words).lower()
    return normalized.strip()

def detect_ai_percentage(text):
    """
    Detect AI-generated content percentage using linguistic patterns
    Returns a percentage (0-100) indicating likelihood of AI generation
    """
    if not text or len(text.strip()) < 50:
        return 0
    
    ai_indicators = 0
    total_checks = 0
    
    # Check 1: Flesch-Kincaid Grade Level (AI tends to be more formal)
    try:
        grade = textstat.flesch_kincaid_grade(text)
        total_checks += 1
        if grade > 10:  # More academic/formal
            ai_indicators += 0.3
    except:
        pass
    
    # Check 2: Average sentence length (AI tends to have longer sentences)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if sentences:
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        total_checks += 1
        if avg_sentence_length > 20:  # Long sentences
            ai_indicators += 0.3
    
    # Check 3: Passive voice percentage (AI uses more passive voice)
    passive_pattern = r'\b(was|were|been|be|is|are)\s+\w+ed\b'
    passive_count = len(re.findall(passive_pattern, text, re.IGNORECASE))
    total_checks += 1
    if passive_count > len(sentences) * 0.2:
        ai_indicators += 0.2
    
    # Check 4: Repetition patterns (humans repeat less)
    words = text.lower().split()
    if words:
        unique_ratio = len(set(words)) / len(words)
        total_checks += 1
        if unique_ratio > 0.8:  # High uniqueness can indicate AI
            ai_indicators += 0.2
    
    if total_checks == 0:
        return 0
    
    # Calculate percentage
    ai_percentage = (ai_indicators / total_checks) * 100
    return min(100, max(0, int(ai_percentage)))

def check_plagiarism(input_text, threshold=0.7, top_n=3):
    conn = sqlite3.connect('plagiarism.db')
    c = conn.cursor()

    # Fetch all past submissions
    c.execute("SELECT filename, content, timestamp FROM submissions")
    previous_submissions = c.fetchall()
    conn.close()

    # Normalize input text
    normalized_input = normalize_text(input_text)
    
    # Detect AI percentage
    ai_percentage = detect_ai_percentage(input_text)

    similarity_list = []
    above_threshold_found = False

    for filename, content, timestamp in previous_submissions:
        normalized_db_content = normalize_text(content)
        similarity = SequenceMatcher(None, normalized_input, normalized_db_content).ratio()

        # Format timestamp
        try:
            timestamp_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            timestamp_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        timestamp_str = timestamp_obj.strftime('%b %d, %Y %H:%M')

        snippet = content[:100].replace('\n', ' ').strip() + "..."

        if similarity >= threshold:
            above_threshold_found = True

        similarity_list.append((similarity, filename, timestamp_str, snippet))

    # Sort by similarity descending
    similarity_list.sort(reverse=True, key=lambda x: x[0])
    top_matches = similarity_list[:top_n]

    results = {
        'ai_percentage': ai_percentage,
        'plagiarism_percentage': 0,
        'safety_percentage': 100,  # Will be calculated below
        'top_matches': [],
        'is_original': True,
        'message': ''
    }
    
    # Check plagiarism against database
    if top_matches and top_matches[0][0] >= threshold:
        results['plagiarism_percentage'] = int(top_matches[0][0] * 100)
        results['is_original'] = False
        results['top_matches'] = [
            {
                'filename': top_matches[0][1],
                'similarity': f"{top_matches[0][0]:.2%}",
                'timestamp': top_matches[0][2],
                'snippet': top_matches[0][3]
            }
        ]
        results['message'] = "⚠️ High plagiarism detected! Similar content found in database."
    else:
        results['plagiarism_percentage'] = int(top_matches[0][0] * 100) if top_matches else 0
        results['is_original'] = True
        results['message'] = "✅ No significant plagiarism detected."

    # Calculate overall safety percentage (100 - max risk factor)
    max_risk = max(results['ai_percentage'], results['plagiarism_percentage'])
    results['safety_percentage'] = 100 - max_risk

    return results
