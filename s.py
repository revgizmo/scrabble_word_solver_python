import itertools

# Scrabble letter scores
SCRABBLE_SCORES = {
    "a": 1, "b": 3, "c": 3, "d": 2, "e": 1, "f": 4, "g": 2, "h": 4, "i": 1, "j": 8, "k": 5,
    "l": 1, "m": 3, "n": 1, "o": 1, "p": 3, "q": 10, "r": 1, "s": 1, "t": 1, "u": 1, "v": 4,
    "w": 4, "x": 8, "y": 4, "z": 10
}

def calculate_word_score(word):
    """Calculate the Scrabble score for a word."""
    return sum(SCRABBLE_SCORES.get(letter, 0) for letter in word)

def load_dictionary(file_path):
    """Load the dictionary file into a set."""
    with open(file_path, 'r') as file:
        return set(word.strip().lower() for word in file)

def generate_valid_words(letters, dictionary):
    """Generate all valid Scrabble words from the given letters."""
    valid_words = set()
    for i in range(1, len(letters) + 1):
        for combination in itertools.permutations(letters, i):
            word = ''.join(combination)
            if word in dictionary:
                valid_words.add(word)
    return sorted(valid_words, key=calculate_word_score, reverse=True)

def main():
    # Input Scrabble letters
    letters = input("Enter your Scrabble letters (comma-separated): ").replace(",", "").lower()
    
    # Load dictionary
    dictionary = load_dictionary("dictionary.txt")  # Ensure you have a valid dictionary.txt file
    
    # Generate valid words
    valid_words = generate_valid_words(letters, dictionary)
    
    # Output sorted valid words with scores
    print("Valid Scrabble Words:")
    for word in valid_words:
        print(f"{word} ({calculate_word_score(word)} points)")

if __name__ == "__main__":
    main()