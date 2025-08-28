FROM node:24-alpine
WORKDIR /app
COPY package*.json ./

COPY . .
RUN npm install
RUN npm run build
RUN npm prune --production

COPY package.json .
EXPOSE 3000
ENV NODE_ENV=production
CMD [ "node", "build" ]

