#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger les IDs dupliqués dans repositories.json
Génère des IDs uniques en ajoutant des suffixes numériques (-2, -3, etc.)
"""

import json
import sys
import os
from collections import Counter

# Set UTF-8 encoding for output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def fix_duplicate_ids():
    try:
        # Get the script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, '..', 'data', 'repositories.json')
        
        # Vérifier que le fichier existe
        if not os.path.exists(json_path):
            print(f"ERROR: Le fichier 'data/repositories.json' n'existe pas")
            print(f"   Chemin recherche: {json_path}")
            print(f"   Repertoire courant: {os.getcwd()}")
            sys.exit(1)
        
        # Charger le fichier JSON
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        repositories = data['repositories']
        
        # Liste des IDs dupliqués identifiés
        duplicate_ids = [
            'web-dev-react',
            'web-dev-fastapi',
            'dev-tools-cli',
            'data-science-superset',
            'web-dev-core',
            'web-dev-kit',
            'mobile-dev-react-native',
            'ai-agents-whisper',
            'data-science-altair',
            'embedded-iot-firmware',
            'data-engineering-great_expectations',
            'web-dev-astro',
            'embedded-iot-arduino'
        ]
        
        # Compter les occurrences de chaque ID
        id_counts = Counter(repo['id'] for repo in repositories)
        
        # Dictionnaire pour suivre les comptes actuels
        current_counts = {}
        
        # Corriger les IDs dupliqués
        for repo in repositories:
            original_id = repo['id']
            
            if original_id in duplicate_ids and id_counts[original_id] > 1:
                # Initialiser le compteur pour cet ID
                if original_id not in current_counts:
                    current_counts[original_id] = 1
                
                # Si c'est la première occurrence, garder l'ID original
                if current_counts[original_id] == 1:
                    current_counts[original_id] += 1
                else:
                    # Ajouter un suffixe numerique
                    new_id = f"{original_id}-{current_counts[original_id]}"
                    repo['id'] = new_id
                    current_counts[original_id] += 1
                    print(f"Fixed duplicate ID: {original_id} -> {new_id}")
        
        # Sauvegarder le fichier corrige
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\nSuccessfully updated repositories.json")

        # Verifier qu'il n'y a plus de doublons
        updated_ids = [repo['id'] for repo in repositories]
        updated_counts = Counter(updated_ids)
        remaining_duplicates = {id: count for id, count in updated_counts.items() if count > 1}

        if remaining_duplicates:
            print(f"\nWARNING: Remaining duplicate IDs:")
            for id, count in remaining_duplicates.items():
                print(f"   - {id}: {count} occurrences")
        else:
            print(f"\nAll IDs are now unique")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    fix_duplicate_ids()
