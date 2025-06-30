from datetime import datetime
from app import db
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Admin authentication model
class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.email}>'

# WhatsApp users model
class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), unique=True, nullable=False)
    name = Column(String(100))
    email = Column(String(120))
    is_premium = Column(Boolean, default=False)
    conversation_state = Column(String(50), default='idle')
    conversation_data = Column(Text)  # JSON string to store CV data being built
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    cvs = relationship('CV', backref='user', lazy=True)
    transactions = relationship('Transaction', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.phone_number}>'

class Template(db.Model):
    __tablename__ = 'templates'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    is_premium = Column(Boolean, default=False)
    template_file = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    cvs = relationship('CV', backref='template', lazy=True)
    
    def __repr__(self):
        return f'<Template {self.name}>'

class CV(db.Model):
    __tablename__ = 'cvs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    template_id = Column(Integer, ForeignKey('templates.id'), nullable=False)
    
    # CV Content
    full_name = Column(String(100), nullable=False)
    email = Column(String(120))
    phone = Column(String(20))
    address = Column(Text)
    summary = Column(Text)
    experience = Column(Text)  # JSON string
    education = Column(Text)   # JSON string
    skills = Column(Text)      # JSON string
    profile_photo = Column(String(255))  # File path
    
    # File info
    file_path = Column(String(255))
    file_size = Column(Integer)
    
    # Metadata
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CV {self.full_name}>'

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Transaction details
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default='USD')
    payment_method = Column(String(50))  # EcoCash, etc.
    transaction_ref = Column(String(100))
    status = Column(String(20), default='pending')  # pending, completed, failed
    
    # Product info
    product_type = Column(String(50))  # premium_cv, editable_cv, cover_letter
    description = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    def __repr__(self):
        return f'<Transaction {self.transaction_ref}>'

class ConversationState(db.Model):
    __tablename__ = 'conversation_states'
    
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), unique=True, nullable=False)
    state = Column(String(50), nullable=False)
    data = Column(Text)  # JSON string for storing conversation data
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ConversationState {self.phone_number}: {self.state}>'
