# Script principal de PingWatch
# Objectif:
# Accepter --url ou un fichier --file (liste URL)
# faire un GET simple sur chaque URL
# Afficher UP/DOWN
# Renvoyer le code de sortie(exit) adapté

import argparse # Pour l'analyse des arguments de la ligne de commande
import sys # Pour gérer les codes de sortie
from typing import List, Tuple # Pour les annotations de type

import requests # Pour effectuer les requêtes HTTP

# Fonction pour vérifier une URL
def check_url(url: str, timeout: float = 3.0) -> Tuple[bool, int | None]:
    """Retourne (is_up, status_code)."""
    try:
        response = requests.get(url, timeout=timeout)
        return (200 <= response.status_code < 400, response.status_code)
    except requests.RequestException:
        return (False, None)

# Fonction pour charger les URLs depuis un fichier   
def load_urls_from_file(path: str) -> List[str]:
    urls: List[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    return urls

# Fonction principale
def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PingWatch - HTTP healthcheck simple")
    parser.add_argument(
        "--url",
        "-u",
        action="append",
        help="URL à tester (peut être utilisé plusieurs fois)",
    )
    parser.add_argument(
        "--file",
        "-f",
        help="Fichier contenant une URL par ligne",
    )

    args = parser.parse_args(argv)

    urls: List[str] = []

    if args.url:
        urls.extend(args.url)

    if args.file:
        urls.extend(load_urls_from_file(args.file))

    if not urls:
        print("❌ Aucune URL fournie. Utilisez --url ou --file.")
        return 1

    print("🔍 PingWatch - Vérification des URLs :")
    has_error = False

    for url in urls:
        is_up, status = check_url(url)
        if is_up:
            print(f"✅ {url} est UP (status={status})")
        else:
            print(f"❌ {url} est DOWN (status={status})")
            has_error = True

    if has_error:
        print("\nRésultat global : au moins une URL est DOWN ❌")
        return 1

    print("\nRésultat global : toutes les URLs sont UP ✅")
    return 0

# Point d'entrée du script
if __name__ == "__main__":
    sys.exit(main())