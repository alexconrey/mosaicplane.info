FROM node:24-alpine

RUN apk add libc6-compat gcompat

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

RUN npm ci

# Copy source code
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S vueuser -u 1001

# Change ownership of the app directory
RUN chown -R vueuser:nodejs /app
USER vueuser

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000 || exit 1

# Start development server with Docker-specific config
CMD ["npm", "run", "dev", "--", "--config", "vite.config.docker.js", "--host", "0.0.0.0"]