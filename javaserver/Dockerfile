# Step 1: Build Stage
FROM maven:3.9.8-eclipse-temurin-21 AS build

# Set the working directory inside the container
WORKDIR /app

# Copy the pom.xml and download dependencies
COPY pom.xml /app
RUN mvn dependency:go-offline -B

# Copy the source code and build the application
COPY src /app/src
RUN mvn clean install -U

# Step 2: Runtime Stage
FROM openjdk:21

# Copy the JAR file from the build stage
COPY --from=build /app/target/javaserver-0.0.1-SNAPSHOT.jar /app/app.jar

# Set the working directory inside the container
WORKDIR /app

# Expose the port your Spring Boot application uses
EXPOSE 8080

# Run the Spring Boot application
CMD ["java", "-jar", "app.jar"]
