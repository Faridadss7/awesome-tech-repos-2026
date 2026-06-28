#!/usr/bin/env python3
"""
Convert Markdown repository database to structured JSON format.
This script parses the existing Markdown files and converts them to the JSON schema.
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Set UTF-8 encoding for Windows compatibility
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class MarkdownToJSONConverter:
    """Convert Markdown repository tables to structured JSON."""
    
    def __init__(self, markdown_file: str, output_file: str):
        self.markdown_file = Path(markdown_file)
        self.output_file = Path(output_file)
        self.repositories = []
        self.current_category = None
        self.current_subcategory = None
        
    def parse_markdown(self) -> List[Dict]:
        """Parse the Markdown file and extract repository data."""
        with open(self.markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by category headers (## )
        sections = re.split(r'^## ', content, flags=re.MULTILINE)
        
        for section in sections[1:]:  # Skip empty first section
            self._parse_category_section(section)
        
        return self.repositories
    
    def _parse_category_section(self, section: str):
        """Parse a category section and extract repositories."""
        lines = section.strip().split('\n')
        
        # First line is the category name
        if lines:
            # Clean category name (remove numbering like "1. ")
            category_name = lines[0].strip()
            if re.match(r'^\d+\.', category_name):
                category_name = re.sub(r'^\d+\.\s*', '', category_name)
            self.current_category = category_name
            category_id = self._category_to_id(category_name)
        
        # Split by subcategory headers (### )
        subsections = re.split(r'^### ', section, flags=re.MULTILINE)
        
        for subsection in subsections[1:]:  # Skip empty first part
            self._parse_subcategory_section(subsection, category_id)
    
    def _parse_subcategory_section(self, subsection: str, category_id: str):
        """Parse a subcategory section and extract repository tables."""
        lines = subsection.strip().split('\n')
        
        # First line is the subcategory name
        if lines:
            self.current_subcategory = lines[0].strip()
        
        # Find and parse the table
        table_start = -1
        for i, line in enumerate(lines):
            if '|' in line and table_start == -1:
                table_start = i
            elif '|' not in line and table_start != -1:
                # End of table
                self._parse_table_lines(lines[table_start:i], category_id)
                table_start = -1
        
        # Handle case where table goes to end of section
        if table_start != -1:
            self._parse_table_lines(lines[table_start:], category_id)
    
    def _parse_table_lines(self, table_lines: List[str], category_id: str):
        """Parse markdown table lines and extract repository data."""
        if len(table_lines) < 3:  # Need header, separator, and at least one data row
            return
        
        # Skip header and separator lines
        data_lines = table_lines[2:]
        
        for line in data_lines:
            if not line.strip() or not '|' in line:
                continue
            
            repo = self._parse_table_row(line, category_id)
            if repo:
                self.repositories.append(repo)
    
    def _parse_table_row(self, line: str, category_id: str) -> Optional[Dict]:
        """Parse a single table row and return repository data."""
        # Remove leading/trailing | and split by |
        cells = [cell.strip() for cell in line.strip().split('|')]
        cells = [cell for cell in cells if cell]  # Remove empty cells
        
        # Handle different table formats
        # Standard format: Name, Repository, Stars, Subcategory, Tags, Language, Why Recommended, Learning Level
        # Extended format (v7 additions): Name, Repository, GitHub URL, Stars, Subcategory, Tags, Language, Why Recommended, Learning Level
        
        if len(cells) < 8:
            return None
        
        # Adjust for extended format with GitHub URL column
        github_url_col = None
        if len(cells) >= 9 and cells[2].startswith('http'):
            # Extended format: GitHub URL is at index 2
            github_url_col = 2
            # Shift other indices
            stars_idx = 3
            subcategory_idx = 4
            tags_idx = 5
            language_idx = 6
            why_idx = 7
            level_idx = 8
        else:
            # Standard format
            stars_idx = 2
            subcategory_idx = 3
            tags_idx = 4
            language_idx = 5
            why_idx = 6
            level_idx = 7
        
        try:
            # Parse stars (handle various formats: 45k, ~45k, 45,000, etc.)
            stars_str = cells[stars_idx].replace(',', '').replace('~', '').strip()
            
            # Handle 'k' suffix (e.g., 45k -> 45000)
            if 'k' in stars_str.lower():
                stars_str = stars_str.lower().replace('k', '')
                stars = int(float(stars_str) * 1000) if stars_str.replace('.', '').isdigit() else 0
            else:
                stars = int(stars_str) if stars_str.isdigit() else 0
            
            # Parse tags (comma-separated)
            tags = [tag.strip() for tag in cells[tags_idx].split(',')]
            
            # Generate ID
            repo_name = cells[1].split('/')[-1] if '/' in cells[1] else cells[1]
            repo_id = f"{category_id}-{repo_name.lower().replace(' ', '-')}"
            
            # Extract owner/repo from repository field
            if '/' in cells[1]:
                owner, repo = cells[1].split('/')
                github_url = cells[github_url_col] if github_url_col else f"https://github.com/{cells[1]}"
            else:
                owner, repo = None, cells[1]
                github_url = cells[github_url_col] if github_url_col and cells[github_url_col].startswith('http') else None
            
            return {
                "id": repo_id,
                "name": cells[0],
                "repository": cells[1],
                "github_url": github_url,
                "category": self.current_category,
                "category_id": category_id,
                "subcategory": cells[subcategory_idx] if len(cells) > subcategory_idx else self.current_subcategory,
                "tags": tags,
                "stars": stars,
                "language": cells[language_idx],
                "description": cells[why_idx],
                "why_recommended": cells[why_idx],
                "learning_level": cells[level_idx] if len(cells) > level_idx else "Intermediate",
                "last_updated": None,  # Will be filled by GitHub API
                "added_date": datetime.now().strftime("%Y-%m-%d"),
                "is_active": True
            }
        except (ValueError, IndexError) as e:
            print(f"Error parsing row: {line} - {e}")
            return None
    
    def _category_to_id(self, category_name: str) -> str:
        """Convert category name to ID."""
        category_map = {
            "Web Development": "web-dev",
            "Mobile Development": "mobile-dev",
            "Artificial Intelligence & Agents": "ai-agents",
            "Machine Learning & Deep Learning": "ml-dl",
            "Data Science & Analytics": "data-science",
            "Data Engineering & Big Data": "data-engineering",
            "DevOps, Cloud & Infrastructure": "devops-cloud",
            "Cybersecurity": "cybersecurity",
            "Embedded Systems & IoT": "embedded-iot",
            "Robotics & Autonomous Systems": "robotics",
            "Programming Languages & Core Tools": "programming-languages",
            "Developer Tools & Productivity": "dev-tools"
        }
        return category_map.get(category_name, category_name.lower().replace(' ', '-').replace('&', 'and'))
    
    def save_json(self):
        """Save the repositories to JSON file."""
        output_data = {
            "repositories": self.repositories,
            "metadata": {
                "version": "1.0.0",
                "total_repositories": len(self.repositories),
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "categories": len(set(repo["category"] for repo in self.repositories))
            }
        }
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"Converted {len(self.repositories)} repositories to {self.output_file}")


def main():
    """Main function to run the conversion."""
    import sys
    
    # Default paths
    base_dir = Path(__file__).parent.parent
    markdown_file = base_dir.parent / "repositories-database-v7.md"
    output_file = base_dir / "data" / "repositories.json"
    
    # Allow command line arguments
    if len(sys.argv) > 1:
        markdown_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    print(f"Reading Markdown file: {markdown_file}")
    print(f"Output JSON file: {output_file}")
    
    if not Path(markdown_file).exists():
        print(f"Error: Markdown file not found: {markdown_file}")
        sys.exit(1)
    
    converter = MarkdownToJSONConverter(markdown_file, output_file)
    converter.parse_markdown()
    converter.save_json()
    
    print(f"Conversion complete!")


if __name__ == "__main__":
    main()