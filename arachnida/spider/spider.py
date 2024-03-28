import requests
import argparse

# This progran will get a webpage and download all the images 

def get_page(url):
	response = requests.get(url)
	return response.text

def main():
	parser = argparse.ArgumentParser(description="Get a webpage") 

	# Parse options from the command line [-rlp]
	parser.add_argument("-r", "--recursive", action="store_true", help="Get the page recursively")
	parser.add_argument("-l", "--level", type=int, help="The level of recursion")
	parser.add_argument("-p", "--path", help="The path to save the images")
	parser.add_argument("url", help="The URL to get")
	args = parser.parse_args()
	url = args.url

	print("URL: ", url)
	if args.recursive:
		print("Recursive")
	if args.level:
		print("Level: ", args.level)
	if args.path:
		print("Path: ", args.path)


main()
