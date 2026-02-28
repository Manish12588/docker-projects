import time
from app import create_app
from app.services import db_service

# ── DB init with retry (Postgres may not be ready immediately) ────────────────
for attempt in range(10):
    try:
        db_service.init_db()
        print("✅ DB initialized")
        break
    except Exception as e:
        print(f"⏳ Waiting for DB... ({attempt + 1}/10): {e}")
        time.sleep(2)
else:
    print("❌ Could not connect to DB. Exiting.")
    raise SystemExit(1)

# ── Start Flask ───────────────────────────────────────────────────────────────
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
