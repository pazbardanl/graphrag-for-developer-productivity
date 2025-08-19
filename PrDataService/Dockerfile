FROM eclipse-temurin:21-jdk
WORKDIR /app
COPY PrDataService/. .
RUN chmod +x gradlew
RUN ./gradlew build --no-daemon
EXPOSE 8080
CMD ["java", "-jar", "build/libs/PrDataService-0.0.1-SNAPSHOT.jar"]