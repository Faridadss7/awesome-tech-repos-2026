#!/usr/bin/env python3
"""
Progressive repository discovery - finds repos in smaller batches to avoid rate limits.
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


def progressive_discovery(github_token=None):
    """Discover repositories progressively in small batches."""
    base_dir = Path(__file__).parent.parent
    data_file = base_dir / "data" / "repositories.json"
    categories_file = base_dir / "data" / "categories.json"
    output_file = base_dir / "data" / "progressive_discovered.json"
    
    print("Progressive Repository Discovery")
    print("=" * 50)
    
    # Load existing data
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(categories_file, 'r', encoding='utf-8') as f:
        categories_data = json.load(f)
    
    existing_repos = set(repo["repository"] for repo in data["repositories"])
    print(f"Existing repositories: {len(existing_repos)}")
    
    # Focus on a few categories first
    priority_categories = [
        ("web-dev", "Web Development", 20),
        ("ai-agents", "Artificial Intelligence & Agents", 15),
        ("ml-dl", "Machine Learning & Deep Learning", 15),
        ("dev-tools", "Developer Tools & Productivity", 15),
        ("mobile-dev", "Mobile Development", 10),
        ("data-science", "Data Science & Analytics", 10)
    ]
    
    discovered = []
    headers = {"Accept": "application/vnd.github.v3+json"}
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    for cat_id, cat_name, target in priority_categories:
        print(f"\n{'='*50}")
        print(f"Category: {cat_name} (target: {target})")
        print(f"{'='*50}")
        
        # Simple search terms for this category
        if cat_id == "web-dev":
            search_terms = [
                "javascript framework stars:>10000",
                "typescript framework stars:>10000", 
                "react library stars:>10000",
                "css framework stars:>10000"
            ]
        elif cat_id == "ai-agents":
            search_terms = [
                "artificial intelligence stars:>10000",
                "machine learning framework stars:>10000",
                "deep learning stars:>10000"
            ]
        elif cat_id == "ml-dl":
            search_terms = [
                "tensorflow stars:>10000",
                "pytorch stars:>10000",
                "neural network stars:>10000"
            ]
        elif cat_id == "mobile-dev":
            search_terms = [
                "mobile framework stars:>10000",
                "android development stars:>10000",
                "ios development stars:>10000"
            ]
        elif cat_id == "data-science":
            search_terms = [
                "data analysis stars:>10000",
                "data visualization stars:>10000",
                "pandas stars:>10000"
            ]
        else:
            search_terms = [
                "developer tools stars:>10000",
                "code editor stars:>10000",
                "productivity stars:>10000"
            ]
        
        for term in search_terms:
            if len(discovered) >= target:
                break
            
            print(f"  Searching: '{term}'")
            
            try:
                response = requests.get(
                    "https://api.github.com/search/repositories",
                    params={"q": term, "sort": "stars", "order": "desc", "per_page": 10},
                    headers=headers
                )
                
                if response.status_code == 200:
                    results = response.json()
                    items = results.get("items", [])
                    
                    for repo in items:
                        repo_full_name = f"{repo['owner']['login']}/{repo['name']}"
                        
                        if repo_full_name not in existing_repos:
                            stars = repo.get("stargazers_count", 0)
                            if stars >= 5000:  # Quality filter
                                discovered.append({
                                    "repository": repo_full_name,
                                    "name": repo["name"],
                                    "stars": stars,
                                    "github_url": repo["html_url"],
                                    "description": repo.get("description", ""),
                                    "language": repo.get("language", ""),
                                    "category": cat_name,
                                    "category_id": cat_id,
                                    "subcategory": "Notable Projects",
                                    "tags": [],
                                    "why_recommended": f"Popular {cat_name} repository with {stars} stars and active development.",
                                    "learning_level": "Intermediate",
                                    "last_updated": repo.get("updated_at"),
                                    "added_date": datetime.now().strftime("%Y-%m-%d"),
                                    "is_active": True
                                })
                                print(f"    Found: {repo_full_name} ({stars} stars)")
                                
                                if len(discovered) >= target:
                                    break
                            else:
                                print(f"    Skipped (low stars): {repo_full_name} ({stars})")
                        else:
                            print(f"    Skipped (exists): {repo_full_name}")
                    
                    if len(discovered) >= target:
                        break
                else:
                    print(f"    Error: {response.status_code}")
                    if response.status_code == 403:
                        print("    Rate limit reached, stopping...")
                        break
                
                # Rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"    Request failed: {e}")
    
    # Save results
    output_data = {
        "discovered_repositories": discovered,
        "metadata": {
            "total_discovered": len(discovered),
            "discovery_date": datetime.now().strftime("%Y-%m-%d"),
            "categories_processed": len(priority_categories),
            "note": "Progressive discovery - limited batch to avoid rate limits"
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*50}")
    print(f"Progressive discovery complete!")
    print(f"Found {len(discovered)} new repositories")
    print(f"Results saved to: {output_file}")
    print(f"{'='*50}")


if __name__ == "__main__":
    token = None
    if len(sys.argv) > 1 and sys.argv[1].startswith("ghp_"):
        token = sys.argv[1]
    
    progressive_discovery(token)