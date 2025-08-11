"""
Grouping utilities for Scrabble Word Solver.
Provides functions to group words by various criteria.
"""

from collections import defaultdict
from typing import List, Dict, Any


def extract_word_metadata(word_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract additional metadata from word data.
    
    Args:
        word_data: Dictionary containing word information
        
    Returns:
        Enhanced word data with first_letter and last_letter
    """
    word = word_data['word']
    return {
        **word_data,
        'first_letter': word[0] if word else '',
        'last_letter': word[-1] if word else ''
    }


def group_by_length(words: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Group words by their length.
    
    Args:
        words: List of word dictionaries
        
    Returns:
        List of groups with group metadata
    """
    groups = defaultdict(list)
    
    for word_data in words:
        length = word_data['length']
        groups[length].append(word_data)
    
    # Convert to list of group dictionaries
    result = []
    for length in sorted(groups.keys()):
        group_words = groups[length]
        total_score = sum(word['score'] for word in group_words)
        
        result.append({
            'name': f"{length} letter{'s' if length != 1 else ''}",
            'count': len(group_words),
            'total_score': total_score,
            'words': group_words
        })
    
    return result


def group_by_first_letter(words: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Group words by their first letter.
    
    Args:
        words: List of word dictionaries
        
    Returns:
        List of groups with group metadata
    """
    groups = defaultdict(list)
    
    for word_data in words:
        first_letter = word_data.get('first_letter', word_data['word'][0])
        groups[first_letter].append(word_data)
    
    # Convert to list of group dictionaries
    result = []
    for first_letter in sorted(groups.keys()):
        group_words = groups[first_letter]
        total_score = sum(word['score'] for word in group_words)
        
        result.append({
            'name': f"Starts with '{first_letter.upper()}'",
            'count': len(group_words),
            'total_score': total_score,
            'words': group_words
        })
    
    return result


def group_by_last_letter(words: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Group words by their last letter.
    
    Args:
        words: List of word dictionaries
        
    Returns:
        List of groups with group metadata
    """
    groups = defaultdict(list)
    
    for word_data in words:
        last_letter = word_data.get('last_letter', word_data['word'][-1])
        groups[last_letter].append(word_data)
    
    # Convert to list of group dictionaries
    result = []
    for last_letter in sorted(groups.keys()):
        group_words = groups[last_letter]
        total_score = sum(word['score'] for word in group_words)
        
        result.append({
            'name': f"Ends with '{last_letter.upper()}'",
            'count': len(group_words),
            'total_score': total_score,
            'words': group_words
        })
    
    return result


def group_words(words: List[Dict[str, Any]], group_by: str = 'length') -> List[Dict[str, Any]]:
    """
    Group words by the specified criteria.
    
    Args:
        words: List of word dictionaries
        group_by: Grouping criteria ('length', 'first_letter', 'last_letter')
        
    Returns:
        List of groups with group metadata
    """
    # Extract metadata for all words
    enhanced_words = [extract_word_metadata(word_data) for word_data in words]
    
    if group_by == 'length':
        return group_by_length(enhanced_words)
    elif group_by == 'first_letter':
        return group_by_first_letter(enhanced_words)
    elif group_by == 'last_letter':
        return group_by_last_letter(enhanced_words)
    else:
        # Default to length grouping
        return group_by_length(enhanced_words)


def get_available_grouping_options() -> List[Dict[str, str]]:
    """
    Get available grouping options for the API.
    
    Returns:
        List of grouping options with labels and values
    """
    return [
        {'value': 'length', 'label': 'By Word Length'},
        {'value': 'first_letter', 'label': 'By First Letter'},
        {'value': 'last_letter', 'label': 'By Last Letter'}
    ]
