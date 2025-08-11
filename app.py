from flask import Flask, render_template, request, jsonify
from scrabble_solver import calculate_word_score, generate_valid_words, load_dictionary
from utils.grouping import group_words, get_available_grouping_options
from utils.sorting import apply_sorting, sort_flat_words, get_available_sorting_options
from utils.filtering import apply_filters, validate_filters, get_filter_summary
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
    """API endpoint to solve Scrabble words from letters with grouping and filtering."""
    try:
        data = request.get_json()
        letters = data.get('letters', '').lower().strip()
        
        if not letters:
            return jsonify({'error': 'No letters provided'}), 400
        
        # Remove any non-alphabetic characters
        letters = ''.join(c for c in letters if c.isalpha())
        
        if not letters:
            return jsonify({'error': 'No valid letters found'}), 400
        
        # Get grouping and sorting parameters
        group_by = data.get('group_by', 'length')
        sort_groups = data.get('sort_groups', 'asc')
        sort_within_groups = data.get('sort_within_groups', 'score')
        view_type = data.get('view_type', 'grouped')  # 'grouped' or 'flat'
        filters = data.get('filters', {})
        
        # Validate filters
        filter_errors = validate_filters(filters)
        if filter_errors:
            return jsonify({'error': 'Invalid filters', 'details': filter_errors}), 400
        
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
        
        # Apply filters
        filtered_results = apply_filters(results, filters)
        
        # Prepare response based on view type
        if view_type == 'flat':
            # Sort flat results
            sorted_results = sort_flat_words(filtered_results, sort_within_groups)
            
            return jsonify({
                'letters': letters,
                'words': sorted_results,
                'total_words': len(sorted_results),
                'view_type': 'flat',
                'filters_applied': get_filter_summary(filters)
            })
        else:
            # Group and sort results
            groups = group_words(filtered_results, group_by)
            sorted_groups = apply_sorting(groups, sort_groups, sort_within_groups)
            
            return jsonify({
                'letters': letters,
                'total_words': len(filtered_results),
                'view_type': 'grouped',
                'grouping': {
                    'type': group_by,
                    'sort_order': sort_groups,
                    'groups': sorted_groups
                },
                'filters_applied': get_filter_summary(filters)
            })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/groups')
def get_grouping_options():
    """API endpoint to get available grouping options."""
    try:
        return jsonify({
            'options': get_available_grouping_options()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sorting')
def get_sorting_options():
    """API endpoint to get available sorting options."""
    try:
        return jsonify(get_available_sorting_options())
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