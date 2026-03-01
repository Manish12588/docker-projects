"""
app.py — Flask API
Connects to PostgreSQL and Redis, exposes health endpoints.
"""

import os
import time
import redis
import psycopg2
from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)

# ── Enable CORS for all routes (fixes browser cross-origin requests) ──
CORS(app)

# ── Config (read from environment variables set in docker-compose.yml) ──
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB   = os.getenv("POSTGRES_DB",   "practicedb")
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASS = os.getenv("POSTGRES_PASSWORD", "secret")

MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_DB   = os.getenv("MYSQL_DB",   "mysql_db")
MYSQL_USER = os.getenv("MYSQL_USER", "sql_user")
MYSQL_PASS = os.getenv("MYSQL_PASSWORD", "Test@123")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


# ── Helper: check PostgreSQL ──────────────────────────────────────────
def check_postgres():
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST, port=POSTGRES_PORT,
            dbname=POSTGRES_DB, user=POSTGRES_USER,
            password=POSTGRES_PASS, connect_timeout=3
        )
        conn.close()
        return "connected"
    except Exception as e:
        return "stopped"


# ── Helper: check Redis ───────────────────────────────────────────────
def check_redis():
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_timeout=3)
        r.ping()
        return "connected"
    except Exception as e:
        return "stopped"

# ── Helper: check MySQL ───────────────────────────────────────────────
def check_mysql():
    try:
        import pymysql
        conn = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=MYSQL_DB,
            connect_timeout=3
        )
        conn.close()
        return "connected"
    except Exception as e:
        print(f"MySQL error: {e}")
        return "stopped"

# ── Routes ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return jsonify({
        "app": "Docker Practice App",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route("/health")
def health():
    """Master health endpoint — returns status of every service."""
    postgres_status = check_postgres()
    redis_status    = check_redis()
    mysql_status    = check_mysql()
    flask_status    = "running"

    all_ok = (
        postgres_status == "connected" and
        redis_status    == "connected" and
        mysql_status    == "connected"
    )

    return jsonify({
        "services": {
            "PostgreSQL": postgres_status,
            "Redis":      redis_status,
            "MySQL": mysql_status,
            "Flask API":  flask_status,
        },
        "healthy": all_ok,
        "checked_at": datetime.utcnow().isoformat()
    }), 200 if all_ok else 207


@app.route("/health/postgres")
def health_postgres():
    status = check_postgres()
    return jsonify({"service": "PostgreSQL", "status": status})


@app.route("/health/redis")
def health_redis():
    status = check_redis()
    return jsonify({"service": "Redis", "status": status})


@app.route("/health/flask")
def health_flask():
    return jsonify({"service": "Flask API", "status": "running"})

@app.route("/health/mysql")
def health_mysql():
    status = check_mysql()
    return jsonify({"service": "MySQL", "status": status})



# ── Add a new health endpoint below when you add a new service ─────────
# Example for Nginx:
# @app.route("/health/nginx")
# def health_nginx():
#     import urllib.request
#     try:
#         urllib.request.urlopen("http://nginx:80", timeout=3)
#         return jsonify({"service": "Nginx", "status": "running"})
#     except:
#         return jsonify({"service": "Nginx", "status": "stopped"})


if __name__ == "__main__":
    # Wait a moment for databases to be ready on first boot
    time.sleep(2)
    app.run(host="0.0.0.0", port=5000, debug=True)
