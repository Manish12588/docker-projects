from flask import Blueprint, jsonify
from datetime import datetime
from app.services import db_service, cache_service

system_bp = Blueprint("system", __name__)


@system_bp.get("/health")
def health():
    """Check connectivity to Postgres and Redis."""
    status = {
        "postgres":  False,
        "redis":     False,
        "timestamp": datetime.utcnow().isoformat(),
    }

    try:
        db_service.ping()
        status["postgres"] = True
    except Exception as e:
        status["postgres_error"] = str(e)

    try:
        cache_service.ping()
        status["redis"] = True
    except Exception as e:
        status["redis_error"] = str(e)

    ok = status["postgres"] and status["redis"]
    return jsonify(status), 200 if ok else 503


@system_bp.get("/stats")
def stats():
    """Return Redis cache stats and Postgres row count."""
    return jsonify({
        "postgres_notes": db_service.count_notes(),
        **cache_service.get_stats(),
    })


@system_bp.post("/cache/flush")
def flush_cache():
    """Manually flush the entire Redis DB."""
    cache_service.flush_all()
    return jsonify({"message": "Cache flushed"})
