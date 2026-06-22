import time
import traceback

from flask import Flask, request, jsonify, g
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from database.db import db
# Import models so SQLAlchemy registers them before db.create_all().
# Without these imports the projects/tasks tables are silently never created.
from models.user import User
from models.project import Project
from models.task import Task
from config import config
from routes.user_routes import user_bp
from routes.project_routes import project_bp
from routes.task_routes import task_bp
from logger_config import LoggerSetup, get_logger

# Initialize logger
logger = get_logger(__name__)


def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(
        config.get(config_name, config['development'])
    )

    # Setup logging
    LoggerSetup.setup_logging(app)

    # Initialize database
    db.init_app(app)

    # Enable CORS
    CORS(app)

    # -------------------------
    # Request Logging
    # -------------------------
    @app.before_request
    def log_request_info():
        g.start_time = time.time()

        app.logger.debug(
            f"REQUEST: {request.method} {request.path}"
        )

        if request.method in ['POST', 'PUT'] and request.is_json:
            app.logger.debug(
                f"Body: {request.get_json()}"
            )

    # -------------------------
    # Response Logging
    # -------------------------
    @app.after_request
    def log_response_info(response):
        if hasattr(g, 'start_time'):
            elapsed = time.time() - g.start_time

            app.logger.info(
                f"RESPONSE: {request.method} {request.path} - "
                f"Status: {response.status_code} - "
                f"Time: {elapsed:.3f}s"
            )

        return response

    # -------------------------
    # Home Route
    # -------------------------
    @app.route('/')
    def home():
        return jsonify({
            "message": "CRUD API is running successfully",
            "status": "healthy"
        })

    # -------------------------
    # Error Handler
    # -------------------------
    @app.errorhandler(Exception)
    def handle_error(error):

        # Handle normal HTTP errors (404, 405, etc.)
        if isinstance(error, HTTPException):
            return jsonify({
                "error": error.description
            }), error.code

        # Handle unexpected errors
        app.logger.error(
            f"UNHANDLED ERROR: {str(error)}"
        )

        app.logger.error(
            traceback.format_exc()
        )

        return jsonify({
            "error": "Internal server error"
        }), 500

    # -------------------------
    # Register Blueprints
    # -------------------------
    app.register_blueprint(
        user_bp,
        url_prefix='/api'
    )
    app.register_blueprint(
        project_bp,
        url_prefix='/api'
    )
    app.register_blueprint(
        task_bp,
        url_prefix='/api'
    )

    # -------------------------
    # Create Database Tables
    # -------------------------
    with app.app_context():
        db.create_all()
        app.logger.info(
            "Database tables initialized"
        )

    return app


# Global app instance for Gunicorn
# Global app instance for Gunicorn.
# On Render, set FLASK_CONFIG=production so ProductionConfig (Postgres) is used.
# Defaults to development locally.
import os
app = create_app(os.getenv('FLASK_CONFIG', 'development'))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
