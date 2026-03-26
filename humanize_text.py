import re
import random

def simple_humanize(text):
    """
    Simple humanization using synonym replacement and sentence restructuring
    Note: For production, consider using APIs like OpenAI, Paraphrase API, etc.
    """
    
    # Dictionary of common AI phrases and their more human alternatives
    ai_replacements = {
        r'\bin conclusion\b': 'so',
        r'\brevertheless\b': 'but',
        r'\bmoreover\b': 'plus',
        r'\bfurthermore\b': 'also',
        r'\btherefore\b': 'so',
        r'\bhence\b': 'so',
        r'\bthus\b': 'so',
        r'\baccordingly\b': 'so',
        r'\bit is important to note that\b': 'it\'s worth noting that',
        r'\bit can be seen that\b': 'you can see that',
        r'\bthis suggests that\b': 'this means',
        r'\bthe fact that\b': 'that',
        r'\bit is clear that\b': 'clearly',
        r'\bwithout a doubt\b': 'definitely',
    }
    
    humanized = text
    
    # Apply replacements (case-insensitive)
    for ai_phrase, human_phrase in ai_replacements.items():
        humanized = re.sub(ai_phrase, human_phrase, humanized, flags=re.IGNORECASE)
    
    # Break up very long sentences
    sentences = re.split(r'(?<=[.!?])\s+', humanized)
    restructured = []
    
    for sentence in sentences:
        words = sentence.split()
        # If sentence is too long, try to break it up
        if len(words) > 25:
            # Find common conjunctions/conjunctions to split on
            split_points = []
            for i, word in enumerate(words):
                if word.lower() in ['and', 'but', 'or', 'while', 'although', 'because']:
                    split_points.append(i)
            
            if split_points:
                # Split at the midpoint conjunction
                mid_point = split_points[len(split_points) // 2]
                part1 = ' '.join(words[:mid_point]).strip()
                part2 = ' '.join(words[mid_point:]).strip()
                if part1.endswith(part1.split()[-1]) and part1.split()[-1].lower() in ['and', 'but', 'or']:
                    part1 = part1.rsplit(' ', 1)[0]
                    part2 = words[mid_point-1] + ' ' + part2
                restructured.append(part1 + '.')
                restructured.append(part2)
            else:
                restructured.append(sentence)
        else:
            restructured.append(sentence)
    
    humanized = ' '.join(restructured)
    
    # Add some casual markers (sparingly)
    random.seed(hash(text) % 2**32)  # Deterministic but unique per text
    
    # Convert some passive voice to active where possible
    passive_pattern = r'(\w+)\s+(?:was|were)\s+(\w+(?:ed)?)\s+(?:by\s+)?(?:the\s+)?(\w+)'
    
    return humanized.strip()

def estimate_humanization_improvement(original_text, humanized_text):
    """
    Estimate how much the humanization improved the text
    Returns a percentage of improvement
    """
    # Simple metric: compare word variety and structure
    original_words = set(original_text.lower().split())
    humanized_words = set(humanized_text.lower().split())
    
    # Higher word variety = more human
    improvement = len(humanized_words - original_words) / max(len(original_words), 1) * 50
    improvement = min(100, max(0, int(improvement)))
    
    return improvement
