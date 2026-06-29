# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-06-29

### Added
- Pagination system (24 repositories per page) to improve performance on mobile devices
- LocalStorage cache (24h TTL) for repository data to reduce bandwidth usage
- Sorting functionality (stars, name, date added) in the search interface
- SEO and Open Graph meta tags for better social media sharing
- Dark/Light mode toggle with localStorage persistence
- Comprehensive tags generation for repositories (810 repositories updated)
- Language inference for repositories with null language values (67 repositories updated)
- Learning level reevaluation for better distribution (222 Beginner, 413 Intermediate, 365 Advanced)

### Changed
- Fixed 13 duplicate repository IDs by adding numeric suffixes
- Updated README.md banner references to use single banner.jpg file
- Removed duplicate banner.jpg files (saved ~700KB)
- Updated update_stars.py to use pushed_at instead of updated_at for last_updated field
- Enhanced frontend with premium design features (glassmorphism, gradients, animations)

### Fixed
- Repository ID conflicts by implementing unique ID generation
- Empty tags array issue for 810 repositories
- Null language values for 67 repositories
- Improved learning level distribution for better filtering experience

## [1.1.0] - 2026-06-28

### Added
- GitHub Pages website with interactive filtering and search
- GitHub Actions workflow for automatic star count updates
- Bilingual documentation (English/French)
- Repository discovery automation scripts
- Data validation and conversion utilities
- Professional project structure with organized directories

### Changed
- Converted from Markdown-based data to JSON format
- Implemented automated metadata updates via GitHub API
- Enhanced repository categorization system

## [1.0.0] - 2026-06-27

### Added
- Initial collection of 1,000 curated GitHub repositories
- 12 major technology domains
- JSON data structure with enriched metadata
- Basic repository selection criteria
- Core Python scripts for data management
- Project documentation and contribution guidelines

[1.2.0]: https://github.com/Faridadss7/awesome-tech-repos-2026/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/Faridadss7/awesome-tech-repos-2026/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Faridadss7/awesome-tech-repos-2026/releases/tag/v1.0.0
