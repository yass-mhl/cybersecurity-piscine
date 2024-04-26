# This program recieve imagge files as parameters and must be able to parse them for EXIF and other metadata, displaying them on the screen

import sys
import os
import exifread
from PIL import Image


def get_exif_data(image):
    with open(image, 'rb') as file:
        tags = exifread.process_file(file)
        print('EXIF data for: ' + image)
        for tag in tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                print('Key: %s, value %s' % (tag, tags[tag]))
        print('\n')


def get_metadata(image):
    img = Image.open(image)
    print('Metadata for: ' + image)
    print('Format: ' + img.format)
    print('Size: ' + str(img.size))
    print('Mode: ' + img.mode)
    print('Info: ' + str(img.info))
    print('Palette: ' + str(img.getpalette()))
    print('Color: ' + str(img.getcolors()))
    print('Histogram: ' + str(img.histogram()))
    print('Layers: ' + str(img.getbands()))
    print('Resolution: ' + str(img.info.get('dpi')))
    print('ICC Profile: ' + str(img.info.get('icc_profile')))
    print('Transparency: ' + str(img.info.get('transparency')))
    print('Megapixels: ' + str(img.size[0] * img.size[1] / 1000000) + ' MP')
    print('FileAccessDate: ' + str(os.path.getatime(image)))
    print('FileModifiedDate: ' + str(os.path.getmtime(image)))
    print('FileCreationDate: ' + str(os.path.getctime(image)))
    print('FilePermissions: ' + str(oct(os.stat(image).st_mode)[-3:]))
    print('FileSize: ' + str(os.path.getsize(image)) + ' bytes')
    print('Filter: ' + str(img.filter(ImageFilter.BLUR)))
    print("Gamma: " + str(img.info.get('gamma')))
    print("Compression: " + str(img.info.get('compression')))
    print('\n')


def main():
    if len(sys.argv) < 2:
        print('Usage: python scorpion.py <image1> <image2> ... <imageN>')
        sys.exit(1)

    print('Scorpion - Image Metadata Parser\n')
    for i in range(1, len(sys.argv)):
        image = sys.argv[i]
        if os.path.exists(image):
            print('Processing: ' + image)
            print('\n')
            print('------------------------------------')
            get_exif_data(image)
            print('------------------------------------')
            get_metadata(image)
        else:
            print('File not found: ' + image)

if __name__ == '__main__':
    main()
        