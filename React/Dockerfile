# Use the official Node.js image as the base image
FROM node:22.11.0

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

RUN npm install

RUN npm i -g serve

COPY . .

RUN npm run build

EXPOSE 3000

CMD [ "serve", "-s", "dist" ]


#docker build . -t "sample-project:v1.0"
#docker images
#docker run -p 3000:3000 sample-project:v1.0
#https://thedkpatel.medium.com/dockerizing-react-application-built-with-vite-a-simple-guide-4c41eb09defa
