# Maximo Middleware (Public)

Ce dépôt contient une version publique et nettoyée d'un middleware d'intégration
entre SQL Server et un service web Maximo (SOAP).  
La version publique est dénuée de données sensibles et sert de démonstration / template.

## But
- Extraire des données d'une base SQL Server
- Construire un XML conforme (SOAP)
- Poster vers Maximo
- Logger réponses et états

## Exécution (mode test)
1. Copier `config/config.txt.example` → `config/config.txt`
2. Mettre `TEST_MODE=True` pour exécuter sans appeler Maximo
3. Installer dépendances:
```bash
pip install -r requirements.txt
