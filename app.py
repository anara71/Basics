from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from auth import auth_bp, bcrypt
from api import api_bp
import os
from datetime import timedelta

def create_app():
    """Application factory"""
    app = Flask(__name__, static_folder='static', static_url_path='')

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Support both DATABASE_URL (Heroku) and SQLALCHEMY_DATABASE_URI
    database_url = os.environ.get('DATABASE_URL') or os.environ.get('SQLALCHEMY_DATABASE_URI')
    if database_url:
        # Heroku uses postgres:// but SQLAlchemy needs postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///billionaire_tracker.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    JWTManager(app)
    CORS(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')

    # Serve frontend
    @app.route('/')
    def index():
        return send_from_directory('static', 'index.html')

    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

    return app


# Create app instance for WSGI servers (gunicorn, etc.)
app = create_app()

if __name__ == '__main__':
    print("Starting Billionaire Relationship Tracker...")
    print("Server running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
