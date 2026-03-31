# interfaceclient

Script en ligne de commande pour saisir les informations d'un client, les stocker dans MariaDB et transmettre le nombre de moteurs demandés au futur module de gestion de stock.

## Prérequis

- Python 3.10+
- Accès réseau à la base MariaDB :
  - Hôte : `mariadb-std-7fbcfa043f21.apps.kappsul.su.univ-lorraine.fr`
  - Port : `3306`
  - Utilisateur : `root`
  - Mot de passe par défaut : `3edDCAo0Ll` (surchargable via les variables d'environnement ci-dessous)

## Installation

```bash
cd /home/runner/work/interfaceclient/interfaceclient
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Les paramètres de connexion peuvent être modifiés par variables d'environnement :

- `DB_HOST` (par défaut `mariadb-std-7fbcfa043f21.apps.kappsul.su.univ-lorraine.fr`)
- `DB_PORT` (par défaut `3306`)
- `DB_USER` (par défaut `root`)
- `DB_PASSWORD` (par défaut `3edDCAo0Ll`)
- `DB_NAME` (par défaut `interfaceclient`)

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

1. crée la base et la table `client_orders` si elles n'existent pas ;
2. enregistre le client et la quantité de moteurs demandée ;
3. transmet la demande au module stock (placeholder pour l'intégration future).
