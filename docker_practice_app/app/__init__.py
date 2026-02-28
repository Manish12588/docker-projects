from flask import Flask
from app.routes import register_routes


def create_app() -> Flask:
    """Application factory — creates and configures the Flask app."""
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    register_routes(app)

    return app
