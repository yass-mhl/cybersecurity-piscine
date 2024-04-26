import requests
import argparse
import os
import hashlib
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse, parse_qs, urlencode

def normalize_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    filtered_query = {k: v for k, v in query_params.items() if k in ['param_requis']}
    clean_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, urlencode(filtered_query, doseq=True), ''))
    return clean_url

def download_image(src, path):
    try:
        response = requests.get(src, timeout=10)
        if response.status_code == 200:
            content = response.content
            hash_prefix = hashlib.md5(src.encode('utf-8')).hexdigest()[:8]
            filename = f"{hash_prefix}_{os.path.basename(src)}"
            file_path = os.path.join(path, filename)
            with open(file_path, 'wb') as file:
                file.write(content)
            print(f"Image downloaded: {file_path}")
        else:
            print(f"Failed to download {src}: Status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {src}: {e}")

def get_images(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        images = soup.find_all('img')
        for img in images:
            img_path = img.get('src')
            src = requests.get(img_path)
            if src and src.status_code == 200:
                src = urljoin(url, src)
                if src.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
                    download_image(src, path)
    else:
        print(f"Error accessing the page: {url}")

def get_images_recursive(url, path, level, prefix='', visited=None):
    if visited is None:
        visited = set()
    if url in visited or level < 0:
        return
    visited.add(url)

    normalized_url = normalize_url(url)
    print(f"{prefix}Level: {level} - Processing {normalized_url}")
    response = requests.get(normalized_url, timeout=10)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        for img in images:
            img_src = img.get('src')
            if img_src:
                img_src = urljoin(normalized_url, img_src)
                if img_src.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
                    download_image(img_src, path)

        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href:
                full_link = urljoin(normalized_url, href)
                if level > 0:
                    get_images_recursive(full_link, path, level - 1, prefix + '---', visited)
    else:
        print(f"Failed to access {normalized_url}: Status {response.status_code}")

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
