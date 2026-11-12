FROM node:20-alpine
WORKDIR /app
COPY package.json server.js ./
ARG APP_VERSION=v1
ENV APP_VERSION=$APP_VERSION
USER node
EXPOSE 3000
CMD ["node", "server.js"]
