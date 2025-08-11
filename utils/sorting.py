"""
Sorting utilities for Scrabble Word Solver.
Provides functions to sort groups and words within groups.
"""

from typing import List, Dict, Any


def sort_groups(groups: List[Dict[str, Any]], sort_order: str = 'asc') -> List[Dict[str, Any]]:
    """
    Sort groups by their criteria (length, alphabetical, etc.).
    
    Args:
        groups: List of group dictionaries
        sort_order: Sort order ('asc' or 'desc')
        
    Returns:
        Sorted list of groups
    """
    if not groups:
        return groups
    
    # Determine sort key based on group name
    def get_sort_key(group):
        name = group['name'].lower()
        
        # For length groups, extract the number
        if 'letter' in name:
            import re
            numbers = re.findall(r'\d+', name)
            if numbers:
                return int(numbers[0])
        
        # For letter groups, extract the letter
        if "starts with" in name or "ends with" in name:
            import re
            letters = re.findall(r"'([a-z])'", name)
            if letters:
                return letters[0]
        
        # Default to alphabetical
        return name
    
    reverse = sort_order.lower() == 'desc'
    return sorted(groups, key=get_sort_key, reverse=reverse)


def sort_words_within_groups(groups: List[Dict[str, Any]], sort_by: str = 'score') -> List[Dict[str, Any]]:
    """
    Sort words within each group by the specified criteria.
    
    Args:
        groups: List of group dictionaries
        sort_by: Sort criteria ('score' or 'alphabetical')
        
    Returns:
        Groups with sorted words
    """
    for group in groups:
        if sort_by == 'score':
            # Sort by score descending (highest first)
            group['words'] = sorted(group['words'], key=lambda x: x['score'], reverse=True)
        elif sort_by == 'alphabetical':
            # Sort alphabetically
            group['words'] = sorted(group['words'], key=lambda x: x['word'])
        else:
            # Default to score sorting
            group['words'] = sorted(group['words'], key=lambda x: x['score'], reverse=True)
    
    return groups


def sort_flat_words(words: List[Dict[str, Any]], sort_by: str = 'score') -> List[Dict[str, Any]]:
    """
    Sort a flat list of words by the specified criteria.
    
    Args:
        words: List of word dictionaries
        sort_by: Sort criteria ('score' or 'alphabetical')
        
    Returns:
        Sorted list of words
    """
    if sort_by == 'score':
        # Sort by score descending (highest first)
        return sorted(words, key=lambda x: x['score'], reverse=True)
    elif sort_by == 'alphabetical':
        # Sort alphabetically
        return sorted(words, key=lambda x: x['word'])
    else:
        # Default to score sorting
        return sorted(words, key=lambda x: x['score'], reverse=True)


def apply_sorting(groups: List[Dict[str, Any]], 
                 group_sort_order: str = 'asc', 
                 sort_within_groups: str = 'score') -> List[Dict[str, Any]]:
    """
    Apply sorting to groups and words within groups.
    
    Args:
        groups: List of group dictionaries
        group_sort_order: Group sort order ('asc' or 'desc')
        sort_within_groups: Within-group sort criteria ('score' or 'alphabetical')
        
    Returns:
        Sorted groups with sorted words
    """
    # First sort words within groups
    groups = sort_words_within_groups(groups, sort_within_groups)
    
    # Then sort the groups themselves
    groups = sort_groups(groups, group_sort_order)
    
    return groups


def get_available_sorting_options() -> Dict[str, List[Dict[str, str]]]:
    """
    Get available sorting options for the API.
    
    Returns:
        Dictionary with group and within-group sorting options
    """
    return {
        'group_sort': [
            {'value': 'asc', 'label': 'Ascending'},
            {'value': 'desc', 'label': 'Descending'}
        ],
        'within_group_sort': [
            {'value': 'score', 'label': 'By Score'},
            {'value': 'alphabetical', 'label': 'Alphabetically'}
        ]
    }
