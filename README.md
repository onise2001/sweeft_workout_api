# Sweeft Workout API

A RESTful API for a fitness application that allows users to design custom workouts, track progress, and manage exercise routines. Users can select exercises from a predefined database, customize their workout parameters, and track their progress in real-time.

## Features

- User authentication with JWT
- Predefined exercise database with detailed instructions
- Personalized workout plans
- Progress tracking
- Real-time workout mode
- Exercise completion tracking


## Prerequisites

- Python 3.13+
- Docker (optional)


## Installation

### 1. With Docker

```bash
# Clone and setup
git clone https://github.com/onise2001/sweeft_workout_api.git
cd sweeft_workout_api

# Run with docker
docker compose up -d
```

### 2. Without Docker

```bash
# Clone and setup
git clone https://github.com/onise2001/sweeft_workout_api.git
cd sweeft_workout_api

# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux
# or
.\venv\Scripts\activate  # Windows

# Dependencies and setup
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_exercises
python manage.py runserver
```




## API Documentation

After getting the local copy up and running you will be able to see the swagger documentation at any of the following endpoints:

```
Swagger: 'http://localhost:8000/swagger'

Redoc: 'http://localhost:8000/redoc'

OpenAPI JSON: `http://localhost:8000/swagger.json`
```