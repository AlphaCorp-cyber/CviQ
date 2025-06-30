import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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
                name="Creative Designer",
                description="Stylish template for creative professionals",
                is_premium=True,
                template_file="template1.py"
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
