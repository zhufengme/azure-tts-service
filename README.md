# Azure Text-to-Speech Service

For the Chinese version of this document, please refer to [简体中文](README_zh.md).

This project provides a RESTful API for converting text to speech using Microsoft's Azure Cognitive Services. The service is built using Flask and can be containerized using Docker.

## Features

- Convert text to speech using Microsoft Azure Cognitive Services.
- Specify voice model, speech style, and speech rate.
- Containerized using Docker for easy deployment.
- Configurable using environment variables.
- Logs are available for monitoring and debugging.

## Getting Started

### Prerequisites

- Python 3.10
- Docker
- Azure Cognitive Services subscription key and region

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/zhufengme/azure-tts-service.git
    cd azure-tts-service
    ```

2. Install dependencies (for local development):

    ```bash
    pip install Flask requests
    ```

### Configuration

Set the following environment variables:

- `AZURE_SUBSCRIPTION_KEY`: Your Azure subscription key.
- `AZURE_REGION`: Your Azure region.

### Running the Service Locally

1. Set environment variables:

    ```bash
    export AZURE_SUBSCRIPTION_KEY=your_azure_subscription_key
    export AZURE_REGION=your_azure_region
    ```

2. Run the Flask application:

    ```bash
    python app.py
    ```

### Building and Running with Docker

#### Building the Docker Image

1. Build the Docker image:

    ```bash
    docker build -t azure-tts-service .
    ```

2. Run the Docker container:

    ```bash
    docker run -d -p 5000:5000 --name azure-tts-service -e AZURE_SUBSCRIPTION_KEY=your_azure_subscription_key -e AZURE_REGION=your_azure_region azure-tts-service
    ```

### Running from DockerHub

You can pull the Docker image from DockerHub and run it directly.

1. Pull the Docker image:

    ```bash
    docker pull andiezhu/azure-tts-service
    ```

2. Run the Docker container:

    ```bash
    docker run -d -p 5000:5000 --name azure-tts-service -e AZURE_SUBSCRIPTION_KEY=your_azure_subscription_key -e AZURE_REGION=your_azure_region andiezhu/azure-tts-service
    ```

### API Usage

#### Endpoint

- `POST /tts`

#### Request Body

- `text` (string, required): The text to be converted to speech.
- `voice_name` (string, optional): The voice model to be used. Default is `en-US-AriaNeural`.
- `style` (string, optional): The speech style to be used. Default is `general`.
- `rate` (string, optional): The speech rate. Default is `0%`.

#### Example Request

```bash
curl -X POST http://localhost:5000/tts \
     -H "Content-Type: application/json" \
     -d '{
           "text": "Hello, this is a test of Microsoft Text to Speech service.",
           "voice_name": "en-US-AriaNeural",
           "style": "cheerful",
           "rate": "10%"
         }' --output output.wav
```

### Health Check

The service provides a health check endpoint:

- `GET /health`

#### Example Request

```bash
curl http://localhost:5000/health
```

### Logging

Logs are available for monitoring and debugging. By default, logs are written to both the console and a file named `app.log`.

#### Viewing Logs

To view logs, you can use the `docker logs` command:

```bash
docker logs -f azure-tts-service
```

If you configured logging to a file, you can view the logs using:

```bash
tail -f app.log
```

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Requests](https://docs.python-requests.org/)
- [Microsoft Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/)

