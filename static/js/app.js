// Scrabble Word Solver JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('scrabble-form');
    const lettersInput = document.getElementById('letters-input');
    const solveBtn = document.getElementById('solve-btn');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const error = document.getElementById('error');
    const wordsContainer = document.getElementById('words-container');
    const inputLetters = document.getElementById('input-letters');
    const wordCount = document.getElementById('word-count');
    const errorMessage = document.getElementById('error-message');

    // Form submission handler
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        solveWords();
    });

    // Enter key handler
    lettersInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            solveWords();
        }
    });

    // Input validation
    lettersInput.addEventListener('input', function() {
        validateInput();
    });

    function validateInput() {
        const letters = lettersInput.value.toLowerCase().replace(/[^a-z]/g, '');
        lettersInput.value = letters;
        
        if (letters.length > 15) {
            lettersInput.value = letters.substring(0, 15);
        }
        
        // Remove validation classes
        lettersInput.classList.remove('is-valid', 'is-invalid');
        
        if (letters.length > 0) {
            lettersInput.classList.add('is-valid');
        }
    }

    async function solveWords() {
        const letters = lettersInput.value.trim();
        
        if (!letters) {
            showError('Please enter some letters');
            return;
        }

        // Show loading state
        showLoading();
        hideError();
        hideResults();

        try {
            const response = await fetch('/solve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ letters: letters })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to solve words');
            }

            displayResults(data);
            
        } catch (err) {
            showError(err.message);
        } finally {
            hideLoading();
        }
    }

    function displayResults(data) {
        // Update header information
        inputLetters.textContent = data.letters.toUpperCase();
        wordCount.textContent = `${data.total_words} word${data.total_words !== 1 ? 's' : ''}`;

        // Clear previous results
        wordsContainer.innerHTML = '';

        if (data.words.length === 0) {
            wordsContainer.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i>
                    No valid words found with the letters "${data.letters.toUpperCase()}"
                </div>
            `;
        } else {
            // Create word items
            data.words.forEach((wordData, index) => {
                const wordItem = createWordItem(wordData, index + 1);
                wordsContainer.appendChild(wordItem);
            });
        }

        showResults();
    }

    function createWordItem(wordData, rank) {
        const wordItem = document.createElement('div');
        wordItem.className = 'word-item d-flex justify-content-between align-items-center';
        
        const scoreClass = getScoreClass(wordData.score);
        
        wordItem.innerHTML = `
            <div class="d-flex align-items-center">
                <span class="badge bg-secondary me-3">#${rank}</span>
                <div>
                    <div class="word-text">${wordData.word.toUpperCase()}</div>
                    <div class="word-length">${wordData.length} letter${wordData.length !== 1 ? 's' : ''}</div>
                </div>
            </div>
            <div class="d-flex align-items-center">
                <span class="score-badge ${scoreClass} me-2">${wordData.score} pts</span>
                <button class="copy-btn" onclick="copyToClipboard('${wordData.word}')" title="Copy word">
                    <i class="fas fa-copy"></i>
                </button>
            </div>
        `;

        return wordItem;
    }

    function getScoreClass(score) {
        if (score >= 10) return 'high-score';
        if (score >= 5) return 'medium-score';
        return 'low-score';
    }

    function showLoading() {
        loading.classList.remove('d-none');
        solveBtn.disabled = true;
    }

    function hideLoading() {
        loading.classList.add('d-none');
        solveBtn.disabled = false;
    }

    function showResults() {
        results.classList.remove('d-none');
    }

    function hideResults() {
        results.classList.add('d-none');
    }

    function showError(message) {
        errorMessage.textContent = message;
        error.classList.remove('d-none');
    }

    function hideError() {
        error.classList.add('d-none');
    }
});

// Global function for copying to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        // Find the button that was clicked
        const buttons = document.querySelectorAll('.copy-btn');
        buttons.forEach(btn => {
            if (btn.querySelector('i').classList.contains('fa-copy')) {
                btn.classList.remove('copied');
            }
        });
        
        // Find the specific button and update it
        const clickedButton = event.target.closest('.copy-btn');
        if (clickedButton) {
            const icon = clickedButton.querySelector('i');
            icon.classList.remove('fa-copy');
            icon.classList.add('fa-check');
            clickedButton.classList.add('copied');
            
            // Reset after 2 seconds
            setTimeout(() => {
                icon.classList.remove('fa-check');
                icon.classList.add('fa-copy');
                clickedButton.classList.remove('copied');
            }, 2000);
        }
    }).catch(function(err) {
        console.error('Failed to copy text: ', err);
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
    });
}

// Add some keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to solve
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        document.getElementById('scrabble-form').dispatchEvent(new Event('submit'));
    }
    
    // Escape to clear input
    if (e.key === 'Escape') {
        document.getElementById('letters-input').value = '';
        document.getElementById('letters-input').focus();
    }
}); 