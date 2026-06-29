#!/usr/bin/env python3
"""
Script pour générer des tags pour les repos avec des tags vides
Génère 2 à 4 tags pertinents basés sur le name, description, category et language
"""

import json
import sys
import os
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def generate_tags_from_repo(repo):
    """Génère des tags pertinents pour un repo donné"""
    tags = []
    
    name = (repo.get('name') or '').lower()
    description = (repo.get('description') or '').lower()
    category = (repo.get('category') or '').lower()
    category_id = (repo.get('category_id') or '').lower()
    language = (repo.get('language') or '').lower()
    subcategory = (repo.get('subcategory') or '').lower()
    
    # Mapping des catégories vers des tags génériques
    category_tags = {
        'web development': ['web', 'web-development'],
        'web-dev': ['web', 'web-development'],
        'data science': ['data-science', 'analytics'],
        'data-science': ['data-science', 'analytics'],
        'machine learning': ['machine-learning', 'ml', 'ai'],
        'ml': ['machine-learning', 'ml', 'ai'],
        'ai': ['artificial-intelligence', 'ai'],
        'ai-agents': ['ai', 'agents', 'automation'],
        'devops': ['devops', 'infrastructure'],
        'cybersecurity': ['security', 'cybersecurity'],
        'cyber-security': ['security', 'cybersecurity'],
        'mobile development': ['mobile', 'mobile-development'],
        'mobile-dev': ['mobile', 'mobile-development'],
        'cloud computing': ['cloud', 'cloud-computing'],
        'cloud': ['cloud', 'cloud-computing'],
        'embedded systems': ['embedded', 'iot'],
        'embedded-iot': ['embedded', 'iot'],
        'developer tools': ['developer-tools', 'productivity'],
        'dev-tools': ['developer-tools', 'productivity'],
        'data engineering': ['data-engineering', 'etl'],
        'data-engineering': ['data-engineering', 'etl']
    }
    
    # Ajouter des tags basés sur la catégorie
    if category in category_tags:
        tags.extend(category_tags[category])
    elif category_id in category_tags:
        tags.extend(category_tags[category_id])
    
    # Tags basés sur le langage
    language_tags = {
        'javascript': ['javascript', 'js'],
        'typescript': ['typescript', 'ts'],
        'python': ['python'],
        'java': ['java'],
        'go': ['golang', 'go'],
        'rust': ['rust'],
        'c++': ['cpp', 'c-plus-plus'],
        'c#': ['csharp', 'c-sharp'],
        'ruby': ['ruby'],
        'php': ['php'],
        'swift': ['swift'],
        'kotlin': ['kotlin'],
        'shell': ['shell', 'bash'],
        'markdown': ['markdown', 'documentation'],
        'html': ['html', 'frontend'],
        'css': ['css', 'frontend']
    }
    
    if language in language_tags:
        tags.extend(language_tags[language])
    
    # Tags basés sur la sous-catégorie
    subcategory_mapping = {
        'learning resources': ['learning', 'education', 'tutorials'],
        'notable projects': ['popular', 'featured'],
        'contribution projects': ['contribution', 'open-source'],
        'tools': ['tools', 'utilities'],
        'frameworks': ['framework', 'library'],
        'security tools': ['security', 'tools']
    }
    
    if subcategory in subcategory_mapping:
        tags.extend(subcategory_mapping[subcategory])
    
    # Tags basés sur des mots-clés dans le nom et la description
    keyword_mapping = {
        'api': ['api', 'rest'],
        'framework': ['framework'],
        'library': ['library'],
        'cli': ['cli', 'command-line'],
        'tool': ['tools'],
        'automation': ['automation'],
        'testing': ['testing', 'test'],
        'monitoring': ['monitoring'],
        'docker': ['docker', 'containers'],
        'kubernetes': ['kubernetes', 'k8s'],
        'database': ['database', 'db'],
        'backend': ['backend', 'server'],
        'frontend': ['frontend', 'client'],
        'fullstack': ['fullstack', 'full-stack'],
        'react': ['react', 'reactjs'],
        'vue': ['vue', 'vuejs'],
        'angular': ['angular'],
        'node': ['nodejs', 'node'],
        'django': ['django'],
        'flask': ['flask'],
        'tensorflow': ['tensorflow', 'deep-learning'],
        'pytorch': ['pytorch', 'deep-learning'],
        'security': ['security'],
        'network': ['networking'],
        'ai': ['ai', 'artificial-intelligence'],
        'ml': ['machine-learning', 'ml'],
        'data': ['data'],
        'analytics': ['analytics'],
        'visualization': ['visualization', 'charts'],
        'ui': ['ui', 'user-interface'],
        'ux': ['ux', 'user-experience'],
        'design': ['design'],
        'mobile': ['mobile'],
        'android': ['android'],
        'ios': ['ios'],
        'web': ['web'],
        'cloud': ['cloud'],
        'devops': ['devops'],
        'git': ['git', 'version-control'],
        'github': ['github'],
        'gitlab': ['gitlab'],
        'database': ['database'],
        'sql': ['sql'],
        'nosql': ['nosql'],
        'mongodb': ['mongodb'],
        'postgresql': ['postgresql'],
        'mysql': ['mysql'],
        'redis': ['redis'],
        'elasticsearch': ['elasticsearch', 'search'],
        'graphql': ['graphql'],
        'grpc': ['grpc'],
        'microservices': ['microservices'],
        'serverless': ['serverless'],
        'blockchain': ['blockchain'],
        'crypto': ['cryptocurrency'],
        'iot': ['iot', 'internet-of-things'],
        'embedded': ['embedded'],
        'arduino': ['arduino'],
        'raspberry': ['raspberry-pi'],
        'linux': ['linux'],
        'windows': ['windows'],
        'macos': ['macos'],
        'cross-platform': ['cross-platform']
    }
    
    # Chercher des mots-clés dans le nom
    for keyword, keyword_tags in keyword_mapping.items():
        if keyword in name:
            tags.extend(keyword_tags)
    
    # Chercher des mots-clés dans la description
    for keyword, keyword_tags in keyword_mapping.items():
        if keyword in description:
            tags.extend(keyword_tags)
    
    # Éliminer les doublons tout en préservant l'ordre
    seen = set()
    unique_tags = []
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            unique_tags.append(tag)
    
    # Limiter à 2-4 tags
    if len(unique_tags) > 4:
        unique_tags = unique_tags[:4]
    elif len(unique_tags) < 2:
        # Si on a moins de 2 tags, ajouter des tags génériques
        if 'web' not in unique_tags and 'web' in category:
            unique_tags.append('web')
        if 'data' not in unique_tags and 'data' in category:
            unique_tags.append('data')
        if 'ai' not in unique_tags and 'ai' in category:
            unique_tags.append('ai')
        if 'development' not in unique_tags and 'development' in category:
            unique_tags.append('development')
    
    return unique_tags

def generate_tags_for_empty_repos():
    try:
        # Change to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Go to parent directory (project root)
        os.chdir('..')
        
        data_file = 'data/repositories.json'
        
        # Verifier que le fichier existe
        if not os.path.exists(data_file):
            print(f"ERROR: Le fichier '{data_file}' n'existe pas")
            print(f"   Repertoire courant: {os.getcwd()}")
            sys.exit(1)
        
        # Charger le fichier JSON
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        repositories = data['repositories']
        
        # Compter les repos avec tags vides
        empty_tags_count = sum(1 for repo in repositories if not repo.get('tags') or repo.get('tags') == [])
        print(f"Repos with empty tags: {empty_tags_count}")

        # Generer des tags pour les repos avec tags vides
        updated_count = 0
        for repo in repositories:
            if not repo.get('tags') or repo.get('tags') == []:
                new_tags = generate_tags_from_repo(repo)
                repo['tags'] = new_tags
                updated_count += 1
                if updated_count <= 10:  # Afficher les 10 premiers exemples
                    print(f"Generated tags for '{repo['name']}': {new_tags}")

        print(f"\nGenerated tags for {updated_count} repos")

        # Sauvegarder le fichier mis a jour
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Successfully updated repositories.json")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    generate_tags_for_empty_repos()
