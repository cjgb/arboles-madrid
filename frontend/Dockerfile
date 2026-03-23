# Stage 1: Build the React application
FROM node:20-slim AS builder

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy all source files
COPY frontend/ ./

# Build the application
# We use an environment variable for the API URL, defaulting to localhost:8000 for the browser
ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy the built assets to Nginx html directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# The default nginx command starts the server
CMD ["nginx", "-g", "daemon off;"]
