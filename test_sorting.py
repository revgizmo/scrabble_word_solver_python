"""
Unit tests for sorting functionality in Scrabble Word Solver.
"""

import unittest
from utils.sorting import (
    sort_groups,
    sort_words_within_groups,
    sort_flat_words,
    apply_sorting,
    get_available_sorting_options
)


class TestSorting(unittest.TestCase):
    
    def setUp(self):
        """Set up test data."""
        self.sample_groups = [
            {
                'name': '4 letters',
                'count': 2,
                'total_score': 10,
                'words': [
                    {'word': 'star', 'score': 4, 'length': 4},
                    {'word': 'moon', 'score': 6, 'length': 4}
                ]
            },
            {
                'name': '3 letters',
                'count': 3,
                'total_score': 22,
                'words': [
                    {'word': 'cat', 'score': 5, 'length': 3},
                    {'word': 'dog', 'score': 5, 'length': 3},
                    {'word': 'zoo', 'score': 12, 'length': 3}
                ]
            },
            {
                'name': '1 letter',
                'count': 1,
                'total_score': 1,
                'words': [
                    {'word': 'a', 'score': 1, 'length': 1}
                ]
            }
        ]
        
        self.sample_words = [
            {'word': 'cat', 'score': 5, 'length': 3},
            {'word': 'dog', 'score': 5, 'length': 3},
            {'word': 'star', 'score': 4, 'length': 4},
            {'word': 'moon', 'score': 6, 'length': 4},
            {'word': 'a', 'score': 1, 'length': 1},
            {'word': 'zoo', 'score': 12, 'length': 3}
        ]
    
    def test_sort_groups_ascending(self):
        """Test sorting groups in ascending order."""
        sorted_groups = sort_groups(self.sample_groups, 'asc')
        
        # Should be sorted by length: 1, 3, 4
        self.assertEqual(sorted_groups[0]['name'], '1 letter')
        self.assertEqual(sorted_groups[1]['name'], '3 letters')
        self.assertEqual(sorted_groups[2]['name'], '4 letters')
    
    def test_sort_groups_descending(self):
        """Test sorting groups in descending order."""
        sorted_groups = sort_groups(self.sample_groups, 'desc')
        
        # Should be sorted by length: 4, 3, 1
        self.assertEqual(sorted_groups[0]['name'], '4 letters')
        self.assertEqual(sorted_groups[1]['name'], '3 letters')
        self.assertEqual(sorted_groups[2]['name'], '1 letter')
    
    def test_sort_groups_letter_groups(self):
        """Test sorting letter-based groups."""
        letter_groups = [
            {'name': "Starts with 'Z'", 'count': 1, 'total_score': 12, 'words': []},
            {'name': "Starts with 'A'", 'count': 1, 'total_score': 1, 'words': []},
            {'name': "Starts with 'C'", 'count': 1, 'total_score': 5, 'words': []}
        ]
        
        sorted_groups = sort_groups(letter_groups, 'asc')
        
        # Should be sorted alphabetically: A, C, Z
        self.assertEqual(sorted_groups[0]['name'], "Starts with 'A'")
        self.assertEqual(sorted_groups[1]['name'], "Starts with 'C'")
        self.assertEqual(sorted_groups[2]['name'], "Starts with 'Z'")
    
    def test_sort_words_within_groups_by_score(self):
        """Test sorting words within groups by score."""
        sorted_groups = sort_words_within_groups(self.sample_groups, 'score')
        
        # Check that words are sorted by score (descending) within each group
        for group in sorted_groups:
            scores = [word['score'] for word in group['words']]
            self.assertEqual(scores, sorted(scores, reverse=True))
    
    def test_sort_words_within_groups_alphabetically(self):
        """Test sorting words within groups alphabetically."""
        sorted_groups = sort_words_within_groups(self.sample_groups, 'alphabetical')
        
        # Check that words are sorted alphabetically within each group
        for group in sorted_groups:
            words = [word['word'] for word in group['words']]
            self.assertEqual(words, sorted(words))
    
    def test_sort_flat_words_by_score(self):
        """Test sorting flat word list by score."""
        sorted_words = sort_flat_words(self.sample_words, 'score')
        
        # Should be sorted by score (descending)
        scores = [word['score'] for word in sorted_words]
        self.assertEqual(scores, sorted(scores, reverse=True))
        
        # Highest score should be first
        self.assertEqual(sorted_words[0]['word'], 'zoo')
        self.assertEqual(sorted_words[0]['score'], 12)
    
    def test_sort_flat_words_alphabetically(self):
        """Test sorting flat word list alphabetically."""
        sorted_words = sort_flat_words(self.sample_words, 'alphabetical')
        
        # Should be sorted alphabetically
        words = [word['word'] for word in sorted_words]
        self.assertEqual(words, sorted(words))
        
        # First word should be 'a'
        self.assertEqual(sorted_words[0]['word'], 'a')
    
    def test_sort_flat_words_invalid_criteria(self):
        """Test sorting flat words with invalid criteria defaults to score."""
        sorted_words = sort_flat_words(self.sample_words, 'invalid')
        
        # Should default to score sorting
        scores = [word['score'] for word in sorted_words]
        self.assertEqual(scores, sorted(scores, reverse=True))
    
    def test_apply_sorting(self):
        """Test applying sorting to groups and words within groups."""
        sorted_groups = apply_sorting(self.sample_groups, 'asc', 'score')
        
        # Groups should be sorted ascending
        self.assertEqual(sorted_groups[0]['name'], '1 letter')
        self.assertEqual(sorted_groups[1]['name'], '3 letters')
        self.assertEqual(sorted_groups[2]['name'], '4 letters')
        
        # Words within groups should be sorted by score
        for group in sorted_groups:
            scores = [word['score'] for word in group['words']]
            self.assertEqual(scores, sorted(scores, reverse=True))
    
    def test_apply_sorting_descending_alphabetical(self):
        """Test applying sorting with descending groups and alphabetical words."""
        sorted_groups = apply_sorting(self.sample_groups, 'desc', 'alphabetical')
        
        # Groups should be sorted descending
        self.assertEqual(sorted_groups[0]['name'], '4 letters')
        self.assertEqual(sorted_groups[1]['name'], '3 letters')
        self.assertEqual(sorted_groups[2]['name'], '1 letter')
        
        # Words within groups should be sorted alphabetically
        for group in sorted_groups:
            words = [word['word'] for word in group['words']]
            self.assertEqual(words, sorted(words))
    
    def test_get_available_sorting_options(self):
        """Test getting available sorting options."""
        options = get_available_sorting_options()
        
        self.assertIn('group_sort', options)
        self.assertIn('within_group_sort', options)
        
        # Check group sort options
        group_sort_options = options['group_sort']
        self.assertEqual(len(group_sort_options), 2)
        
        group_sort_values = [opt['value'] for opt in group_sort_options]
        self.assertIn('asc', group_sort_values)
        self.assertIn('desc', group_sort_values)
        
        # Check within group sort options
        within_group_options = options['within_group_sort']
        self.assertEqual(len(within_group_options), 2)
        
        within_group_values = [opt['value'] for opt in within_group_options]
        self.assertIn('score', within_group_values)
        self.assertIn('alphabetical', within_group_values)
    
    def test_empty_groups(self):
        """Test sorting with empty groups list."""
        sorted_groups = sort_groups([], 'asc')
        self.assertEqual(sorted_groups, [])
        
        sorted_groups = sort_words_within_groups([], 'score')
        self.assertEqual(sorted_groups, [])
        
        sorted_groups = apply_sorting([], 'asc', 'score')
        self.assertEqual(sorted_groups, [])
    
    def test_empty_words(self):
        """Test sorting with empty words list."""
        sorted_words = sort_flat_words([], 'score')
        self.assertEqual(sorted_words, [])
    
    def test_single_group(self):
        """Test sorting with single group."""
        single_group = [self.sample_groups[0]]
        sorted_groups = sort_groups(single_group, 'asc')
        self.assertEqual(len(sorted_groups), 1)
        self.assertEqual(sorted_groups[0]['name'], '4 letters')
    
    def test_single_word(self):
        """Test sorting with single word."""
        single_word = [self.sample_words[0]]
        sorted_words = sort_flat_words(single_word, 'score')
        self.assertEqual(len(sorted_words), 1)
        self.assertEqual(sorted_words[0]['word'], 'cat')


if __name__ == '__main__':
    unittest.main()
