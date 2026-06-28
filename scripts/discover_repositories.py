#!/usr/bin/env python3
"""
Discover new repositories using GitHub Search API.
This script helps find high-quality repositories to reach the target of 1000 repos.
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
import requests

# Set UTF-8 encoding for Windows compatibility
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class RepositoryDiscoverer:
    """Discover new repositories using GitHub Search API."""
    
    def __init__(self, data_file: str, categories_file: str, github_token: Optional[str] = None):
        self.data_file = Path(data_file)
        self.categories_file = Path(categories_file)
        self.github_token = github_token
        self.base_url = "https://api.github.com"
        
        # Load existing data
        with open(self.data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        with open(self.categories_file, 'r', encoding='utf-8') as f:
            self.categories_data = json.load(f)
        
        self.existing_repos = set()
        for repo in self.data.get("repositories", []):
            self.existing_repos.add(repo["repository"])
        
        self.categories = {cat["id"]: cat for cat in self.categories_data.get("categories", [])}
        self.discovered_repos = []
    
    def _make_github_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make a request to GitHub API with rate limiting handling."""
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                print(f"Warning: Rate limit exceeded")
                return None
            elif response.status_code == 422:
                print(f"Warning: Invalid query parameters")
                return None
            else:
                print(f"Error {response.status_code} for {url}")
                return None
                
        except Exception as e:
            print(f"Request failed: {e}")
            return None
    
    def _search_github(self, query: str, sort: str = "stars", order: str = "desc", per_page: int = 100) -> List[Dict]:
        """Search GitHub repositories."""
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": per_page
        }
        
        results = self._make_github_request("/search/repositories", params)
        if results and "items" in results:
            return results["items"]
        return []
    
    def _get_category_search_terms(self, category_id: str) -> List[str]:
        """Get search terms for a specific category."""
        category = self.categories.get(category_id, {})
        category_name = category.get("name", "").lower()
        
        # Define search terms for each category
        search_terms = {
            "web-dev": [
                "web framework language:javascript",
                "web framework language:typescript", 
                "react framework stars:>5000",
                "vue framework stars:>5000",
                "backend framework stars:>5000",
                "css framework stars:>5000",
                "web development tools stars:>5000"
            ],
            "mobile-dev": [
                "mobile framework stars:>5000",
                "react native stars:>5000",
                "flutter stars:>5000",
                "android development stars:>5000",
                "ios development stars:>5000"
            ],
            "ai-agents": [
                "artificial intelligence stars:>5000",
                "machine learning framework stars:>5000",
                "llm stars:>5000",
                "prompt engineering stars:>5000",
                "ai agents stars:>5000"
            ],
            "ml-dl": [
                "deep learning framework stars:>5000",
                "neural network stars:>5000",
                "tensorflow stars:>5000",
                "pytorch stars:>5000",
                "machine learning library stars:>5000"
            ],
            "data-science": [
                "data analysis stars:>5000",
                "data visualization stars:>5000",
                "jupyter notebook stars:>5000",
                "pandas stars:>5000",
                "data science tools stars:>5000"
            ],
            "data-engineering": [
                "data pipeline stars:>5000",
                "etl stars:>5000",
                "big data stars:>5000",
                "apache spark stars:>5000",
                "data engineering stars:>5000"
            ],
            "devops-cloud": [
                "devops stars:>5000",
                "docker stars:>5000",
                "kubernetes stars:>5000",
                "ci/cd stars:>5000",
                "infrastructure as code stars:>5000"
            ],
            "cybersecurity": [
                "security tools stars:>5000",
                "penetration testing stars:>5000",
                "cryptography stars:>5000",
                "cybersecurity stars:>5000",
                "network security stars:>5000"
            ],
            "embedded-iot": [
                "embedded systems stars:>1000",
                "iot stars:>1000",
                "microcontroller stars:>1000",
                "raspberry pi stars:>1000",
                "arduino stars:>1000"
            ],
            "robotics": [
                "robotics stars:>1000",
                "ros stars:>1000",
                "autonomous systems stars:>1000",
                "drone stars:>1000",
                "robot simulation stars:>1000"
            ],
            "programming-languages": [
                "programming language stars:>5000",
                "compiler stars:>5000",
                "interpreter stars:>5000",
                "runtime stars:>5000",
                "language implementation stars:>5000"
            ],
            "dev-tools": [
                "developer tools stars:>5000",
                "ide stars:>5000",
                "code editor stars:>5000",
                "productivity tools stars:>5000",
                "developer utilities stars:>5000"
            ]
        }
        
        return search_terms.get(category_id, [category_name])
    
    def _check_repository_quality(self, repo_data: Dict) -> tuple[bool, str]:
        """Check if a repository meets quality criteria."""
        # Check stars
        stars = repo_data.get("stargazers_count", 0)
        if stars < 1000:  # Minimum threshold for discovery
            return False, "Too few stars"
        
        # Check if updated recently
        updated_at = repo_data.get("updated_at", "")
        if updated_at:
            try:
                # Handle various datetime formats from GitHub API
                if updated_at.endswith('Z'):
                    updated_at = updated_at.replace('Z', '+00:00')
                last_updated = datetime.fromisoformat(updated_at)
                
                # Make both datetimes offset-aware or offset-naive
                if last_updated.tzinfo is not None:
                    six_months_ago = datetime.now(last_updated.tzinfo) - timedelta(days=180)
                else:
                    six_months_ago = datetime.now() - timedelta(days=180)
                    
                if last_updated < six_months_ago:
                    return False, "Not recently updated"
            except (ValueError, TypeError) as e:
                # If date parsing fails, still accept the repo
                pass
        
        # Check if it's a fork (prefer original repos)
        if repo_data.get("fork", False):
            return False, "Is a fork"
        
        # Check if it has a README
        if not repo_data.get("has_readme", False):
            return False, "No README"
        
        return True, "Meets criteria"
    
    def discover_for_category(self, category_id: str, target_count: int) -> List[Dict]:
        """Discover repositories for a specific category."""
        category = self.categories.get(category_id, {})
        category_name = category.get("name", category_id)
        
        print(f"\nDiscovering repositories for: {category_name}")
        print(f"Target count: {target_count}")
        
        search_terms = self._get_category_search_terms(category_id)
        discovered = []
        seen = set()
        
        for term in search_terms:
            if len(discovered) >= target_count:
                break
            
            print(f"  Searching: '{term}'")
            results = self._search_github(term)
            
            for repo in results:
                repo_full_name = f"{repo['owner']['login']}/{repo['name']}"
                
                # Skip if already in existing repos
                if repo_full_name in self.existing_repos:
                    continue
                
                # Skip if already discovered in this session
                if repo_full_name in seen:
                    continue
                
                seen.add(repo_full_name)
                
                # Check quality
                is_valid, reason = self._check_repository_quality(repo)
                if is_valid:
                    discovered.append({
                        "repository": repo_full_name,
                        "name": repo["name"],
                        "stars": repo["stargazers_count"],
                        "github_url": repo["html_url"],
                        "description": repo.get("description", ""),
                        "language": repo.get("language", ""),
                        "category": category_name,
                        "category_id": category_id,
                        "subcategory": "Notable Projects",  # Default
                        "tags": [],
                        "why_recommended": f"Popular {category_name} repository with {repo['stargazers_count']} stars and active development.",
                        "learning_level": "Intermediate",
                        "last_updated": repo.get("updated_at"),
                        "added_date": datetime.now().strftime("%Y-%m-%d"),
                        "is_active": True,
                        "forks": repo.get("forks_count", 0),
                        "open_issues": repo.get("open_issues_count", 0)
                    })
                    print(f"    Found: {repo_full_name} ({repo['stargazers_count']} stars)")
                
                if len(discovered) >= target_count:
                    break
            
            # Rate limiting
            time.sleep(1)
        
        print(f"  Discovered {len(discovered)} repositories for {category_name}")
        return discovered
    
    def discover_all_categories(self):
        """Discover repositories for all categories to reach target of 1000."""
        print("Starting repository discovery...")
        print(f"Current repositories: {len(self.existing_repos)}")
        print(f"Target: 1000 repositories")
        print(f"Need to discover: {1000 - len(self.existing_repos)} repositories\n")
        
        all_discovered = []
        
        for category_id, category in self.categories.items():
            current_count = sum(1 for r in self.data.get("repositories", []) if r.get("category_id") == category_id)
            target_count = category.get("target_count", 80)
            needed = max(0, target_count - current_count)
            
            if needed > 0:
                discovered = self.discover_for_category(category_id, needed)
                all_discovered.extend(discovered)
        
        self.discovered_repos = all_discovered
        print(f"\nDiscovery complete! Found {len(all_discovered)} new repositories")
        
        return all_discovered
    
    def save_discovered_repos(self, output_file: str):
        """Save discovered repositories to a separate file for review."""
        output_path = Path(output_file)
        
        output_data = {
            "discovered_repositories": self.discovered_repos,
            "metadata": {
                "total_discovered": len(self.discovered_repos),
                "discovery_date": datetime.now().strftime("%Y-%m-%d"),
                "needs_manual_review": True
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved discovered repositories to {output_path}")
        print(f"Please review these repositories before adding to main database")


def main():
    """Main function to run discovery."""
    import sys
    import os
    
    base_dir = Path(__file__).parent.parent
    data_file = base_dir / "data" / "repositories.json"
    categories_file = base_dir / "data" / "categories.json"
    output_file = base_dir / "data" / "discovered_repositories.json"
    
    # Try to get token from environment variable or command line
    github_token = os.environ.get("GITHUB_TOKEN")
    
    # Allow token as command line argument
    if len(sys.argv) > 1:
        if sys.argv[1].startswith("ghp_"):
            github_token = sys.argv[1]
        else:
            data_file = sys.argv[1]
    
    if len(sys.argv) > 2 and sys.argv[2].startswith("ghp_"):
        github_token = sys.argv[2]
    
    print(f"Data file: {data_file}")
    print(f"Categories file: {categories_file}")
    print(f"GitHub token: {'Set' if github_token else 'Not set (limited rate limits)'}")
    
    if not Path(data_file).exists():
        print(f"Error: Data file not found: {data_file}")
        sys.exit(1)
    
    discoverer = RepositoryDiscoverer(data_file, categories_file, github_token)
    discoverer.discover_all_categories()
    discoverer.save_discovered_repos(output_file)
    
    print("Discovery complete! Please review the discovered repositories.")


if __name__ == "__main__":
    main()