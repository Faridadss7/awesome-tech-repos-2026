# Contributing to Awesome Tech Repos 2026

Thank you for your interest in contributing to Awesome Tech Repos 2026! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Adding New Repositories

1. **Check Selection Criteria**
   - Minimum 5,000 stars (with exceptions for specialized niches)
   - Active development (updated within 6 months)
   - Good documentation and active community
   - Relevant in 2026
   - No duplicates (one tool per dominant use case)

2. **Verify It's Not Already Listed**
   - Search the existing `data/repositories.json` file
   - Check for similar tools that might serve the same use case

3. **Add Repository Data**
   - Edit `data/repositories.json`
   - Follow the exact schema format
   - Provide meaningful "why_recommended" description (not generic)
   - Set appropriate learning level (Beginner/Intermediate/Advanced)

4. **Validate Your Changes**
   ```bash
   python scripts/validate_data.py data/repositories.json
   ```

5. **Submit a Pull Request**
   - Describe the repository and why it should be included
   - Link to the repository
   - Explain its relevance for 2026

### Updating Existing Repositories

If you notice outdated information:

1. **Star counts** - These are updated automatically weekly via GitHub Actions
2. **Repository status** - If a repository is abandoned or inactive, mark `is_active: false`
3. **Descriptions** - Improve "why_recommended" to be more specific and helpful
4. **Categories** - Suggest category changes if misclassified

### Improving Documentation

- Fix typos and grammatical errors
- Improve clarity of explanations
- Add examples where helpful
- Translate documentation (we're bilingual!)

### Reporting Issues

When reporting issues, please include:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if relevant

## 📋 Repository Schema

When adding repositories, use this exact schema:

```json
{
  "id": "category-xxx",
  "name": "Repository Name",
  "repository": "owner/repository",
  "github_url": "https://github.com/owner/repository",
  "category": "Category Name",
  "category_id": "category-id",
  "subcategory": "Learning Resources or Notable Projects",
  "tags": ["tag1", "tag2"],
  "stars": 10000,
  "language": "Language",
  "description": "Brief description",
  "why_recommended": "Specific reason why this is recommended",
  "learning_level": "Beginner|Intermediate|Advanced",
  "last_updated": "YYYY-MM-DD",
  "added_date": "YYYY-MM-DD",
  "is_active": true
}
```

## 🎯 Selection Guidelines

### Quality Over Quantity

We prioritize quality over hitting numerical targets. Each repository should:

- Solve a real problem well
- Have active maintenance
- Provide clear documentation
- Offer genuine learning or practical value

### Learning Level Classification

- **Beginner**: Good starting point, gentle learning curve, well-documented
- **Intermediate**: Requires some experience, assumes basic knowledge
- **Advanced**: Complex concepts, requires deep expertise

### "Why Recommended" Guidelines

The "why_recommended" field should:

- Be specific (not "great repository" or "very useful")
- Explain the unique value proposition
- Mention what makes it stand from alternatives
- Include context about who should use it

**Good examples:**
- "Excellent for building REST APIs with automatic OpenAPI documentation and type safety"
- "Best-in-class React state management with built-in devtools and minimal boilerplate"
- "Industry-standard for computer vision with comprehensive algorithms and GPU acceleration"

**Bad examples:**
- "Great repository"
- "Very useful tool"
- "Popular and well-maintained"

## 🔧 Development Workflow

### Setting Up Development Environment

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/awesome-tech-repos-2026.git
   cd awesome-tech-repos-2026
   ```

3. Install dependencies:
   ```bash
   pip install requests
   ```

4. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Making Changes

1. Edit the relevant files
2. Validate your changes:
   ```bash
   python scripts/validate_data.py data/repositories.json
   ```

3. Test any scripts you modified
4. Commit your changes:
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request

### Commit Message Guidelines

Use conventional commit format:

- `Add:` - New repositories or features
- `Update:` - Updates to existing data
- `Fix:` - Bug fixes
- `Docs:` - Documentation changes
- `Refactor:` - Code refactoring

Examples:
- `Add: Add TensorFlow to ML & Deep Learning category`
- `Update: Update star counts for web development repositories`
- `Fix: Fix validation script to handle missing fields`

## 🌍 Bilingual Contributions

This project is bilingual (English/French). When contributing:

- **README.md** - Always maintain both languages
- **Repository data** - "why_recommended" can be in either language (we'll normalize later)
- **Documentation** - Prefer English for technical docs, French for community-facing content

## 🤖 Automated Scripts

The project includes several automated scripts:

### `convert_markdown_to_json.py`
Converts Markdown tables to JSON format

### `validate_data.py`
Validates repository data against selection criteria

### `update_stars.py`
Updates star counts and metadata via GitHub API

### `discover_repositories.py`
Discovers new repositories using GitHub Search API

## 📊 Category Targets

Our target distribution across categories:

- Web Development: ~100 repos
- Mobile Development: ~60 repos
- AI & Agents: ~100 repos
- ML & Deep Learning: ~100 repos
- Data Science: ~80 repos
- Data Engineering: ~60 repos
- DevOps & Cloud: ~100 repos
- Cybersecurity: ~80 repos
- Embedded & IoT: ~60 repos
- Robotics: ~60 repos
- Programming Languages: ~100 repos
- Developer Tools: ~100 repos

## ⚠️ Common Pitfalls

### Don't:

- Add repositories just because they're popular
- Include duplicate tools for the same use case
- Use generic descriptions
- Add inactive or abandoned projects
- Ignore the selection criteria

### Do:

- Research alternatives before adding
- Provide specific, helpful descriptions
- Check activity and maintenance status
- Consider learning value
- Follow the schema exactly

## 🎉 Recognition

Contributors will be recognized in:

- CONTRIBUTORS.md file
- Release notes for significant contributions
- Project documentation for major additions

## 📞 Getting Help

If you need help:

- Open an issue with your question
- Check existing issues for similar problems
- Read the documentation thoroughly
- Be patient with volunteer maintainers

## 📜 Code of Conduct

Be respectful, constructive, and inclusive. We welcome contributors from all backgrounds and experience levels.

---

Thank you for contributing to Awesome Tech Repos 2026! 🚀