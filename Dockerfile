FROM node:18-bullseye as nodebase
RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /app