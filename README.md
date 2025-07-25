# Scrabble Word Solver Python

A Python web application that helps Scrabble players find the best possible words from their available letters. The solver generates all valid words from given letters and sorts them by their Scrabble point values.

## Features

- **Web Interface**: Modern, responsive web application built with Flask
- **Word Generation**: Finds all possible valid words from given letters using permutations
- **Scoring System**: Calculates Scrabble point values for each word using official letter scores
- **Dictionary Validation**: Uses a comprehensive dictionary (466,550+ words) to ensure only valid words are returned
- **Sorted Results**: Returns words sorted by point value (highest scoring first)
- **Interactive UI**: Beautiful, modern interface with copy-to-clipboard functionality
- **API Endpoints**: RESTful API for programmatic access
- **Mobile Responsive**: Works perfectly on desktop and mobile devices

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

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd scrabble_word_solver_python
```

2. Ensure you have Python 3.6+ installed:
```bash
python --version
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5001`

### Heroku Deployment

The application is configured for easy deployment to Heroku:

1. Install Heroku CLI and login:
```bash
# Install Heroku CLI (if not already installed)
# Visit: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login
```

2. Create a new Heroku app:
```bash
heroku create your-scrabble-solver-app-name
```

3. Deploy to Heroku:
```bash
git add .
git commit -m "Initial Heroku deployment"
git push heroku main
```

4. Open your deployed app:
```bash
heroku open
```

## Usage

### Web Interface

1. Open the web application in your browser
2. Enter your Scrabble letters in the input field (up to 15 letters)
3. Click "Find Words" or press Enter
4. View the results sorted by score (highest first)
5. Click the copy icon next to any word to copy it to your clipboard

### API Usage

The application provides RESTful API endpoints:

#### Solve Words
```bash
POST /solve
Content-Type: application/json

{
  "letters": "aetrs"
}
```

Response:
```json
{
  "letters": "aetrs",
  "total_words": 64,
  "words": [
    {
      "word": "aster",
      "score": 5,
      "length": 5
    },
    ...
  ]
}
```

#### Get Word Score
```bash
GET /api/score/aster
```

Response:
```json
{
  "word": "aster",
  "score": 5,
  "length": 5
}
```

### Command Line Interface (Legacy)

You can still use the original command-line interface:

```bash
python scrabble_solver.py
```

When prompted, enter your Scrabble letters (comma-separated or as a single string):
```
Enter your Scrabble letters (comma-separated): a,e,t,r,s
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

## Project Structure

```
scrabble_word_solver_python/
├── app.py                 # Main Flask application
├── scrabble_solver.py     # Core Scrabble logic
├── test_scrabble_solver.py # Unit tests
├── dictionary.txt         # Word dictionary (466,550+ words)
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment configuration
├── runtime.txt           # Python version for Heroku
├── templates/
│   ├── base.html         # Base HTML template
│   └── index.html        # Main page template
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── app.js        # Frontend JavaScript
└── README.md             # This file
```

## Algorithm

The word generation algorithm:
1. Takes input letters from the user
2. Generates all possible permutations of the letters (1 to n letters)
3. Checks each permutation against the dictionary
4. Calculates Scrabble scores for valid words
5. Sorts results by score (descending)

## Web App Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Validation**: Input validation with visual feedback
- **Loading States**: Visual feedback during word generation
- **Copy to Clipboard**: One-click copying of words
- **Score Highlighting**: Color-coded scores (high/medium/low)
- **Keyboard Shortcuts**: Ctrl+Enter to solve, Escape to clear
- **Error Handling**: User-friendly error messages

## Deployment

### Heroku Configuration

The application includes all necessary files for Heroku deployment:

- `Procfile`: Tells Heroku to run the Flask app with gunicorn
- `runtime.txt`: Specifies Python 3.11.7
- `requirements.txt`: Lists all Python dependencies

### Environment Variables

No environment variables are required for basic functionality. The dictionary file is included in the repository.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is open source and available under the MIT License.