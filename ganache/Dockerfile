FROM node:10.19.0 as build
WORKDIR /app
COPY package.json /app/package.json
RUN npm install --no-optional --no-shrinkwrap

FROM node:10.19.0-alpine3.11
WORKDIR /app
COPY --from=build /app/ /app/
EXPOSE 7545
CMD ["npm", "run", "serve"]