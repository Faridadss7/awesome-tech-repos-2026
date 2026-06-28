// Awesome Tech Repos 2026 - Website JavaScript

const API_BASE_URL = 'data';

// State
let allRepositories = [];
let filteredRepositories = [];
let currentCategory = null;

// Language colors for GitHub-style language indicators
const languageColors = {
    'JavaScript': '#f1e05a',
    'TypeScript': '#2b7489',
    'Python': '#3572A5',
    'Java': '#b07219',
    'Go': '#00ADD8',
    'Rust': '#dea584',
    'C++': '#f34b7d',
    'C': '#555555',
    'C#': '#239120',
    'Ruby': '#701516',
    'PHP': '#4F5D95',
    'Swift': '#F05138',
    'Kotlin': '#A97BFF',
    'Dart': '#00B4AB',
    'HTML': '#e34c26',
    'CSS': '#563d7c',
    'Markdown': '#083fa1',
    'Shell': '#89e051',
    'R': '#198CE7',
    'Scala': '#c22d40',
    'Julia': '#a270ba'
};

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    loadCategories();
    loadRepositories();
    setupEventListeners();
});

// Load categories configuration
async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/categories.json`);
        const data = await response.json();
        renderCategories(data.categories);
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Load repositories data
async function loadRepositories() {
    try {
        const response = await fetch(`${API_BASE_URL}/repositories.json`);
        const data = await response.json();
        allRepositories = data.repositories;
        filteredRepositories = [...allRepositories];
        
        updateStats();
        renderRepositories();
    } catch (error) {
        console.error('Error loading repositories:', error);
        showLoadingError();
    }
}

// Setup event listeners
function setupEventListeners() {
    const searchInput = document.getElementById('search-input');
    const categoryFilter = document.getElementById('category-filter');
    const levelFilter = document.getElementById('level-filter');

    searchInput.addEventListener('input', debounce(applyFilters, 300));
    categoryFilter.addEventListener('change', applyFilters);
    levelFilter.addEventListener('change', applyFilters);
}

// Render categories
function renderCategories(categories) {
    const container = document.getElementById('categories-container');
    
    const grid = document.createElement('div');
    grid.className = 'categories-grid';
    
    categories.forEach(category => {
        const card = document.createElement('div');
        card.className = 'category-card';
        card.dataset.categoryId = category.id;
        
        const repoCount = allRepositories.filter(r => r.category_id === category.id).length;
        
        card.innerHTML = `
            <h3>${category.name}</h3>
            <div class="count">${repoCount} repositories</div>
            <div class="description">${category.description}</div>
        `;
        
        card.addEventListener('click', () => filterByCategory(category.id));
        grid.appendChild(card);
    });
    
    container.innerHTML = '';
    container.appendChild(grid);
}

// Render repositories
function renderRepositories() {
    const container = document.getElementById('repositories-container');
    
    if (filteredRepositories.length === 0) {
        container.innerHTML = '<div class="loading">No repositories found matching your criteria.</div>';
        return;
    }
    
    const grid = document.createElement('div');
    grid.className = 'repositories-grid';
    
    filteredRepositories.forEach(repo => {
        const card = createRepositoryCard(repo);
        grid.appendChild(card);
    });
    
    container.innerHTML = '';
    container.appendChild(grid);
}

// Create repository card
function createRepositoryCard(repo) {
    const card = document.createElement('div');
    card.className = 'repo-card';
    
    const languageColor = languageColors[repo.language] || '#ccc';
    const starsFormatted = formatNumber(repo.stars);
    const levelClass = repo.learning_level.toLowerCase();
    
    card.innerHTML = `
        <div class="repo-header">
            <div class="repo-name">
                <a href="${repo.github_url}" target="_blank" rel="noopener noreferrer">${repo.name}</a>
            </div>
            <div class="repo-stars">
                ⭐ ${starsFormatted}
            </div>
        </div>
        
        <div class="repo-description">${repo.description}</div>
        
        <div class="repo-meta">
            ${repo.tags.map(tag => `<span class="repo-tag">${tag}</span>`).join('')}
        </div>
        
        <div class="repo-language">
            <span class="language-dot" style="background-color: ${languageColor}"></span>
            ${repo.language}
        </div>
        
        <div class="why-recommended">
            <strong>Why recommended:</strong> ${repo.why_recommended}
        </div>
        
        <div class="repo-footer">
            <span class="learning-level ${levelClass}">${repo.learning_level}</span>
            <span class="repo-category">${repo.category}</span>
        </div>
    `;
    
    return card;
}

// Apply filters
function applyFilters() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const categoryFilter = document.getElementById('category-filter').value;
    const levelFilter = document.getElementById('level-filter').value;
    
    filteredRepositories = allRepositories.filter(repo => {
        // Search filter
        const matchesSearch = !searchTerm || 
            repo.name.toLowerCase().includes(searchTerm) ||
            repo.description.toLowerCase().includes(searchTerm) ||
            repo.tags.some(tag => tag.toLowerCase().includes(searchTerm));
        
        // Category filter
        const matchesCategory = !categoryFilter || repo.category_id === categoryFilter;
        
        // Level filter
        const matchesLevel = !levelFilter || repo.learning_level === levelFilter;
        
        return matchesSearch && matchesCategory && matchesLevel;
    });
    
    renderRepositories();
}

// Filter by category (from category card click)
function filterByCategory(categoryId) {
    const categoryFilter = document.getElementById('category-filter');
    categoryFilter.value = categoryId;
    applyFilters();
    
    // Scroll to repositories
    document.getElementById('repositories-container').scrollIntoView({ behavior: 'smooth' });
}

// Update statistics
function updateStats() {
    const totalRepos = document.getElementById('total-repos');
    totalRepos.textContent = allRepositories.length;
}

// Format number (e.g., 15000 -> 15k)
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'k';
    }
    return num.toString();
}

// Debounce function for search input
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Show loading error
function showLoadingError() {
    const container = document.getElementById('repositories-container');
    container.innerHTML = `
        <div class="loading">
            <p>❌ Error loading repositories. Please try again later.</p>
            <p>Make sure the data files are available in the data/ directory.</p>
        </div>
    `;
}

// Update category counts after repositories are loaded
function updateCategoryCounts() {
    const categoryCards = document.querySelectorAll('.category-card');
    categoryCards.forEach(card => {
        const categoryId = card.dataset.categoryId;
        const count = allRepositories.filter(r => r.category_id === categoryId).length;
        card.querySelector('.count').textContent = `${count} repositories`;
    });
}

// Call this after repositories are loaded
const originalLoadRepositories = loadRepositories;
loadRepositories = async function() {
    await originalLoadRepositories();
    updateCategoryCounts();
};