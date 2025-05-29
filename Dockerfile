FROM node:18-bullseye as nodebase
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y python3 python3-pip

# Install both deps: Conditional installation is bad cos of layer caching
RUN cd src/js-api && npm install
RUN cd src/py-api && pip3 install -r requirements.txt

# Make scripts executable
RUN chmod +x scripts/docker/start-py.sh
RUN chmod +x scripts/docker/start-js.sh

# Conditional runtime execution: Runs at runtime, no layer caching issues
CMD ["sh", "-c", "\
  if [ \"$RUNTIME\" = \"python\" ]; then \
    ./scripts/docker/start-python.sh; \
  else \
    ./scripts/docker/start-js.sh; \
  fi"]
