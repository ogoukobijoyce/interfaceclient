# interfaceclient

Script en ligne de commande pour saisir les informations d'un client, les stocker dans MariaDB et transmettre le nombre de moteurs demandés au futur module de gestion de stock.

## Prérequis

- Python 3.10+
- Accès réseau à la base MariaDB :
  - Hôte : `mariadb-std-7fbcfa043f21.apps.kappsul.su.univ-lorraine.fr`
  - Port : `3306`
  - Utilisateur : `root` (ou un utilisateur disposant des droits nécessaires)

## Installation

```bash
# depuis la racine du dépôt
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Les paramètres de connexion peuvent être modifiés par variables d'environnement :

- `DB_HOST` (par défaut `mariadb-std-7fbcfa043f21.apps.kappsul.su.univ-lorraine.fr`)
- `DB_PORT` (par défaut `3306`)
- `DB_USER` (par défaut `root`)
- `DB_PASSWORD` (**obligatoire, pas de valeur par défaut**)
- `DB_NAME` (par défaut `interfaceclient`)

> Assurez-vous que la base `DB_NAME` existe avant d'exécuter le script. Le script crée uniquement la table `client_orders` si elle est absente.

## Utilisation

Lancer le script et suivre les invites :

```bash
python app.py
```

Pour un usage non interactif, les valeurs peuvent être passées en arguments :

```bash
python app.py \
  --last-name Dupont \
  --first-name Jeanne \
  --role Acheteur \
  --company Exemples SA \
  --email jeanne.dupont@example.com \
  --engines 4
```

Le script :

1. suppose que la base `DB_NAME` existe déjà et crée la table `client_orders` si nécessaire ;
2. enregistre le client et la quantité de moteurs demandée ;
3. transmet la demande au module stock (placeholder pour l'intégration future).
