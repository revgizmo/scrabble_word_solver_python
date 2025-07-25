import unittest
from scrabble_solver import calculate_word_score, generate_valid_words

class TestScrabbleSolver(unittest.TestCase):
    def test_calculate_word_score(self):
        self.assertEqual(calculate_word_score("hello"), 8)
        self.assertEqual(calculate_word_score("scrabble"), 14)
        self.assertEqual(calculate_word_score("quiz"), 22)

    def test_generate_valid_words(self):
        dictionary = {"cat", "bat", "tab", "rat", "art"}
        letters = "atcb"
        result = generate_valid_words(letters, dictionary)
        # Check that all expected words are present, regardless of order
        expected_words = {"bat", "tab", "cat"}
        result_words = set(result)
        self.assertEqual(result_words, expected_words)
        # Check that words are sorted by score (descending)
        for i in range(len(result) - 1):
            self.assertGreaterEqual(calculate_word_score(result[i]), calculate_word_score(result[i + 1]))

if __name__ == "__main__":
    unittest.main()
