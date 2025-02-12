# Hacker News Scraper

Un script Python qui scrape les articles de Hacker News et les stocke dans une base SQLite et un fichier CSV.

## Fonctionnalités
- Récupération des articles populaires de Hacker News
- Stockage en **SQLite** et **CSV**
- Exécution automatique **toutes les minutes** avec `schedule`
- Journalisation des événements (`scraper.log`)

## Installation
1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/Younes210701/hackernews-scraper.git
   cd hackernews-scraper
2. **Installer les dépendances** :
   ```bash
    pip install -r requirements.txt
3. **Lancer le scraper** :
   ```bash
   python scraper.py
4. **Lancer le scheduler (scraping automatique)** :
   ```bash
   python scheduler.py

