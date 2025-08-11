"""
Filtering utilities for Scrabble Word Solver.
Provides functions to filter words by various criteria.
"""

from typing import List, Dict, Any


def filter_words_by_length(words: List[Dict[str, Any]], 
                          min_length: int = None, 
                          max_length: int = None) -> List[Dict[str, Any]]:
    """
    Filter words by length range.
    
    Args:
        words: List of word dictionaries
        min_length: Minimum word length (inclusive)
        max_length: Maximum word length (inclusive)
        
    Returns:
        Filtered list of words
    """
    filtered_words = words
    
    if min_length is not None:
        filtered_words = [word for word in filtered_words if word['length'] >= min_length]
    
    if max_length is not None:
        filtered_words = [word for word in filtered_words if word['length'] <= max_length]
    
    return filtered_words


def filter_words_by_first_letter(words: List[Dict[str, Any]], 
                                starts_with: str = None) -> List[Dict[str, Any]]:
    """
    Filter words by first letter.
    
    Args:
        words: List of word dictionaries
        starts_with: Letter that words should start with
        
    Returns:
        Filtered list of words
    """
    if not starts_with:
        return words
    
    starts_with = starts_with.lower()
    return [word for word in words if word['word'].lower().startswith(starts_with)]


def filter_words_by_last_letter(words: List[Dict[str, Any]], 
                               ends_with: str = None) -> List[Dict[str, Any]]:
    """
    Filter words by last letter.
    
    Args:
        words: List of word dictionaries
        ends_with: Letter that words should end with
        
    Returns:
        Filtered list of words
    """
    if not ends_with:
        return words
    
    ends_with = ends_with.lower()
    return [word for word in words if word['word'].lower().endswith(ends_with)]


def apply_filters(words: List[Dict[str, Any]], filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """
    Apply all filters to the word list.
    
    Args:
        words: List of word dictionaries
        filters: Dictionary containing filter criteria
        
    Returns:
        Filtered list of words
    """
    if not filters:
        return words
    
    filtered_words = words
    
    # Apply length filters
    if 'min_length' in filters and filters['min_length'] is not None:
        filtered_words = filter_words_by_length(filtered_words, min_length=filters['min_length'])
    
    if 'max_length' in filters and filters['max_length'] is not None:
        filtered_words = filter_words_by_length(filtered_words, max_length=filters['max_length'])
    
    # Apply letter position filters
    if 'starts_with' in filters and filters['starts_with']:
        filtered_words = filter_words_by_first_letter(filtered_words, filters['starts_with'])
    
    if 'ends_with' in filters and filters['ends_with']:
        filtered_words = filter_words_by_last_letter(filtered_words, filters['ends_with'])
    
    return filtered_words


def validate_filters(filters: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate filter parameters and return any errors.
    
    Args:
        filters: Dictionary containing filter criteria
        
    Returns:
        Dictionary of validation errors (empty if valid)
    """
    errors = {}
    
    if filters:
        # Validate length filters
        if 'min_length' in filters and filters['min_length'] is not None:
            try:
                min_length = int(filters['min_length'])
                if min_length < 1:
                    errors['min_length'] = 'Minimum length must be at least 1'
            except (ValueError, TypeError):
                errors['min_length'] = 'Minimum length must be a valid number'
        
        if 'max_length' in filters and filters['max_length'] is not None:
            try:
                max_length = int(filters['max_length'])
                if max_length < 1:
                    errors['max_length'] = 'Maximum length must be at least 1'
            except (ValueError, TypeError):
                errors['max_length'] = 'Maximum length must be a valid number'
        
        # Validate that min_length <= max_length
        if ('min_length' in filters and filters['min_length'] is not None and
            'max_length' in filters and filters['max_length'] is not None):
            try:
                min_length = int(filters['min_length'])
                max_length = int(filters['max_length'])
                if min_length > max_length:
                    errors['length_range'] = 'Minimum length cannot be greater than maximum length'
            except (ValueError, TypeError):
                pass  # Already handled above
        
        # Validate letter filters
        if 'starts_with' in filters and filters['starts_with']:
            starts_with = str(filters['starts_with']).strip()
            if not starts_with.isalpha() or len(starts_with) != 1:
                errors['starts_with'] = 'Starts with must be a single letter'
        
        if 'ends_with' in filters and filters['ends_with']:
            ends_with = str(filters['ends_with']).strip()
            if not ends_with.isalpha() or len(ends_with) != 1:
                errors['ends_with'] = 'Ends with must be a single letter'
    
    return errors


def get_filter_summary(filters: Dict[str, Any]) -> str:
    """
    Generate a human-readable summary of applied filters.
    
    Args:
        filters: Dictionary containing filter criteria
        
    Returns:
        String summary of filters
    """
    if not filters:
        return "No filters applied"
    
    filter_parts = []
    
    if 'min_length' in filters and filters['min_length'] is not None:
        filter_parts.append(f"min length: {filters['min_length']}")
    
    if 'max_length' in filters and filters['max_length'] is not None:
        filter_parts.append(f"max length: {filters['max_length']}")
    
    if 'starts_with' in filters and filters['starts_with']:
        filter_parts.append(f"starts with: '{filters['starts_with'].upper()}'")
    
    if 'ends_with' in filters and filters['ends_with']:
        filter_parts.append(f"ends with: '{filters['ends_with'].upper()}'")
    
    if filter_parts:
        return f"Filters: {', '.join(filter_parts)}"
    else:
        return "No filters applied"
