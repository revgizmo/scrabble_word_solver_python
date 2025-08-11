"""
Unit tests for filtering functionality in Scrabble Word Solver.
"""

import unittest
from utils.filtering import (
    filter_words_by_length,
    filter_words_by_first_letter,
    filter_words_by_last_letter,
    apply_filters,
    validate_filters,
    get_filter_summary
)


class TestFiltering(unittest.TestCase):
    
    def setUp(self):
        """Set up test data."""
        self.sample_words = [
            {'word': 'cat', 'score': 5, 'length': 3},
            {'word': 'dog', 'score': 5, 'length': 3},
            {'word': 'star', 'score': 4, 'length': 4},
            {'word': 'moon', 'score': 6, 'length': 4},
            {'word': 'a', 'score': 1, 'length': 1},
            {'word': 'zoo', 'score': 12, 'length': 3},
            {'word': 'apple', 'score': 9, 'length': 5},
            {'word': 'banana', 'score': 8, 'length': 6}
        ]
    
    def test_filter_words_by_length_min_only(self):
        """Test filtering words by minimum length only."""
        filtered = filter_words_by_length(self.sample_words, min_length=4)
        
        # Should only include words with length >= 4
        self.assertEqual(len(filtered), 4)
        for word in filtered:
            self.assertGreaterEqual(word['length'], 4)
    
    def test_filter_words_by_length_max_only(self):
        """Test filtering words by maximum length only."""
        filtered = filter_words_by_length(self.sample_words, max_length=3)
        
        # Should only include words with length <= 3
        self.assertEqual(len(filtered), 4)
        for word in filtered:
            self.assertLessEqual(word['length'], 3)
    
    def test_filter_words_by_length_range(self):
        """Test filtering words by length range."""
        filtered = filter_words_by_length(self.sample_words, min_length=3, max_length=4)
        
        # Should only include words with length 3-4
        self.assertEqual(len(filtered), 5)
        for word in filtered:
            self.assertGreaterEqual(word['length'], 3)
            self.assertLessEqual(word['length'], 4)
    
    def test_filter_words_by_length_no_filters(self):
        """Test filtering words by length with no filters."""
        filtered = filter_words_by_length(self.sample_words)
        
        # Should return all words
        self.assertEqual(len(filtered), len(self.sample_words))
    
    def test_filter_words_by_first_letter(self):
        """Test filtering words by first letter."""
        filtered = filter_words_by_first_letter(self.sample_words, 'a')
        
        # Should only include words starting with 'a'
        self.assertEqual(len(filtered), 2)  # 'a' and 'apple'
        for word in filtered:
            self.assertTrue(word['word'].startswith('a'))
    
    def test_filter_words_by_first_letter_case_insensitive(self):
        """Test filtering words by first letter (case insensitive)."""
        filtered = filter_words_by_first_letter(self.sample_words, 'A')
        
        # Should only include words starting with 'a' (case insensitive)
        self.assertEqual(len(filtered), 2)  # 'a' and 'apple'
        for word in filtered:
            self.assertTrue(word['word'].lower().startswith('a'))
    
    def test_filter_words_by_first_letter_no_match(self):
        """Test filtering words by first letter with no matches."""
        filtered = filter_words_by_first_letter(self.sample_words, 'x')
        
        # Should return empty list
        self.assertEqual(len(filtered), 0)
    
    def test_filter_words_by_first_letter_no_filter(self):
        """Test filtering words by first letter with no filter."""
        filtered = filter_words_by_first_letter(self.sample_words, None)
        
        # Should return all words
        self.assertEqual(len(filtered), len(self.sample_words))
    
    def test_filter_words_by_last_letter(self):
        """Test filtering words by last letter."""
        filtered = filter_words_by_last_letter(self.sample_words, 'r')
        
        # Should only include words ending with 'r'
        self.assertEqual(len(filtered), 1)  # 'star'
        for word in filtered:
            self.assertTrue(word['word'].endswith('r'))
    
    def test_filter_words_by_last_letter_case_insensitive(self):
        """Test filtering words by last letter (case insensitive)."""
        filtered = filter_words_by_last_letter(self.sample_words, 'R')
        
        # Should only include words ending with 'r' (case insensitive)
        self.assertEqual(len(filtered), 1)  # 'star'
        for word in filtered:
            self.assertTrue(word['word'].lower().endswith('r'))
    
    def test_filter_words_by_last_letter_no_match(self):
        """Test filtering words by last letter with no matches."""
        filtered = filter_words_by_last_letter(self.sample_words, 'x')
        
        # Should return empty list
        self.assertEqual(len(filtered), 0)
    
    def test_filter_words_by_last_letter_no_filter(self):
        """Test filtering words by last letter with no filter."""
        filtered = filter_words_by_last_letter(self.sample_words, None)
        
        # Should return all words
        self.assertEqual(len(filtered), len(self.sample_words))
    
    def test_apply_filters_length_only(self):
        """Test applying length filters only."""
        filters = {'min_length': 4, 'max_length': 5}
        filtered = apply_filters(self.sample_words, filters)
        
        # Should only include words with length 4-5
        self.assertEqual(len(filtered), 3)  # 'star', 'moon', 'apple'
        for word in filtered:
            self.assertGreaterEqual(word['length'], 4)
            self.assertLessEqual(word['length'], 5)
    
    def test_apply_filters_letter_only(self):
        """Test applying letter filters only."""
        filters = {'starts_with': 'a', 'ends_with': 'e'}
        filtered = apply_filters(self.sample_words, filters)
        
        # Should only include words starting with 'a' and ending with 'e'
        self.assertEqual(len(filtered), 1)  # 'apple'
        for word in filtered:
            self.assertTrue(word['word'].lower().startswith('a'))
            self.assertTrue(word['word'].lower().endswith('e'))
    
    def test_apply_filters_combined(self):
        """Test applying combined filters."""
        filters = {
            'min_length': 3,
            'max_length': 4,
            'starts_with': 's'
        }
        filtered = apply_filters(self.sample_words, filters)
        
        # Should only include words with length 3-4 starting with 's'
        self.assertEqual(len(filtered), 1)  # 'star'
        for word in filtered:
            self.assertGreaterEqual(word['length'], 3)
            self.assertLessEqual(word['length'], 4)
            self.assertTrue(word['word'].lower().startswith('s'))
    
    def test_apply_filters_no_filters(self):
        """Test applying no filters."""
        filtered = apply_filters(self.sample_words, None)
        
        # Should return all words
        self.assertEqual(len(filtered), len(self.sample_words))
    
    def test_apply_filters_empty_filters(self):
        """Test applying empty filters."""
        filtered = apply_filters(self.sample_words, {})
        
        # Should return all words
        self.assertEqual(len(filtered), len(self.sample_words))
    
    def test_validate_filters_valid(self):
        """Test validating valid filters."""
        filters = {
            'min_length': 3,
            'max_length': 5,
            'starts_with': 'a',
            'ends_with': 'e'
        }
        errors = validate_filters(filters)
        
        # Should have no errors
        self.assertEqual(len(errors), 0)
    
    def test_validate_filters_invalid_min_length(self):
        """Test validating invalid minimum length."""
        filters = {'min_length': 0}
        errors = validate_filters(filters)
        
        # Should have error for min_length
        self.assertIn('min_length', errors)
    
    def test_validate_filters_invalid_max_length(self):
        """Test validating invalid maximum length."""
        filters = {'max_length': -1}
        errors = validate_filters(filters)
        
        # Should have error for max_length
        self.assertIn('max_length', errors)
    
    def test_validate_filters_invalid_range(self):
        """Test validating invalid length range."""
        filters = {'min_length': 5, 'max_length': 3}
        errors = validate_filters(filters)
        
        # Should have error for length_range
        self.assertIn('length_range', errors)
    
    def test_validate_filters_invalid_starts_with(self):
        """Test validating invalid starts_with filter."""
        filters = {'starts_with': 'ab'}  # More than one character
        errors = validate_filters(filters)
        
        # Should have error for starts_with
        self.assertIn('starts_with', errors)
    
    def test_validate_filters_invalid_ends_with(self):
        """Test validating invalid ends_with filter."""
        filters = {'ends_with': '123'}  # Non-alphabetic
        errors = validate_filters(filters)
        
        # Should have error for ends_with
        self.assertIn('ends_with', errors)
    
    def test_validate_filters_no_filters(self):
        """Test validating no filters."""
        errors = validate_filters(None)
        
        # Should have no errors
        self.assertEqual(len(errors), 0)
    
    def test_get_filter_summary_no_filters(self):
        """Test getting filter summary with no filters."""
        summary = get_filter_summary({})
        
        # Should return "No filters applied"
        self.assertEqual(summary, "No filters applied")
    
    def test_get_filter_summary_length_only(self):
        """Test getting filter summary with length filters only."""
        filters = {'min_length': 3, 'max_length': 5}
        summary = get_filter_summary(filters)
        
        # Should include length filters
        self.assertIn("min length: 3", summary)
        self.assertIn("max length: 5", summary)
    
    def test_get_filter_summary_letter_only(self):
        """Test getting filter summary with letter filters only."""
        filters = {'starts_with': 'a', 'ends_with': 'e'}
        summary = get_filter_summary(filters)
        
        # Should include letter filters
        self.assertIn("starts with: 'A'", summary)
        self.assertIn("ends with: 'E'", summary)
    
    def test_get_filter_summary_combined(self):
        """Test getting filter summary with combined filters."""
        filters = {
            'min_length': 3,
            'max_length': 5,
            'starts_with': 'a',
            'ends_with': 'e'
        }
        summary = get_filter_summary(filters)
        
        # Should include all filters
        self.assertIn("min length: 3", summary)
        self.assertIn("max length: 5", summary)
        self.assertIn("starts with: 'A'", summary)
        self.assertIn("ends with: 'E'", summary)
    
    def test_empty_word_list(self):
        """Test filtering with empty word list."""
        filtered = filter_words_by_length([], min_length=3)
        self.assertEqual(filtered, [])
        
        filtered = filter_words_by_first_letter([], 'a')
        self.assertEqual(filtered, [])
        
        filtered = filter_words_by_last_letter([], 'e')
        self.assertEqual(filtered, [])
        
        filtered = apply_filters([], {'min_length': 3})
        self.assertEqual(filtered, [])


if __name__ == '__main__':
    unittest.main()
