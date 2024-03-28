# Arachnida

## Overview

This project provides a comprehensive solution for processing web data by automating the extraction and analysis of online information and metadata. It comprises two main components: `Spider` and `Scorpion`, each designed to handle specific aspects of data processing. `Spider` focuses on the automated extraction of image data from websites, while `Scorpion` analyzes these images for metadata, revealing insights into the data's origins and characteristics.

## Components

### Spider - Web Data Extraction

`Spider` is a versatile tool that crawls websites to download images, supporting various formats. It offers several options to customize the extraction process, including recursive downloading and depth specification.

#### Features:

- **Recursive Downloading**: Specify a URL, and `Spider` will download all relevant images, with the option to recurse through linked pages.
- **Depth Control**: Limit the recursion depth to avoid extensive data collection, with a default maximum depth of 5.
- **Custom Save Path**: Choose where to save the downloaded images, defaulting to `./data/` if no path is specified.

#### Supported Formats:

- JPG/JPEG
- PNG
- GIF
- BMP

#### Usage:

```shell
./spider [-rlp] URL
-r            Recursively download images from the specified URL.
-r -l [N]     Set the maximum recursion depth (default is 5).
-p [PATH]     Specify the download directory (defaults to ./data/).
```

### Scorpion - Metadata Analyzer

`Scorpion` complements `Spider` by analyzing the downloaded images for metadata, including EXIF data, to provide insights into the creation and modification of the data.

#### Features:

*   **EXIF and Metadata Extraction**: Extracts and displays metadata from image files, including creation date and other relevant information.

#### Supported Formats:

Compatible with the same image formats as `Spider`.

#### Usage:

`./scorpion FILE1 [FILE2 ...]`

Provide one or more image files as arguments to display their metadata.

Getting Started
---------------

To use this project, clone the repository and follow the compilation instructions for each component. Ensure you have the necessary dependencies installed for HTTP requests and file handling.

Compilation
-----------

Use `make` in the desired folder

Contributions
-------------

Contributions are welcome. If you have improvements or bug fixes, please submit a pull request or open an issue.

License
-------

This project is open-source. Feel free to use, modify, and distribute according to the license agreement.
