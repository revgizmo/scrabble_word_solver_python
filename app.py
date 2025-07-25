from flask import Flask, render_template, request, jsonify
from scrabble_solver import calculate_word_score, generate_valid_words, load_dictionary
import os

app = Flask(__name__)

# Load dictionary once when app starts
DICTIONARY_PATH = os.path.join(os.path.dirname(__file__), 'dictionary.txt')
dictionary = load_dictionary(DICTIONARY_PATH)

@app.route('/')
def index():
    """Main page with letter input form."""
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    """API endpoint to solve Scrabble words from letters."""
    try:
        data = request.get_json()
        letters = data.get('letters', '').lower().strip()
        
        if not letters:
            return jsonify({'error': 'No letters provided'}), 400
        
        # Remove any non-alphabetic characters
        letters = ''.join(c for c in letters if c.isalpha())
        
        if not letters:
            return jsonify({'error': 'No valid letters found'}), 400
        
        # Generate valid words
        valid_words = generate_valid_words(letters, dictionary)
        
        # Format results with scores
        results = []
        for word in valid_words:
            score = calculate_word_score(word)
            results.append({
                'word': word,
                'score': score,
                'length': len(word)
            })
        
        return jsonify({
            'letters': letters,
            'words': results,
            'total_words': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/score/<word>')
def get_word_score(word):
    """API endpoint to get score for a specific word."""
    try:
        word = word.lower().strip()
        if not word.isalpha():
            return jsonify({'error': 'Invalid word'}), 400
        
        score = calculate_word_score(word)
        return jsonify({
            'word': word,
            'score': score,
            'length': len(word)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) 