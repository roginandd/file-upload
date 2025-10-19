import os
import logging
from flask import Flask
from config import Config
from extensions import db  # ✅ import shared db here

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)  # ✅ binds db to this Flask app

    # Configure logging
    os.makedirs(app.config['LOG_FOLDER'], exist_ok=True)
    logging.basicConfig(
        filename=f"{app.config['LOG_FOLDER']}/app.log",
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )

    # Import blueprints after db setup
    from controllers.file_controller import file_bp
    app.register_blueprint(file_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
