FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm install

# Copy all source files
COPY . .

# Create the build
RUN npm run build

EXPOSE 5173

# Use production-ready command
CMD ["node", "build"] 