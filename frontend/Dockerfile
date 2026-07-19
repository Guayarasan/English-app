# Etapa 1: build de los assets estáticos con Vite
FROM node:20-slim AS build

WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install

COPY . .
# VITE_API_URL se inyecta en build time porque Vite resuelve
# import.meta.env al compilar, no en runtime.
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# Etapa 2: servir los archivos estáticos con nginx (imagen final mucho
# más liviana que arrastrar node + node_modules a producción)
FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
