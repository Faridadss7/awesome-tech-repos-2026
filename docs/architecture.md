# Architecture Documentation

## Overview

Awesome Tech Repos 2026 follows a modular, scalable architecture designed for easy maintenance and automation.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Repository                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Data Layer │  │  Script Layer│  │  Web Layer   │       │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤       │
│  │ repositories │  │  Python      │  │  HTML/CSS/JS │       │
│  │ categories   │  │  Scripts     │  │  (GitHub     │       │
│  │ metadata     │  │              │  │   Pages)     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│         │                  │                  │              │
│         └──────────────────┼──────────────────┘              │
│                            │                                 │
│                    ┌───────▼───────┐                          │
│                    │ GitHub Actions │                          │
│                    │  Automation    │                          │
│                    └───────────────┘                          │
│                            │                                 │
│                    ┌───────▼───────┐                          │
│                    │  GitHub API   │                          │
│                    └───────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

## Data Layer

### JSON Schema

The data layer uses JSON for maximum compatibility and ease of parsing:

**repositories.json**: Main database
```json
{
  "repositories": [
    {
      "id": "category-xxx",
      "name": "Repository Name",
      "repository": "owner/repo",
      "github_url": "https://github.com/owner/repo",
      "category": "Category Name",
      "category_id": "category-id",
      "subcategory": "Learning Resources|Notable Projects",
      "tags": ["tag1", "tag2"],
      "stars": 10000,
      "language": "Language",
      "description": "Description",
      "why_recommended": "Why recommended",
      "learning_level": "Beginner|Intermediate|Advanced",
      "last_updated": "YYYY-MM-DD",
      "added_date": "YYYY-MM-DD",
      "is_active": true
    }
  ],
  "metadata": {
    "version": "1.0.0",
    "total_repositories": 1000,
    "last_updated": "YYYY-MM-DD",
    "categories": 12
  }
}
```

**categories.json**: Category configuration
```json
{
  "categories": [
    {
      "id": "web-dev",
      "name": "Web Development",
      "description": "Description",
      "subcategories": ["Learning Resources", "Notable Projects"],
      "target_count": 100
    }
  ]
}
```

### Data Validation

- Schema validation via Python scripts
- Automatic type checking
- Required field validation
- Range validation (stars, dates)

## Script Layer

### Python Scripts

**convert_markdown_to_json.py**
- Parses existing Markdown tables
- Converts to JSON schema
- Generates unique IDs
- Extracts GitHub URLs

**validate_data.py**
- Validates against selection criteria
- Checks required fields
- Validates data types
- Generates validation reports

**update_stars.py**
- Fetches real-time data from GitHub API
- Updates star counts
- Checks activity status
- Handles rate limiting

**discover_repositories.py**
- Searches GitHub via API
- Applies quality filters
- Categorizes automatically
- Generates candidate lists

### Automation

**GitHub Actions** (`.github/workflows/update-stars.yml`)
- Runs weekly on Sundays
- Updates repository metadata
- Validates updated data
- Commits changes automatically

## Web Layer

### GitHub Pages

**Static Website** (`website/`)
- Pure HTML/CSS/JavaScript
- No build process required
- Fast loading times
- Easy deployment

**Features**
- Category browsing
- Search functionality
- Filter by level
- Responsive design
- Real-time data loading

### JavaScript Architecture

```javascript
// Data Loading
async function loadRepositories() {
    const response = await fetch('../data/repositories.json');
    const data = await response.json();
    return data.repositories;
}

// Filtering System
function applyFilters(search, category, level) {
    return repositories.filter(repo => {
        return matchesSearch(repo, search) &&
               matchesCategory(repo, category) &&
               matchesLevel(repo, level);
    });
}

// Rendering
function renderRepositories(repositories) {
    repositories.forEach(repo => {
        const card = createRepositoryCard(repo);
        container.appendChild(card);
    });
}
```

## API Integration

### GitHub API Usage

**Authentication**
```python
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
```

**Rate Limiting**
- Authenticated: 5,000 requests/hour
- Unauthenticated: 60 requests/hour
- Automatic sleep when approaching limits
- Exponential backoff on errors

**Endpoints Used**
- `/search/repositories` - Discovery
- `/repos/{owner}/{repo}` - Metadata
- `/rate_limit` - Rate limit status

## Workflow

### Adding New Repositories

1. **Manual Addition**
   - Edit `data/repositories.json`
   - Follow schema exactly
   - Run validation script
   - Submit PR

2. **Automated Discovery**
   - Run discovery script
   - Review candidates
   - Add validated repos
   - Update metadata

3. **Validation**
   - Check selection criteria
   - Verify no duplicates
   - Validate data quality
   - Test website rendering

### Data Update Cycle

```
┌─────────────┐
│   Manual    │
│   Input     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Validation  │
│   Script    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   JSON      │
│   Database  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   GitHub    │
│   Actions   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   GitHub    │
│   API       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Updated   │
│   Metadata  │
└─────────────┘
```

## Security Considerations

### GitHub Token Management
- Store in GitHub Secrets
- Never commit to repository
- Use least privilege principle
- Rotate regularly

### Data Validation
- Sanitize all user inputs
- Validate JSON schema
- Check for malicious content
- Rate limit API calls

### Website Security
- HTTPS only
- Content Security Policy
- No server-side processing
- Static file serving only

## Scalability

### Current Capacity
- Target: 1,000 repositories
- Categories: 12
- Average per category: ~80 repos

### Scaling Strategy
- JSON format handles 10,000+ repos easily
- JavaScript pagination for large datasets
- Server-side search if needed
- Database migration if >10,000 repos

### Performance Optimization
- Lazy loading of categories
- Debounced search input
- CSS-based animations
- Minimal JavaScript dependencies

## Maintenance

### Regular Tasks
- Weekly: Automatic star updates
- Monthly: Review inactive repos
- Quarterly: Category balance review
- Annually: Selection criteria review

### Monitoring
- GitHub Actions status
- API rate limits
- Website performance
- Link validity

## Future Enhancements

### Phase 2 Features
- Advanced search with filters
- User favorites/bookmarks
- Contribution analytics
- Trending repositories
- Learning paths

### Phase 3 Features
- User accounts
- Submission system
- Community voting
- Integration with other platforms
- API for third-party use

---

This architecture ensures the project remains maintainable, scalable, and professional while being easy to contribute to and extend.