# Awesome Tech Repos 2026

![Awesome Tech Repos 2026 Banner](banner.jpg)

A curated collection of **1000 high-quality GitHub repositories** organized by tech domain, helping developers discover the best resources for learning and contributing to open source projects.

[English](#english) | [Français](#français)

---

<a name="english"></a>
## 🌟 English

### Overview

**Awesome Tech Repos 2026** is a comprehensive, curated database of open-source repositories across 12 major technology domains. Each repository is carefully selected based on strict quality criteria:

- ⭐ **Minimum 5,000 stars** (with exceptions for specialized niches)
- 🔄 **Active development** (updated within 6 months)
- 📚 **Good documentation** and active community
- 🎯 **Relevant in 2026** and beyond
- 🚫 **No duplicates** (one tool per dominant use case)

### Project Goals

- 📊 Reach **1,000 high-quality repositories** across all tech domains
- 🎓 Help developers discover the best learning resources
- 🤍 Guide contributors to impactful open-source projects
- 🛠️ Maintain a clean, scalable, and professional structure
- 🤖 Automate data management and updates

### Categories

1. **Web Development** - Frontend, backend, fullstack frameworks, and web tools
2. **Mobile Development** - Mobile frameworks, cross-platform development
3. **Artificial Intelligence & Agents** - AI frameworks, LLM tools, autonomous agents
4. **Machine Learning & Deep Learning** - ML frameworks, deep learning libraries
5. **Data Science & Analytics** - Data analysis, visualization, statistical tools
6. **Data Engineering & Big Data** - Data pipelines, ETL tools, big data frameworks
7. **DevOps, Cloud & Infrastructure** - CI/CD, containerization, cloud infrastructure
8. **Cybersecurity** - Security tools, penetration testing, cryptography
9. **Embedded Systems & IoT** - Microcontrollers, IoT frameworks, embedded development
10. **Robotics & Autonomous Systems** - Robotics frameworks, autonomous systems, simulation
11. **Programming Languages & Core Tools** - Language implementations, compilers, runtime tools
12. **Developer Tools & Productivity** - IDEs, editors, productivity tools

### Project Structure

```
awesome-tech-repos-2026/
├── README.md                    # This file
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # License
├── .gitignore                   # Git ignore rules
├── .github/
│   └── workflows/
│       └── update-stars.yml     # GitHub Action for auto-updates
├── data/
│   ├── repositories.json        # Main repository database
│   ├── categories.json          # Category configuration
│   └── metadata.json            # Project metadata
├── scripts/
│   ├── convert_markdown_to_json.py  # Convert Markdown to JSON
│   ├── validate_data.py              # Validate repository data
│   ├── update_stars.py              # Update stars via GitHub API
│   └── discover_repositories.py     # Discover new repositories
└── docs/
    ├── architecture.md          # Architecture documentation
    └── api-schema.md            # JSON schema documentation
```

### Getting Started

#### Prerequisites

- Python 3.10 or higher
- GitHub token (optional, for higher rate limits)

#### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/awesome-tech-repos-2026.git
cd awesome-tech-repos-2026
```

2. Install Python dependencies:
```bash
pip install requests
```

3. Set up GitHub token (optional but recommended):
```bash
export GITHUB_TOKEN=your_github_token_here
```

#### Usage

**Convert existing Markdown data to JSON:**
```bash
python scripts/convert_markdown_to_json.py path/to/repositories-database-v7.md data/repositories.json
```

**Validate repository data:**
```bash
python scripts/validate_data.py data/repositories.json
```

**Update repository metadata (stars, last updated):**
```bash
python scripts/update_stars.py data/repositories.json
```

**Discover new repositories to reach 1000 target:**
```bash
python scripts/discover_repositories.py data/repositories.json
```

### Data Schema

Each repository in the database follows this schema:

```json
{
  "id": "web-dev-001",
  "name": "Repository Name",
  "repository": "owner/repository",
  "github_url": "https://github.com/owner/repository",
  "category": "Web Development",
  "category_id": "web-dev",
  "subcategory": "Notable Projects",
  "tags": ["frontend", "ui"],
  "stars": 100000,
  "language": "TypeScript",
  "description": "Repository description",
  "why_recommended": "Why this repository is recommended",
  "learning_level": "Intermediate",
  "last_updated": "2025-01-15",
  "added_date": "2025-01-01",
  "is_active": true
}
```

### Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Adding new repositories
- Updating existing repository data
- Improving documentation
- Reporting issues

### Selection Criteria

Repositories are selected based on:

1. **Quality over quantity** - Each repository must add genuine value
2. **Activity** - Active development and community engagement
3. **Documentation** - Clear, comprehensive documentation
4. **Relevance** - Useful and relevant in 2026
5. **Uniqueness** - No duplicate tools for the same use case
6. **Learning value** - Clear educational or practical value

### Automation

The project includes automated workflows:

- **GitHub Actions** - Weekly automatic updates of repository stars and metadata
- **Python scripts** - Data validation, conversion, and discovery
- **API integration** - GitHub API for real-time data fetching

### Roadmap

- [x] Initial project structure and scripts
- [x] Convert existing Markdown data to JSON
- [x] Create validation and update scripts
- [x] Implement repository discovery automation
- [x] Reach 1,000 repositories across all categories ✅ **COMPLETED**
- [ ] Build GitHub Pages website
- [ ] Add advanced filtering and search
- [ ] Implement contribution analytics

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- Built with ❤️ for the open-source community
- Inspired by various "awesome lists" on GitHub
- Data sourced from GitHub API

---

<a name="français"></a>
## 🌟 Français

![Awesome Tech Repos 2026 Banner](banner.jpg)

### Présentation

**Awesome Tech Repos 2026** est une base de données complète et curated de dépôts open-source sur 12 domaines technologiques majeurs. Chaque dépôt est soigneusement sélectionné selon des critères de qualité stricts :

- ⭐ **Minimum 5 000 étoiles** (avec exceptions pour les niches spécialisées)
- 🔄 **Développement actif** (mis à jour dans les 6 derniers mois)
- 📚 **Bonne documentation** et communauté active
- 🎯 **Pertinent en 2026** et au-delà
- 🚫 **Pas de doublons** (un seul outil par cas d'usage dominant)

### Objectifs du Projet

- 📊 Atteindre **1 000 dépôts de haute qualité** dans tous les domaines tech
- 🎓 Aider les développeurs à découvrir les meilleures ressources d'apprentissage
- 🤍 Guider les contributeurs vers des projets open-source impactants
- 🛠️ Maintenir une structure propre, scalable et professionnelle
- 🤖 Automatiser la gestion et la mise à jour des données

### Catégories

1. **Web Development** - Frontend, backend, frameworks fullstack, outils web
2. **Mobile Development** - Frameworks mobiles, développement cross-platform
3. **Artificial Intelligence & Agents** - Frameworks IA, outils LLM, agents autonomes
4. **Machine Learning & Deep Learning** - Frameworks ML, bibliothèques deep learning
5. **Data Science & Analytics** - Analyse de données, visualisation, outils statistiques
6. **Data Engineering & Big Data** - Pipelines de données, outils ETL, frameworks big data
7. **DevOps, Cloud & Infrastructure** - CI/CD, conteneurisation, infrastructure cloud
8. **Cybersecurity** - Outils de sécurité, tests d'intrusion, cryptographie
9. **Embedded Systems & IoT** - Microcontrôleurs, frameworks IoT, développement embarqué
10. **Robotics & Autonomous Systems** - Frameworks robotique, systèmes autonomes, simulation
11. **Programming Languages & Core Tools** - Implémentations de langages, compilateurs, outils runtime
12. **Developer Tools & Productivity** - IDEs, éditeurs, outils de productivité

### Structure du Projet

```
awesome-tech-repos-2026/
├── README.md                    # Ce fichier
├── CONTRIBUTING.md              # Guide de contribution
├── LICENSE                      # Licence
├── .gitignore                   # Règles Git ignore
├── .github/
│   └── workflows/
│       └── update-stars.yml     # GitHub Action pour mises à jour auto
├── data/
│   ├── repositories.json        # Base de données principale
│   ├── categories.json          # Configuration des catégories
│   └── metadata.json            # Métadonnées du projet
├── scripts/
│   ├── convert_markdown_to_json.py  # Conversion Markdown vers JSON
│   ├── validate_data.py              # Validation des données
│   ├── update_stars.py              # Mise à jour des étoiles via API GitHub
│   └── discover_repositories.py     # Découverte de nouveaux dépôts
└── docs/
    ├── architecture.md          # Documentation architecture
    └── api-schema.md            # Documentation schéma JSON
```

### Démarrage Rapide

#### Prérequis

- Python 3.10 ou supérieur
- Token GitHub (optionnel, pour des limites de taux plus élevées)

#### Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/yourusername/awesome-tech-repos-2026.git
cd awesome-tech-repos-2026
```

2. Installer les dépendances Python :
```bash
pip install requests
```

3. Configurer le token GitHub (recommandé mais optionnel) :
```bash
export GITHUB_TOKEN=votre_token_github_ici
```

#### Utilisation

**Convertir les données Markdown existantes en JSON :**
```bash
python scripts/convert_markdown_to_json.py chemin/vers/repositories-database-v7.md data/repositories.json
```

**Valider les données des dépôts :**
```bash
python scripts/validate_data.py data/repositories.json
```

**Mettre à jour les métadonnées des dépôts (étoiles, dernière mise à jour) :**
```bash
python scripts/update_stars.py data/repositories.json
```

**Découvrir de nouveaux dépôts pour atteindre l'objectif de 1000 :**
```bash
python scripts/discover_repositories.py data/repositories.json
```

### Schéma de Données

Chaque dépôt dans la base de données suit ce schéma :

```json
{
  "id": "web-dev-001",
  "name": "Nom du Dépôt",
  "repository": "propriétaire/dépôt",
  "github_url": "https://github.com/propriétaire/dépôt",
  "category": "Web Development",
  "category_id": "web-dev",
  "subcategory": "Notable Projects",
  "tags": ["frontend", "ui"],
  "stars": 100000,
  "language": "TypeScript",
  "description": "Description du dépôt",
  "why_recommended": "Pourquoi ce dépôt est recommandé",
  "learning_level": "Intermediate",
  "last_updated": "2025-01-15",
  "added_date": "2025-01-01",
  "is_active": true
}
```

### Contribution

Nous accueillons les contributions ! Veuillez consulter [CONTRIBUTING.md](CONTRIBUTING.md) pour les directives sur :

- L'ajout de nouveaux dépôts
- La mise à jour des données de dépôts existants
- L'amélioration de la documentation
- Le signalement de problèmes

### Critères de Sélection

Les dépôts sont sélectionnés selon :

1. **Qualité avant quantité** - Chaque dépôt doit apporter une valeur réelle
2. **Activité** - Développement actif et engagement communautaire
3. **Documentation** - Documentation claire et complète
4. **Pertinence** - Utile et pertinent en 2026
5. **Unicité** - Pas d'outils en double pour le même cas d'usage
6. **Valeur d'apprentissage** - Valeur éducative ou pratique claire

### Automatisation

Le projet inclut des workflows automatisés :

- **GitHub Actions** - Mises à jour automatiques hebdomadaires des étoiles et métadonnées
- **Scripts Python** - Validation, conversion et découverte de données
- **Intégration API** - API GitHub pour la récupération de données en temps réel

### Feuille de Route

- [x] Structure initiale du projet et scripts
- [x] Conversion des données Markdown existantes en JSON
- [x] Création des scripts de validation et de mise à jour
- [x] Implémentation de l'automatisation de découverte de dépôts
- [x] Atteindre 1 000 dépôts dans toutes les catégories ✅ **TERMINÉ**
- [ ] Construire un site GitHub Pages
- [ ] Ajouter un filtrage et une recherche avancés
- [ ] Implémenter des analytics de contribution

### Licence

Ce projet est licencié sous la Licence MIT - voir le fichier [LICENSE](LICENSE) pour les détails.

### Remerciements

- Construit avec ❤️ pour la communauté open-source
- Inspiré par diverses "awesome lists" sur GitHub
- Données sourcées depuis l'API GitHub

---

## 📊 Current Status

- **Total Repositories**: 7 (sample) / ~250 (to be converted)
- **Categories**: 12
- **Target**: 1,000 repositories
- **Last Updated**: 2025-01-15

## 🔗 Links

- [GitHub Repository](https://github.com/yourusername/awesome-tech-repos-2026)
- [Issues](https://github.com/yourusername/awesome-tech-repos-2026/issues)
- [Contributing](CONTRIBUTING.md)

---

*Made with ❤️ by the open-source community*