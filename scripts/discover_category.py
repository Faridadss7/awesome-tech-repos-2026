#!/usr/bin/env python3
"""
Discover repositories for a specific category.
Usage: py discover_category.py <category_id> <category_name> <target_count> <github_token>
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime
import requests

# Set UTF-8 encoding for Windows compatibility
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def discover_category(category_id, category_name, target_count, github_token=None):
    """Discover repositories for a specific category."""
    base_dir = Path(__file__).parent.parent
    data_file = base_dir / "data" / "repositories.json"
    output_file = base_dir / "data" / f"discovered_{category_id}.json"
    
    print(f"Discovering: {category_name}")
    print(f"Target: {target_count} repositories")
    print("=" * 50)
    
    # Load existing data
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    existing_repos = set(repo["repository"] for repo in data["repositories"])
    print(f"Existing repositories: {len(existing_repos)}")
    
    # Search terms for this category
    search_terms_map = {
        "ai-agents": [
            "artificial intelligence stars:>10000",
            "machine learning framework stars:>10000",
            "deep learning stars:>10000",
            "llm stars:>10000"
        ],
        "ml-dl": [
            "tensorflow stars:>10000",
            "pytorch stars:>10000",
            "neural network stars:>10000",
            "computer vision stars:>10000"
        ],
        "mobile-dev": [
            "mobile framework stars:>10000",
            "android development stars:>10000",
            "ios development stars:>10000",
            "cross-platform stars:>10000"
        ],
        "data-science": [
            "data analysis stars:>10000",
            "data visualization stars:>10000",
            "pandas stars:>10000",
            "jupyter stars:>10000"
        ],
        "dev-tools": [
            "developer tools stars:>10000",
            "code editor stars:>10000",
            "ide stars:>10000",
            "productivity stars:>10000"
        ],
        "devops-cloud": [
            "devops stars:>10000",
            "docker stars:>10000",
            "kubernetes stars:>10000",
            "infrastructure stars:>10000"
        ]
    }
    
    search_terms = search_terms_map.get(category_id, [
        f"{category_name} stars:>10000"
    ])
    
    discovered = []
    headers = {"Accept": "application/vnd.github.v3+json"}
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    for term in search_terms:
        if len(discovered) >= target_count:
            break
        
        print(f"Searching: '{term}'")
        
        try:
            response = requests.get(
                "https://api.github.com/search/repositories",
                params={"q": term, "sort": "stars", "order": "desc", "per_page": 20},
                headers=headers
            )
            
            if response.status_code == 200:
                results = response.json()
                items = results.get("items", [])
                
                for repo in items:
                    repo_full_name = f"{repo['owner']['login']}/{repo['name']}"
                    
                    if repo_full_name not in existing_repos:
                        stars = repo.get("stargazers_count", 0)
                        if stars >= 5000:
                            discovered.append({
                                "repository": repo_full_name,
                                "name": repo["name"],
                                "stars": stars,
                                "github_url": repo["html_url"],
                                "description": repo.get("description", ""),
                                "language": repo.get("language", ""),
                                "category": category_name,
                                "category_id": category_id,
                                "subcategory": "Notable Projects",
                                "tags": [],
                                "why_recommended": f"Popular {category_name} repository with {stars} stars and active development.",
                                "learning_level": "Intermediate",
                                "last_updated": repo.get("updated_at"),
                                "added_date": datetime.now().strftime("%Y-%m-%d"),
                                "is_active": True
                            })
                            print(f"  Found: {repo_full_name} ({stars} stars)")
                            
                            if len(discovered) >= target_count:
                                break
                        else:
                            print(f"  Skipped (low stars): {repo_full_name} ({stars})")
                    else:
                        print(f"  Skipped (exists): {repo_full_name}")
                
                if len(discovered) >= target_count:
                    break
            else:
                print(f"  Error: {response.status_code}")
                if response.status_code == 403:
                    print("  Rate limit reached, stopping...")
                    break
            
            time.sleep(2)
            
        except Exception as e:
            print(f"  Request failed: {e}")
    
    # Save results
    output_data = {
        "discovered_repositories": discovered,
        "metadata": {
            "total_discovered": len(discovered),
            "discovery_date": datetime.now().strftime("%Y-%m-%d"),
            "category": category_name,
            "category_id": category_id
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*50}")
    print(f"Discovery complete for {category_name}!")
    print(f"Found {len(discovered)} new repositories")
    print(f"Results saved to: {output_file}")
    print(f"{'='*50}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: py discover_category.py <category_id> <category_name> <target_count> [github_token]")
        sys.exit(1)
    
    category_id = sys.argv[1]
    category_name = sys.argv[2]
    target_count = int(sys.argv[3])
    token = sys.argv[4] if len(sys.argv) > 4 else None
    
    discover_category(category_id, category_name, target_count, token)