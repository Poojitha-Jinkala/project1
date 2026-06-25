// Main JS file for ResumeParser Front-end interactions

document.addEventListener('DOMContentLoaded', () => {
    // ---------------------------------
    // 1. Navigation / Active State
    // ---------------------------------
    // Ensure navigation state is highlighted if endpoints are matched
    
    // ---------------------------------
    // 2. Tab Control Logic (Detail View)
    // ---------------------------------
    const tabButtons = document.querySelectorAll('.tab-btn');
    if (tabButtons.length > 0) {
        tabButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                // Remove active classes
                tabButtons.forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
                
                // Add active to current button
                btn.classList.add('active');
                
                // Show corresponding tab pane
                const targetTabId = btn.getAttribute('data-tab');
                const targetPane = document.getElementById(targetTabId);
                if (targetPane) {
                    targetPane.classList.add('active');
                }
            });
        });
    }

    // ---------------------------------
    // 3. Search and Skills Filters (Dashboard)
    // ---------------------------------
    const searchInput = document.getElementById('search-input');
    const clearSearchBtn = document.getElementById('clear-search-btn');
    const skillPills = document.querySelectorAll('.filter-pill');
    const candidateCards = document.querySelectorAll('.candidate-card');
    const resultsCountIndicator = document.getElementById('results-count');
    
    let activeSearchText = "";
    let activeSkillFilters = new Set();
    
    function filterCandidates() {
        let visibleCount = 0;
        
        candidateCards.forEach(card => {
            const searchableContent = card.getAttribute('data-searchable').toLowerCase();
            
            // Search text match
            const matchesSearch = searchableContent.includes(activeSearchText.toLowerCase());
            
            // Skill filter match
            let matchesSkills = true;
            if (activeSkillFilters.size > 0) {
                // The card must match all of the active skill filters (intersection)
                // or any? Let's check if all selected skills match (stricter and cleaner)
                activeSkillFilters.forEach(skill => {
                    if (!searchableContent.includes(skill.toLowerCase())) {
                        matchesSkills = false;
                    }
                });
            }
            
            if (matchesSearch && matchesSkills) {
                card.style.display = 'flex';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        // Update results counter
        if (resultsCountIndicator) {
            resultsCountIndicator.textContent = `Showing ${visibleCount} of ${candidateCards.length} candidates`;
        }
    }
    
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            activeSearchText = e.target.value;
            
            // Show/hide clear button
            if (activeSearchText.length > 0) {
                clearSearchBtn.style.display = 'block';
            } else {
                clearSearchBtn.style.display = 'none';
            }
            
            filterCandidates();
        });
    }
    
    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', () => {
            searchInput.value = "";
            activeSearchText = "";
            clearSearchBtn.style.display = 'none';
            filterCandidates();
        });
    }
    
    if (skillPills.length > 0) {
        skillPills.forEach(pill => {
            pill.addEventListener('click', () => {
                const skill = pill.getAttribute('data-skill');
                
                if (pill.classList.contains('active')) {
                    pill.classList.remove('active');
                    activeSkillFilters.delete(skill);
                } else {
                    pill.classList.add('active');
                    activeSkillFilters.add(skill);
                }
                
                filterCandidates();
            });
        });
    }

    // ---------------------------------
    // 4. Drag & Drop File Upload Handler
    // ---------------------------------
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const uploadStatusContainer = document.getElementById('upload-status-container');
    const processingFileName = document.getElementById('processing-file-name');
    const uploadProgressFill = document.getElementById('upload-progress-fill');
    const uploadPercentage = document.getElementById('upload-percentage');
    const statusMessage = document.getElementById('status-message');
    const parserFeedbackBox = document.getElementById('parser-feedback-box');
    const viewProfileBtn = document.getElementById('view-profile-btn');

    if (dropZone && fileInput) {
        // Drag events
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.remove('dragover');
            }, false);
        });

        // Handle drop files
        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                handleFileUpload(files[0]);
            }
        });

        // Input change event
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileUpload(e.target.files[0]);
            }
        });
    }

    function handleFileUpload(file) {
        // Validate size / type (PDF or DOCX)
        const allowedTypes = [
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ];
        const extension = file.name.split('.').pop().toLowerCase();
        
        if (!allowedTypes.includes(file.type) && !['pdf', 'docx'].includes(extension)) {
            alert('Unsupported file format. Please upload PDF or DOCX resume.');
            return;
        }

        // Show status panel, hide dropzone
        dropZone.style.display = 'none';
        uploadStatusContainer.style.display = 'block';
        processingFileName.textContent = file.name;
        uploadProgressFill.style.width = '0%';
        uploadPercentage.textContent = '0%';
        statusMessage.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Uploading document...';

        // Build FormData
        const formData = new FormData();
        formData.append('file', file);

        // AJAX Request using XMLHttpRequest (to track progress)
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/upload', true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        // Track upload progress
        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percentComplete = Math.round((e.loaded / e.total) * 100);
                // Cap upload display at 90%, the rest is server processing
                const displayPercent = Math.round(percentComplete * 0.9);
                uploadProgressFill.style.width = displayPercent + '%';
                uploadPercentage.textContent = displayPercent + '%';
                
                if (percentComplete === 100) {
                    statusMessage.innerHTML = '<i class="fa-solid fa-gears fa-spin"></i> Parsing resume contents and extracting details...';
                }
            }
        });

        xhr.onload = function() {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                if (response.success) {
                    // Update progress completion
                    uploadProgressFill.style.width = '100%';
                    uploadPercentage.textContent = '100%';
                    
                    // Show success block
                    uploadStatusContainer.style.display = 'none';
                    parserFeedbackBox.style.display = 'block';
                    
                    // Setup direct profile navigation link
                    if (viewProfileBtn) {
                        viewProfileBtn.href = `/resume/${response.candidate_id}`;
                    }
                } else {
                    handleUploadError(response.message || 'Error occurred during parsing.');
                }
            } else {
                let errorMsg = 'An error occurred during file upload.';
                try {
                    const response = JSON.parse(xhr.responseText);
                    errorMsg = response.message || errorMsg;
                } catch(e) {}
                handleUploadError(errorMsg);
            }
        };

        xhr.onerror = function() {
            handleUploadError('Network error occurred during upload.');
        };

        xhr.send(formData);
    }

    function handleUploadError(message) {
        uploadStatusContainer.style.display = 'none';
        
        // Show drop zone again with alert details
        dropZone.style.display = 'block';
        alert('Upload Failed: ' + message);
    }

    window.resetUploadForm = function() {
        if (dropZone) {
            dropZone.style.display = 'block';
            parserFeedbackBox.style.display = 'none';
            uploadStatusContainer.style.display = 'none';
            fileInput.value = "";
        }
    };
});

// ---------------------------------
// 5. Candidate Deletion Confirm (Modal UI)
// ---------------------------------
let candidateIdToDelete = null;

window.confirmDeleteCandidate = function(id, event) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    candidateIdToDelete = id;
    const modal = document.getElementById('delete-modal');
    if (modal) {
        modal.classList.add('active');
        
        // Connect confirm button
        const confirmBtn = document.getElementById('confirm-delete-btn');
        if (confirmBtn) {
            confirmBtn.onclick = function() {
                executeDeletion(candidateIdToDelete);
            };
        }
    }
};

window.triggerDeleteProfile = function(id) {
    candidateIdToDelete = id;
    const modal = document.getElementById('delete-modal');
    if (modal) {
        modal.classList.add('active');
        
        // Connect confirm button
        const confirmBtn = document.getElementById('confirm-delete-btn');
        if (confirmBtn) {
            confirmBtn.onclick = function() {
                executeDeletion(candidateIdToDelete, true);
            };
        }
    }
};

window.closeDeleteModal = function() {
    const modal = document.getElementById('delete-modal');
    if (modal) {
        modal.classList.remove('active');
    }
    candidateIdToDelete = null;
};

function executeDeletion(id, redirectOnSuccess = false) {
    const xhr = new XMLHttpRequest();
    xhr.open('DELETE', `/api/delete/${id}`, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    
    xhr.onload = function() {
        closeDeleteModal();
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            if (response.success) {
                if (redirectOnSuccess) {
                    window.location.href = '/';
                } else {
                    // Remove candidate card dynamically from UI grid
                    const card = document.querySelector(`.candidate-card[data-id="${id}"]`);
                    if (card) {
                        card.remove();
                        
                        // Decrement stats counter
                        const totalResumes = document.getElementById('stat-total-resumes');
                        if (totalResumes) {
                            const currentVal = parseInt(totalResumes.textContent);
                            totalResumes.textContent = Math.max(0, currentVal - 1);
                        }
                        
                        // Check if grid is now empty
                        const grid = document.getElementById('candidates-grid');
                        if (grid && grid.children.length === 0) {
                            location.reload(); // Quick reload to show empty state template
                        }
                    }
                }
            } else {
                alert('Deletion failed: ' + response.message);
            }
        } else {
            alert('Server error occurred during deletion.');
        }
    };
    
    xhr.onerror = function() {
        closeDeleteModal();
        alert('Network error occurred during deletion.');
    };
    
    xhr.send();
}
