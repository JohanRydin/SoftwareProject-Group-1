# Step 1: Use the official Ubuntu image as the base
FROM ubuntu:latest

# Step 2: Install Java and Maven (required for building Spring Boot apps)
RUN apt-get update && apt-get install -y \
    openjdk-21-jdk \  
    maven \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Copy the entire project into the container (to build it)
COPY . .

# Step 5: Run Maven to clean, install, and build the project
RUN mvn clean install

# Step 6: Expose the port that the Spring Boot app will run on (8080 by default)
EXPOSE 8080

# Step 7: Run the Spring Boot application (can also use `mvn spring-boot:run` or `java -jar`)
CMD ["mvn", "spring-boot:run"]
