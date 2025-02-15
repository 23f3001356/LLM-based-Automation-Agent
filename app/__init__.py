from flask import Flask

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__)

    # Import and register blueprints or routes if needed
    from .api import app as api_app  # Import the main API module
    app.register_blueprint(api_app)

    return app