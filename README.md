# Scrabble Word Solver Python

A Python application that helps Scrabble players find the best possible words from their available letters. The solver generates all valid words from given letters and sorts them by their Scrabble point values.

## Features

- **Word Generation**: Finds all possible valid words from given letters using permutations
- **Scoring System**: Calculates Scrabble point values for each word using official letter scores
- **Dictionary Validation**: Uses a comprehensive dictionary (466,550+ words) to ensure only valid words are returned
- **Sorted Results**: Returns words sorted by point value (highest scoring first)
- **Interactive Interface**: Simple command-line interface for easy use

## Scrabble Letter Scores

The application uses the official Scrabble letter scoring system:
- 1 point: A, E, I, L, N, O, R, S, T, U
- 2 points: D, G
- 3 points: B, C, M, P
- 4 points: F, H, V, W, Y
- 5 points: K
- 8 points: J, X
- 10 points: Q, Z

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd scrabble_word_solver_python
```

2. Ensure you have Python 3.6+ installed:
```bash
python --version
```

3. No additional dependencies required - the project uses only Python standard library modules.

## Usage

### Command Line Interface

Run the main application:
```bash
python scrabble_solver.py
```

When prompted, enter your Scrabble letters (comma-separated or as a single string):
```
Enter your Scrabble letters (comma-separated): a,e,t,r,s
```

The application will output all valid words sorted by score:
```
Valid Scrabble Words:
star (4 points)
rate (4 points)
tear (4 points)
ear (3 points)
ate (3 points)
tea (3 points)
art (3 points)
rat (3 points)
tar (3 points)
as (2 points)
at (2 points)
ta (2 points)
a (1 points)
```

### Programmatic Usage

You can also use the functions in your own code:

```python
from scrabble_solver import calculate_word_score, generate_valid_words, load_dictionary

# Load dictionary
dictionary = load_dictionary("dictionary.txt")

# Generate words from letters
letters = "aetrs"
valid_words = generate_valid_words(letters, dictionary)

# Calculate score for a specific word
score = calculate_word_score("star")  # Returns 4
```

## Testing

Run the test suite to verify functionality:
```bash
python test_scrabble_solver.py
```

The tests cover:
- Word score calculation
- Valid word generation from letters
- Result sorting by score

## Development Environment Setup

1. **Python Environment**: The project works with Python 3.6+ and uses only standard library modules.

2. **Virtual Environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Code Quality**: Consider using tools like:
   - `pylint` for code linting
   - `black` for code formatting
   - `mypy` for type checking

4. **Running Tests**: The project includes unit tests that can be run with:
```bash
python -m unittest test_scrabble_solver.py
```

## Project Structure

```
scrabble_word_solver_python/
├── scrabble_solver.py      # Main application logic
├── test_scrabble_solver.py # Unit tests
├── dictionary.txt          # Word dictionary (466,550+ words)
├── requirements.txt        # Project dependencies (none external)
└── README.md              # This file
```

## Algorithm

The word generation algorithm:
1. Takes input letters from the user
2. Generates all possible permutations of the letters (1 to n letters)
3. Checks each permutation against the dictionary
4. Calculates Scrabble scores for valid words
5. Sorts results by score (descending)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is open source and available under the MIT License.