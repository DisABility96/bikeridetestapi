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

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd bike-ride-api