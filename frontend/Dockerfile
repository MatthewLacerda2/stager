# Build stage
FROM node:20-slim as build

WORKDIR /app

# Copy package files from the frontend directory
COPY frontend/package*.json ./
RUN npm install

# Copy the rest of the frontend code
COPY frontend/ .

# Build the application
RUN npm run build

# Production stage
FROM nginx:stable-alpine

# Copy the built assets from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy the nginx configuration
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
