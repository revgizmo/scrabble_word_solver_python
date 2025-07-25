#!/usr/bin/env python3
"""
Example usage of the Scrabble Word Solver
This script demonstrates how to use the scrabble_solver module programmatically.
"""

from scrabble_solver import calculate_word_score, generate_valid_words, load_dictionary

def main():
    print("Scrabble Word Solver - Example Usage")
    print("=" * 40)
    
    # Example 1: Calculate word scores
    print("\n1. Word Score Examples:")
    test_words = ["hello", "scrabble", "quiz", "python"]
    for word in test_words:
        score = calculate_word_score(word)
        print(f"   '{word}' = {score} points")
    
    # Example 2: Generate words from letters
    print("\n2. Word Generation Examples:")
    
    # Load dictionary
    try:
        dictionary = load_dictionary("dictionary.txt")
        print("   Dictionary loaded successfully!")
    except FileNotFoundError:
        print("   Error: dictionary.txt not found!")
        return
    
    # Test with different letter sets
    test_letters = [
        ("aetrs", "Letters: A, E, T, R, S"),
        ("python", "Letters: P, Y, T, H, O, N"),
        ("scrabble", "Letters: S, C, R, A, B, B, L, E")
    ]
    
    for letters, description in test_letters:
        print(f"\n   {description}")
        valid_words = generate_valid_words(letters, dictionary)
        
        # Show top 5 results
        top_words = valid_words[:5]
        for word in top_words:
            score = calculate_word_score(word)
            print(f"     {word} ({score} points)")
        
        if len(valid_words) > 5:
            print(f"     ... and {len(valid_words) - 5} more words")
    
    print("\n" + "=" * 40)
    print("Example completed!")

if __name__ == "__main__":
    main() 