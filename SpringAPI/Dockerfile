# Building from predefined Image maven 
FROM maven:3.9.4-eclipse-temurin-17 AS build

# Set the working directory inside the container
WORKDIR /app

# Copy only the pom.xml file and download dependencies (should reduce build time)
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy the entire project into the container
COPY . .

# Build the Spring Boot application
RUN mvn clean package -DskipTests

# Now we actually build the working java program
FROM openjdk:21-jdk-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the packaged JAR file from the build stage
COPY --from=build /app/target/*.jar app.jar

# Expose the port the application runs on (from Docker to your computer)
EXPOSE 8080

# Command to run the Spring Boot application
CMD ["java", "-jar", "app.jar"]
