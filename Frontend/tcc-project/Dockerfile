FROM node:22-alpine AS build-stage

WORKDIR /app

COPY package*.json ./
RUN npm install && npm audit fix --force

COPY . .
RUN npm run build

# Etapa 2: Produção com Nginx
FROM nginx:stable-alpine AS production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENV PORT=80
EXPOSE ${PORT}

ENTRYPOINT ["/entrypoint.sh"]