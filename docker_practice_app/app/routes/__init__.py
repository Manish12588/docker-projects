from app.routes.notes  import notes_bp
from app.routes.system import system_bp
from app.routes.ui     import ui_bp


def register_routes(app):
    """Attach all blueprints to the Flask app."""
    app.register_blueprint(ui_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(system_bp)
