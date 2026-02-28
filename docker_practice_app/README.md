# 🐳 Docker Practice App — Structured Edition

A multi-container Docker practice app with a clean, production-style Python project layout.

**Stack:** Flask (Python) · PostgreSQL · Redis

---

## 📁 Project Structure

```
docker_practice_app/
│
├── main.py                        # Entry point: DB init + Flask boot
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
│
├── app/
│   ├── __init__.py                # App factory (create_app)
│   │
│   ├── config/
│   │   └── __init__.py            # All env vars & constants (Config class)
│   │
│   ├── services/                  # Business logic — no Flask imports here
│   │   ├── __init__.py
│   │   ├── db_service.py          # All Postgres queries
│   │   └── cache_service.py       # All Redis operations
│   │
│   └── routes/                    # HTTP layer — thin, delegates to services
│       ├── __init__.py            # register_routes() helper
│       ├── notes.py               # GET/POST/DELETE /notes  (Blueprint)
│       ├── system.py              # /health  /stats  /cache/flush
│       └── ui.py                  # GET / (serves index.html)
│
└── templates/
    └── index.html                 # Frontend UI
```

### Separation of Concerns

| Layer | Folder | Responsibility |
|-------|--------|---------------|
| **Config** | `app/config/` | Reads env vars, defines constants |
| **Services** | `app/services/` | All DB & cache logic, no HTTP |
| **Routes** | `app/routes/` | HTTP in/out, calls services |
| **Entry point** | `main.py` | DB init retry + `create_app()` |

---

## 🚀 Quick Start

```bash
docker compose up --build
open http://localhost:5000

# Stop
docker compose down

# Stop + wipe volumes
docker compose down -v
```

---

## 🧪 Things to Practice

### Containers & Images
```bash
docker ps
docker images
docker compose build
docker compose logs -f web
```

### Exec into containers
```bash
docker exec -it practice_web bash
docker exec -it practice_postgres psql -U admin -d practicedb
docker exec -it practice_redis redis-cli
```

### Postgres queries
```sql
SELECT * FROM notes;
SELECT COUNT(*) FROM notes;
\dt
```

### Redis commands
```
KEYS *
GET notes:all
TTL notes:all
FLUSHDB
```

---

## 🌐 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Web UI |
| GET | `/health` | Postgres + Redis connectivity |
| GET | `/notes/` | List notes (cache-aware) |
| POST | `/notes/` | Create note `{"content":"…","author":"…"}` |
| DELETE | `/notes/<id>` | Delete note |
| GET | `/stats` | Cache hits/misses + DB row count |
| POST | `/cache/flush` | Manually flush Redis |
