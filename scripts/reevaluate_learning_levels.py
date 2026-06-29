#!/usr/bin/env python3
"""
Script pour réévaluer learning_level pour tous les repos
Assure une distribution cohérente: Beginner, Intermediate, Advanced
"""

import json
import sys
import os

def evaluate_learning_level(repo):
    """Évalue le niveau d'apprentissage basé sur les caractéristiques du repo"""
    name = repo.get('name', '').lower()
    description = repo.get('description', '').lower()
    category = repo.get('category', '').lower()
    subcategory = repo.get('subcategory', '').lower()
    tags = repo.get('tags', [])
    stars = repo.get('stars', 0)
    
    # Convertir les tags en minuscules
    tags_lower = [tag.lower() for tag in tags]
    
    # CRITÈRES POUR BEGINNER
    beginner_patterns = [
        # Documentation et tutoriels
        'tutorial', 'guide', 'documentation', 'learn', 'learning', 'course', 'education',
        'beginner', 'intro', 'introduction', 'getting started', '101', 'basics',
        'cheatsheet', 'handbook', 'roadmap', 'awesome', 'curated', 'list',
        
        # Boilerplates et templates
        'boilerplate', 'template', 'starter', 'scaffold', 'seed', 'kit',
        
        # Outils simples
        'tool', 'utility', 'helper', 'plugin', 'extension', 'snippet',
        
        # Sous-catégories Beginner
        'learning resources', 'tutorials', 'documentation'
    ]
    
    # CRITÈRES POUR ADVANCED
    advanced_patterns = [
        # Systèmes distribués
        'distributed', 'kubernetes', 'k8s', 'microservices', 'mesh', 'consensus',
        'raft', 'paxos', 'cluster', 'swarm', 'orchestration',
        
        # Compilateurs et interpréteurs
        'compiler', 'interpreter', 'transpiler', 'parser', 'lexer', 'ast',
        'llvm', 'gcc', 'clang', 'jit', 'runtime',
        
        # Systèmes d'exploitation
        'kernel', 'operating system', 'os', 'filesystem', 'driver', 'bootloader',
        
        # Sécurité offensive
        'exploit', 'payload', 'malware', 'reverse engineering', 'penetration',
        'red team', 'offensive security', 'vulnerability', '0day',
        
        # ML research
        'research', 'paper', 'arxiv', 'transformer', 'attention', 'gnn',
        'reinforcement learning', 'deep learning research', 'neural architecture',
        
        # Base de données avancées
        'database engine', 'storage engine', 'consensus', 'replication',
        'sharding', 'acid', 'cap theorem',
        
        # Crypto et blockchain
        'blockchain', 'cryptocurrency', 'smart contract', 'consensus', 'mining',
        
        # Performance et optimisation avancée
        'performance optimization', 'low latency', 'high frequency', 'hpc',
    ]
    
    # Vérifier d'abord les critères Advanced
    for pattern in advanced_patterns:
        if pattern in name or pattern in description or pattern in subcategory.lower():
            return 'Advanced'
    
    for pattern in advanced_patterns:
        if pattern in tags_lower:
            return 'Advanced'
    
    # Vérifier ensuite les critères Beginner
    for pattern in beginner_patterns:
        if pattern in name or pattern in description or pattern in subcategory.lower():
            return 'Beginner'
    
    for pattern in beginner_patterns:
        if pattern in tags_lower:
            return 'Beginner'
    
    # Cas spécifiques par catégorie
    beginner_categories = {
        'learning resources': True,
        'tutorials': True,
        'documentation': True
    }
    
    if subcategory.lower() in beginner_categories:
        return 'Beginner'
    
    # Patterns spécifiques par langage/technologie
    beginner_tech_patterns = {
        'markdown': ['awesome', 'list', 'collection', 'readme'],
        'html': ['boilerplate', 'template', 'starter'],
        'css': ['framework', 'library'],
    }
    
    for tech, patterns in beginner_tech_patterns.items():
        if tech in name or tech in description:
            for pattern in patterns:
                if pattern in name or pattern in description:
                    return 'Beginner'
    
    # Patterns pour Intermediate (défaut pour la plupart des frameworks/bibliothèques)
    intermediate_patterns = [
        'framework', 'library', 'sdk', 'api', 'rest', 'graphql',
        'web framework', 'backend', 'frontend', 'fullstack',
        'database', 'orm', 'migration',
        'testing', 'ci/cd', 'devops',
        'machine learning', 'deep learning', 'data science',
        'mobile development', 'cloud computing',
    ]
    
    for pattern in intermediate_patterns:
        if pattern in name or pattern in description or pattern in subcategory.lower():
            return 'Intermediate'
    
    # Par défaut, si c'est un projet "notable" ou "contribution", c'est Intermediate
    if subcategory.lower() in ['notable projects', 'contribution projects', 'tools']:
        return 'Intermediate'
    
    # Si on a beaucoup d'étoiles (>50k), c'est probablement Intermediate ou Advanced
    if stars > 50000:
        return 'Intermediate'
    
    # Par défaut: Intermediate
    return 'Intermediate'

def reevaluate_learning_levels():
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
        
        # Compter la distribution actuelle
        current_distribution = {'Beginner': 0, 'Intermediate': 0, 'Advanced': 0}
        for repo in repositories:
            level = repo.get('learning_level', 'Intermediate')
            current_distribution[level] += 1
        
        print(f"Distribution actuelle:")
        print(f"  Beginner: {current_distribution['Beginner']}")
        print(f"  Intermediate: {current_distribution['Intermediate']}")
        print(f"  Advanced: {current_distribution['Advanced']}")
        
        # Réévaluer tous les niveaux
        updated_count = 0
        new_distribution = {'Beginner': 0, 'Intermediate': 0, 'Advanced': 0}
        
        for repo in repositories:
            old_level = repo.get('learning_level', 'Intermediate')
            new_level = evaluate_learning_level(repo)
            
            if old_level != new_level:
                repo['learning_level'] = new_level
                updated_count += 1
                if updated_count <= 15:  # Afficher les 15 premiers changements
                    print(f"[CHANGE] '{repo['name']}': {old_level} -> {new_level}")
            
            new_distribution[new_level] += 1
        
        print(f"\n[OK] Niveau reevalue pour {updated_count} repos")
        print(f"\nNouvelle distribution:")
        print(f"  Beginner: {new_distribution['Beginner']}")
        print(f"  Intermediate: {new_distribution['Intermediate']}")
        print(f"  Advanced: {new_distribution['Advanced']}")
        
        # Sauvegarder le fichier mis à jour
        with open('data/repositories.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n[OK] Fichier repositories.json mis a jour avec succes")
        
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    reevaluate_learning_levels()
