FROM nikolaik/python-nodejs:python3.12-nodejs24-alpine
# Install missing tools
RUN apk update && apk add bash git
WORKDIR /app