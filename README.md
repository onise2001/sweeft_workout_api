# Sweeft Workout API

A RESTful API for a fitness application that allows users to design custom workouts, track progress, and manage exercise routines. Users can select exercises from a predefined database, customize their workout parameters, and track their progress in real-time. Since this not a production application I kept few things simple to save time, for example the security, with cors_allow_all_origins=True and allowed_hosts=['*'],also I did not use the .env file from the start so you could find the SECRET_KEY in my commit history, also the scheduling system is simple with only being able to choose week days, also the goal tracking system is a little confusing since i track weight loss goal and progression on exercises in a single model.

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
```

- Create a '.env' file (not tracked in git) and populate it according to .env.example or the following:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

```bash
# Run with docker
docker compose up -d
```

### 2. Without Docker

```bash
# Clone and setup
git clone https://github.com/onise2001/sweeft_workout_api.git
cd sweeft_workout_api
```
- Create a '.env' file (not tracked in git) and populate it according to .env.example or the following:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

```bash
# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux
# or
.\venv\Scripts\activate  # Windows

# Dependencies and setup
pip install -r requirements.txt
python manage.py collectstatic
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

To test endpoints that require authentication from Swagger docs you must find the `api/auth/signup/` endpoint in swagger documentation, register with username and password, and then find `api/auth/login/` endpoint and enter the credentials of the user you just registered and execute, you will get two tokens in response, access and refresh, you should copy the access token, without the double quotes and then scroll to the top of the page and find the Autorization button and click on it, in th input field enter: Bearer, follwoed by space and then the token you copied.

### Hope you have pleasent experience with my project and thank you Sweeft for considering me for this role.