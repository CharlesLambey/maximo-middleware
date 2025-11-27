# Maximo Middleware – Sage X3 → IBM Maximo

Ce dépôt contient une version publique, nettoyée et totalement sécurisée d’un **middleware d’intégration entre Sage X3 et IBM Maximo**.  
Il permet d’extraire des données depuis la base SQL Server de Sage X3, de construire des messages XML conformes au format SOAP attendu par Maximo, puis de transmettre ces données via un endpoint webservice.

Cette version **ne contient aucune donnée sensible**, aucun identifiant, aucune URL réelle : elle sert de **modèle open-source**, de documentation et de démonstration du fonctionnement général.

---

## 🧩 **Fonctionnalités principales**
- Connexion à la base SQL Server de **Sage X3** (tables, vues, dossiers…).  
- Extraction et transformation des données (ex. : partenaires, fournisseurs…).  
- Génération d’un XML SOAP conforme à l’API IBM Maximo.  
- Envoi du message via HTTP(S) au webservice Maximo.  
- Gestion des journaux :
  - Logs XML envoyés et reçus.
  - Journal de synchronisation.
- Mode **TEST_MODE** permettant l'exécution locale sans appeler Maximo.

---

## 🏛️ **Architecture du projet**
    maximo-middleware/
    ├── src/
    │ └── middleware/
    │ ├── main.py → Point d'entrée
    │ ├── db.py → Connexion SQL + lecture config
    │ ├── xml_builder.py → Construction XML SOAP
    │ ├── soap_client.py → Envoi HTTP/POST vers Maximo
    │ ├── logger.py → Gestion des logs
    │ └── init.py
    ├── config/
    │ └── config.txt.example → Exemple de config sans données
    ├── logs/ → Générés automatiquement
    ├── requirements.txt
    ├── .gitignore
    └── README.md

---

## ⚙️ **Configuration**

Renommez d’abord le fichier :
config/config.txt.example → config/config.txt


Puis complétez les valeurs :

```text
DRIVER=ODBC Driver 18 for SQL Server;
SERVER=SERVER_NAME;
DATABASE=SAGE_X3_DATABASE;
UID=USERNAME;
PWD=PASSWORD;
TrustServerCertificate=yes;

# Endpoint SOAP Maximo (à renseigner en version privée)
MAXIMO_ENDPOINT=https://maximo.example.com/api/soap?wsdl

# Pour exécuter localement sans envoyer à Maximo
TEST_MODE=True
```
## ▶️ Exécution (mode sécurisé – TEST_MODE)
1. Installer les dépendances
```cmd
pip install -r requirements.txt
```
2. Lancer le middleware
```cmd
python -m src.middleware.main
```

En mode TEST_MODE=True :

- Le middleware n’envoie rien à Maximo
- Il simule une réponse "OK"
- Il écrit les logs dans /logs/

Ce mode est idéal pour :

- tester la structure du projet
- vérifier la génération XML
- tester l’extraction SQL Sage X3 localement
- préparer CI/CD

## 🔄 Mode Production (TEST_MODE=False)

Lorsque vous êtes prêts à tester contre Maximo :
 ```cmd
TEST_MODE=False
MAXIMO_ENDPOINT=https://votre_endpoint_maximo/...
```

Le middleware :

- envoie réellement le XML à Maximo
- lit la réponse du webservice
- journalise les envois
- peut être adapté pour mettre à jour Sage X3 (version privée uniquement)


## 🔌 Principe de fonctionnement
1. Source : Sage X3 (SQL Server)

Le middleware lit les données dans les tables :
- Dossiers Sage X3
- Tables partenaires / fournisseurs / tiers (BPCUSTOMER, BPARTNER, etc.)
- Tables personnalisées (ex : YBPS)

2. Transformation

Le middleware convertit chaque enregistrement Sage X3 en :

- dictionnaire Python

- enveloppe XML SOAP structurée

3. Destination : IBM Maximo

Le XML généré est envoyé via :

```html
POST → Maximo SOAP Endpoint (CreateMXL_COMPANIES)
```
La réponse est :

- journalisée

- analysée (OK / Error)

- stockée dans un fichier journalier

## 🧪 Tests et validation

Le projet inclut :

- un mode de simulation
- un XML généré entièrement contrôlable
- un endpoint Maximo fictif en test

Vous pouvez ainsi :

- tester le middleware sans connexion réelle
- inspecter les XML produits
- mocker Maximo lors d’un pipeline CI/CD

🛡️ Sécurité & bonnes pratiques

- config.txt ne doit jamais être versionné.
- Les identifiants Sage X3 doivent être stockés dans un coffre-fort (Vault, Key Vault…).
- En production, activer SSL/TLS strict.
- Ne jamais exposer les logs XML contenant des données réelles.

📌 Limitations de la version publique

Cette version n’exécute pas :
- les mises à jour dans Sage X3
- les webservices Maximo réels
- la gestion des erreurs avancée
- la synchronisation complète

C’est un modèle 100 % safe, destiné :
- à la documentation
- à l’open-source
- à la formation
- à la préparation du dépôt privé
