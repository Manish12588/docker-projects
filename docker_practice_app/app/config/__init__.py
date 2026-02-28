import os


class Config:
    # ── PostgreSQL ────────────────────────────────────────────────────────────
    POSTGRES_HOST     = os.getenv("POSTGRES_HOST", "db")
    POSTGRES_PORT     = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB       = os.getenv("POSTGRES_DB", "practicedb")
    POSTGRES_USER     = os.getenv("POSTGRES_USER", "admin")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")

    # ── Redis ─────────────────────────────────────────────────────────────────
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    # ── Cache ─────────────────────────────────────────────────────────────────
    CACHE_TTL = 15  # seconds — short so you can observe hit/miss easily
