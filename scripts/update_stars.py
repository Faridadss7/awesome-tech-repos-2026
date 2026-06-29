#!/usr/bin/env python3
"""
Update repository metadata using GitHub API.
This script fetches current star counts, last updated dates, and activity status.
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import requests

# Set UTF-8 encoding for Windows compatibility
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class GitHubDataUpdater:
    """Update repository data using GitHub API."""
    
    def __init__(self, data_file: str, github_token: Optional[str] = None) -> None:
        self.data_file = Path(data_file)
        self.github_token = github_token
        self.base_url = "https://api.github.com"
        self.rate_limit_remaining = 5000
        self.rate_limit_reset: Optional[int] = None
        
        # Load existing data
        with open(self.data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.repositories: List[Dict] = self.data.get("repositories", [])
    
    def _make_github_request(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Make a request to GitHub API with rate limiting handling."""
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, headers=headers)
            
            # Update rate limit info
            self.rate_limit_remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
            self.rate_limit_reset = int(response.headers.get("X-RateLimit-Reset", 0))
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                print(f"WARNING: Rate limit exceeded. Reset at: {datetime.fromtimestamp(self.rate_limit_reset)}")
                return None
            else:
                print(f"ERROR: {response.status_code} for {url}")
                return None

        except Exception as e:
            print(f"ERROR: Request failed: {e}")
            return None
    
    def _extract_owner_repo(self, repository: str) -> Optional[Tuple[str, str]]:
        """Extract owner and repo name from repository string."""
        if '/' in repository:
            parts = repository.split('/')
            if len(parts) == 2:
                return parts[0], parts[1]
        return None
    
    def update_repository_data(self, repo: Dict[str, Any]) -> Dict[str, Any]:
        """Update a single repository's data from GitHub API."""
        owner_repo = self._extract_owner_repo(repo["repository"])
        if not owner_repo:
            print(f"Warning: Could not parse repository: {repo['repository']}")
            return repo
        
        owner, repo_name = owner_repo
        endpoint = f"/repos/{owner}/{repo_name}"
        
        repo_data = self._make_github_request(endpoint)
        if not repo_data:
            return repo
        
        # Update fields
        repo["stars"] = repo_data.get("stargazers_count", repo["stars"])

        # Ensure last_updated is always set with proper format
        if 'pushed_at' in repo_data and repo_data['pushed_at']:
            repo["last_updated"] = repo_data['pushed_at'][:10]  # Format YYYY-MM-DD
        elif not repo.get("last_updated"):
            # If no pushed_at and no existing last_updated, set to current date
            repo["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        
        # Check if active (updated within 6 months)
        if repo["last_updated"]:
            last_updated = datetime.fromisoformat(repo["last_updated"].replace('Z', '+00:00'))
            six_months_ago = datetime.now() - timedelta(days=180)
            repo["is_active"] = last_updated > six_months_ago
        
        # Ensure GitHub URL
        repo["github_url"] = repo_data.get("html_url", repo["github_url"])
        
        # Add additional useful metadata
        repo["forks"] = repo_data.get("forks_count", 0)
        repo["open_issues"] = repo_data.get("open_issues_count", 0)
        repo["watchers"] = repo_data.get("subscribers_count", 0)
        repo["has_wiki"] = repo_data.get("has_wiki", False)
        repo["has_pages"] = repo_data.get("has_pages", False)
        repo["license"] = repo_data.get("license", {}).get("name", "") if repo_data.get("license") else ""
        
        print(f"Updated {repo['name']}: {repo['stars']} stars, active: {repo['is_active']}")
        
        # Rate limiting: sleep if we're getting close to limit
        if self.rate_limit_remaining < 100:
            sleep_time = 2
            print(f"Sleeping {sleep_time}s to respect rate limits...")
            time.sleep(sleep_time)
        
        return repo
    
    def update_all_repositories(self) -> None:
        """Update all repositories in the dataset."""
        print(f"Updating {len(self.repositories)} repositories...")

        updated_count = 0
        for i, repo in enumerate(self.repositories):
            print(f"[{i+1}/{len(self.repositories)}] ", end="")

            try:
                self.repositories[i] = self.update_repository_data(repo)
                updated_count += 1
            except Exception as e:
                print(f"ERROR: Failed to update {repo['name']}: {e}")

        print(f"\nSuccessfully updated {updated_count}/{len(self.repositories)} repositories")
    
    def save_updated_data(self) -> None:
        """Save the updated data back to file."""
        self.data["repositories"] = self.repositories
        self.data["metadata"]["total_repositories"] = len(self.repositories)
        self.data["metadata"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")

        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, separators=(',', ':'), ensure_ascii=False)

        print(f"Saved updated data to {self.data_file}")


def main():
    """Main function to run the update."""
    import sys
    import os
    
    base_dir = Path(__file__).parent.parent
    data_file = base_dir / "data" / "repositories.json"
    github_token = os.environ.get("GITHUB_TOKEN")
    
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
    
    print(f"Data file: {data_file}")
    print(f"GitHub token: {'Set' if github_token else 'Not set (using unauthenticated requests)'}")
    
    if not Path(data_file).exists():
        print(f"Error: Data file not found: {data_file}")
        sys.exit(1)
    
    updater = GitHubDataUpdater(data_file, github_token)
    updater.update_all_repositories()
    updater.save_updated_data()
    
    print("Update complete!")


if __name__ == "__main__":
    main()