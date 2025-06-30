# WhatsApp CV Maker Bot

## Overview

This is a Flask-based WhatsApp bot that helps users create professional CVs through conversational interactions. The system integrates with Twilio for WhatsApp messaging and generates PDF CVs using custom templates.

## System Architecture

The application follows a modular Flask architecture with the following key components:

### Backend Architecture
- **Flask Web Framework**: Main application server handling webhook requests and admin panel
- **SQLAlchemy ORM**: Database abstraction layer with SQLite as default storage
- **Twilio Integration**: WhatsApp messaging through Twilio's API
- **Conversation State Management**: Stateful conversation handling for CV creation workflow
- **PDF Generation**: Custom PDF generation using ReportLab library

### Database Schema
- **Users**: Store phone numbers, names, premium status, and conversation states
- **Templates**: Manage CV template definitions and metadata
- **CVs**: Store generated CV records linked to users and templates
- **Transactions**: Track premium upgrade payments
- **ConversationState**: Manage ongoing conversation contexts

## Key Components

### 1. WhatsApp Bot (`whatsapp_bot.py`)
- Processes incoming messages from Twilio webhook
- Manages user registration and authentication
- Routes messages to conversation manager

### 2. Conversation Manager (`conversation_manager.py`)
- Implements state machine for CV creation workflow
- Handles different conversation states (welcome, data collection, template selection)
- Manages user input validation and data persistence

### 3. PDF Generator (`pdf_generator.py`)
- Creates professional PDF CVs using ReportLab
- Supports multiple template layouts
- Handles image embedding and formatting

### 4. Template System (`cv_templates/`)
- Modular template architecture
- Currently supports two templates: Modern Professional and Executive Classic
- Extensible design for adding new templates

### 5. Admin Panel
- User management interface
- CV generation analytics
- Template administration
- Revenue tracking for premium features

## Data Flow

1. **Message Reception**: Twilio webhook receives WhatsApp messages
2. **User Identification**: System identifies or creates user based on phone number
3. **State Management**: Conversation state determines message handling logic
4. **Data Collection**: Bot guides users through CV information gathering
5. **Template Selection**: Users choose from available CV templates
6. **PDF Generation**: System creates professional PDF using collected data
7. **Delivery**: Generated CV is sent back to user via WhatsApp

## External Dependencies

### Core Services
- **Twilio**: WhatsApp messaging API integration
- **ReportLab**: PDF generation library
- **SQLAlchemy**: Database ORM

### Frontend Dependencies
- **Bootstrap 5**: Admin panel UI framework
- **Font Awesome**: Icon library
- **Chart.js**: Analytics visualization
- **DataTables**: Table management in admin panel

### Environment Variables
- `TWILIO_ACCOUNT_SID`: Twilio account identifier
- `TWILIO_AUTH_TOKEN`: Twilio authentication token
- `TWILIO_PHONE_NUMBER`: WhatsApp business phone number
- `DATABASE_URL`: Database connection string
- `SESSION_SECRET`: Flask session encryption key

## Deployment Strategy

### Local Development
- SQLite database for development
- Flask development server on port 5000
- Debug mode enabled for error tracking

### Production Considerations
- Environment variable configuration for sensitive data
- Database migration support through SQLAlchemy
- File upload handling for profile photos
- Webhook endpoint security for Twilio integration

The application is designed to be easily deployable on platforms like Replit, Heroku, or similar PaaS providers with minimal configuration changes.

## Changelog
- June 30, 2025: Initial setup complete with working WhatsApp bot, CV generation, and full admin interface
- June 30, 2025: Fixed admin interface template errors and JSON serialization issues
- June 30, 2025: Added sample data for testing (templates, users, CVs, transactions)

## User Preferences

Preferred communication style: Simple, everyday language.