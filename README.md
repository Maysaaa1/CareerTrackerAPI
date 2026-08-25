# CareerTracker API

A REST API for tracking job applications through the hiring process — from the day you apply to the final outcome. Built with Django REST Framework, secured with JWT, and backed by PostgreSQL.

---

## Tech stack

- **Django 6.0** · **Django REST Framework 3.17**
- **Authentication:** JWT via `djangorestframework-simplejwt`
- **Database:** PostgreSQL (`psycopg 3`)
- **Testing:** Postman

---

## Features

- Register an account and authenticate with JWT access and refresh tokens
- Create, read, update and delete job applications
- Track each application's status through the hiring pipeline

---

## Authentication

The API uses JWT. Obtain a token pair, then send the access token on every protected request:

```
Authorization: Bearer <access_token>
```

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/token/` | Obtain access + refresh tokens |
| POST | `/api/token/refresh/` | Exchange a refresh token for a new access token |

---

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/applications/` | List your job applications |
| POST | `/api/applications/` | Add a new application |
| GET | `/api/applications/{id}/` | Retrieve a single application |
| PUT | `/api/applications/{id}/` | Update an application |
| DELETE | `/api/applications/{id}/` | Delete an application |

Example request body:

```json
{
  "company": "Diraya Software",
  "position": "Backend Developer",
  "status": "Applied",
  "applied_date": "2026-08-01",
  "notes": "Referred by a friend"
}
```

---

## Running locally

```bash
git clone https://github.com/Maysaaa1/CareerTrackerAPI.git
cd CareerTrackerAPI
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a PostgreSQL database, then add a `.env` file in the project root:

```
SECRET_KEY=your-secret-key
DB_NAME=career_tracker
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

Then:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API runs at `http://127.0.0.1:8000/api/`.

---

## Roadmap

- [ ] Unit tests for views and serializers
- [ ] Filtering and search on the applications list
- [ ] Pagination
- [ ] Deployment (Railway / Render)

---

## Author

**Maysaa Alatrash** — Backend Developer
GitHub: [@Maysaaa1](https://github.com/Maysaaa1) · maysaaalatrash1@gmail.com
