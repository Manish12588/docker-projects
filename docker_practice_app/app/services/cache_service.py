import json
import redis
from app.config import Config

NOTES_CACHE_KEY = "notes:all"


def get_client() -> redis.Redis:
    """Return a Redis client instance."""
    return redis.Redis(
        host=Config.REDIS_HOST,
        port=Config.REDIS_PORT,
        decode_responses=True,
    )


def ping() -> bool:
    """Return True if Redis is reachable."""
    return get_client().ping()


def get_notes() -> list | None:
    """Return cached notes list, or None on a miss."""
    raw = get_client().get(NOTES_CACHE_KEY)
    return json.loads(raw) if raw else None


def get_notes_ttl() -> int:
    """Return remaining TTL in seconds for the notes cache key."""
    return get_client().ttl(NOTES_CACHE_KEY)


def set_notes(notes: list) -> None:
    """Store notes in Redis with the configured TTL."""
    get_client().setex(NOTES_CACHE_KEY, Config.CACHE_TTL, json.dumps(notes))


def invalidate_notes() -> None:
    """Delete the notes cache key (e.g. after a write)."""
    get_client().delete(NOTES_CACHE_KEY)


def flush_all() -> None:
    """Flush the entire Redis DB (useful for manual testing)."""
    get_client().flushdb()


def get_stats() -> dict:
    """Return hit/miss counters and current key count."""
    r = get_client()
    info     = r.info("stats")
    keyspace = r.info("keyspace")
    return {
        "redis_hits":   info.get("keyspace_hits", 0),
        "redis_misses": info.get("keyspace_misses", 0),
        "redis_keys":   sum(v.get("keys", 0) for v in keyspace.values()) if keyspace else 0,
    }
