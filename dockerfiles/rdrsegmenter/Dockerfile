FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Install system dependencies
RUN apk update && apk add --no-cache curl

# Download jar file
RUN curl -L -O https://github.com/LLM-UET/RDRsegmenter/releases/download/0.9.1/RDRsegmenter.jar
RUN echo "47d3581e050bd686b9eac4727d4d453a5458d6b843e9b3c618a23f3654bdd7fa  RDRsegmenter.jar" | sha256sum --check

# Expose segmenter port
EXPOSE 8024

# Run the jar
CMD ["java", "-jar", "RDRsegmenter.jar", "TXT-RPC", "8024"]
