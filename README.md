# RAGineer

An LLM-based project, aims to be a good point to start from for any RAG application or AI Agent, Designed for maximum efficiency and scalability. 

## Features

### NOTE: the project is in it's development phase, some of the following features aren't ready yet.

- Various database options
- Various LLM setups for generation/embeddings
- Support for basic files upload and processing with chunked streaming
- Secure file validation and storage
- RESTful API endpoints using FASTAPI
- Environment-based configuration

## Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)
- Git

## Installation

### Poetry Installation

#### Using pip (Recommended)
```bash
pip install poetry
```

#### Using curl (Alternative)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### Using Homebrew (macOS)
```bash
brew install poetry
```

### Project Setup

1. Clone the repository:
```bash
git clone https://github.com/Ebrahim-Saad/RAGineer.git
cd ai-assistant
```

2. Install dependencies:
```bash
poetry install
```

3. Create and configure `.env` file:
```bash
cp .env.example .env
```

Edit the `.env` file with your own configuration

## Running the Application

### Development Mode
```bash
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Running Docker
```bash
docker-compose up -d
```

## API Endpoints

### File Upload
- **POST** `/data/upload_file/{user_id}`
  - Upload files with chunked streaming
  - Automatic file validation
  - Secure storage

### File Deletion
- **DELETE** `/data/delete_file`
  - Delete a file by providing user ID and file ID
  - Removes file from the server and the database

### Agentic RAG features
- Under development

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
