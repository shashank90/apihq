# Download base image Ubuntu 20.04
FROM ubuntu:20.04

# Label custom image
LABEL maintainer="Shashank Gudipati"

# Update Ubuntu software repository and install core dependencies
RUN apt update && apt-get install -y curl sudo

# Install npm
RUN apt-get update && apt-get install -y \
    software-properties-common \
    npm
RUN npm install npm@latest -g && \
    npm install n -g && \
    n stable

# Install node modules:
# ibm-openapi validator for openapi spec validation
RUN sudo npm install -g ibm-openapi-validator
# TODO: Add openapi code generator


# newman for running postman collection via cli
RUN sudo npm install -g newman

# Expose Port for Application
EXPOSE 80 443