# Use the official Node.js image as the base image
FROM node:22.11.0

# Set the working directory inside the container
WORKDIR /app

# Copy only the package.json and package-lock.json for dependency installation
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Expose the port used by the development server
EXPOSE 5173  
# Default port for Vite dev server

# Run the development server
CMD ["npx", "vite"]

