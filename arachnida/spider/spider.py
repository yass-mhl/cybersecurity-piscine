import requests
import argparse
import os
import hashlib 
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse, parse_qs, urlencode
import logging # Pour gerer les logs

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fonction pour gérer les erreurs de requête
def handle_request_error(e, url):
    if isinstance(e, requests.exceptions.MissingSchema):
        logging.error(f"URL mal formée: {url}. Avez-vous oublié 'http://' ou 'https://' ?")
    elif isinstance(e, requests.exceptions.ConnectionError):
        logging.error(f"Impossible de se connecter à l'URL: {url}. Vérifiez que l'URL est correcte et que le serveur est accessible.")
    elif isinstance(e, requests.exceptions.Timeout):
        logging.error(f"Le temps de réponse a expiré pour l'URL: {url}. Le serveur est peut-être trop lent ou surchargé.")
    else:
        logging.error(f"Erreur lors de l'accès à l'URL: {url}. Erreur: {e}")

# Fonction pour normaliser l'URL en supprimant les paramètres inutiles
def normalize_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    filtered_query = {k: v for k, v in query_params.items() if k in ['param_requis']}
    clean_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, urlencode(filtered_query, doseq=True), ''))
    return clean_url

# Fonction pour télécharger une image
def download_image(src, path):
    try:
        response = requests.get(src, timeout=10)
        if response.status_code == 200: # Vérifier si la requête a réussi
            content = response.content
            hash_prefix = hashlib.md5(src.encode('utf-8')).hexdigest()[:8] # Générer un hash pour le nom du fichier pour eviter les doublons
            filename = f"{hash_prefix}_{os.path.basename(src)}"
            file_path = os.path.join(path, filename) # Créer le chemin complet du fichier
            with open(file_path, 'wb') as file: 
                file.write(content)
            print(f"Image downloaded: {file_path}")
        else:
            print(f"Failed to download {src}: Status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {src}: {e}")

# Fonction pour récupérer les images d'une page
def get_images(url, path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            images = soup.find_all('img')
            for img in images:
                img_path = img.get('src')
                if img_path:  # Assurez-vous que img_path n'est pas None
                    full_url = urljoin(url, img_path)  # Créer l'URL complète
                    try:
                        image_response = requests.get(full_url)  # Faire la requête avec l'URL complète
                        if image_response.status_code == 200 and full_url.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
                            download_image(full_url, path)  # Passer l'URL complète à download_image
                    except requests.exceptions.RequestException as e:
                        handle_request_error(e, full_url)
        else:
            logging.error(f"Erreur lors de l'accès à la page: {url}. Code de statut: {response.status_code}")
    except requests.exceptions.RequestException as e:
        handle_request_error(e, url)


# Fonction pour récupérer les images de manière récursive
def get_images_recursive(url, path, level, prefix='', visited=None):
    if visited is None:
        visited = set()
    if url in visited or level < 0:
        return
    visited.add(url)

    normalized_url = normalize_url(url)
    logging.info(f"{prefix}Level: {level} - Processing {normalized_url}")
    try:
        response = requests.get(normalized_url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            images = soup.find_all('img')
            for img in images:
                img_src = img.get('src')
                if img_src:
                    full_img_src = urljoin(normalized_url, img_src)
                    if full_img_src.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
                        try:
                            download_image(full_img_src, path)
                        except requests.exceptions.RequestException as e:
                            handle_request_error(e, full_img_src)
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href:
                    full_link = urljoin(normalized_url, href)
                    if level > 0:
                        get_images_recursive(full_link, path, level - 1, prefix + '---', visited)
        else:
            logging.error(f"Échec d'accès à {normalized_url}: Statut {response.status_code}")
    except requests.exceptions.RequestException as e:
        handle_request_error(e, normalized_url)

# Assurez-vous que la gestion des erreurs est cohérente dans toutes les parties du script où des requêtes réseau sont effectuées.


def main():
    parser = argparse.ArgumentParser(description="Download images from a webpage")
    parser.add_argument("-r", "--recursive", action="store_true", help="Download images recursively")
    parser.add_argument("-l", "--level", type=int, default=5, help="Recursion depth level")
    parser.add_argument("-p", "--path", type=str, default="images", help="Path to save the images")
    parser.add_argument("url", help="The URL to download images from")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        os.makedirs(args.path)

    if args.level < 0:
        print("The level must be greater than zero")
        return
    elif args.level > 5:
        print("The level must be less than or equal to 5")
        return

    if args.recursive:
        get_images_recursive(args.url, args.path, args.level)
    else:
        get_images(args.url, args.path)

if __name__ == "__main__":
    main()
