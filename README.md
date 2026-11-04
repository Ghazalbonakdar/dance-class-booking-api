# Dance Class Booking API

A RESTful API built with Django and Django REST Framework for managing dance classes and student enrollments.

## Project Overview

The Dance Class Booking API allows users to manage dance classes and student registrations.

The API supports:
- Creating, viewing, updating, and deleting dance classes.
- Viewing the number of enrolled students.
- Checking the number of available spots in each class.
- Enrolling students in dance classes.
- Cancelling student enrollments.
- Preventing duplicate enrollments.
- Validating class capacity and enrollment data.

## Technologies Used

- Python
- Django
- Django REST Framework
- SQLite

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ghazalbonakdar/dance-class-booking-api.git
cd dance-class-booking-api
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it:

**macOS / Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

The API will be available at:

`http://127.0.0.1:8000/`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/classes/` | Retrieve all dance classes |
| POST | `/api/classes/` | Create a dance class |
| GET | `/api/classes/<id>/` | Retrieve a specific class |
| PATCH | `/api/classes/<id>/` | Update a dance class |
| DELETE | `/api/classes/<id>/` | Delete a dance class |
| POST | `/api/classes/<id>/enroll/` | Enroll a student |
| POST | `/api/classes/<id>/cancel/` | Cancel a student enrollment |

## Validation Rules

- Class capacity must be greater than zero.
- Class capacity cannot be reduced below the current number of enrollments.
- A student cannot enroll in a class that has reached its capacity.
- The same student email cannot be registered twice for the same class.
- Enrollment cancellation frees an available spot.

## Database Models

The project contains two main models:

**DanceClass**

Stores information about each dance class, including its title, instructor, level, capacity, date, and start time.

**Enrollment**

Stores student enrollment information and has a foreign key relationship with `DanceClass`.

A student can enroll in multiple classes, but their email address must be unique within each individual class.

## Project Structure

```text
danceclassbooking/
├── bookings/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   └── urls.py
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## License

This project was created as an educational programming assignment.