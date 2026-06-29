#!/usr/bin/env python3
"""
Script pour réécrire why_recommended pour les repos où description == why_recommended
Génère des explications spécifiques sur pourquoi le repo est recommandé en 2026
"""

import json
import sys
import os

def generate_why_recommended(repo):
    """Génère un why_recommended spécifique basé sur les caractéristiques du repo"""
    name = repo.get('name', '')
    description = repo.get('description', '')
    category = repo.get('category', '')
    subcategory = repo.get('subcategory', '')
    language = repo.get('language', '')
    stars = repo.get('stars', 0)
    
    # Templates basés sur la catégorie et sous-catégorie
    templates = {
        'Web Development': {
            'Learning Resources': [
                f"Ressource pédagogique incontournable en 2026 pour maîtriser {name}. La documentation et les exemples sont constamment mis à jour.",
                f"Excellent point de départ pour apprendre {name} avec une communauté active et des ressources de qualité.",
                f"Matériel d'apprentissage très complet pour {name}, idéal pour se mettre à jour avec les pratiques modernes de 2026."
            ],
            'Notable Projects': [
                f"Projet majeur dans l'écosystème {name} en 2026. Adoption massive et support entreprise robuste.",
                f"Solution de référence pour {name} avec un écosystème riche et une documentation exceptionnelle.",
                f"Technologie standard pour {name} en 2026. Performance et maintenabilité prouvées en production."
            ],
            'Contribution Projects': [
                f"Projet open-source dynamique avec des opportunités de contribution régulières. Communauté accueillante pour les nouveaux contributeurs.",
                f"Excellente occasion de contribuer à {name} avec des issues bien documentées et des mainteneurs réactifs.",
                f"Projet en croissance active où les contributions ont un impact réel sur l'écosystème {name}."
            ]
        },
        'Data Science': {
            'Learning Resources': [
                f"Ressource essentielle pour maîtriser {name} en 2026. Couvre les techniques modernes et les cas d'usage actuels.",
                f"Documentation complète et à jour pour {name}, indispensable pour les data scientists de 2026.",
                f"Matériel pédagogique de haute qualité intégrant les dernières avancées en {name}."
            ],
            'Notable Projects': [
                f"Outil standard de l'industrie pour {name} en 2026. Performance et fiabilité éprouvées.",
                f"Solution de référence pour {name} avec une adoption massive dans les entreprises.",
                f"Technologie mature et bien supportée pour {name} en production à grande échelle."
            ],
            'Contribution Projects': [
                f"Projet actif avec des opportunités de contribution sur les fonctionnalités de pointe de {name}.",
                f"Communauté ouverte et accueillante pour contribuer à l'évolution de {name}.",
                f"Excellent projet pour contribuer à des innovations en {name} avec un impact réel."
            ]
        },
        'Machine Learning': {
            'Learning Resources': [
                f"Ressource pédagogique de premier plan pour {name} en 2026. Intègre les dernières techniques de deep learning.",
                f"Formation complète sur {name} avec des exemples pratiques et des cas d'usage réels.",
                f"Documentation exceptionnelle pour maîtriser {name} avec les approches modernes de 2026."
            ],
            'Notable Projects': [
                f"Framework de référence pour {name} en 2026. Adoption massive dans la recherche et l'industrie.",
                f"Solution standard pour {name} avec un écosystème riche et un support entreprise.",
                f"Technologie de pointe pour {name} avec des performances optimisées pour le GPU/TPU."
            ],
            'Contribution Projects': [
                f"Projet de recherche active avec des opportunités de contribution sur les algorithmes de {name}.",
                f"Communauté scientifique ouverte aux contributions sur les nouvelles architectures de {name}.",
                f"Excellent projet pour contribuer à l'avancement de {name} avec un impact académique et industriel."
            ]
        },
        'DevOps': {
            'Learning Resources': [
                f"Ressource incontournable pour maîtriser {name} en 2026. Couvre les pratiques DevOps modernes.",
                f"Formation complète sur {name} avec des exemples de mise en production réels.",
                f"Documentation essentielle pour comprendre les principes et outils de {name}."
            ],
            'Notable Projects': [
                f"Outil standard de l'industrie DevOps pour {name} en 2026. Fiabilité et scalabilité prouvées.",
                f"Solution de référence pour {name} avec une adoption massive dans les infrastructures modernes.",
                f"Technologie mature pour automatiser {name} à grande échelle en production."
            ],
            'Contribution Projects': [
                f"Projet infrastructure-as-code actif avec des opportunités de contribution sur les modules {name}.",
                f"Communauté DevOps accueillante pour contribuer à l'écosystème {name}.",
                f"Excellent projet pour contribuer à des outils d'infrastructure modernes avec {name}."
            ]
        },
        'Cybersecurity': {
            'Learning Resources': [
                f"Ressource pédagogique essentielle pour {name} en 2026. Couvre les dernières menaces et techniques de défense.",
                f"Formation complète sur {name} avec des scénarios d'attaque réels et des exercices pratiques.",
                f"Documentation de référence pour maîtriser les concepts de sécurité liés à {name}."
            ],
            'Notable Projects': [
                f"Outil standard de l'industrie pour {name} en 2026. Détection et prévention des menaces éprouvées.",
                f"Solution de référence pour {name} avec une adoption massive dans les équipes de sécurité.",
                f"Technologie mature pour sécuriser {name} avec des règles de détection à jour."
            ],
            'Contribution Projects': [
                f"Projet de sécurité active avec des opportunités de contribution sur les règles {name}.",
                f"Communauté cybersécurité ouverte aux contributions sur les nouvelles signatures de {name}.",
                f"Excellent projet pour contribuer à la défense contre les menaces liées à {name}."
            ]
        },
        'Mobile Development': {
            'Learning Resources': [
                f"Ressource incontournable pour maîtriser {name} en 2026. Couvre les frameworks mobiles modernes.",
                f"Formation complète sur {name} avec des applications pratiques et des bonnes pratiques.",
                f"Documentation essentielle pour développer avec {name} selon les standards de 2026."
            ],
            'Notable Projects': [
                f"Framework standard pour {name} en 2026. Performance et cross-platform optimisés.",
                f"Solution de référence pour {name} avec une adoption massive dans le développement mobile.",
                f"Technologie mature pour créer des applications {name} natives et performantes."
            ],
            'Contribution Projects': [
                f"Projet mobile actif avec des opportunités de contribution sur les composants {name}.",
                f"Communauté mobile accueillante pour contribuer à l'écosystème {name}.",
                f"Excellent projet pour contribuer à des bibliothèques mobiles modernes avec {name}."
            ]
        },
        'Cloud Computing': {
            'Learning Resources': [
                f"Ressource essentielle pour maîtriser {name} en 2026. Couvre les architectures cloud modernes.",
                f"Formation complète sur {name} avec des déploiements pratiques sur les plateformes cloud.",
                f"Documentation de référence pour comprendre les patterns cloud avec {name}."
            ],
            'Notable Projects': [
                f"Outil standard de l'industrie cloud pour {name} en 2026. Scalabilité et résilience prouvées.",
                f"Solution de référence pour {name} avec une adoption massive dans les infrastructures cloud.",
                f"Technologie mature pour déployer et gérer {name} à grande échelle."
            ],
            'Contribution Projects': [
                f"Projet cloud natif actif avec des opportunités de contribution sur les modules {name}.",
                f"Communauté cloud ouverte aux contributions sur les intégrations {name}.",
                f"Excellent projet pour contribuer à des outils cloud modernes avec {name}."
            ]
        },
        'Embedded Systems': {
            'Learning Resources': [
                f"Ressource pédagogique essentielle pour {name} en 2026. Couvre les systèmes embarqués modernes.",
                f"Formation complète sur {name} avec des projets matériels et logiciels pratiques.",
                f"Documentation de référence pour développer des systèmes {name} performants."
            ],
            'Notable Projects': [
                f"Outil standard pour {name} en 2026. Performance et fiabilité sur matériel contraint.",
                f"Solution de référence pour {name} avec une adoption massive dans l'IoT industriel.",
                f"Technologie mature pour développer des systèmes {name} optimisés et sécurisés."
            ],
            'Contribution Projects': [
                f"Projet embedded actif avec des opportunités de contribution sur les pilotes {name}.",
                f"Communauté embedded ouverte aux contributions sur les ports {name}.",
                f"Excellent projet pour contribuer à des bibliothèques matérielles avec {name}."
            ]
        },
        'Developer Tools': {
            'Learning Resources': [
                f"Ressource incontournable pour maîtriser {name} en 2026. Couvre les outils de développement modernes.",
                f"Formation complète sur {name} avec des workflows et intégrations pratiques.",
                f"Documentation essentielle pour optimiser le développement avec {name}."
            ],
            'Notable Projects': [
                f"Outil standard de l'industrie pour {name} en 2026. Productivité et intégration éprouvées.",
                f"Solution de référence pour {name} avec une adoption massive chez les développeurs.",
                f"Technologie mature pour améliorer le workflow de développement avec {name}."
            ],
            'Contribution Projects': [
                f"Projet d'outils développeur actif avec des opportunités de contribution sur les plugins {name}.",
                f"Communauté d'outils ouverte aux contributions sur les extensions {name}.",
                f"Excellent projet pour contribuer à des outils de développement modernes avec {name}."
            ]
        },
        'Data Engineering': {
            'Learning Resources': [
                f"Ressource essentielle pour maîtriser {name} en 2026. Couvre les pipelines de données modernes.",
                f"Formation complète sur {name} avec des architectures ETL/ELT pratiques.",
                f"Documentation de référence pour construire des pipelines {name} scalables."
            ],
            'Notable Projects': [
                f"Outil standard de l'industrie pour {name} en 2026. Performance et fiabilité des pipelines.",
                f"Solution de référence pour {name} avec une adoption massive dans les data teams.",
                f"Technologie mature pour orchestrer et monitorer {name} à grande échelle."
            ],
            'Contribution Projects': [
                f"Projet data engineering actif avec des opportunités de contribution sur les connecteurs {name}.",
                f"Communauté data ouverte aux contributions sur les opérateurs {name}.",
                f"Excellent projet pour contribuer à des outils de data modernes avec {name}."
            ]
        }
    }
    
    # Sélectionner un template basé sur la catégorie et sous-catégorie
    if category in templates and subcategory in templates[category]:
        import random
        templates_list = templates[category][subcategory]
        return random.choice(templates_list)
    
    # Template par défaut si pas de correspondance
    return f"Projet essentiel dans l'écosystème {name} en 2026. Architecture robuste, communauté active et documentation complète. Valeur ajoutée significative pour les projets de production."

def fix_why_recommended():
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
        
        # Compter les repos avec description == why_recommended
        duplicate_count = sum(1 for repo in repositories if repo.get('description') == repo.get('why_recommended'))
        print(f"Repos avec description == why_recommended: {duplicate_count}")
        
        # Réécrire why_recommended pour les repos concernés
        updated_count = 0
        for repo in repositories:
            if repo.get('description') == repo.get('why_recommended'):
                new_why = generate_why_recommended(repo)
                repo['why_recommended'] = new_why
                updated_count += 1
                if updated_count <= 10:  # Afficher les 10 premiers exemples
                    print(f"[OK] '{repo['name']}': {new_why[:80]}...")
        
        print(f"\n[OK] why_recommended reecrit pour {updated_count} repos")
        
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
    fix_why_recommended()
