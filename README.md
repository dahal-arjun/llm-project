# LangGraph RAG System with Ollama LLM

A free and open-source RAG (Retrieval Augmented Generation) system built with LangGraph for agent orchestration, Chroma for vector storage, and Ollama for local LLM inference.

## Key Features

- **100% Free & Open Source**: All components are free to use and self-hosted
- **Local LLM Integration**: Uses Ollama for running models locally without API costs
- **Vector Database**: Chroma DB for efficient document storage and retrieval
- **LangGraph Agent Orchestration**: Pure LangGraph implementation for building stateful, multi-step agents
- **Simple API**: Focused API with only essential endpoints for document ingestion and querying
- **Modular Design**: Well-structured FastAPI application following best practices
- **Observability**: Structured JSON logging and health monitoring
- **Developer Experience**: Comprehensive Makefile for common development tasks

## Step-by-Step Instructions

### Prerequisites

1. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
2. Install [Git](https://git-scm.com/downloads)
3. Clone this repository:
   ```bash
   git clone https://github.com/dahal-arjun/langgraph-rag-system.git
   cd langgraph-rag-system
   ```

### Option 1: Quick Start with Docker (Recommended)

1. **Build and start all services**:
   ```bash
   make bootstrap
   ```
   This will:
   - Build the Docker images
   - Start all services (app, Chroma, Ollama)
   - Pull the default language model (tinyllama:latest)

2. **Verify the services are running**:
   ```bash
   curl http://localhost:8081/health
   ```
   You should see: `{"status":"healthy","services":{"chroma":true,"ollama":true}}`

3. **Create a test collection**:
   ```bash
   curl -X POST http://localhost:8081/collections/documents
   ```

4. **Upload a document**:
   ```bash
   # Create a test document
   echo "Vector databases are specialized database systems designed to store and search high-dimensional vectors efficiently." > test_document.txt
   
   # Upload the document
   curl -X POST -F "file=@test_document.txt" -F "collection_name=documents" -F "chunk_size=500" -F "keep_file=true" http://localhost:8081/upload
   ```

5. **Ask a question**:
   ```bash
   curl -X GET "http://localhost:8081/ask?query=What%20are%20vector%20databases?&collection_name=documents"
   ```

6. **Access the API documentation**:
   Open your browser and navigate to http://localhost:8081/docs

### Option 2: Local Development Setup

1. **Install Python dependencies**:
   ```bash
   make setup
   ```

2. **Start Chroma and Ollama using Docker**:
   ```bash
   docker-compose up -d chroma ollama
   ```

3. **Pull the language model**:
   ```bash
   docker exec -it llm-project-ollama-1 ollama pull tinyllama:latest
   ```

4. **Start the application in development mode**:
   ```bash
   make dev
   ```

5. **Test the application**:
   Follow steps 2-6 from Option 1 to test the application.

### Monitoring and Observability

1. **View application logs**:
   ```bash
   make docker-logs-app
   ```

2. **Check service health**:
   ```bash
   curl http://localhost:8081/health
   ```

3. **Test API endpoints**:
   ```bash
   python scripts/test_observability.py
   ```

### Stopping the Services

1. **Stop all services**:
   ```bash
   make docker-down
   ```

2. **Stop and remove volumes (caution: this will delete all data)**:
   ```bash
   make docker-down-volumes
   ```

## Troubleshooting

### Common Issues

1. **Services not starting properly**:
   - Check if ports 8000, 8081, or 11434 are already in use
   - Solution: Stop any conflicting services or change the ports in `docker-compose.yml`

2. **Ollama model download fails**:
   - Check your internet connection
   - Solution: Try downloading a smaller model like `tinyllama:latest` or check Ollama logs with `docker-compose logs ollama`

3. **Application can't connect to Chroma or Ollama**:
   - Check if the services are running with `docker-compose ps`
   - Solution: Restart the services with `make docker-down && make docker-up`

4. **Slow response times**:
   - This is normal for the first few queries as the model loads into memory
   - Solution: Wait for subsequent queries which should be faster

5. **Out of memory errors**:
   - The LLM might be too large for your system
   - Solution: Use a smaller model or increase Docker's memory allocation

### Checking Logs

To diagnose issues, check the logs for each service:

```bash
# App logs
make docker-logs-app

# Chroma logs
docker-compose logs chroma

# Ollama logs
docker-compose logs ollama
```

## Project Structure

```
.
├── README.md                 # Project documentation
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Application Dockerfile
├── Makefile                  # Development and deployment tasks
├── log_config.json           # Logging configuration
├── requirements.txt          # Python dependencies
├── data/                     # Data directory
│   ├── persistent/           # Persistent sample documents
│   └── uploads/              # Directory for uploaded files
├── docs/                     # Documentation
├── scripts/                  # Utility scripts
│   └── test_observability.py # Script to test API observability
└── src/                      # Source code
    ├── __init__.py           # Package initialization
    ├── main.py               # FastAPI application entry point
    ├── api/                  # API layer
    │   ├── __init__.py
    │   ├── routes/           # API routes
    │   │   ├── __init__.py
    │   │   ├── collection_routes.py
    │   │   ├── file_routes.py
    │   │   └── query_routes.py
    │   ├── models/           # Pydantic models
    │   │   ├── __init__.py
    │   │   └── api_models.py
    │   └── dependencies/     # FastAPI dependencies
    │       ├── __init__.py
    │       └── dependencies.py
    ├── core/                 # Core application code
    │   ├── __init__.py
    │   └── config.py         # Application configuration
    ├── db/                   # Database layer
    │   ├── __init__.py
    │   └── chroma_client.py  # ChromaDB client
    └── services/             # Business logic services
        ├── __init__.py
        ├── file_service.py   # File processing service
        ├── langgraph_service.py # LangGraph agent service
        └── ollama_service.py # Ollama LLM service
```

## Development with Make

The project includes a comprehensive Makefile to simplify common development tasks:

```bash
# Show available commands
make help

# Run the application locally with hot reload
make dev

# Build Docker images
make docker-build

# Start all services in Docker
make docker-up

# Stop all Docker services
make docker-down

# View logs from all services
make docker-logs

# View logs from the app service only
make docker-logs-app

# Pull a specific model in Ollama
make ollama-pull MODEL=llama3:latest

# Format code with black
make format

# Run linting
make lint

# Run tests
make test

# Clean up temporary files
make clean
```

## Observability

The application includes structured JSON logging and health monitoring:

- **Structured Logs**: All application logs are output as JSON to stdout for easy parsing by log aggregation tools
- **Log Levels**: Control verbosity with the `LOG_LEVEL` environment variable (debug, info, warning, error)
- **Health Endpoint**: Monitor service health at `/health`
- **Docker Logs**: View container logs with `make docker-logs` or `make docker-logs-app`

## API Endpoints

### Ask Question (GET)
```
GET /ask?query={query}&collection_name={collection_name}&model_name={model_name}
```
Ask a question and get an answer with sources using the LangGraph agent.

Parameters:
- `query`: Your question
- `collection_name`: The name of the collection to search in
- `model_name`: (Optional) The model to use (default: "tinyllama:latest")

Response:
```json
{
  "answer": "The generated answer based on the retrieved documents",
  "sources": [
    {
      "content": "Source document content",
      "metadata": {
        "source": "filename.txt",
        "chunk": 0
      }
    }
  ]
}
```

### Document Ingestion
```
POST /upload
```
Upload a .txt or .md file and add its content to the specified collection.

Parameters:
- `file`: The file to upload (.txt or .md)
- `collection_name`: The name of the collection to add the document to
- `chunk_size`: (Optional) The size of chunks to split the document into (default: 1000)
- `keep_file`: (Optional) Whether to keep the uploaded file in the data/uploads directory (default: false)

### Collection Management
```
GET /collections
POST /collections/{collection_name}
```
List collections or create a new collection.

### Health Check
```
GET /health
```
Check the health of the application and its dependencies.

## Data Persistence

Chroma data is stored in a Docker volume named `chroma_data` to ensure persistence between container restarts.
Ollama models are stored in a Docker volume named `ollama_data`.
Uploaded files can be kept in the `data/uploads` directory by setting `keep_file=true` when uploading.