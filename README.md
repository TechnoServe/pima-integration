# PIMA Integration

A Flask-based ETL service that receives webhooks from **CommCare**, stores payloads in **Firestore**, and processes them into a **PostgreSQL** database. Deployed on Google Cloud Run.

---

## How It Works

1. CommCare submits form data via webhook to `/save-payload/<source>`
2. The payload is stored in Firestore with status `new`
3. `/process-jobs/<source>` picks up new jobs and routes them to the correct orchestrator
4. Processed records are written to PostgreSQL; job status is updated in Firestore
5. Failed jobs can be retried via `/retry-job/<source>`

### Supported Form Types

| Form Name | Orchestrator |
|---|---|
| Farmer Registration / Edit Farmer Details / Field Day Farmer Registration | Participant Registration & Update |
| Attendance Full / Field Day Attendance Full | Attendance Full |
| Attendance Light | Attendance Light |
| Training Observation / Demo Plot Observation | Observation |
| Farm Visit Full / Farm Visit - AA | Farm Visit |
| Wet Mill Registration Form | Wetmill Registration |
| Wet Mill Visit | Wetmill Visit |

---

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL instance
- Google Cloud project with Firestore and Cloud Run enabled
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TechnoServe/pima-integration.git
   cd pima-integration
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** — create a `.env` file in the root:
   ```env
   SYSTEM_USER_ID_TEST=<your-system-user-id>
   DATABASE_URL=postgresql://user:password@localhost:5432/pima
   GOOGLE_APPLICATION_CREDENTIALS=<path-to-your-service-account.json>
   ```

5. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start the app:**
   ```bash
   python app/main.py
   ```
   The app runs on `http://localhost:8080`.

---

## Usage & Examples

### API Endpoints

#### Save a payload (webhook receiver)
```
POST /save-payload/<source>
```
`source` can be `commcare` or `cc`.

```bash
curl -X POST http://localhost:8080/save-payload/commcare \
  -H "Content-Type: application/json" \
  -d '{"id": "abc123", "form": {"@name": "Farmer Registration", ...}}'
```

#### Process new jobs
```
GET /process-jobs/<source>
```
Picks up to 10 `new` jobs from Firestore and processes them into PostgreSQL.

```bash
curl http://localhost:8080/process-jobs/commcare
```

#### Retry failed jobs
```
# Auto-retry all failed jobs (up to 3 retries)
GET /retry-job/<source>

# Retry a single job
GET /retry-job/<source>/<job_id>

# Bulk retry by list of IDs
POST /retry-job/<source>
Content-Type: application/json
{"ids": ["id1", "id2"]}
```

#### Job status summary
```
GET /status-count/<source>
```
Returns counts for `new`, `processing`, `failed`, and `completed` jobs.

#### Get failed jobs
```
GET /failed-jobs/<source>?start_date=2025-01-01&end_date=2025-12-31&job_name=Farmer Registration
```

#### Fetch payloads
```
# All payloads (optional ?limit=20)
GET /get-payload/<source>

# Single payload
GET /get-payload/<source>/<job_id>

# Bulk fetch
POST /get-payload/<source>
Content-Type: application/json
{"ids": ["id1", "id2"]}
```

#### Bulk update payloads
```
POST /update-payloads/<source>
Content-Type: application/json
{"status": "new", "run_retries": 0, "job_ids": ["id1", "id2"]}
```

### Build & Deploy to Google Cloud Run

**Build the container image:**
```bash
gcloud builds submit --tag gcr.io/pima-gcp/pima-integration-app
```

**Deploy:**
```bash
gcloud run deploy pima-integration-app \
  --image gcr.io/pima-gcp/pima-integration-app \
  --platform managed \
  --allow-unauthenticated \
  --region europe-west1 \
  --network=default \
  --subnet=default
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "describe your change"

# Apply migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1
```

---

## Project Structure

```
pima-integration/
├── app/
│   ├── core/               # DB init, Firestore utils, logging, mapping
│   ├── jobs/
│   │   └── commcare_to_postgresql/   # Orchestrators per form type
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   └── main.py             # Flask app & routes
├── alembic/                # Migration environment
├── migrations/             # Migration scripts
├── requirements.txt
└── pyproject.toml
```

---

## Contributing

1. **Fork** the repo and create a branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** — add an orchestrator in `jobs/commcare_to_postgresql/` and register it in the `job_mapping` in `main.py`.

3. **Write tests** using `pytest`:
   ```bash
   pytest
   ```

4. **Commit** with a clear message:
   ```bash
   git commit -m "feat: add support for new form type"
   ```

5. **Push** and open a **Pull Request** against `main`.

### Adding a New Form Type

1. Create a new orchestrator file in `app/jobs/commcare_to_postgresql/`
2. Implement a class with a `process_data(payload, system_id)` method
3. Export it from `app/jobs/commcare_to_postgresql/__init__.py`
4. Add the mapping in `job_mapping` in `main.py`
5. Add it to `MIGRATED_FORM_TYPES` in `core` if it should be processed

---

## Built With

- [Flask](https://flask.palletsprojects.com/) — Web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) + [Alembic](https://alembic.sqlalchemy.org/) — ORM & migrations
- [Google Cloud Firestore](https://cloud.google.com/firestore) — Job queue & status tracking
- [Google Cloud Run](https://cloud.google.com/run) — Deployment
- [psycopg2](https://www.psycopg.org/) — PostgreSQL driver
- [GeoAlchemy2](https://geoalchemy-2.readthedocs.io/) + [Shapely](https://shapely.readthedocs.io/) — Geospatial support

---

*Maintained by [TechnoServe](https://github.com/TechnoServe)*
