// Initialize Socket.IO
const socket = io();

// DOM Elements
const statusIndicator = document.getElementById('statusIndicator');
const currentStep = document.getElementById('currentStep');
const progressBar = document.getElementById('progressBar');
const progressContainer = document.getElementById('progressContainer');
const estimatedTime = document.getElementById('estimatedTime');
const chapterInfo = document.getElementById('chapterInfo');
const chaptersCompleted = document.getElementById('chaptersCompleted');
const totalChapters = document.getElementById('totalChapters');
const chapterProgress = document.getElementById('chapterProgress');
const contentPreview = document.getElementById('contentPreview');
const logContainer = document.getElementById('logContainer');
const outlineTable = document.getElementById('outlineTable');
const stopGenerationBtn = document.getElementById('stopGenerationBtn');
const newBookBtn = document.getElementById('newBookBtn');
const viewLibraryBtn = document.getElementById('viewLibraryBtn');
const clearLogBtn = document.getElementById('clearLogBtn');
const refreshStatus = document.getElementById('refreshStatus');
const refreshLibrary = document.getElementById('refreshLibrary');
const booksTable = document.getElementById('booksTable');
const bookPreview = document.getElementById('bookPreview');
const fullBookPreview = document.getElementById('fullBookPreview');
const bookPreviewModal = new bootstrap.Modal(document.getElementById('bookPreviewModal'));
const downloadBookBtn = document.getElementById('downloadBookBtn');
const generationForm = document.getElementById('generationForm');
const providerSelect = document.getElementById('providerSelect');
const modelSelect = document.getElementById('modelSelect');
const apiKeyContainer = document.getElementById('apiKeyContainer');
const modelInfo = document.getElementById('modelInfo');
const apiSettingsForm = document.getElementById('apiSettingsForm');
const generationSettingsForm = document.getElementById('generationSettingsForm');

// Model information
const modelData = {
    openai: {
        'gpt-4': {
            name: 'GPT-4',
            strengths: 'High-quality writing, complex reasoning, adherence to instructions',
            limitations: 'More expensive, slower generation',
            bestFor: 'High-quality books where cost is not a concern',
            cost: '$0.03-$0.06 per 1K tokens'
        },
        'gpt-4-turbo': {
            name: 'GPT-4 Turbo',
            strengths: 'Similar quality to GPT-4, faster, larger context window',
            limitations: 'Still relatively expensive',
            bestFor: 'Longer books that need to reference earlier chapters',
            cost: '$0.01-$0.03 per 1K tokens'
        },
        'gpt-3.5-turbo': {
            name: 'GPT-3.5 Turbo',
            strengths: 'Fast, cost-effective, decent quality',
            limitations: 'Less sophisticated writing, may struggle with complex instructions',
            bestFor: 'Testing, drafts, or budget-conscious projects',
            cost: '$0.0015-$0.002 per 1K tokens'
        },
        'gpt-3.5-turbo-16k': {
            name: 'GPT-3.5 Turbo 16K',
            strengths: 'Larger context window at reasonable cost',
            limitations: 'Same quality limitations as GPT-3.5 Turbo',
            bestFor: 'Longer books on a budget',
            cost: '$0.003-$0.004 per 1K tokens'
        }
    },
    anthropic: {
        'claude-3-7-sonnet-20250219': {
            name: 'Claude 3.7 Sonnet (Extended Thinking)',
            strengths: 'Extremely long outputs (64K tokens), high quality, large context window',
            limitations: 'Can be slower, higher cost',
            bestFor: 'Generating very long, detailed chapters',
            cost: 'Varies based on usage'
        },
        'claude-3-5-sonnet-20240620': {
            name: 'Claude 3.5 Sonnet',
            strengths: 'High-quality output, large context window',
            limitations: 'Limited output length compared to 3.7',
            bestFor: 'High-quality books with moderate chapter length',
            cost: 'Varies based on usage'
        },
        'claude-3-5-haiku-20241022': {
            name: 'Claude 3.5 Haiku',
            strengths: 'Faster generation, large context window',
            limitations: 'Lower quality than Sonnet or Opus',
            bestFor: 'Faster generation when quality is less critical',
            cost: 'Lower than Sonnet/Opus'
        },
        'claude-3-opus-20240229': {
            name: 'Claude 3 Opus',
            strengths: 'Highest quality writing and reasoning',
            limitations: 'More expensive, limited output length',
            bestFor: 'Highest quality books where output length is not critical',
            cost: 'Highest among Claude models'
        },
        'claude-3-sonnet-20240229': {
            name: 'Claude 3 Sonnet',
            strengths: 'Good balance of quality and performance',
            limitations: 'Limited output length',
            bestFor: 'General purpose book generation',
            cost: 'Moderate'
        }
    },
    local: {
        'mistral-7b': {
            name: 'Mistral 7B',
            strengths: 'Good balance of quality and performance, runs on consumer hardware',
            limitations: 'Lower quality than commercial models',
            bestFor: 'Local generation on machines with 16GB+ RAM',
            cost: 'Free (requires 16GB+ RAM)'
        },
        'llama-2-13b': {
            name: 'Llama 2 13B',
            strengths: 'Better quality than 7B models',
            limitations: 'Requires more RAM, slower without GPU',
            bestFor: 'Higher quality local generation',
            cost: 'Free (requires 24GB+ RAM)'
        },
        'mixtral-8x7b': {
            name: 'Mixtral 8x7B',
            strengths: 'Near commercial-quality results',
            limitations: 'Very high resource requirements',
            bestFor: 'High-quality local generation on powerful hardware',
            cost: 'Free (requires 32GB+ RAM)'
        },
        'phi-2': {
            name: 'Phi-2',
            strengths: 'Very efficient, runs on modest hardware',
            limitations: 'Limited context, lower quality',
            bestFor: 'Testing on lower-end hardware',
            cost: 'Free (requires 8GB+ RAM)'
        }
    }
};

// Populate model select based on provider
function updateModelSelect() {
    const provider = providerSelect.value;
    modelSelect.innerHTML = '';
    
    if (provider === 'openai') {
        apiKeyContainer.style.display = 'block';
        
        const models = [
            { value: 'gpt-4', text: 'GPT-4 (Best quality)' },
            { value: 'gpt-4-turbo', text: 'GPT-4 Turbo (Faster)' },
            { value: 'gpt-3.5-turbo', text: 'GPT-3.5 Turbo (Cheaper)' },
            { value: 'gpt-3.5-turbo-16k', text: 'GPT-3.5 Turbo 16K (Longer context)' }
        ];
        
        models.forEach(model => {
            const option = document.createElement('option');
            option.value = model.value;
            option.textContent = model.text;
            modelSelect.appendChild(option);
        });
    } else if (provider === 'anthropic') {
        apiKeyContainer.style.display = 'block';
        
        const models = [
            { value: 'claude-3-7-sonnet-20250219', text: 'Claude 3.7 Sonnet (64K tokens output)' },
            { value: 'claude-3-5-sonnet-20240620', text: 'Claude 3.5 Sonnet (8K tokens output)' },
            { value: 'claude-3-5-haiku-20241022', text: 'Claude 3.5 Haiku (8K tokens output)' },
            { value: 'claude-3-opus-20240229', text: 'Claude 3 Opus (4K tokens output)' },
            { value: 'claude-3-sonnet-20240229', text: 'Claude 3 Sonnet (4K tokens output)' }
        ];
        
        models.forEach(model => {
            const option = document.createElement('option');
            option.value = model.value;
            option.textContent = model.text;
            modelSelect.appendChild(option);
        });
    } else if (provider === 'local') {
        apiKeyContainer.style.display = 'none';
        
        const models = [
            { value: 'mistral-7b', text: 'Mistral 7B (Balanced)' },
            { value: 'llama-2-13b', text: 'Llama 2 13B (Higher quality)' },
            { value: 'mixtral-8x7b', text: 'Mixtral 8x7B (Best quality)' },
            { value: 'phi-2', text: 'Phi-2 (Fastest)' }
        ];
        
        models.forEach(model => {
            const option = document.createElement('option');
            option.value = model.value;
            option.textContent = model.text;
            modelSelect.appendChild(option);
        });
    }
    
    updateModelInfo();
}

// Update model information
function updateModelInfo() {
    const provider = providerSelect.value;
    const model = modelSelect.value;
    
    if (modelData[provider] && modelData[provider][model]) {
        const data = modelData[provider][model];
        modelInfo.innerHTML = `
            <h6>${data.name}</h6>
            <p><strong>Strengths:</strong> ${data.strengths}</p>
            <p><strong>Limitations:</strong> ${data.limitations}</p>
            <p><strong>Best For:</strong> ${data.bestFor}</p>
            <p><strong>Cost:</strong> ${data.cost}</p>
        `;
    } else {
        modelInfo.innerHTML = '<p class="text-muted">Select a model to see information</p>';
    }
}

// Socket.IO event handlers
socket.on('connect', () => {
    addLogMessage('Connected to server');
    fetchStatus();
    fetchBookList();
});

socket.on('status_update', (data) => {
    updateStatusUI(data);
});

socket.on('log_message', (data) => {
    addLogEntryToUI(data);
});

socket.on('generation_complete', () => {
    addLogMessage('Generation complete!');
    fetchBookList();
});

// Update UI based on status
function updateStatusUI(data) {
    // Update status indicator
    if (data.is_generating) {
        statusIndicator.innerHTML = '<span class="badge bg-primary">Generating</span>';
        stopGenerationBtn.disabled = false;
        progressContainer.style.display = 'block';
    } else {
        statusIndicator.innerHTML = '<span class="badge bg-secondary">Idle</span>';
        stopGenerationBtn.disabled = true;
        progressContainer.style.display = 'none';
    }
    
    // Update current step and progress
    currentStep.textContent = data.current_step || 'No active generation';
    progressBar.style.width = `${data.progress}%`;
    progressBar.setAttribute('aria-valuenow', data.progress);
    
    // Update estimated time
    if (data.estimated_completion) {
        const estimatedDate = new Date(data.estimated_completion);
        const now = new Date();
        const diffMs = estimatedDate - now;
        const diffMins = Math.round(diffMs / 60000);
        
        if (diffMins > 0) {
            estimatedTime.textContent = `Estimated completion in ${diffMins} minute${diffMins !== 1 ? 's' : ''}`;
        } else {
            estimatedTime.textContent = 'Completing soon...';
        }
    } else {
        estimatedTime.textContent = '';
    }
    
    // Update chapter info
    if (data.current_chapter > 0) {
        const chapterTitle = data.outline.find(ch => ch.number === data.current_chapter)?.title || `Chapter ${data.current_chapter}`;
        chapterInfo.textContent = `Chapter ${data.current_chapter}: ${chapterTitle}`;
    } else {
        chapterInfo.textContent = 'No chapter being generated';
    }
    
    chaptersCompleted.textContent = data.chapters_completed;
    totalChapters.textContent = data.total_chapters;
    
    if (data.total_chapters > 0) {
        const chapterProgressPercent = (data.chapters_completed / data.total_chapters) * 100;
        chapterProgress.style.width = `${chapterProgressPercent}%`;
    } else {
        chapterProgress.style.width = '0%';
    }
    
    // Update content preview
    if (data.current_preview) {
        contentPreview.innerHTML = marked.parse(data.current_preview);
    }
    
    // Update outline table
    if (data.outline && data.outline.length > 0) {
        updateOutlineTable(data.outline, data.current_chapter, data.chapters_completed);
    }
}

// Update outline table
function updateOutlineTable(outline, currentChapter, completedChapters) {
    const tbody = outlineTable.querySelector('tbody');
    tbody.innerHTML = '';
    
    outline.forEach(chapter => {
        const row = document.createElement('tr');
        
        // Highlight current chapter
        if (chapter.number === currentChapter) {
            row.classList.add('table-primary');
        } else if (chapter.number <= completedChapters) {
            row.classList.add('table-success');
        }
        
        row.innerHTML = `
            <td>${chapter.number}</td>
            <td>${chapter.title}</td>
            <td>${chapter.prompt}</td>
            <td>
                ${chapter.number < currentChapter ? 
                    '<span class="badge bg-success">Completed</span>' : 
                    chapter.number === currentChapter ? 
                        '<span class="badge bg-primary">In Progress</span>' : 
                        '<span class="badge bg-secondary">Pending</span>'}
            </td>
        `;
        
        tbody.appendChild(row);
    });
}

// Add log entry to UI
function addLogEntryToUI(entry) {
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    logEntry.innerHTML = `
        <span class="log-time">${entry.timestamp}</span>
        <span class="log-message">${entry.message}</span>
    `;
    
    logContainer.appendChild(logEntry);
    logContainer.scrollTop = logContainer.scrollHeight;
}

// Add log message
function addLogMessage(message) {
    const timestamp = new Date().toTimeString().split(' ')[0];
    addLogEntryToUI({ timestamp, message });
}

// Fetch current status
function fetchStatus() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            updateStatusUI(data);
            
            // Load log messages
            logContainer.innerHTML = '';
            if (data.log_messages) {
                data.log_messages.forEach(entry => {
                    addLogEntryToUI(entry);
                });
            }
        })
        .catch(error => {
            console.error('Error fetching status:', error);
        });
}

// Fetch book list
function fetchBookList() {
    fetch('/api/get_book_list')
        .then(response => response.json())
        .then(data => {
            const tbody = booksTable.querySelector('tbody');
            tbody.innerHTML = '';
            
            if (data.books && data.books.length > 0) {
                data.books.forEach(book => {
                    const row = document.createElement('tr');
                    
                    // Format date
                    const date = new Date(book.modified);
                    const formattedDate = date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
                    
                    // Format size
                    const sizeKB = Math.round(book.size / 1024);
                    const sizeMB = (book.size / (1024 * 1024)).toFixed(2);
                    const formattedSize = sizeKB < 1000 ? `${sizeKB} KB` : `${sizeMB} MB`;
                    
                    row.innerHTML = `
                        <td>${book.filename}</td>
                        <td>${formattedDate}</td>
                        <td>${formattedSize}</td>
                        <td>
                            <button class="btn btn-sm btn-outline-primary preview-btn" data-filename="${book.filename}">
                                <i class="bi bi-eye"></i>
                            </button>
                            <a href="/book_output/${book.filename}" download class="btn btn-sm btn-outline-success">
                                <i class="bi bi-download"></i>
                            </a>
                        </td>
                    `;
                    
                    tbody.appendChild(row);
                });
                
                // Add event listeners to preview buttons
                document.querySelectorAll('.preview-btn').forEach(button => {
                    button.addEventListener('click', () => {
                        const filename = button.getAttribute('data-filename');
                        previewBook(filename);
                    });
                });
            } else {
                tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">No books found</td></tr>';
            }
        })
        .catch(error => {
            console.error('Error fetching book list:', error);
        });
}

// Preview book
function previewBook(filename) {
    fetch(`/api/get_book/${filename}`)
        .then(response => response.json())
        .then(data => {
            if (data.content) {
                // Update preview in library tab
                bookPreview.innerHTML = marked.parse(data.content.substring(0, 1000) + '...');
                
                // Update modal for full preview
                fullBookPreview.innerHTML = marked.parse(data.content);
                document.getElementById('bookPreviewModalLabel').textContent = filename;
                downloadBookBtn.setAttribute('data-filename', filename);
                bookPreviewModal.show();
            } else {
                bookPreview.innerHTML = '<p class="text-danger">Error loading book content</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching book content:', error);
            bookPreview.innerHTML = '<p class="text-danger">Error loading book content</p>';
        });
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize model select
    updateModelSelect();
    
    // Provider change
    providerSelect.addEventListener('change', updateModelSelect);
    
    // Model change
    modelSelect.addEventListener('change', updateModelInfo);
    
    // New book button
    newBookBtn.addEventListener('click', () => {
        document.querySelector('a[data-bs-target="#generate"]').click();
    });
    
    // View library button
    viewLibraryBtn.addEventListener('click', () => {
        document.querySelector('a[data-bs-target="#library"]').click();
    });
    
    // Stop generation button
    stopGenerationBtn.addEventListener('click', () => {
        fetch('/api/stop_generation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            addLogMessage('Requested to stop generation');
        })
        .catch(error => {
            console.error('Error stopping generation:', error);
        });
    });
    
    // Clear log button
    clearLogBtn.addEventListener('click', () => {
        logContainer.innerHTML = '';
        addLogMessage('Log cleared');
    });
    
    // Refresh status button
    refreshStatus.addEventListener('click', fetchStatus);
    
    // Refresh library button
    refreshLibrary.addEventListener('click', fetchBookList);
    
    // Download book button
    downloadBookBtn.addEventListener('click', () => {
        const filename = downloadBookBtn.getAttribute('data-filename');
        window.location.href = `/book_output/${filename}`;
    });
    
    // Generation form submit
    generationForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const formData = {
            provider: providerSelect.value,
            model: modelSelect.value,
            prompt: document.getElementById('promptTextarea').value,
            num_chapters: parseInt(document.getElementById('numChapters').value),
            min_chapter_length: parseInt(document.getElementById('minChapterLength').value),
            min_scenes: parseInt(document.getElementById('minScenes').value),
            enable_research: document.getElementById('enableResearch').checked,
            api_key: document.getElementById('apiKey').value
        };
        
        fetch('/api/start_generation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'started') {
                document.querySelector('a[data-bs-target="#dashboard"]').click();
                addLogMessage('Generation started');
            }
        })
        .catch(error => {
            console.error('Error starting generation:', error);
        });
    });
    
    // API settings form submit
    apiSettingsForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const openaiApiKey = document.getElementById('openaiApiKey').value;
        const anthropicApiKey = document.getElementById('anthropicApiKey').value;
        const lmStudioUrl = document.getElementById('lmStudioUrl').value;
        
        // Save to localStorage
        if (openaiApiKey) localStorage.setItem('openaiApiKey', openaiApiKey);
        if (anthropicApiKey) localStorage.setItem('anthropicApiKey', anthropicApiKey);
        if (lmStudioUrl) localStorage.setItem('lmStudioUrl', lmStudioUrl);
        
        addLogMessage('API settings saved');
        
        // Show success alert
        alert('API settings saved successfully!');
    });
    
    // Generation settings form submit
    generationSettingsForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const outputDir = document.getElementById('outputDir').value;
        const maxRetries = document.getElementById('maxRetries').value;
        const autoOpenBrowser = document.getElementById('autoOpenBrowser').checked;
        
        // Save to localStorage
        localStorage.setItem('outputDir', outputDir);
        localStorage.setItem('maxRetries', maxRetries);
        localStorage.setItem('autoOpenBrowser', autoOpenBrowser);
        
        addLogMessage('Generation settings saved');
        
        // Show success alert
        alert('Generation settings saved successfully!');
    });
    
    // Load saved settings
    if (localStorage.getItem('openaiApiKey')) {
        document.getElementById('openaiApiKey').value = localStorage.getItem('openaiApiKey');
    }
    
    if (localStorage.getItem('anthropicApiKey')) {
        document.getElementById('anthropicApiKey').value = localStorage.getItem('anthropicApiKey');
    }
    
    if (localStorage.getItem('lmStudioUrl')) {
        document.getElementById('lmStudioUrl').value = localStorage.getItem('lmStudioUrl');
    }
    
    if (localStorage.getItem('outputDir')) {
        document.getElementById('outputDir').value = localStorage.getItem('outputDir');
    }
    
    if (localStorage.getItem('maxRetries')) {
        document.getElementById('maxRetries').value = localStorage.getItem('maxRetries');
    }
    
    if (localStorage.getItem('autoOpenBrowser') !== null) {
        document.getElementById('autoOpenBrowser').checked = localStorage.getItem('autoOpenBrowser') === 'true';
    }
});
