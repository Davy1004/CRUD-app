import os
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from database.db import db
from config import config
from routes.user_routes import user_bp
from logger_config import LoggerSetup, get_logger
import time
import traceback

# Initialize logger
logger = get_logger(__name__)


def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config.get(config_name, config['development']))

    # Setup logging
    LoggerSetup.setup_logging(app)

    # Initialize database
    db.init_app(app)

    # Enable CORS
    CORS(
        app,
        resources={r"/*": {"origins": "http://localhost:4200"}}
    )

    # Request/Response logging middleware
    @app.before_request
    def log_request_info():
        """Log incoming request information"""
        g.start_time = time.time()
        app.logger.debug(f"REQUEST: {request.method} {request.path}")
        app.logger.debug(f"Headers: {dict(request.headers)}")
        if request.method in ['POST', 'PUT'] and request.is_json:
            app.logger.debug(f"Body: {request.get_json()}")

    @app.after_request
    def log_response_info(response):
        """Log response information"""
        if hasattr(g, 'start_time'):
            elapsed = time.time() - g.start_time
            app.logger.info(
                f"RESPONSE: {request.method} {request.path} - "
                f"Status: {response.status_code} - Time: {elapsed:.3f}s"
            )
        return response

    @app.errorhandler(Exception)
    def handle_error(error):
        """Global error handler"""
        app.logger.error(f"UNHANDLED ERROR: {str(error)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/api')

    # Create database tables
    with app.app_context():
        db.create_all()
        app.logger.info("Database tables initialized")

    return app


if __name__ == "__main__":
    app = create_app('development')
    app.logger.info("Starting Flask development server...")
