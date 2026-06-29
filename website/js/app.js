// Awesome Tech Repos 2026 - Website JavaScript

const API_BASE_URL = './data';

// State
let allRepositories = [];
let filteredRepositories = [];
let currentCategory = null;
let currentPage = 1;
const itemsPerPage = 24;

// Performance monitoring
const performanceMetrics = {
    pageLoadTime: null,
    firstContentfulPaint: null,
    domContentLoaded: null,
    apiLoadTime: null,
    renderTime: null
};

// Initialize performance monitoring
function initPerformanceMonitoring() {
    if ('performance' in window) {
        window.addEventListener('load', () => {
            performanceMetrics.pageLoadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
            performanceMetrics.domContentLoaded = performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart;

            // Log to console for development
            console.log('Performance Metrics:', performanceMetrics);
        });
    }
}

// Type classification logic
function classifyRepositoryType(repo) {
    const name = repo.name.toLowerCase();
    const description = repo.description.toLowerCase();
    const tags = repo.tags.map(t => t.toLowerCase());
    
    // Courses & Tutorials
    if (name.includes('course') || name.includes('tutorial') || name.includes('guide') || 
        name.includes('learn') || name.includes('book') || name.includes('handbook') ||
        description.includes('course') || description.includes('tutorial') || 
        description.includes('guide') || description.includes('learn') ||
        tags.includes('course') || tags.includes('tutorial') || tags.includes('guide') ||
        tags.includes('book') || tags.includes('learning')) {
        return 'courses';
    }
    
    // Contribution Projects
    if (name.includes('contribution') || name.includes('project') || 
        description.includes('contribution') || description.includes('participate') ||
        tags.includes('contribution') || tags.includes('project') || 
        tags.includes('participate')) {
        return 'contribution';
    }
    
    // Contribution Resources
    if (name.includes('resource') || name.includes('tool') || name.includes('framework') ||
        description.includes('resource') || description.includes('tool') || 
        description.includes('framework') || description.includes('library') ||
        tags.includes('resource') || tags.includes('tool') || tags.includes('framework') ||
        tags.includes('library')) {
        return 'resources';
    }
    
    // Default to resources for general projects
    return 'resources';
}

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
    initPerformanceMonitoring();
    setupErrorBoundary();
    loadCategories();
    loadRepositories();
    setupEventListeners();
    setupThemeToggle();
    setupScrollAnimations();
    loadURLState();
});

// Setup scroll-triggered animations
function setupScrollAnimations() {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements with scroll-reveal classes
    const scrollElements = document.querySelectorAll('.scroll-reveal, .scroll-reveal-left, .scroll-reveal-right, .scroll-reveal-scale');
    scrollElements.forEach(el => observer.observe(el));
}

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
    const apiLoadStart = performance.now();

    try {
        // Show skeleton loader initially
        renderSkeletonLoader();

        // Fetch fresh data
        const response = await fetch(`${API_BASE_URL}/repositories.json`);
        console.log('Response status:', response.status);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Loaded repositories count:', data.repositories?.length || 0);

        allRepositories = data.repositories;
        filteredRepositories = [...allRepositories];

        performanceMetrics.apiLoadTime = performance.now() - apiLoadStart;

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
    const typeFilter = document.getElementById('type-filter');
    const sortFilter = document.getElementById('sort-filter');
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');

    searchInput.addEventListener('input', debounce(applyFilters, 300));
    categoryFilter.addEventListener('change', applyFilters);
    levelFilter.addEventListener('change', applyFilters);
    typeFilter.addEventListener('change', applyFilters);
    sortFilter.addEventListener('change', applyFilters);

    // Pagination event listeners
    prevPageBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            renderRepositories();
            // Scroll to top of repositories
            document.getElementById('repositories-container').scrollIntoView({ behavior: 'smooth' });
        }
    });

    nextPageBtn.addEventListener('click', () => {
        const totalPages = Math.ceil(filteredRepositories.length / itemsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            renderRepositories();
            // Scroll to top of repositories
            document.getElementById('repositories-container').scrollIntoView({ behavior: 'smooth' });
        }
    });

    // Mobile menu listeners
    setupMobileMenuListeners();
}

// Setup mobile menu listeners
function setupMobileMenuListeners() {
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileMenuClose = document.getElementById('mobile-menu-close');
    const mobileApplyBtn = document.getElementById('mobile-apply-filters');

    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            const isExpanded = mobileMenuToggle.getAttribute('aria-expanded') === 'true';
            mobileMenuToggle.setAttribute('aria-expanded', !isExpanded);
            mobileMenu.classList.toggle('active');
            mobileMenu.setAttribute('aria-hidden', isExpanded);
            document.body.style.overflow = isExpanded ? '' : 'hidden';
        });
    }

    if (mobileMenuClose && mobileMenu) {
        mobileMenuClose.addEventListener('click', () => {
            mobileMenuToggle.setAttribute('aria-expanded', 'false');
            mobileMenu.classList.remove('active');
            mobileMenu.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        });
    }

    if (mobileApplyBtn) {
        mobileApplyBtn.addEventListener('click', () => {
            // Sync mobile filters with main filters
            const mobileSearch = document.getElementById('mobile-search').value;
            const mobileCategory = document.getElementById('mobile-category').value;
            const mobileLevel = document.getElementById('mobile-level').value;
            const mobileType = document.getElementById('mobile-type').value;
            const mobileSort = document.getElementById('mobile-sort').value;

            document.getElementById('search-input').value = mobileSearch;
            document.getElementById('category-filter').value = mobileCategory;
            document.getElementById('level-filter').value = mobileLevel;
            document.getElementById('type-filter').value = mobileType;
            document.getElementById('sort-filter').value = mobileSort;

            applyFilters();

            // Close mobile menu
            mobileMenuToggle.setAttribute('aria-expanded', 'false');
            mobileMenu.classList.remove('active');
            mobileMenu.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        });
    }

    // Close menu when clicking outside
    mobileMenu.addEventListener('click', (e) => {
        if (e.target === mobileMenu) {
            mobileMenuToggle.setAttribute('aria-expanded', 'false');
            mobileMenu.classList.remove('active');
            mobileMenu.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        }
    });

    // Close menu on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && mobileMenu.classList.contains('active')) {
            mobileMenuToggle.setAttribute('aria-expanded', 'false');
            mobileMenu.classList.remove('active');
            mobileMenu.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        }
    });
}

// Render categories
function renderCategories(categories) {
    const container = document.getElementById('categories-container');
    
    const grid = document.createElement('div');
    grid.className = 'categories-grid';
    
    categories.forEach((category, index) => {
        const card = document.createElement('div');
        card.className = 'category-card';
        card.dataset.categoryId = category.id;
        card.style.animationDelay = `${index * 0.1}s`;
        
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
    const renderStart = performance.now();
    
    const container = document.getElementById('repositories-container');

    if (filteredRepositories.length === 0) {
        const searchTerm = document.getElementById('search-input').value;
        showEmptyState(searchTerm);
        updatePaginationControls(0);
        return;
    }

    // Calculate pagination
    const totalPages = Math.ceil(filteredRepositories.length / itemsPerPage);
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedRepos = filteredRepositories.slice(startIndex, endIndex);

    const grid = document.createElement('div');
    grid.className = 'repositories-grid';

    paginatedRepos.forEach((repo, index) => {
        const card = createRepositoryCard(repo);
        card.style.animationDelay = `${index * 0.05}s`;
        grid.appendChild(card);
    });

    container.innerHTML = '';
    container.appendChild(grid);

    // Update pagination controls
    updatePaginationControls(totalPages);
    
    performanceMetrics.renderTime = performance.now() - renderStart;
}

// Render skeleton loading state
function renderSkeletonLoader() {
    const container = document.getElementById('repositories-container');
    const grid = document.createElement('div');
    grid.className = 'repositories-grid';

    for (let i = 0; i < 8; i++) {
        const skeletonCard = document.createElement('div');
        skeletonCard.className = 'skeleton-card';
        skeletonCard.innerHTML = `
            <div class="skeleton-header">
                <div class="skeleton skeleton-title"></div>
                <div class="skeleton skeleton-badge"></div>
            </div>
            <div class="skeleton skeleton-description"></div>
            <div class="skeleton skeleton-description"></div>
            <div class="skeleton skeleton-description"></div>
            <div class="skeleton-meta">
                <div class="skeleton skeleton-tag"></div>
                <div class="skeleton skeleton-tag"></div>
                <div class="skeleton skeleton-tag"></div>
            </div>
            <div class="skeleton-footer">
                <div class="skeleton skeleton-level"></div>
                <div class="skeleton skeleton-category"></div>
            </div>
        `;
        grid.appendChild(skeletonCard);
    }

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
    const repoType = classifyRepositoryType(repo);
    
    // Type-specific styling
    const typeClass = repoType;
    const typeLabel = repoType.charAt(0).toUpperCase() + repoType.slice(1);
    
    card.innerHTML = `
        <div class="repo-header">
            <div class="repo-name">
                <a href="${repo.github_url}" target="_blank" rel="noopener noreferrer">${repo.name}</a>
            </div>
            <div class="repo-stars">
                ${starsFormatted} stars
            </div>
        </div>
        
        <div class="repo-type-badge type-${typeClass}">${typeLabel}</div>
        
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
    const typeFilter = document.getElementById('type-filter').value;
    const sortFilter = document.getElementById('sort-filter').value;

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

        // Type filter
        const repoType = classifyRepositoryType(repo);
        const matchesType = !typeFilter || repoType === typeFilter;

        return matchesSearch && matchesCategory && matchesLevel && matchesType;
    });

    // Apply sorting
    switch (sortFilter) {
        case 'stars-desc':
            filteredRepositories.sort((a, b) => b.stars - a.stars);
            break;
        case 'stars-asc':
            filteredRepositories.sort((a, b) => a.stars - b.stars);
            break;
        case 'name-asc':
            filteredRepositories.sort((a, b) => a.name.localeCompare(b.name));
            break;
        case 'name-desc':
            filteredRepositories.sort((a, b) => b.name.localeCompare(a.name));
            break;
        case 'added-desc':
            filteredRepositories.sort((a, b) => new Date(b.added_date) - new Date(a.added_date));
            break;
        default:
            // Default: stars descending
            filteredRepositories.sort((a, b) => b.stars - a.stars);
    }

    // Reset to page 1 when filters change
    currentPage = 1;
    renderRepositories();

    // Update URL state
    updateURLState(searchTerm, categoryFilter, levelFilter, typeFilter, sortFilter);
}

// Update URL state for shareable filtered views
function updateURLState(search, category, level, type, sort) {
    const params = new URLSearchParams();

    if (search) params.set('search', search);
    if (category) params.set('category', category);
    if (level) params.set('level', level);
    if (type) params.set('type', type);
    if (sort) params.set('sort', sort);

    const newURL = params.toString() ? `?${params.toString()}` : window.location.pathname;
    window.history.replaceState(null, '', newURL);
}

// Load state from URL
function loadURLState() {
    const params = new URLSearchParams(window.location.search);

    const search = params.get('search') || '';
    const category = params.get('category') || '';
    const level = params.get('level') || '';
    const type = params.get('type') || '';
    const sort = params.get('sort') || 'stars-desc';

    // Set form values
    document.getElementById('search-input').value = search;
    document.getElementById('category-filter').value = category;
    document.getElementById('level-filter').value = level;
    document.getElementById('type-filter').value = type;
    document.getElementById('sort-filter').value = sort;

    // Apply filters
    applyFilters();
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
        <div class="error-container">
            <div class="error-icon">⚠️</div>
            <h2 class="error-title">Unable to Load Repositories</h2>
            <p class="error-message">
                We encountered an error while loading the repository data. This could be due to network issues or temporary server problems.
            </p>
            <div class="error-actions">
                <button class="error-btn error-btn-primary" onclick="location.reload()">Try Again</button>
                <button class="error-btn error-btn-secondary" onclick="clearCacheAndReload()">Clear Cache & Reload</button>
            </div>
        </div>
    `;
}

function clearCacheAndReload() {
    localStorage.removeItem('repos_cache');
    location.reload();
}

// Show empty state
function showEmptyState(searchTerm = '') {
    const container = document.getElementById('repositories-container');
    const message = searchTerm
        ? `No repositories found matching "${searchTerm}"`
        : 'No repositories found matching your criteria';

    container.innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">🔍</div>
            <h2 class="empty-title">${message}</h2>
            <p class="empty-message">
                Try adjusting your filters or search terms to find what you're looking for.
            </p>
            <div class="empty-suggestions">
                <h4>Suggestions:</h4>
                <ul>
                    <li>Clear all filters and try again</li>
                    <li>Use broader search terms</li>
                    <li>Check for typos in your search</li>
                    <li>Try a different category or level</li>
                </ul>
            </div>
        </div>
    `;
}

// Update pagination controls
function updatePaginationControls(totalPages: number) {
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');
    const pageInfo = document.getElementById('page-info');
    
    if (totalPages === 0) {
        pageInfo.textContent = 'Page 1 of 1';
        prevPageBtn.disabled = true;
        nextPageBtn.disabled = true;
        return;
    }
    
    pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    prevPageBtn.disabled = currentPage === 1;
    nextPageBtn.disabled = currentPage === totalPages;
}

// Error boundary for JavaScript errors
function setupErrorBoundary() {
    window.addEventListener('error', (event) => {
        console.error('JavaScript Error:', event.error);
        // Could send to error tracking service like Sentry
    });
    
    window.addEventListener('unhandledrejection', (event) => {
        console.error('Unhandled Promise Rejection:', event.reason);
        // Could send to error tracking service
    });
}

// Setup theme toggle
function setupThemeToggle() {
    const toggle = document.getElementById('theme-toggle');
    const themeIcon = toggle.querySelector('.theme-icon');
    
    // Load saved theme or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme, themeIcon);
    
    toggle.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
        updateThemeIcon(next, themeIcon);
    });
}

function updateThemeIcon(theme, icon) {
    icon.textContent = 'Theme';
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