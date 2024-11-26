# Step 1: Build Stage
FROM maven:3.8.6-openjdk-23-slim AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy the pom.xml and the source code to the container
COPY pom.xml .
COPY src ./src

# Run mvn clean install to build the application and create the .jar file
RUN mvn clean install -DskipTests

# Step 2: Runtime Stage
FROM openjdk:23-jdk-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the generated .jar file from the builder stage
COPY --from=builder /app/target/springServer-0.0.1-SNAPSHOT.jar app.jar

# Expose the port your Spring Boot app runs on
EXPOSE 8080

# Command to run the application
ENTRYPOINT ["java", "-jar", "app.jar"]
