IMAGE=ft_otp

# Build the Docker image
build:
	docker build -t $(IMAGE) .

# Run a bash shell in the container
shell:
	docker run --rm -it --name ft_otp $(IMAGE) /bin/bash


# Remove the container and image
clean:
	docker container prune -f
	docker image prune -f
