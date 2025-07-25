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
        expected = ["bat", "tab", "cat"]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
