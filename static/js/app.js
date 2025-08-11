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
    
    // Advanced options elements
    const toggleAdvanced = document.getElementById('toggle-advanced');
    const advancedOptions = document.getElementById('advanced-options');
    const groupBy = document.getElementById('group-by');
    const sortGroups = document.getElementById('sort-groups');
    const sortWithinGroups = document.getElementById('sort-within-groups');
    const viewTypeGrouped = document.getElementById('view-grouped');
    const viewTypeFlat = document.getElementById('view-flat');
    const minLength = document.getElementById('min-length');
    const maxLength = document.getElementById('max-length');
    const startsWith = document.getElementById('starts-with');
    const endsWith = document.getElementById('ends-with');
    
    // Results elements
    const filterSummary = document.getElementById('filter-summary');
    const filterText = document.getElementById('filter-text');
    const resultsViewToggle = document.getElementById('results-view-toggle');
    const toggleGroupedView = document.getElementById('toggle-grouped-view');
    const toggleFlatView = document.getElementById('toggle-flat-view');
    
    // Store current results data
    let currentResults = null;

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

    // Advanced options toggle
    toggleAdvanced.addEventListener('click', function() {
        const isVisible = !advancedOptions.classList.contains('d-none');
        if (isVisible) {
            advancedOptions.classList.add('d-none');
            toggleAdvanced.innerHTML = '<i class="fas fa-chevron-down"></i> Show Options';
        } else {
            advancedOptions.classList.remove('d-none');
            toggleAdvanced.innerHTML = '<i class="fas fa-chevron-up"></i> Hide Options';
        }
    });

    // Results view toggle handlers
    toggleGroupedView.addEventListener('click', function() {
        if (currentResults && currentResults.view_type === 'grouped') {
            displayGroupedResults(currentResults);
        }
        toggleGroupedView.classList.add('active');
        toggleFlatView.classList.remove('active');
    });

    toggleFlatView.addEventListener('click', function() {
        if (currentResults && currentResults.view_type === 'grouped') {
            displayFlatResults(currentResults);
        }
        toggleFlatView.classList.add('active');
        toggleGroupedView.classList.remove('active');
    });

    // Input validation
    lettersInput.addEventListener('input', function() {
        validateInput();
    });

    // Filter input validation
    startsWith.addEventListener('input', function() {
        this.value = this.value.replace(/[^a-zA-Z]/g, '').toUpperCase();
    });

    endsWith.addEventListener('input', function() {
        this.value = this.value.replace(/[^a-zA-Z]/g, '').toUpperCase();
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
            // Prepare request data
            const requestData = {
                letters: letters,
                group_by: groupBy.value,
                sort_groups: sortGroups.value,
                sort_within_groups: sortWithinGroups.value,
                view_type: viewTypeGrouped.checked ? 'grouped' : 'flat',
                filters: {}
            };

            // Add filters if they have values
            if (minLength.value) requestData.filters.min_length = parseInt(minLength.value);
            if (maxLength.value) requestData.filters.max_length = parseInt(maxLength.value);
            if (startsWith.value) requestData.filters.starts_with = startsWith.value.toLowerCase();
            if (endsWith.value) requestData.filters.ends_with = endsWith.value.toLowerCase();

            const response = await fetch('/solve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to solve words');
            }

            currentResults = data;
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

        // Show filter summary if filters were applied
        if (data.filters_applied && data.filters_applied !== 'No filters applied') {
            filterText.textContent = data.filters_applied;
            filterSummary.classList.remove('d-none');
        } else {
            filterSummary.classList.add('d-none');
        }

        // Show results view toggle for grouped results
        if (data.view_type === 'grouped') {
            resultsViewToggle.classList.remove('d-none');
        } else {
            resultsViewToggle.classList.add('d-none');
        }

        // Clear previous results
        wordsContainer.innerHTML = '';

        if (data.total_words === 0) {
            wordsContainer.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i>
                    No valid words found with the letters "${data.letters.toUpperCase()}"
                </div>
            `;
        } else if (data.view_type === 'grouped') {
            displayGroupedResults(data);
        } else {
            displayFlatResults(data);
        }

        showResults();
    }

    function displayGroupedResults(data) {
        wordsContainer.innerHTML = '';
        
        if (data.grouping && data.grouping.groups) {
            data.grouping.groups.forEach((group, groupIndex) => {
                const groupElement = createGroupElement(group, groupIndex);
                wordsContainer.appendChild(groupElement);
            });
        }
    }

    function displayFlatResults(data) {
        wordsContainer.innerHTML = '';
        
        if (data.words) {
            data.words.forEach((wordData, index) => {
                const wordItem = createWordItem(wordData, index + 1);
                wordsContainer.appendChild(wordItem);
            });
        }
    }

    function createGroupElement(group, groupIndex) {
        const groupDiv = document.createElement('div');
        groupDiv.className = 'group-container mb-4';
        
        const groupHeader = createGroupHeader(group, groupIndex);
        const groupContent = createGroupContent(group);
        
        groupDiv.appendChild(groupHeader);
        groupDiv.appendChild(groupContent);
        
        return groupDiv;
    }

    function createGroupHeader(group, groupIndex) {
        const headerDiv = document.createElement('div');
        headerDiv.className = 'group-header d-flex justify-content-between align-items-center';
        
        const headerLeft = document.createElement('div');
        headerLeft.className = 'd-flex align-items-center';
        
        const toggleIcon = document.createElement('i');
        toggleIcon.className = 'fas fa-chevron-down me-2 group-toggle-icon';
        toggleIcon.style.transition = 'transform 0.3s ease';
        
        const groupName = document.createElement('h5');
        groupName.className = 'mb-0 me-3';
        groupName.textContent = group.name;
        
        const groupStats = document.createElement('span');
        groupStats.className = 'badge bg-secondary';
        groupStats.textContent = `${group.count} word${group.count !== 1 ? 's' : ''}, ${group.total_score} pts`;
        
        headerLeft.appendChild(toggleIcon);
        headerLeft.appendChild(groupName);
        headerLeft.appendChild(groupStats);
        
        const headerRight = document.createElement('div');
        const copyGroupBtn = document.createElement('button');
        copyGroupBtn.className = 'btn btn-outline-primary btn-sm';
        copyGroupBtn.innerHTML = '<i class="fas fa-copy"></i> Copy Group';
        copyGroupBtn.onclick = () => copyGroupToClipboard(group);
        
        headerRight.appendChild(copyGroupBtn);
        
        headerDiv.appendChild(headerLeft);
        headerDiv.appendChild(headerRight);
        
        // Add click handler for collapse/expand
        headerDiv.addEventListener('click', function(e) {
            if (!e.target.closest('.btn')) {
                toggleGroup(groupIndex);
            }
        });
        
        return headerDiv;
    }

    function createGroupContent(group) {
        const contentDiv = document.createElement('div');
        contentDiv.className = 'group-content';
        
        group.words.forEach((wordData, index) => {
            const wordItem = createWordItem(wordData, index + 1);
            contentDiv.appendChild(wordItem);
        });
        
        return contentDiv;
    }

    function toggleGroup(groupIndex) {
        const groupContainer = wordsContainer.children[groupIndex];
        const groupContent = groupContainer.querySelector('.group-content');
        const toggleIcon = groupContainer.querySelector('.group-toggle-icon');
        
        if (groupContent.style.display === 'none') {
            groupContent.style.display = 'block';
            toggleIcon.style.transform = 'rotate(0deg)';
        } else {
            groupContent.style.display = 'none';
            toggleIcon.style.transform = 'rotate(-90deg)';
        }
    }

    function copyGroupToClipboard(group) {
        const words = group.words.map(word => word.word).join(', ');
        copyToClipboard(words);
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