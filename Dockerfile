FROM vyperlang/vyper:0.1.0b16

RUN apt-get update
RUN apt-get install -y vim git curl gnupg gnupg1 gnupg2

ENTRYPOINT /bin/bash

# Node.js + npm
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs
RUN npm install npm@latest -g

# Truffle
WORKDIR /app
COPY package.json /app/package.json
RUN npm i
RUN npm run compile
