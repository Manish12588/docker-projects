from flask import Blueprint, jsonify, request
from app.services import db_service, cache_service
from app.config import Config

notes_bp = Blueprint("notes", __name__, url_prefix="/notes")


@notes_bp.get("/")
def list_notes():
    """Return all notes — served from Redis cache when fresh."""
    cached = cache_service.get_notes()

    if cached is not None:
        return jsonify({
            "notes":     cached,
            "source":    "cache",
            "cache_ttl": cache_service.get_notes_ttl(),
        })

    notes = db_service.get_all_notes()
    cache_service.set_notes(notes)

    return jsonify({
        "notes":     notes,
        "source":    "database",
        "cache_ttl": Config.CACHE_TTL,
    })


@notes_bp.post("/")
def create_note():
    """Insert a note and invalidate the cache."""
    data    = request.get_json(force=True)
    content = (data.get("content") or "").strip()
    author  = (data.get("author")  or "Anonymous").strip() or "Anonymous"

    if not content:
        return jsonify({"error": "content is required"}), 400

    result = db_service.insert_note(content, author)
    cache_service.invalidate_notes()

    return jsonify({
        "id":         result["id"],
        "content":    content,
        "author":     author,
        "created_at": result["created_at"],
    }), 201


@notes_bp.delete("/<int:note_id>")
def delete_note(note_id):
    """Delete a note by id and invalidate the cache."""
    deleted = db_service.delete_note(note_id)
    if not deleted:
        return jsonify({"error": "Note not found"}), 404

    cache_service.invalidate_notes()
    return jsonify({"deleted": note_id})
