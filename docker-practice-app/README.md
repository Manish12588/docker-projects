# 🐳 Docker Practice App

A minimal, beginner-friendly project to learn how **Flask**, **PostgreSQL**, and **Redis** talk to each other inside Docker containers — with a live health dashboard to see everything at a glance.

---

## Project Structure

```
docker-practice-app/
│
├── app/                        # Flask Python API
│   ├── app.py                  # Main application + health endpoints
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # How to build the Flask container
│
├── dashboard/
│   └── index.html              # Health dashboard (HTML + CSS + JS)
│
├── nginx/
│   └── nginx.conf              # Nginx config (serves the dashboard)
│
├── docker-compose.yml          # Orchestrates all containers together
├── .env                        # Environment variables (secrets/config)
├── .gitignore
└── docker-practice-app.code-workspace   # VS Code workspace file
```

---

## Prerequisites

| Tool | Install |
|------|---------|
| Docker Desktop | https://www.docker.com/products/docker-desktop |
| VS Code | https://code.visualstudio.com |
| VS Code Docker extension | Install from the Extensions panel |

---

## Quick Start

```bash
# 1. Open this folder in VS Code
code docker-practice-app.code-workspace

# 2. Start all containers
docker compose up --build

# 3. Open the dashboard
open http://localhost:8080

# 4. Test the API directly
open http://localhost:5000/health
```

That's it! You'll see the dashboard show live status for all services.

---

## URLs at a Glance

| URL | What it is |
|-----|-----------|
| `http://localhost:8080` | Health dashboard |
| `http://localhost:5000` | Flask API root |
| `http://localhost:5000/health` | All services status (JSON) |
| `http://localhost:5000/health/postgres` | PostgreSQL only |
| `http://localhost:5000/health/redis` | Redis only |
| `http://localhost:5000/health/flask` | Flask API only |

---

## How to Add a New Service

Follow these **4 steps** every time you want to monitor a new container.

---

### Step 1 — Add the service to `docker-compose.yml`

Open `docker-compose.yml` and add a new block under `services:`.  
Find the comment `# ── ADD NEW SERVICES HERE` and add below it:

```yaml
  nginx:
    image: nginx:alpine
    container_name: practice_nginx
    ports:
      - "80:80"
    depends_on:
      - flask
```

---

### Step 2 — Add a health endpoint in `app/app.py`

Open `app/app.py`. Find the comment `# ── Add a new health endpoint below` and add:

```python
@app.route("/health/nginx")
def health_nginx():
    import urllib.request
    try:
        urllib.request.urlopen("http://nginx:80", timeout=3)
        return jsonify({"service": "Nginx", "status": "running"})
    except Exception as e:
        return jsonify({"service": "Nginx", "status": "stopped"})
```

Also add the service to the `/health` master route inside the `services` dict:

```python
"Nginx": check_nginx(),   # add this line
```

---

### Step 3 — Add the service to the dashboard

Open `dashboard/index.html`. Find the `SERVICES` array and add:

```js
{
  name:     "Nginx",
  desc:     "Reverse proxy / load balancer",
  port:     "80",
  endpoint: "http://localhost:5000/health/nginx"
},
```

---

### Step 4 — Restart Docker Compose

```bash
docker compose up --build
```

Reload `http://localhost:8080` — your new service row appears automatically.

---

## Useful Docker Commands

```bash
# Start everything (rebuild if code changed)
docker compose up --build

# Start in background (detached)
docker compose up -d

# Stop everything
docker compose down

# Stop and delete all volumes (wipes database data!)
docker compose down -v

# See logs for one service
docker compose logs flask
docker compose logs postgres

# Follow logs live
docker compose logs -f flask

# List running containers
docker ps

# Open a shell inside a container
docker exec -it practice_flask bash
docker exec -it practice_postgres psql -U admin practicedb
docker exec -it practice_redis redis-cli
```

---

## How the Health Check Works

```
Browser → http://localhost:8080        (Dashboard served by Nginx)
              ↓  JS calls every 30s
         http://localhost:5000/health/postgres
         http://localhost:5000/health/redis
         http://localhost:5000/health/flask
              ↓
         Flask API (in Docker)
              ↓  checks real connections
         PostgreSQL container
         Redis container
```

Each route in `app.py` tries to make a real connection to the service and returns either `"connected"`, `"running"`, or `"stopped"`.

---

## Environment Variables

All configuration lives in `.env`:

| Variable | Default | Used by |
|----------|---------|---------|
| `POSTGRES_DB` | `practicedb` | postgres, flask |
| `POSTGRES_USER` | `admin` | postgres, flask |
| `POSTGRES_PASSWORD` | `secret` | postgres, flask |
| `REDIS_HOST` | `redis` | flask |
| `REDIS_PORT` | `6379` | flask |

> ⚠️ Never commit `.env` with real passwords to Git. The `.gitignore` already excludes it.

---

## Customising the Dashboard

All colours are CSS variables at the top of `dashboard/index.html`:

```css
:root {
  --bg:      #0d1117;   /* page background   */
  --surface: #161b22;   /* card background   */
  --green:   #3fb950;   /* healthy status    */
  --yellow:  #d29922;   /* starting status   */
  --red:     #f85149;   /* stopped status    */
  --accent:  #58a6ff;   /* blue highlights   */
}
```

Change a value, save, and refresh the browser.

---

## Quick Cheatsheet for Adding a Service

```
1. docker-compose.yml  →  add service block
2. app/app.py          →  add @app.route("/health/<name>")
3. dashboard/index.html →  add object to SERVICES array
4. docker compose up --build
```
