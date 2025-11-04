# Personal Notes Manager - Backend API

This is a Django REST Framework backend that provides authentication and CRUD operations for personal notes.

## Quick Start

- Install dependencies:
  - pip install -r notes_backend/requirements.txt
- Run migrations:
  - python notes_backend/manage.py migrate
- (Optional) Load sample data:
  - python notes_backend/manage.py loaddata api/fixtures/sample_data.json
- Start server:
  - python notes_backend/manage.py runserver 0.0.0.0:3001

Environment:
- Copy notes_backend/.env.example to .env (same directory) and set DJANGO_SECRET_KEY.

## API Overview

Base path: /api/

- Health
  - GET /api/health/ -> {"message":"Server is up!"}

- Auth (session-based)
  - POST /api/auth/register/ {username, email?, password}
  - POST /api/auth/login/ {username, password}
  - POST /api/auth/logout/

- Notes (authenticated)
  - GET /api/notes/?archived=true|false
  - POST /api/notes/ {title, content, is_archived?}
  - GET /api/notes/{id}/
  - PUT/PATCH /api/notes/{id}/
  - DELETE /api/notes/{id}/
  - POST /api/notes/{id}/archive/
  - POST /api/notes/{id}/unarchive/

Permissions:
- Users can only access their own notes.

API Docs:
- Swagger UI at /docs
- Redoc at /redoc