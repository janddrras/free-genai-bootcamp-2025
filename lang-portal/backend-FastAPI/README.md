# Language Learning Portal Backend

A FastAPI-based backend for the language learning portal that provides vocabulary management, learning record storage, and a unified launchpad for learning apps.

## Features

- Vocabulary management with Hungarian-English word pairs
- Learning Record Store (LRS) functionality
- Study session tracking
- Group-based vocabulary organization
- RESTful API endpoints
- SQLite database with Alembic migrations

## Prerequisites

- Python 3.8+
- pip
- SQLite3

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize the database:
   ```bash
   alembic upgrade head
   ```

## Development

1. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```
2. Access the API documentation at:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend-FastAPI/
├── alembic/              # Database migrations
├── app/                  # Application package
│   ├── api/             # API endpoints
│   ├── core/            # Core functionality
│   ├── db/              # Database models and session
│   ├── schemas/         # Pydantic models
│   └── main.py          # FastAPI application
├── tests/               # Test suite
├── words.db             # SQLite database
└── requirements.txt     # Project dependencies
```

## Testing

Run tests with pytest:

```bash
pytest
```

## Configuration

Environment variables can be set in a `.env` file:

```
DATABASE_URL=sqlite:///./words.db
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Contact

For any questions or feedback, please open an issue in the repository.
