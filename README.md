# CareerTracker API

A REST API for managing a job search end to end: the companies you're targeting, the applications you've sent, the interviews they lead to, and a full history of how each application's status changed over time.

Built with Django REST Framework, secured with JWT, and backed by PostgreSQL with constraints enforced at the database level rather than only in application code.

---

## Tech stack

- **Django 6.0** · **Django REST Framework 3.17**
- **Authentication:** JWT via `djangorestframework-simplejwt`
- **Database:** PostgreSQL (`psycopg 3`)
- **Testing:** Postman

---

## Data model

Four related models, each row owned by the user who created it.

### Company
The organisations a user is tracking.

| Field | Type | Notes |
|---|---|---|
| `owner` | FK → User | Cascade delete |
| `name` | CharField(150) | |
| `website` | URLField | Optional |
| `location` | CharField(150) | Optional |
| `industry` | CharField(100) | Optional |
| `description` | TextField | Optional |
| `created_at` / `updated_at` | DateTimeField | Auto-managed |

A `UniqueConstraint` on `(owner, name)` means one user can't save the same company twice, while two different users can each track the same company independently.

### JobApplication
An application to a company, moving through the hiring pipeline.

| Field | Type | Notes |
|---|---|---|
| `owner` | FK → User | |
| `company` | FK → Company | |
| `position_title` | CharField(150) | |
| `job_description` | TextField | Optional |
| `status` | Choice | `saved` · `applied` · `screening` · `interview` · `offer` · `rejected` · `withdrawn` |
| `source` | CharField(100) | Where the listing was found |
| `job_url` | URLField | Optional |
| `applied_date` | DateField | Nullable — an application can be saved before it's sent |
| `salary_min` / `salary_max` | Decimal(10,2) | Both optional |
| `notes` | TextField | Optional |

A `CheckConstraint` guarantees `salary_max >= salary_min` whenever both are set, so an invalid salary range can't reach the database even if a client skips validation.

### Interview
Interviews attached to an application.

| Field | Type | Notes |
|---|---|---|
| `job_application` | FK → JobApplication | |
| `interview_type` | Choice | `phone` · `hr` · `technical` · `managerial` · `final` · `other` |
| `scheduled_at` | DateTimeField | |
| `location_or_link` | CharField(255) | Room or video call URL |
| `interviewer_name` | CharField(150) | Optional |
| `result` | Choice | `pending` · `passed` · `failed` · `cancelled` |
| `notes` | TextField | Optional |

Ordered by `scheduled_at`, so the next interview comes first.

### ApplicationStatusHistory
An audit trail. Every status change is recorded with its old and new value and a timestamp, giving a full history of how an application progressed rather than only its current state.

| Field | Type |
|---|---|
| `job_application` | FK → JobApplication |
| `old_status` | Choice (blank on creation) |
| `new_status` | Choice |
| `changed_at` | DateTimeField |

---

## Authentication

Register, then obtain a JWT token pair and send the access token on every protected request:

```
Authorization: Bearer <access_token>
```

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Create a user account |
| POST | `/api/token/` | Obtain access + refresh tokens |
| POST | `/api/token/refresh/` | Exchange a refresh token for a new access token |

---

## Endpoints

### Companies

| Method | Endpoint |
|---|---|
| GET / POST | `/api/companies/` |
| GET / PUT / PATCH / DELETE | `/api/companies/{id}/` |

### Job applications

| Method | Endpoint |
|---|---|
| GET / POST | `/api/job-applications/` |
| GET / PUT / PATCH / DELETE | `/api/job-applications/{id}/` |

### Interviews

| Method | Endpoint |
|---|---|
| GET / POST | `/api/interviews/` |
| GET / PUT / PATCH / DELETE | `/api/interviews/{id}/` |

### Status history

| Method | Endpoint |
|---|---|
| GET | `/api/status-history/` |
| GET | `/api/status-history/{id}/` |

Example — creating a job application:

```json
{
  "company": 1,
  "position_title": "Backend Developer",
  "status": "applied",
  "source": "LinkedIn",
  "job_url": "https://example.com/jobs/123",
  "applied_date": "2026-08-01",
  "salary_min": "1200.00",
  "salary_max": "1800.00",
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

## Design notes

- **Ownership on the model.** `Company` and `JobApplication` both carry an `owner` foreign key, so records are scoped per user rather than shared globally.
- **Constraints in the database.** Uniqueness and the salary range rule are enforced by PostgreSQL, not only by serializer validation — they hold even for writes that bypass the API.
- **History over state.** Status changes are appended to `ApplicationStatusHistory` instead of only overwriting a field, so an application's full progression is recoverable.

---

## Roadmap

- [ ] Unit tests for views, serializers and constraints
- [ ] Filtering and search on the applications list (by status, company, date)
- [ ] Pagination
- [ ] Deployment (Railway / Render)

---

## Author

**Maysaa Alatrash** — Backend Developer
GitHub: [@Maysaaa1](https://github.com/Maysaaa1) · maysaaalatrash1@gmail.com
