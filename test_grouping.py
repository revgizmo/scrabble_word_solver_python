"""
Unit tests for grouping functionality in Scrabble Word Solver.
"""

import unittest
from utils.grouping import (
    extract_word_metadata, 
    group_by_length, 
    group_by_first_letter, 
    group_by_last_letter,
    group_words,
    get_available_grouping_options
)


class TestGrouping(unittest.TestCase):
    
    def setUp(self):
        """Set up test data."""
        self.sample_words = [
            {'word': 'cat', 'score': 5, 'length': 3},
            {'word': 'dog', 'score': 5, 'length': 3},
            {'word': 'star', 'score': 4, 'length': 4},
            {'word': 'moon', 'score': 6, 'length': 4},
            {'word': 'a', 'score': 1, 'length': 1},
            {'word': 'zoo', 'score': 12, 'length': 3}
        ]
    
    def test_extract_word_metadata(self):
        """Test extracting word metadata."""
        word_data = {'word': 'test', 'score': 4, 'length': 4}
        result = extract_word_metadata(word_data)
        
        expected = {
            'word': 'test',
            'score': 4,
            'length': 4,
            'first_letter': 't',
            'last_letter': 't'
        }
        
        self.assertEqual(result, expected)
    
    def test_group_by_length(self):
        """Test grouping words by length."""
        groups = group_by_length(self.sample_words)
        
        # Should have 3 groups: 1 letter, 3 letters, 4 letters
        self.assertEqual(len(groups), 3)
        
        # Check group names
        group_names = [group['name'] for group in groups]
        self.assertIn('1 letter', group_names)
        self.assertIn('3 letters', group_names)
        self.assertIn('4 letters', group_names)
        
        # Check 3-letter group
        three_letter_group = next(g for g in groups if g['name'] == '3 letters')
        self.assertEqual(three_letter_group['count'], 3)
        self.assertEqual(three_letter_group['total_score'], 22)  # 5+5+12
    
    def test_group_by_first_letter(self):
        """Test grouping words by first letter."""
        groups = group_by_first_letter(self.sample_words)
        
        # Should have groups for 'a', 'c', 'd', 'm', 's', 'z'
        self.assertEqual(len(groups), 6)
        
        # Check group names
        group_names = [group['name'] for group in groups]
        self.assertIn("Starts with 'A'", group_names)
        self.assertIn("Starts with 'C'", group_names)
        self.assertIn("Starts with 'Z'", group_names)
        
        # Check 'c' group
        c_group = next(g for g in groups if g['name'] == "Starts with 'C'")
        self.assertEqual(c_group['count'], 1)
        self.assertEqual(c_group['total_score'], 5)
    
    def test_group_by_last_letter(self):
        """Test grouping words by last letter."""
        groups = group_by_last_letter(self.sample_words)
        
        # Should have groups for 'a', 'g', 'n', 'r', 't', 'o'
        self.assertEqual(len(groups), 6)
        
        # Check group names
        group_names = [group['name'] for group in groups]
        self.assertIn("Ends with 'A'", group_names)
        self.assertIn("Ends with 'G'", group_names)
        self.assertIn("Ends with 'O'", group_names)
        
        # Check 'g' group
        g_group = next(g for g in groups if g['name'] == "Ends with 'G'")
        self.assertEqual(g_group['count'], 1)
        self.assertEqual(g_group['total_score'], 5)
    
    def test_group_words_length(self):
        """Test main grouping function with length grouping."""
        groups = group_words(self.sample_words, 'length')
        
        self.assertEqual(len(groups), 3)
        self.assertEqual(groups[0]['name'], '1 letter')
        self.assertEqual(groups[1]['name'], '3 letters')
        self.assertEqual(groups[2]['name'], '4 letters')
    
    def test_group_words_first_letter(self):
        """Test main grouping function with first letter grouping."""
        groups = group_words(self.sample_words, 'first_letter')
        
        self.assertEqual(len(groups), 6)
        # Should be sorted alphabetically
        self.assertEqual(groups[0]['name'], "Starts with 'A'")
        self.assertEqual(groups[5]['name'], "Starts with 'Z'")
    
    def test_group_words_last_letter(self):
        """Test main grouping function with last letter grouping."""
        groups = group_words(self.sample_words, 'last_letter')
        
        self.assertEqual(len(groups), 6)
        # Should be sorted alphabetically
        self.assertEqual(groups[0]['name'], "Ends with 'A'")
    
    def test_group_words_invalid_type(self):
        """Test grouping with invalid type defaults to length."""
        groups = group_words(self.sample_words, 'invalid_type')
        
        self.assertEqual(len(groups), 3)
        self.assertEqual(groups[0]['name'], '1 letter')
    
    def test_get_available_grouping_options(self):
        """Test getting available grouping options."""
        options = get_available_grouping_options()
        
        self.assertEqual(len(options), 3)
        
        option_values = [opt['value'] for opt in options]
        self.assertIn('length', option_values)
        self.assertIn('first_letter', option_values)
        self.assertIn('last_letter', option_values)
        
        option_labels = [opt['label'] for opt in options]
        self.assertIn('By Word Length', option_labels)
        self.assertIn('By First Letter', option_labels)
        self.assertIn('By Last Letter', option_labels)
    
    def test_empty_word_list(self):
        """Test grouping with empty word list."""
        groups = group_words([], 'length')
        self.assertEqual(groups, [])
        
        groups = group_by_length([])
        self.assertEqual(groups, [])
        
        groups = group_by_first_letter([])
        self.assertEqual(groups, [])
        
        groups = group_by_last_letter([])
        self.assertEqual(groups, [])


if __name__ == '__main__':
    unittest.main()
