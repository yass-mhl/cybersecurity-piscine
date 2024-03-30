IMAGE=spider

# Build the Docker image
build:
	docker build -t $(IMAGE) .

# Run a bash shell in the container
shell:
	docker run --rm -it -v ./images_from_docker --name webscraper $(IMAGE) /bin/bash


# Remove the container and image
clean:
	docker container prune -f
	docker image prune -f
