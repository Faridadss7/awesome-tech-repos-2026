#!/usr/bin/env python3
"""
Test script to discover a small number of repositories (for demonstration).
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import requests

# Set UTF-8 encoding for Windows compatibility
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def test_discovery():
    """Test discovery with a small sample."""
    base_dir = Path(__file__).parent.parent
    data_file = base_dir / "data" / "repositories.json"
    output_file = base_dir / "data" / "test_discovered.json"
    
    print("Test Repository Discovery")
    print("=" * 50)
    print(f"Data file: {data_file}")
    
    # Load existing repos
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    existing_repos = set(repo["repository"] for repo in data["repositories"])
    print(f"Existing repositories: {len(existing_repos)}")
    
    # Test search for a few popular repositories
    test_searches = [
        "react framework stars:>50000",
        "python web framework stars:>50000",
        "machine learning stars:>50000"
    ]
    
    discovered = []
    
    for search_query in test_searches:
        print(f"\nSearching: '{search_query}'")
        
        try:
            response = requests.get(
                "https://api.github.com/search/repositories",
                params={"q": search_query, "sort": "stars", "order": "desc", "per_page": 5},
                headers={"Accept": "application/vnd.github.v3+json"}
            )
            
            if response.status_code == 200:
                results = response.json()
                for repo in results.get("items", []):
                    repo_full_name = f"{repo['owner']['login']}/{repo['name']}"
                    
                    if repo_full_name not in existing_repos:
                        discovered.append({
                            "repository": repo_full_name,
                            "name": repo["name"],
                            "stars": repo["stargazers_count"],
                            "github_url": repo["html_url"],
                            "description": repo.get("description", ""),
                            "language": repo.get("language", ""),
                            "why_recommended": f"Popular repository with {repo['stargazers_count']} stars",
                            "last_updated": repo.get("updated_at"),
                            "added_date": datetime.now().strftime("%Y-%m-%d")
                        })
                        print(f"  Found: {repo_full_name} ({repo['stargazers_count']} stars)")
                    else:
                        print(f"  Skipped (already exists): {repo_full_name}")
            else:
                print(f"  Error: {response.status_code}")
        
        except Exception as e:
            print(f"  Request failed: {e}")
        
        # Rate limiting
        time.sleep(2)
    
    # Save results
    output_data = {
        "test_discovered": discovered,
        "metadata": {
            "total_found": len(discovered),
            "test_date": datetime.now().strftime("%Y-%m-%d"),
            "note": "This is a test sample. Use discover_repositories.py for full discovery."
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n" + "=" * 50)
    print(f"Test complete! Found {len(discovered)} new repositories")
    print(f"Results saved to: {output_file}")
    print("\nFor full discovery to reach 1000 repositories:")
    print("1. Get a GitHub token from https://github.com/settings/tokens")
    print("2. Set GITHUB_TOKEN environment variable")
    print("3. Run: py scripts/discover_repositories.py")


if __name__ == "__main__":
    test_discovery()