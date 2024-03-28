import requests
import argparse
import os


# This progran will get a webpage and download all the images it will only download the images in jpg/jpeg, png, gif, bmp format

def get_images(url, path):
	r = requests.get(url)
	if r.status_code == 200: # Check if the request was successful
		content = r.text # Get the content of the page
		images = content.split("<img")
		# Loop through the images
		for i in images:
			src = i.split("src=")[1].split(" ")[0].strip("\"") # Find the source of the image
			if src.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
				r = requests.get(src)
				if r.status_code == 200:
					# Get the content of the image
					content = r.content
					# Get the name of the image
					name = src.split("/")[-1]
					# Save the image
					with open(os.path.join(path, name), "wb") as f:
						f.write(content)
				else:
					print("Error getting image: ", src)
	else:
		print("Error getting page: ", url)

def get_images_recursive(url, path, level):
	r = requests.get(url)
	if r.status_code == 200: # Check if the request was successful
		content = r.text # Get the content of the page
		images = content.split("<img")
		# Loop through the images
		for i in images:
			src = i.split("src=")[1].split(" ")[0].strip("\"") # Find the source of the image
			if src.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
				r = requests.get(src)
				if r.status_code == 200:
					# Get the content of the image
					content = r.content
					# Get the name of the image
					name = src.split("/")[-1]
					# Save the image
					with open(os.path.join(path, name), "wb") as f:
						f.write(content)
				else:
					print("Error getting image: ", src)
	else:
		print("Error getting page: ", url)

	# Get the links
	links = content.split("<a")
	# Loop through the links
	for l in links:
		href = l.split("href=")[1].split(" ")[0].strip("\"") # Find the href of the link
		if href.startswith("http"):
			if level > 0:
				get_images_recursive(href, path, level-1)



def main():
	parser = argparse.ArgumentParser(description="Get a webpage") 

	# Parse options from the command line [-rlp]
	parser.add_argument("-r", "--recursive", action="store_true", help="Get the page recursively")
	parser.add_argument("-l", "--level", type=int, help="The level of recursion")
	parser.add_argument("-p", "--path", type=str, help="The path to save the images")
	parser.add_argument("url", help="The URL to get")
	args = parser.parse_args()
	url = args.url


	if args.path:
		path = args.path
	else:
		path = "images"
	if not os.path.exists(path): # Check if the path exists
		os.makedirs(path)
	if args.recursive:
		if args.level:
			get_images_recursive(url, path, args.level)
		else:
			get_images_recursive(url, path, 1)
	else:
		get_images(url, path)


main()
