#!/usr/bin/env python3
"""
Merge discovered repositories into the main database.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Set UTF-8 encoding for Windows compatibility
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def merge_discovered():
    """Merge discovered repositories into main database."""
    base_dir = Path(__file__).parent.parent
    main_file = base_dir / "data" / "repositories.json"
    discovered_file = base_dir / "data" / "progressive_discovered.json"
    
    print("Merging Discovered Repositories")
    print("=" * 50)
    
    # Load main database
    with open(main_file, 'r', encoding='utf-8') as f:
        main_data = json.load(f)
    
    # Load discovered repositories
    with open(discovered_file, 'r', encoding='utf-8') as f:
        discovered_data = json.load(f)
    
    existing_repos = set(repo["repository"] for repo in main_data["repositories"])
    discovered_repos = discovered_data.get("discovered_repositories", [])
    
    print(f"Existing repositories: {len(existing_repos)}")
    print(f"Discovered repositories: {len(discovered_repos)}")
    
    # Add only new repositories
    added_count = 0
    for repo in discovered_repos:
        if repo["repository"] not in existing_repos:
            # Generate proper ID
            cat_id = repo["category_id"]
            repo_name = repo["repository"].split('/')[-1]
            repo["id"] = f"{cat_id}-{repo_name.lower().replace(' ', '-')}"
            
            main_data["repositories"].append(repo)
            existing_repos.add(repo["repository"])
            added_count += 1
            print(f"Added: {repo['repository']} ({repo['stars']} stars)")
    
    # Update metadata
    main_data["metadata"]["total_repositories"] = len(main_data["repositories"])
    main_data["metadata"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    
    # Save updated database
    with open(main_file, 'w', encoding='utf-8') as f:
        json.dump(main_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*50}")
    print(f"Merge complete!")
    print(f"Added {added_count} new repositories")
    print(f"Total repositories: {len(main_data['repositories'])}")
    print(f"{'='*50}")


if __name__ == "__main__":
    merge_discovered()