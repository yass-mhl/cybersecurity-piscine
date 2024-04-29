from exif import Image
from colorama import Fore, Style
import sys
from PIL import Image as PILImage  # Importer PIL pour vérifier le format

extension = [".jpeg", ".jpg", ".png", ".gif", ".bmp"]

def main():
    # Parcours des arguments passés au script
    for image_path in sys.argv[1:]:
        if image_path.endswith(tuple(extension)):
            try:
                # Vérification du format de l'image avant de tenter de lire les EXIF
                with open(image_path, 'rb') as image_file:
                    pil_img = PILImage.open(image_file)
                    format = pil_img.format
                    print(Fore.GREEN + f"==== IMAGE : {image_path} ====")
                    print(Fore.YELLOW + f"Image format: {format}")
                    if format in ["JPEG", "TIFF"]:
                        image_file.seek(0)  # Retourner au début du fichier
                        img = Image(image_file)
                        print(Fore.YELLOW + "EXIF data:")
                        for tag in img.list_all():
                            print(Fore.GREEN + f"{tag}: {img.get(tag)}")
                    else:
                        print(Fore.RED + "EXIF data not available for this image format.")
                    print(Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Error reading image {image_path}: {e}")
                print(Style.RESET_ALL)
        else:
            print(Fore.RED + f"File not found or unsupported format: {image_path}")
            print(Style.RESET_ALL)

if __name__ == "__main__":
    main()
