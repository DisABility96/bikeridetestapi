# Bike Ride Service API

A simple API for managing bike rides with pricing rules (unlock fee, free first 15 minutes, $1 per 5 minutes after, daily cap $25). Built with FastAPI and SQLite.

## Features

- Start a ride
- End a ride
- Get ride details (with duration and cost if ended)
- Get cost for a completed ride

## Requirements

- Python 3.9+
- pip

## Installation

## 1. Clone the repository:

    git clone <repo-url>
    cd bike-ride-api

## 2. Create and activate a virtual environment

On macOS/Linux

    python -m venv venv
    source venv/bin/activate

On Windows

    python -m venv venv
    .\venv\Scripts\activate

## 3. Install dependencies

    pip install -r requirements.txt

## 4. Create the data directory (SQLite database will be created automatically)

    mkdir data

## 5. Running the API: Start the server with uvicorn (auto‑reload enabled for development)

    uvicorn app.main:app --reload
    The server will start at http://127.0.0.1:8000.

Interactive API documentation (Swagger UI): http://127.0.0.1:8000/docs

## 6. Testing
The project includes unit tests written with pytest. To run them:

    pytest