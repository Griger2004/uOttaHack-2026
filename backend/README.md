# Agentic Fake News Detector - Backend

A FastAPI backend that uses a 3-step agentic pipeline to detect fake news in articles.

## Architecture

The backend follows a modular architecture with clear separation of concerns:

```
backend/
├── main.py              # Application entry point & factory
├── config.py            # Settings & environment configuration
├── requirements.txt     # Python dependencies
│
├── schemas/             # Pydantic models for request/response
│   ├── __init__.py
│   └── verify.py        # Verification schemas
│
├── clients/             # External API integrations
│   ├── __init__.py
│   ├── gemini.py        # Google Gemini AI client
│   ├── serper.py        # Serper (Google Search) client
│   └── yellowcake.py    # Yellowcake web scraping client
│
├── services/            # Business logic layer
│   ├── __init__.py
│   ├── reader.py        # Step 1: Extract core claims
│   ├── researcher.py    # Step 2: Search & scrape sources
│   ├── judge.py         # Step 3: Compare & verdict
│   └── pipeline.py      # Orchestrates the full pipeline
│
└── routers/             # API endpoint handlers
    ├── __init__.py
    ├── health.py        # Health check endpoints
    └── verify.py        # /verify endpoint
```

## The 3-Step Pipeline

1. **The Reader** (`services/reader.py`)
   - Analyzes the article text
   - Extracts the core claim to verify
   - Generates a concise search query

2. **The Researcher** (`services/researcher.py`)
   - Searches Google using the generated query
   - Scrapes content from top results
   - Compiles source material for comparison

3. **The Judge** (`services/judge.py`)
   - Compares the original article with scraped sources
   - Calculates a trust score (0-100)
   - Renders a verdict: "Fake", "True", or "Unverified"

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Required API Keys
GEMINI_API_KEY=your_gemini_api_key_here
SERPER_API_KEY=your_serper_api_key_here
YELLOWCAKE_API_KEY=your_yellowcake_api_key_here

# Optional Settings
DEBUG=false
```

### 4. Run the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check

```
GET /
```

Returns API status and available endpoints.

### Detailed Health

```
GET /health
```

Returns status of all configured services.

### Verify Article

```
POST /verify
```

**Request Body:**
```json
{
  "article_text": "Your article text to verify..."
}
```

**Response:**
```json
{
  "trust_score": 75,
  "verdict": "True",
  "reasoning": "The claims are supported by multiple trusted sources.",
  "search_query": "climate change research 2024",
  "sources_checked": 3
}
```

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Development

### Code Style

The project follows standard Python conventions:
- Type hints throughout
- Docstrings for all public functions
- Separation of concerns via modules

### Adding New Features

1. **New endpoint**: Add a router in `routers/`
2. **New service**: Add business logic in `services/`
3. **New external API**: Add a client in `clients/`
4. **New models**: Add schemas in `schemas/`

## License

MIT License
