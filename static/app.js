// API Base URL
const API_URL = 'http://localhost:5000';

// Global state
let currentUser = null;
let accessToken = null;
let currentPage = 1;
let currentFilters = {};

// Auth Functions
function showLoginForm() {
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('register-form').style.display = 'none';
    clearAuthMessage();
}

function showRegisterForm() {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('register-form').style.display = 'block';
    clearAuthMessage();
}

function clearAuthMessage() {
    const messageEl = document.getElementById('auth-message');
    messageEl.textContent = '';
    messageEl.className = 'message';
}

function showAuthMessage(message, type) {
    const messageEl = document.getElementById('auth-message');
    messageEl.textContent = message;
    messageEl.className = `message ${type}`;
}

async function register(event) {
    event.preventDefault();

    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;

    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            accessToken = data.access_token;
            currentUser = data.user;
            localStorage.setItem('accessToken', accessToken);
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            showApp();
        } else {
            showAuthMessage(data.error || 'Registration failed', 'error');
        }
    } catch (error) {
        showAuthMessage('Network error. Please try again.', 'error');
    }
}

async function login(event) {
    event.preventDefault();

    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            accessToken = data.access_token;
            currentUser = data.user;
            localStorage.setItem('accessToken', accessToken);
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            showApp();
        } else {
            showAuthMessage(data.error || 'Login failed', 'error');
        }
    } catch (error) {
        showAuthMessage('Network error. Please try again.', 'error');
    }
}

function logout() {
    accessToken = null;
    currentUser = null;
    localStorage.removeItem('accessToken');
    localStorage.removeItem('currentUser');
    document.getElementById('auth-section').style.display = 'flex';
    document.getElementById('app-section').style.display = 'none';
    showLoginForm();
}

function showApp() {
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('app-section').style.display = 'block';
    document.getElementById('username-display').textContent = currentUser.username;
    loadBillionaires();
}

// Tab Navigation
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');

    // Add active class to clicked button
    event.target.classList.add('active');

    // Load data for tab
    if (tabName === 'billionaires') {
        loadBillionaires();
    } else if (tabName === 'relationships') {
        loadRelationships();
    } else if (tabName === 'stats') {
        loadStats();
    }
}

// Billionaires Functions
async function loadBillionaires(page = 1) {
    currentPage = page;

    try {
        const params = new URLSearchParams({
            page: page,
            per_page: 20,
            ...currentFilters
        });

        const response = await fetch(`${API_URL}/api/billionaires?${params}`, {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            displayBillionaires(data.billionaires);
            displayPagination(data.current_page, data.pages);
        } else {
            console.error('Error loading billionaires:', data.error);
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

function displayBillionaires(billionaires) {
    const container = document.getElementById('billionaires-list');

    if (billionaires.length === 0) {
        container.innerHTML = '<p style="text-align: center; padding: 40px; color: #666;">No billionaires found.</p>';
        return;
    }

    container.innerHTML = billionaires.map(b => `
        <div class="billionaire-card">
            <div class="billionaire-header">
                <div class="billionaire-info">
                    <h3>${b.person_name}</h3>
                    <p class="worth">$${b.final_worth.toFixed(1)}B</p>
                </div>
                <span class="billionaire-rank">#${b.rank}</span>
            </div>
            <div class="billionaire-details">
                <div class="detail-item"><strong>Source:</strong> ${b.source || 'N/A'}</div>
                <div class="detail-item"><strong>Country:</strong> ${b.country || 'N/A'}</div>
                <div class="detail-item"><strong>Industry:</strong> ${b.category || 'N/A'}</div>
                <div class="detail-item"><strong>Age:</strong> ${b.age || 'N/A'}</div>
                <div class="detail-item"><strong>Organization:</strong> ${b.organization || 'N/A'}</div>
                <div class="detail-item"><strong>Self Made:</strong> ${b.self_made ? 'Yes' : 'No'}</div>
            </div>
            <div class="billionaire-actions">
                <button class="btn btn-success" onclick="openRelationshipModal(${b.id}, '${b.person_name}')">
                    Track Relationship
                </button>
            </div>
        </div>
    `).join('');
}

function displayPagination(currentPage, totalPages) {
    const container = document.getElementById('pagination');

    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }

    let pages = '';

    // Previous button
    pages += `<button onclick="loadBillionaires(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>Previous</button>`;

    // Page numbers
    for (let i = 1; i <= Math.min(totalPages, 10); i++) {
        pages += `<button class="${i === currentPage ? 'active' : ''}" onclick="loadBillionaires(${i})">${i}</button>`;
    }

    // Next button
    pages += `<button onclick="loadBillionaires(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>Next</button>`;

    container.innerHTML = pages;
}

function searchBillionaires() {
    const search = document.getElementById('search-input').value;
    currentFilters.search = search;
    loadBillionaires(1);
}

function applyFilters() {
    const country = document.getElementById('country-filter').value;
    const category = document.getElementById('category-filter').value;

    if (country) currentFilters.country = country;
    else delete currentFilters.country;

    if (category) currentFilters.category = category;
    else delete currentFilters.category;

    loadBillionaires(1);
}

function resetSearch() {
    document.getElementById('search-input').value = '';
    document.getElementById('country-filter').value = '';
    document.getElementById('category-filter').value = '';
    currentFilters = {};
    loadBillionaires(1);
}

// Relationships Functions
async function loadRelationships() {
    try {
        const params = new URLSearchParams();

        const status = document.getElementById('status-filter').value;
        const priority = document.getElementById('priority-filter').value;

        if (status) params.append('status', status);
        if (priority) params.append('priority', priority);

        const response = await fetch(`${API_URL}/api/relationships?${params}`, {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            displayRelationships(data.relationships);
        } else {
            console.error('Error loading relationships:', data.error);
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

function displayRelationships(relationships) {
    const container = document.getElementById('relationships-list');

    if (relationships.length === 0) {
        container.innerHTML = '<p style="text-align: center; padding: 40px; color: #666;">No relationships tracked yet. Go to Browse Billionaires to start tracking!</p>';
        return;
    }

    container.innerHTML = relationships.map(r => {
        const b = r.billionaire;
        return `
        <div class="relationship-card">
            <div class="relationship-header">
                <div>
                    <h3>${b.person_name}</h3>
                    <p class="worth">$${b.final_worth.toFixed(1)}B</p>
                </div>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <span class="relationship-status status-${r.relationship_status || 'prospect'}">${r.relationship_status || 'Prospect'}</span>
                    <span class="priority-badge priority-${r.priority || 'medium'}">${r.priority || 'Medium'}</span>
                </div>
            </div>
            ${r.notes ? `<div class="relationship-notes">${r.notes}</div>` : ''}
            <div class="billionaire-details">
                <div class="detail-item"><strong>Source:</strong> ${b.source || 'N/A'}</div>
                <div class="detail-item"><strong>Country:</strong> ${b.country || 'N/A'}</div>
                ${r.last_contact_date ? `<div class="detail-item"><strong>Last Contact:</strong> ${r.last_contact_date}</div>` : ''}
                ${r.next_followup_date ? `<div class="detail-item"><strong>Next Follow-up:</strong> ${r.next_followup_date}</div>` : ''}
                ${r.tags ? `<div class="detail-item"><strong>Tags:</strong> ${r.tags}</div>` : ''}
            </div>
            <div class="billionaire-actions">
                <button class="btn btn-primary" onclick="editRelationship(${r.id})">Edit</button>
                <button class="btn btn-danger" onclick="deleteRelationship(${r.id})">Delete</button>
            </div>
        </div>
    `}).join('');
}

function filterRelationships() {
    loadRelationships();
}

// Relationship Modal Functions
function openRelationshipModal(billionaireId, billionaireName) {
    document.getElementById('modal-billionaire-id').value = billionaireId;
    document.getElementById('modal-billionaire-name').textContent = billionaireName;
    document.getElementById('modal-relationship-id').value = '';
    document.getElementById('modal-title').textContent = 'Track Relationship';
    document.getElementById('relationship-form').reset();
    document.getElementById('relationship-modal').style.display = 'block';
}

function closeRelationshipModal() {
    document.getElementById('relationship-modal').style.display = 'none';
}

async function editRelationship(relationshipId) {
    try {
        const response = await fetch(`${API_URL}/api/relationships/${relationshipId}`, {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            const r = data.relationship;
            document.getElementById('modal-billionaire-id').value = r.billionaire.id;
            document.getElementById('modal-billionaire-name').textContent = r.billionaire.person_name;
            document.getElementById('modal-relationship-id').value = r.id;
            document.getElementById('modal-status').value = r.relationship_status || '';
            document.getElementById('modal-priority').value = r.priority || 'medium';
            document.getElementById('modal-notes').value = r.notes || '';
            document.getElementById('modal-last-contact').value = r.last_contact_date || '';
            document.getElementById('modal-next-followup').value = r.next_followup_date || '';
            document.getElementById('modal-tags').value = r.tags || '';
            document.getElementById('modal-title').textContent = 'Edit Relationship';
            document.getElementById('relationship-modal').style.display = 'block';
        }
    } catch (error) {
        console.error('Error loading relationship:', error);
    }
}

async function saveRelationship(event) {
    event.preventDefault();

    const billionaireId = document.getElementById('modal-billionaire-id').value;
    const relationshipId = document.getElementById('modal-relationship-id').value;

    const data = {
        billionaire_id: parseInt(billionaireId),
        relationship_status: document.getElementById('modal-status').value,
        priority: document.getElementById('modal-priority').value,
        notes: document.getElementById('modal-notes').value,
        last_contact_date: document.getElementById('modal-last-contact').value || null,
        next_followup_date: document.getElementById('modal-next-followup').value || null,
        tags: document.getElementById('modal-tags').value
    };

    try {
        let url = `${API_URL}/api/relationships`;
        let method = 'POST';

        if (relationshipId) {
            url = `${API_URL}/api/relationships/${relationshipId}`;
            method = 'PUT';
        }

        const response = await fetch(url, {
            method: method,
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            closeRelationshipModal();
            loadRelationships();
            alert(result.message);
        } else {
            alert(result.error || 'Failed to save relationship');
        }
    } catch (error) {
        console.error('Error saving relationship:', error);
        alert('Network error. Please try again.');
    }
}

async function deleteRelationship(relationshipId) {
    if (!confirm('Are you sure you want to delete this relationship?')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/relationships/${relationshipId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            loadRelationships();
            alert(data.message);
        } else {
            alert(data.error || 'Failed to delete relationship');
        }
    } catch (error) {
        console.error('Error deleting relationship:', error);
        alert('Network error. Please try again.');
    }
}

// Statistics Functions
async function loadStats() {
    try {
        const response = await fetch(`${API_URL}/api/billionaires/stats`, {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            displayStats(data);
        } else {
            console.error('Error loading stats:', data.error);
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

function displayStats(stats) {
    const container = document.getElementById('stats-content');

    container.innerHTML = `
        <div class="stat-card">
            <h3>Overview</h3>
            <div class="stat-number">${stats.total_billionaires}</div>
            <p style="text-align: center; color: #666;">Total Billionaires</p>
        </div>

        <div class="stat-card">
            <h3>Top Countries</h3>
            ${stats.top_countries.map(c => `
                <div class="stat-item">
                    <span>${c.country}</span>
                    <strong>${c.count}</strong>
                </div>
            `).join('')}
        </div>

        <div class="stat-card">
            <h3>Top Industries</h3>
            ${stats.top_categories.map(c => `
                <div class="stat-item">
                    <span>${c.category}</span>
                    <strong>${c.count}</strong>
                </div>
            `).join('')}
        </div>
    `;
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    // Check if user is already logged in
    const savedToken = localStorage.getItem('accessToken');
    const savedUser = localStorage.getItem('currentUser');

    if (savedToken && savedUser) {
        accessToken = savedToken;
        currentUser = JSON.parse(savedUser);
        showApp();
    }

    // Close modal when clicking outside
    window.onclick = function(event) {
        const modal = document.getElementById('relationship-modal');
        if (event.target === modal) {
            closeRelationshipModal();
        }
    }
});
