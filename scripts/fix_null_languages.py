#!/usr/bin/env python3
"""
Script pour assigner un language aux repos avec language: null
Assigne le langage principal basé sur le contenu réel du repo
"""

import json
import sys
import os

def infer_language_from_repo(repo):
    """Infère le langage principal basé sur les caractéristiques du repo"""
    name = repo.get('name', '').lower()
    description = repo.get('description', '').lower()
    repository = repo.get('repository', '').lower()
    category = repo.get('category', '').lower()
    tags = repo.get('tags', [])
    
    # Convertir les tags en minuscules pour la recherche
    tags_lower = [tag.lower() for tag in tags]
    
    # Patterns pour identifier les awesome lists (généralement en Markdown)
    awesome_patterns = ['awesome', 'list', 'collection', 'curated', 'resources']
    if any(pattern in name for pattern in awesome_patterns):
        return 'Markdown'
    
    # Patterns pour les outils shell
    shell_patterns = ['cli', 'command', 'terminal', 'shell', 'bash', 'script', 'automation']
    if any(pattern in name for pattern in shell_patterns):
        return 'Shell'
    
    # Patterns pour les langages spécifiques basés sur le nom et description
    language_patterns = {
        'JavaScript': ['javascript', 'js', 'node', 'npm', 'react', 'vue', 'angular', 'express', 'webpack', 'babel'],
        'TypeScript': ['typescript', 'ts', 'angular', 'nest', 'next', 'nuxt'],
        'Python': ['python', 'django', 'flask', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit'],
        'Java': ['java', 'spring', 'maven', 'gradle'],
        'Go': ['go', 'golang', 'kubernetes', 'docker'],
        'Rust': ['rust', 'cargo'],
        'C++': ['cpp', 'c-plus-plus', 'boost'],
        'C#': ['csharp', 'c-sharp', '.net', 'dotnet'],
        'Ruby': ['ruby', 'rails', 'gem'],
        'PHP': ['php', 'laravel', 'symfony', 'wordpress'],
        'Swift': ['swift', 'ios'],
        'Kotlin': ['kotlin', 'android'],
        'Scala': ['scala', 'spark'],
        'R': ['r ', 'rstats', 'tidyverse'],
        'HTML': ['html', 'boilerplate'],
        'CSS': ['css', 'sass', 'less', 'tailwind'],
        'Shell': ['shell', 'bash', 'zsh', 'fish', 'makefile'],
        'Dockerfile': ['dockerfile', 'container'],
        'YAML': ['yaml', 'yml', 'kubernetes', 'helm'],
        'JSON': ['json'],
        'Markdown': ['markdown', 'md', 'documentation', 'readme'],
        'Lua': ['lua'],
        'Haskell': ['haskell'],
        'Elixir': ['elixir', 'phoenix'],
        'Erlang': ['erlang'],
        'Clojure': ['clojure'],
        'F#': ['fsharp', 'f-sharp'],
        'Dart': ['dart', 'flutter'],
        'Julia': ['julia'],
        'MATLAB': ['matlab'],
        'Perl': ['perl'],
        'Objective-C': ['objective-c', 'objc'],
        'SQL': ['sql', 'database', 'mysql', 'postgresql', 'sqlite'],
    }
    
    # Chercher des correspondances dans le nom
    for language, patterns in language_patterns.items():
        for pattern in patterns:
            if pattern in name:
                return language
    
    # Chercher des correspondances dans la description
    for language, patterns in language_patterns.items():
        for pattern in patterns:
            if pattern in description:
                return language
    
    # Chercher des correspondances dans les tags
    for language, patterns in language_patterns.items():
        for pattern in patterns:
            if pattern in tags_lower:
                return language
    
    # Patterns basés sur le repository
    if 'awesome' in repository:
        return 'Markdown'
    
    # Patterns basés sur la catégorie
    category_defaults = {
        'web development': 'JavaScript',
        'data science': 'Python',
        'machine learning': 'Python',
        'devops': 'Shell',
        'cybersecurity': 'Python',
        'mobile development': 'Swift',
        'cloud computing': 'Go',
        'embedded systems': 'C++',
        'developer tools': 'TypeScript',
        'data engineering': 'Python'
    }
    
    if category in category_defaults:
        return category_defaults[category]
    
    # Par défaut, retourner Markdown pour les awesome lists
    return 'Markdown'

def fix_null_languages():
    try:
        # Vérifier que le fichier existe
        if not os.path.exists('data/repositories.json'):
            print(f"Erreur: Le fichier 'data/repositories.json' n'existe pas")
            print(f"   Repertoire courant: {os.getcwd()}")
            sys.exit(1)
        
        # Charger le fichier JSON
        with open('data/repositories.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        repositories = data['repositories']
        
        # Compter les repos avec language: null
        null_language_count = sum(1 for repo in repositories if repo.get('language') is None or repo.get('language') == '')
        print(f"Repos avec language: null: {null_language_count}")
        
        # Assigner un language aux repos concernés
        updated_count = 0
        for repo in repositories:
            if repo.get('language') is None or repo.get('language') == '':
                new_language = infer_language_from_repo(repo)
                repo['language'] = new_language
                updated_count += 1
                if updated_count <= 10:  # Afficher les 10 premiers exemples
                    print(f"[OK] '{repo['name']}': {new_language}")
        
        print(f"\n[OK] Language assigne pour {updated_count} repos")
        
        # Sauvegarder le fichier mis à jour
        with open('data/repositories.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] Fichier repositories.json mis a jour avec succes")
        
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    fix_null_languages()
