import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

db = SQLAlchemy()
login_manager = LoginManager()

def normalize_db_url(url: str) -> str:
    # Render often provides postgres://; SQLAlchemy prefers postgresql://
    return url.replace("postgres://", "postgresql://", 1) if url.startswith("postgres://") else url

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    # Prefer DATABASE_URL (Render), else fall back to local sqlite
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = normalize_db_url(db_url)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Server-side sessions to keep cart stable across workers
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from .models import User  # noqa

    # Blueprints
    from .routes import bp as main_bp
    from .auth import bp as auth_bp
    from .checkout import bp as checkout_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(checkout_bp, url_prefix="/checkout")

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
