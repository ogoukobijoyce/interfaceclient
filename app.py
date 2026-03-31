import argparse
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional

import mysql.connector
from mysql.connector import errorcode


DEFAULT_DB_CONFIG = {
    "host": os.environ.get(
        "DB_HOST", "mariadb-std-7fbcfa043f21.apps.kappsul.su.univ-lorraine.fr"
    ),
    "port": int(os.environ.get("DB_PORT", "3306")),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "3edDCAo0Ll"),
    "database": os.environ.get("DB_NAME", "interfaceclient"),
}


@dataclass
class ClientOrder:
    last_name: str
    first_name: str
    role: str
    company: str
    email: str
    engines_requested: int


def get_connection(config: Optional[Dict[str, Any]] = None) -> mysql.connector.MySQLConnection:
    """Create a MariaDB/MySQL connection, creating the database if necessary."""
    cfg = dict(config or DEFAULT_DB_CONFIG)
    db_name = cfg.pop("database", None)

    try:
        return mysql.connector.connect(database=db_name, **cfg)
    except mysql.connector.Error as exc:
        if exc.errno == errorcode.ER_BAD_DB_ERROR and db_name:
            bootstrap_conn = mysql.connector.connect(**cfg)
            bootstrap_cursor = bootstrap_conn.cursor()
            bootstrap_cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4"
            )
            bootstrap_cursor.close()
            bootstrap_conn.close()
            return mysql.connector.connect(database=db_name, **cfg)
        raise


def ensure_tables(connection: mysql.connector.MySQLConnection) -> None:
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS client_orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            last_name VARCHAR(100) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            role VARCHAR(100) NOT NULL,
            company VARCHAR(150) NOT NULL,
            email VARCHAR(255) NOT NULL,
            engines_requested INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
    )
    cursor.close()
    connection.commit()


def validate_email(email: str) -> bool:
    return "@" in email and "." in email.split("@")[-1]


def prompt_for_order(args: argparse.Namespace) -> ClientOrder:
    def ask(prompt: str, fallback: Optional[str] = None) -> str:
        if fallback:
            return fallback
        value = ""
        while not value.strip():
            value = input(prompt).strip()
        return value

    last_name = ask("Nom: ", args.last_name)
    first_name = ask("Prénom: ", args.first_name)
    role = ask("Fonction: ", args.role)
    company = ask("Entreprise: ", args.company)
    email = ask("Adresse mail: ", args.email)
    while not validate_email(email):
        print("Adresse mail invalide, merci de réessayer.")
        email = ask("Adresse mail: ")

    engines_requested = args.engines
    while engines_requested is None:
        try:
            engines_requested = int(input("Nombre de moteurs à fabriquer: ").strip())
            if engines_requested < 1:
                raise ValueError
        except ValueError:
            print("Merci de saisir un nombre entier positif.")
            engines_requested = None

    return ClientOrder(
        last_name=last_name,
        first_name=first_name,
        role=role,
        company=company,
        email=email,
        engines_requested=engines_requested,
    )


def store_order(connection: mysql.connector.MySQLConnection, order: ClientOrder) -> int:
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO client_orders
            (last_name, first_name, role, company, email, engines_requested)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            order.last_name,
            order.first_name,
            order.role,
            order.company,
            order.email,
            order.engines_requested,
        ),
    )
    order_id = cursor.lastrowid
    cursor.close()
    connection.commit()
    return order_id


def send_to_stock_module(order: ClientOrder) -> None:
    # Placeholder for future integration with stock validation system.
    print(
        f"[Info] Demande envoyée au module de stock: {order.engines_requested} moteur(s) pour {order.company}."
    )


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Enregistrer les informations client et la demande de fabrication."
    )
    parser.add_argument("--last-name", help="Nom du client")
    parser.add_argument("--first-name", help="Prénom du client")
    parser.add_argument("--role", help="Fonction ou poste du client")
    parser.add_argument("--company", help="Entreprise du client")
    parser.add_argument("--email", help="Adresse mail du client")
    parser.add_argument(
        "--engines",
        type=int,
        help="Nombre de moteurs à fabriquer (entier positif)",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    try:
        connection = get_connection()
    except mysql.connector.Error as exc:
        print(f"Impossible de se connecter à la base de données: {exc}", file=sys.stderr)
        return 1

    ensure_tables(connection)
    order = prompt_for_order(args)
    try:
        order_id = store_order(connection, order)
    except mysql.connector.Error as exc:
        print(f"Erreur lors de l'enregistrement de la commande: {exc}", file=sys.stderr)
        return 1
    finally:
        connection.close()

    send_to_stock_module(order)
    print(f"Commande enregistrée avec l'identifiant {order_id}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
