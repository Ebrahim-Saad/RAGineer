# AI Assistant

A FastAPI-based AI assistant that provides intelligent responses and file handling capabilities.

## Features

- File upload and processing with chunked streaming
- AI-powered responses using LangChain (under development)
- Secure file validation and storage (under development)
- RESTful API endpoints
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
git clone https://github.com/yourusername/ai-assistant.git
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

Edit the `.env` file with your configuration:
```env
# File Upload Settings
MAXIMUM_FILE_SIZE=10 # in MB
ALLOWED_FILE_TYPES=["application/pdf", "text/plain"]
DEFAULT_CHUNK_SIZE=100 # in KB

# AI Settings
AI_MODEL=gpt-3.5-turbo
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=1000

API Keys
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Running the Application

### Development Mode
```bash
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### File Upload
- **POST** `/data/upload_file/{user_id}`
  - Upload files with chunked streaming
  - Automatic file validation
  - Secure storage

### AI Assistant
- Under development

## Project Structure

```
ai-assistant/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   │   └── V1/
│   ├── controllers/
│   ├── core/
│   │   ├── config.py
│   └── main.py
├── tests/
├── assets/
├── .env
├── .env.example
├── pyproject.toml
└── README.md
```

## Development

### Running Tests
```bash
poetry run pytest
```

### Code Formatting
```bash
poetry run black .
poetry run isort .
```

### Linting
```bash
poetry run flake8
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- FastAPI for the amazing web framework
- LangChain for AI capabilities
- Poetry for dependency management
