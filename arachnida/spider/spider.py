import requests
import argparse
import os
import re
from urllib.parse import urljoin, urlparse, urlunparse, parse_qs, urlencode

def get_images(url, path):
    response = requests.get(url)
    if response.status_code == 200:  # Check if the request was successful
        html_content = response.text  # Get the content of the page

        # Regular expression to find images
        images = re.findall(r'<img[^>]+src="([^">]+)"', html_content)

        for src in images:
            # Handles absolute and relative URLs
            src = urljoin(url, src)
            if src.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
                try:
                    img_response = requests.get(src)
                    if img_response.status_code == 200:
                        img_content = img_response.content  # Get the binary content of the image
                        name = os.path.basename(src)
                        with open(os.path.join(path, name), 'wb') as f:
                            f.write(img_content)
                    else:
                        print(f"Error downloading the image: {src}")
                except requests.exceptions.RequestException as e:
                    print(f"Error requesting the image: {src}\nError: {e}")
    else:
        print(f"Error accessing the page: {url}")

visited_urls = set()  # Ensemble global pour suivre les URLs visitées

def get_images_recursive(url, path, level, prefix='', visited=visited_urls):
    normalized_url = normalize_url(url)
    if normalized_url in visited or level <= 0:
        return
    visited.add(normalized_url)
    
    print(f"{prefix}Level: {level} - URL: {normalized_url}")
    response = requests.get(normalized_url)
    if response.status_code == 200:  # Checks if the request was successful
        html_content = response.text  # Gets the content of the page

        # Regular expression to find images
        images = re.findall(r'<img[^>]+src="([^">]+)"', html_content)
        
        print(f"{prefix}Found {len(images)} images for {normalized_url} - Level: {level}")
        for src in images:
            src = urljoin(normalized_url, src)
            if src.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")) and normalize_url(src) not in visited:
                try:
                    img_response = requests.get(src)
                    if img_response.status_code == 200:
                        img_content = img_response.content
                        name = os.path.basename(src)
                        with open(os.path.join(path, name), 'wb') as f:
                            f.write(img_content)
                        visited.add(normalize_url(src))  # Mark the image URL as visited
                    else:
                        print(f"{prefix}Error downloading the image: {src}")
                except requests.exceptions.RequestException as e:
                    print(f"{prefix}Error requesting the image: {src}\nError: {e}")

        # Regular expression to find links for recursion
        links = re.findall(r'<a[^>]+href="([^">]+)"', html_content)
        print(f"{prefix}Found {len(links)} links")
        new_prefix = prefix + '---'  # Increase indentation for the next level of recursion
        for href in links:
            href = urljoin(normalized_url, href)
            if href.startswith("http") and normalize_url(href) not in visited:
                if level - 1 > 0:
                    print(f"{prefix}======== Recursing to: {normalize_url(href)} - Level: {level - 1} ====")
                get_images_recursive(href, path, level - 1, new_prefix, visited)
    else:
        print(f"{prefix}Error accessing the page: {normalized_url}")

def normalize_url(url):
    parsed_url = urlparse(url)
    
    query_params = parse_qs(parsed_url.query)
    filtered_query = {k: v for k, v in query_params.items() if k in ['param_requis']}
    
    clean_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        urlencode(filtered_query, doseq=True),
        ''
    ))
    
    return clean_url

def main():
    parser = argparse.ArgumentParser(description="Download images from a webpage")
    parser.add_argument("-r", "--recursive", action="store_true", help="Download images recursively")
    parser.add_argument("-l", "--level", type=int, default=1, help="Recursion depth level")
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
    elif args.level == 0:
        args.level = 5

    if args.recursive:
        get_images_recursive(args.url, args.path, args.level)
    else:
        get_images(args.url, args.path)

if __name__ == "__main__":
    main()