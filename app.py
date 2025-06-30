import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "whatsapp-cv-maker-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///whatsapp_cv_maker.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Configure upload settings
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['CV_FOLDER'] = 'generated_cvs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Twilio configuration
app.config['TWILIO_ACCOUNT_SID'] = os.environ.get("TWILIO_ACCOUNT_SID")
app.config['TWILIO_AUTH_TOKEN'] = os.environ.get("TWILIO_AUTH_TOKEN")
app.config['TWILIO_PHONE_NUMBER'] = os.environ.get("TWILIO_PHONE_NUMBER")

# Initialize the app with the extension
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_auth.login'
login_manager.login_message = 'Please log in to access the admin panel.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    return Admin.query.get(int(user_id))

# Ensure upload directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CV_FOLDER'], exist_ok=True)

with app.app_context():
    # Import models to ensure tables are created
    import models  # noqa: F401

    # Create all tables
    db.create_all()

    # Initialize default templates
    from models import Template
    if not Template.query.first():
        default_templates = [
            Template(
                name="Modern Professional",
                description="Clean and modern design suitable for all industries",
                is_premium=False,
                template_file="template1.py"
            ),
            Template(
                name="Executive Classic", 
                description="Traditional professional layout for senior positions",
                is_premium=False,
                template_file="template2.py"
            ),
            Template(
                name="Creative Modern",
                description="Colorful and modern design for creative professionals",
                is_premium=True,
                template_file="template3.py"
            ),
            Template(
                name="Minimalist",
                description="Clean and simple design focusing on content",
                is_premium=False,
                template_file="template4.py"
            ),
            Template(
                name="Technical Professional",
                description="Designed for IT and technical professionals",
                is_premium=True,
                template_file="template5.py"
            ),
            Template(
                name="Sales Professional",
                description="Designed for sales and business development professionals",
                is_premium=True,
                template_file="template6.py"
            ),
            Template(
                name="Academic",
                description="Designed for researchers, professors, and academic professionals",
                is_premium=False,
                template_file="template7.py"
            ),
            Template(
                name="Healthcare Professional",
                description="Designed for doctors, nurses, and healthcare professionals",
                is_premium=True,
                template_file="template8.py"
            ),
            Template(
                name="Finance Professional",
                description="Designed for banking, finance, and investment professionals",
                is_premium=True,
                template_file="template9.py"
            ),
            Template(
                name="Creative Arts",
                description="Designed for artists, designers, and creative professionals",
                is_premium=True,
                template_file="template10.py"
            )
        ]

        for template in default_templates:
            db.session.add(template)

        db.session.commit()
        logging.info("Default templates initialized")

# Register blueprints
from routes import main_bp
from admin_routes import admin_bp

app.register_blueprint(main_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')

# Import and register auth blueprint
from auth_routes import auth_bp
app.register_blueprint(auth_bp)