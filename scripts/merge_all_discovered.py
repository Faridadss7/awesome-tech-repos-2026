#!/usr/bin/env python3
"""
Merge all discovered repository files into the main database.
"""

import json
import sys
import glob
from pathlib import Path
from datetime import datetime

# Set UTF-8 encoding for Windows compatibility
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def merge_all_discovered():
    """Merge all discovered repository files into main database."""
    base_dir = Path(__file__).parent.parent
    main_file = base_dir / "data" / "repositories.json"
    data_dir = base_dir / "data"
    
    print("Merging All Discovered Repositories")
    print("=" * 50)
    
    # Load main database
    with open(main_file, 'r', encoding='utf-8') as f:
        main_data = json.load(f)
    
    existing_repos = set(repo["repository"] for repo in main_data["repositories"])
    print(f"Existing repositories: {len(existing_repos)}")
    
    # Find all discovered files
    discovered_files = list(data_dir.glob("discovered_*.json"))
    print(f"Found {len(discovered_files)} discovery files")
    
    total_added = 0
    for discovered_file in discovered_files:
        print(f"\nProcessing: {discovered_file.name}")
        
        with open(discovered_file, 'r', encoding='utf-8') as f:
            discovered_data = json.load(f)
        
        discovered_repos = discovered_data.get("discovered_repositories", [])
        print(f"  Repositories in file: {len(discovered_repos)}")
        
        added_in_file = 0
        for repo in discovered_repos:
            if repo["repository"] not in existing_repos:
                # Generate proper ID
                cat_id = repo["category_id"]
                repo_name = repo["repository"].split('/')[-1]
                repo["id"] = f"{cat_id}-{repo_name.lower().replace(' ', '-')}"
                
                main_data["repositories"].append(repo)
                existing_repos.add(repo["repository"])
                added_in_file += 1
                total_added += 1
                print(f"    Added: {repo['repository']} ({repo['stars']} stars)")
        
        print(f"  Added from this file: {added_in_file}")
    
    # Update metadata
    main_data["metadata"]["total_repositories"] = len(main_data["repositories"])
    main_data["metadata"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    
    # Save updated database
    with open(main_file, 'w', encoding='utf-8') as f:
        json.dump(main_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*50}")
    print(f"Merge complete!")
    print(f"Total repositories added: {total_added}")
    print(f"Total repositories in database: {len(main_data['repositories'])}")
    print(f"{'='*50}")


if __name__ == "__main__":
    merge_all_discovered()