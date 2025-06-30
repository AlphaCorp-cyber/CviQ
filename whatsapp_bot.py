import json
import logging
from datetime import datetime
from app import db
from models import User, ConversationState, Template, CV
from conversation_manager import ConversationManager
from pdf_generator import PDFGenerator

class WhatsAppBot:
    def __init__(self):
        self.conversation_manager = ConversationManager()
        self.pdf_generator = PDFGenerator()
    
    def process_message(self, from_number, message, media_url=None):
        """Process incoming WhatsApp message and return appropriate response"""
        try:
            # Clean phone number (remove whatsapp: prefix if present)
            phone_number = from_number.replace('whatsapp:', '').strip()
            
            # Get or create user
            user = self.get_or_create_user(phone_number)
            
            # Get conversation state
            conv_state = self.get_conversation_state(phone_number)
            
            # Process the message based on current state
            response = self.conversation_manager.handle_message(
                user, conv_state, message, media_url
            )
            
            return response
            
        except Exception as e:
            logging.error(f"Error processing message: {str(e)}")
            return "Sorry, I encountered an error. Please try again later."
    
    def get_or_create_user(self, phone_number):
        """Get existing user or create new one (auto-registration)"""
        user = User.query.filter_by(phone_number=phone_number).first()
        
        if not user:
            # Auto-register new user
            user = User(
                phone_number=phone_number,
                conversation_state='welcome',
                created_at=datetime.utcnow(),
                last_active=datetime.utcnow()
            )
            db.session.add(user)
            db.session.commit()
            logging.info(f"Auto-registered new user: {phone_number}")
        else:
            # Update last active time
            user.last_active = datetime.utcnow()
            db.session.commit()
        
        return user
    
    def get_conversation_state(self, phone_number):
        """Get or create conversation state"""
        conv_state = ConversationState.query.filter_by(phone_number=phone_number).first()
        
        if not conv_state:
            conv_state = ConversationState(
                phone_number=phone_number,
                state='welcome',
                data='{}',
                updated_at=datetime.utcnow()
            )
            db.session.add(conv_state)
            db.session.commit()
        
        return conv_state
