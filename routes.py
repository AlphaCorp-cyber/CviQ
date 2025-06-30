from flask import Blueprint, request, jsonify, current_app
from twilio.twiml.messaging_response import MessagingResponse
import logging

from whatsapp_bot import WhatsAppBot

main_bp = Blueprint('main', __name__)
bot = WhatsAppBot()

@main_bp.route('/')
def index():
    return """
    <h1>WhatsApp CV Maker Bot</h1>
    <p>This is the WhatsApp CV Maker Bot backend.</p>
    <p>Send a message to the bot on WhatsApp to get started!</p>
    <a href="/admin">Admin Panel</a>
    """

@main_bp.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages via Twilio webhook"""
    try:
        # Get the message data
        incoming_msg = request.form.get('Body', '').strip()
        from_number = request.form.get('From', '')
        media_url = request.form.get('MediaUrl0', '')
        
        logging.info(f"Received message from {from_number}: {incoming_msg}")
        
        # Create Twilio response object
        response = MessagingResponse()
        
        # Process the message through the bot
        reply_message = bot.process_message(from_number, incoming_msg, media_url)
        
        # Add the reply to the response
        msg = response.message()
        msg.body(reply_message)
        
        logging.info(f"Sending reply: {reply_message}")
        
        return str(response)
    
    except Exception as e:
        logging.error(f"Error in webhook: {str(e)}")
        response = MessagingResponse()
        msg = response.message()
        msg.body("Sorry, something went wrong. Please try again later.")
        return str(response)

@main_bp.route('/status')
def status():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'WhatsApp CV Maker Bot'
    })
