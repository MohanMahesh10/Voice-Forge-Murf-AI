FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm install && npm install --save-dev @sveltejs/adapter-node

# Copy all source files
COPY . .

# Create the build
RUN npm run build

# Expose the port that SvelteKit runs on in production (3000)
EXPOSE 3000

# Use production-ready command
CMD ["node", "build"]