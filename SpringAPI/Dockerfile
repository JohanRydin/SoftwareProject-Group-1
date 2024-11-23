# ChatGPT gave me this image, it works so why not!  
FROM maven:3.9.4-eclipse-temurin-17 AS build

WORKDIR /app

# Copy only the pom.xml file and download dependencies (should reduce build time)
COPY pom.xml .
RUN mvn dependency:go-offline -B

COPY . .

# Build the "actual" server, maven is just for package stuff basically
RUN mvn clean package -DskipTests

# Now we actually build the working java program OBS: jdk 21 required!
FROM openjdk:21-jdk-slim

WORKDIR /app

COPY --from=build /app/target/*.jar app.jar

EXPOSE 8080

CMD ["java", "-jar", "app.jar"]
