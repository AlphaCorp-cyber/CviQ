import json
import logging
from datetime import datetime
from app import db
from models import User, ConversationState, Template, CV, Transaction

class ConversationManager:
    def __init__(self):
        self.states = {
            'welcome': self.handle_welcome,
            'menu': self.handle_menu,
            'collect_name': self.handle_collect_name,
            'collect_email': self.handle_collect_email,
            'collect_phone': self.handle_collect_phone,
            'collect_address': self.handle_collect_address,
            'collect_summary': self.handle_collect_summary,
            'collect_experience': self.handle_collect_experience,
            'collect_education': self.handle_collect_education,
            'collect_skills': self.handle_collect_skills,
            'select_template': self.handle_select_template,
            'select_color': self.handle_select_color,
            'profile_photo': self.handle_profile_photo,
            'premium_upgrade': self.handle_premium_upgrade,
            'payment': self.handle_payment
        }
    
    def handle_message(self, user, conv_state, message, media_url=None):
        """Route message to appropriate handler based on conversation state"""
        try:
            current_state = conv_state.state
            handler = self.states.get(current_state, self.handle_welcome)
            
            response = handler(user, conv_state, message, media_url)
            
            # Update conversation state timestamp
            conv_state.updated_at = datetime.utcnow()
            db.session.commit()
            
            return response
            
        except Exception as e:
            logging.error(f"Error in conversation manager: {str(e)}")
            return "Sorry, something went wrong. Let's start over. Type 'menu' to see options."
    
    def handle_welcome(self, user, conv_state, message, media_url=None):
        """Handle initial welcome and returning users"""
        # Check if returning user
        existing_cvs = CV.query.filter_by(user_id=user.id).count()
        
        if existing_cvs > 0:
            welcome_msg = f"Welcome back! 👋\n\nI see you've created {existing_cvs} CV(s) with me before.\n\n"
        else:
            welcome_msg = "Welcome to CV Maker Bot! 🎯\n\nI'll help you create a professional CV in minutes, delivered right here on WhatsApp!\n\n"
        
        menu_msg = self.get_main_menu()
        
        # Set state to menu
        conv_state.state = 'menu'
        db.session.commit()
        
        return welcome_msg + menu_msg
    
    def handle_menu(self, user, conv_state, message, media_url=None):
        """Handle main menu selections"""
        message = message.lower().strip()
        
        if message in ['1', 'create', 'new cv']:
            return self.start_cv_creation(user, conv_state)
        elif message in ['2', 'templates', 'view templates']:
            return self.show_templates(user, conv_state)
        elif message in ['3', 'my cvs', 'history']:
            return self.show_user_cvs(user, conv_state)
        elif message in ['4', 'premium', 'upgrade']:
            return self.show_premium_options(user, conv_state)
        elif message in ['5', 'help', 'support']:
            return self.show_help(user, conv_state)
        else:
            return "Please select a valid option (1-5) or type the action name:\n\n" + self.get_main_menu()
    
    def start_cv_creation(self, user, conv_state):
        """Start the CV creation process"""
        # Initialize CV data
        cv_data = {
            'full_name': '',
            'email': '',
            'phone': '',
            'address': '',
            'summary': '',
            'experience': [],
            'education': [],
            'skills': [],
            'profile_photo': None,
            'template_id': None
        }
        
        conv_state.state = 'collect_name'
        conv_state.data = json.dumps(cv_data)
        db.session.commit()
        
        return "Great! Let's create your professional CV! 📄✨\n\nFirst, what's your full name?"
    
    def handle_collect_name(self, user, conv_state, message, media_url=None):
        """Collect user's full name"""
        cv_data = json.loads(conv_state.data)
        cv_data['full_name'] = message.strip()
        
        conv_state.state = 'collect_email'
        conv_state.data = json.dumps(cv_data)
        db.session.commit()
        
        return f"Nice to meet you, {message.strip()}! 👋\n\nWhat's your email address?"
    
    def handle_collect_email(self, user, conv_state, message, media_url=None):
        """Collect user's email"""
        cv_data = json.loads(conv_state.data)
        cv_data['email'] = message.strip()
        
        conv_state.state = 'collect_phone'
        conv_state.data = json.dumps(cv_data)
        db.session.commit()
        
        return "Perfect! 📧\n\nWhat's your phone number?"
    
    def handle_collect_phone(self, user, conv_state, message, media_url=None):
        """Collect user's phone number"""
        cv_data = json.loads(conv_state.data)
        cv_data['phone'] = message.strip()
        
        conv_state.state = 'collect_address'
        conv_state.data = json.dumps(cv_data)
        db.session.commit()
        
        return "Got it! 📱\n\nWhat's your address? (City, Country is fine)"
    
    def handle_collect_address(self, user, conv_state, message, media_url=None):
        """Collect user's address"""
        cv_data = json.loads(conv_state.data)
        cv_data['address'] = message.strip()
        
        conv_state.state = 'collect_summary'
        conv_state.data = json.dumps(cv_data)
        db.session.commit()
        
        return "Great! 🏠\n\nNow, write a brief professional summary about yourself (2-3 sentences):"
    
    def handle_collect_summary(self, user, conv_state, message, media_url=None):
        """Collect professional summary"""
        cv_data = json.loads(conv_state.data)
        cv_data['summary'] = message.strip()
        
        conv_state.state = 'collect_experience'
        conv_state.data = json.dumps(cv_data)
        db.session.commit()
        
        return """Excellent! 💼

Now let's add your work experience. For each job, include:
- Job Title at Company Name
- Duration (e.g., Jan 2020 - Present)
- Key responsibilities/achievements

Send each job as a separate message, or type 'done' when finished."""
    
    def handle_collect_experience(self, user, conv_state, message, media_url=None):
        """Collect work experience"""
        cv_data = json.loads(conv_state.data)
        
        if message.lower().strip() == 'done':
            if not cv_data['experience']:
                return "Please add at least one work experience entry, or type 'skip' to continue without experience."
            
            conv_state.state = 'collect_education'
            conv_state.data = json.dumps(cv_data)
            db.session.commit()
            
            return """Perfect! 🎓

Now let's add your education. For each qualification, include:
- Degree/Certificate Name
- Institution Name
- Year/Duration
- Any honors or relevant details

Send each qualification as a separate message, or type 'done' when finished."""
        
        elif message.lower().strip() == 'skip':
            conv_state.state = 'collect_education'
            conv_state.data = json.dumps(cv_data)
            db.session.commit()
            
            return """No problem! 🎓

Let's add your education. For each qualification, include:
- Degree/Certificate Name
- Institution Name
- Year/Duration
- Any honors or relevant details

Send each qualification as a separate message, or type 'done' when finished."""
        
        else:
            # Add experience entry
            cv_data['experience'].append(message.strip())
            conv_state.data = json.dumps(cv_data)
            db.session.commit()
            
            return f"Added experience entry! ✅\n\nAdd another experience or type 'done' to continue.\n\nTotal entries: {len(cv_data['experience'])}"
    
    def handle_collect_education(self, user, conv_state, message, media_url=None):
        """Collect education information"""
        cv_data = json.loads(conv_state.data)
        
        if message.lower().strip() == 'done':
            if not cv_data['education']:
                return "Please add at least one education entry, or type 'skip' to continue without education."
            
            conv_state.state = 'collect_skills'
            conv_state.data = json.dumps(cv_data)
            db.session.commit()
            
            return """Great! 🛠️

Finally, let's add your skills. Examples:
- Technical skills (Python, Excel, Photoshop)
- Soft skills (Communication, Leadership)
- Languages (English, French)

Send all your skills in one message, separated by commas."""
        
        elif message.lower().strip() == 'skip':
            conv_state.state = 'collect_skills'
            conv_state.data = json.dumps(cv_data)
            db.session.commit()
            
            return """No problem! 🛠️

Let's add your skills. Examples:
- Technical skills (Python, Excel, Photoshop)
- Soft skills (Communication, Leadership)
- Languages (English, French)

Send all your skills in one message, separated by commas."""
        
        else:
            # Add education entry
            cv_data['education'].append(message.strip())
            conv_state.data = json.dumps(cv_data)
            db.session.commit()
            
            return f"Added education entry! ✅\n\nAdd another qualification or type 'done' to continue.\n\nTotal entries: {len(cv_data['education'])}"
    
    def handle_collect_skills(self, user, conv_state, message, media_url=None):
        """Collect skills"""
        cv_data = json.loads(conv_state.data)
        
        if message.lower().strip() == 'skip':
            skills = []
        else:
            # Split skills by comma and clean them
            skills = [skill.strip() for skill in message.split(',') if skill.strip()]
        
        cv_data['skills'] = skills
        
        conv_state.state = 'profile_photo'
        conv_state.data = json.dumps(cv_data)
        db.session.commit()
        
        return """Awesome! 📸

Would you like to add a profile photo to your CV?

1. Send a photo now
2. Skip photo

Type '1' and send photo, or '2' to skip."""
    
    def handle_profile_photo(self, user, conv_state, message, media_url=None):
        """Handle profile photo upload"""
        cv_data = json.loads(conv_state.data)
        
        if message.strip() == '2' or message.lower().strip() == 'skip':
            # Skip photo
            conv_state.state = 'select_template'
            conv_state.data = json.dumps(cv_data)
            db.session.commit()
            
            return self.show_template_selection(user)
        
        elif media_url:
            # Photo uploaded
            try:
                # Here you would normally download and save the photo
                # For now, we'll just store the URL
                cv_data['profile_photo'] = media_url
                
                conv_state.state = 'select_template'
                conv_state.data = json.dumps(cv_data)
                db.session.commit()
                
                return "Great photo! 📸✅\n\n" + self.show_template_selection(user)
            
            except Exception as e:
                logging.error(f"Error handling photo: {str(e)}")
                return "Sorry, couldn't process your photo. Let's continue without it.\n\n" + self.show_template_selection(user)
        
        else:
            return "Please send a photo or type '2' to skip."
    
    def handle_select_template(self, user, conv_state, message, media_url=None):
        """Handle template selection"""
        cv_data = json.loads(conv_state.data)
        
        try:
            template_choice = int(message.strip())
            
            # Get available templates
            if user.is_premium:
                templates = Template.query.filter_by(is_active=True).all()
            else:
                templates = Template.query.filter_by(is_active=True, is_premium=False).all()
            
            if 1 <= template_choice <= len(templates):
                selected_template = templates[template_choice - 1]
                cv_data['template_id'] = selected_template.id
                
                # Check if this is a premium template and ask for color selection
                if selected_template.is_premium and selected_template.template_file in ['template3.py', 'template5.py', 'template6.py', 'template8.py', 'template9.py', 'template10.py']:
                    conv_state.state = 'select_color'
                    conv_state.data = json.dumps(cv_data)
                    db.session.commit()
                    
                    return self.show_color_selection(selected_template)
                
                # For non-premium templates or basic templates, generate CV directly
                cv_data['color_scheme'] = 'blue'  # default color
                
                # Generate CV
                from pdf_generator import PDFGenerator
                pdf_gen = PDFGenerator()
                
                cv_file_path = pdf_gen.generate_cv(user, cv_data, selected_template)
                
                if cv_file_path:
                    # Save CV to database
                    new_cv = CV()
                    new_cv.user_id = user.id
                    new_cv.template_id = selected_template.id
                    new_cv.full_name = cv_data['full_name']
                    new_cv.email = cv_data['email']
                    new_cv.phone = cv_data['phone']
                    new_cv.address = cv_data['address']
                    new_cv.summary = cv_data['summary']
                    new_cv.experience = json.dumps(cv_data['experience'])
                    new_cv.education = json.dumps(cv_data['education'])
                    new_cv.skills = json.dumps(cv_data['skills'])
                    new_cv.profile_photo = cv_data.get('profile_photo')
                    new_cv.file_path = cv_file_path
                    new_cv.is_premium = selected_template.is_premium
                    new_cv.color_scheme = cv_data.get('color_scheme', 'blue')
                    
                    db.session.add(new_cv)
                    db.session.commit()
                    
                    # Reset conversation state
                    conv_state.state = 'menu'
                    conv_state.data = '{}'
                    db.session.commit()
                    
                    success_msg = f"🎉 Your CV has been created successfully!\n\n"
                    success_msg += f"Template: {selected_template.name}\n"
                    success_msg += f"Created: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}\n\n"
                    
                    if not user.is_premium:
                        success_msg += "💎 Want premium templates and editable formats?\n"
                        success_msg += "Type 'premium' to see upgrade options!\n\n"
                    
                    success_msg += self.get_main_menu()
                    
                    return success_msg
                else:
                    return "Sorry, there was an error generating your CV. Please try again."
            else:
                return f"Please select a valid template number (1-{len(templates)})."
                
        except ValueError:
            return "Please enter a number to select a template."
    
    def show_template_selection(self, user):
        """Show available templates for selection"""
        if user.is_premium:
            templates = Template.query.filter_by(is_active=True).all()
        else:
            templates = Template.query.filter_by(is_active=True, is_premium=False).all()
        
        msg = "Choose your CV template:\n\n"
        
        for i, template in enumerate(templates, 1):
            premium_icon = "💎" if template.is_premium else "🆓"
            msg += f"{i}. {premium_icon} {template.name}\n"
            msg += f"   {template.description}\n\n"
        
        msg += f"Type the number (1-{len(templates)}) to select:"
        
        return msg
    
    def show_templates(self, user, conv_state):
        """Show all available templates"""
        templates = Template.query.filter_by(is_active=True).all()
        
        msg = "📋 Available CV Templates:\n\n"
        
        free_templates = [t for t in templates if not t.is_premium]
        premium_templates = [t for t in templates if t.is_premium]
        
        msg += "🆓 FREE TEMPLATES:\n"
        for template in free_templates:
            msg += f"• {template.name}\n  {template.description}\n\n"
        
        if premium_templates:
            msg += "💎 PREMIUM TEMPLATES:\n"
            for template in premium_templates:
                msg += f"• {template.name}\n  {template.description}\n\n"
        
        msg += self.get_main_menu()
        
        return msg
    
    def show_user_cvs(self, user, conv_state):
        """Show user's CV history"""
        cvs = CV.query.filter_by(user_id=user.id).order_by(CV.created_at.desc()).all()
        
        if not cvs:
            msg = "You haven't created any CVs yet! 📄\n\n"
            msg += "Type '1' to create your first CV!\n\n"
        else:
            msg = f"📁 Your CVs ({len(cvs)} total):\n\n"
            
            for i, cv in enumerate(cvs[:5], 1):  # Show last 5 CVs
                premium_icon = "💎" if cv.is_premium else "🆓"
                template_name = cv.template.name if cv.template else "Unknown"
                msg += f"{i}. {premium_icon} {cv.full_name}\n"
                msg += f"   Template: {template_name}\n"
                msg += f"   Created: {cv.created_at.strftime('%Y-%m-%d')}\n\n"
            
            if len(cvs) > 5:
                msg += f"... and {len(cvs) - 5} more\n\n"
        
        msg += self.get_main_menu()
        return msg
    
    def show_premium_options(self, user, conv_state):
        """Show premium upgrade options"""
        if user.is_premium:
            msg = "🌟 You're already a Premium user!\n\n"
            msg += "Premium benefits:\n"
            msg += "✅ Access to all premium templates\n"
            msg += "✅ Editable Word format\n"
            msg += "✅ Cover letter templates\n"
            msg += "✅ Priority support\n\n"
        else:
            msg = "💎 Upgrade to Premium!\n\n"
            msg += "🎯 PREMIUM PACKAGES:\n\n"
            msg += "1. Premium Templates - $3 USD\n"
            msg += "   • Exclusive professional designs\n"
            msg += "   • Advanced layouts\n\n"
            msg += "2. Premium + Editable - $4 USD\n"
            msg += "   • Everything in Premium\n"
            msg += "   • Editable Word (.docx) format\n\n"
            msg += "3. Complete Package - $5 USD\n"
            msg += "   • Everything above\n"
            msg += "   • Cover letter templates\n"
            msg += "   • Priority support\n\n"
            msg += "Type the package number to upgrade!\n\n"
        
        msg += self.get_main_menu()
        return msg
    
    def handle_premium_upgrade(self, user, conv_state, message, media_url=None):
        """Handle premium upgrade selection"""
        try:
            choice = int(message.strip())
            
            packages = {
                1: {"name": "Premium Templates", "price": 3.0, "type": "premium_templates"},
                2: {"name": "Premium + Editable", "price": 4.0, "type": "premium_editable"},
                3: {"name": "Complete Package", "price": 5.0, "type": "complete_package"}
            }
            
            if choice in packages:
                package = packages[choice]
                
                # Create transaction record
                transaction = Transaction()
                transaction.user_id = user.id
                transaction.amount = package["price"]
                transaction.currency = "USD"
                transaction.payment_method = "EcoCash"
                transaction.status = "pending"
                transaction.product_type = package["type"]
                transaction.description = package["name"]
                
                db.session.add(transaction)
                db.session.commit()
                
                conv_state.state = 'payment'
                conv_state.data = json.dumps({"transaction_id": transaction.id})
                db.session.commit()
                
                msg = f"💳 Payment Required\n\n"
                msg += f"Package: {package['name']}\n"
                msg += f"Amount: ${package['price']} USD\n\n"
                msg += "💰 EcoCash Payment Instructions:\n"
                msg += "1. Dial *151#\n"
                msg += "2. Select 'Send Money'\n"
                msg += "3. Enter Merchant Code: 123456\n"
                msg += f"4. Enter Amount: ${package['price']}\n"
                msg += "5. Send payment reference here\n\n"
                msg += "Or type 'cancel' to cancel this upgrade."
                
                return msg
            else:
                return "Please select a valid package (1-3)."
                
        except ValueError:
            return "Please enter a number to select a package."
    
    def handle_payment(self, user, conv_state, message, media_url=None):
        """Handle payment confirmation"""
        if message.lower().strip() == 'cancel':
            conv_state.state = 'menu'
            conv_state.data = '{}'
            db.session.commit()
            
            return "Payment cancelled. No charges applied.\n\n" + self.get_main_menu()
        
        # Mock payment processing
        data = json.loads(conv_state.data)
        transaction_id = data.get('transaction_id')
        
        if transaction_id:
            transaction = Transaction.query.get(transaction_id)
            if transaction:
                # Mock payment success
                transaction.status = 'completed'
                transaction.transaction_ref = message.strip()
                transaction.completed_at = datetime.utcnow()
                
                # Upgrade user to premium
                user.is_premium = True
                
                db.session.commit()
                
                conv_state.state = 'menu'
                conv_state.data = '{}'
                db.session.commit()
                
                msg = "🎉 Payment successful!\n\n"
                msg += "✅ You're now a Premium user!\n"
                msg += "🎯 You now have access to:\n"
                msg += "• All premium CV templates\n"
                msg += "• Editable Word formats\n"
                msg += "• Cover letter templates\n"
                msg += "• Priority support\n\n"
                msg += "Create a new CV to try premium templates!\n\n"
                msg += self.get_main_menu()
                
                return msg
        
        return "Payment verification failed. Please try again or contact support."
    
    def show_help(self, user, conv_state):
        """Show help information"""
        msg = "🆘 Help & Support\n\n"
        msg += "HOW IT WORKS:\n"
        msg += "1. Choose 'Create New CV'\n"
        msg += "2. Follow the guided questions\n"
        msg += "3. Select a template\n"
        msg += "4. Receive your professional CV!\n\n"
        msg += "FEATURES:\n"
        msg += "• Instant PDF delivery\n"
        msg += "• Professional templates\n"
        msg += "• Profile photo support\n"
        msg += "• Premium upgrades available\n\n"
        msg += "SUPPORT:\n"
        msg += "Having issues? Contact us:\n"
        msg += "📧 support@cvmaker.com\n"
        msg += "📱 WhatsApp: +263 XXX XXX\n\n"
        msg += self.get_main_menu()
        
        return msg
    
    def show_color_selection(self, template):
        """Show color selection for premium templates"""
        msg = f"🎨 Choose a color scheme for {template.name}:\n\n"
        msg += "1. 💙 Blue - Professional and trustworthy\n"
        msg += "2. 💚 Green - Fresh and natural\n"
        msg += "3. ❤️ Red - Bold and energetic\n"
        msg += "4. 💜 Purple - Creative and innovative\n"
        msg += "5. 🧡 Orange - Warm and friendly\n"
        msg += "6. 🖤 Navy - Classic and sophisticated\n\n"
        msg += "Reply with the number of your preferred color scheme:"
        return msg
    
    def handle_select_color(self, user, conv_state, message, media_url=None):
        """Handle color scheme selection"""
        cv_data = json.loads(conv_state.data)
        
        color_map = {
            '1': 'blue',
            '2': 'green', 
            '3': 'red',
            '4': 'purple',
            '5': 'orange',
            '6': 'navy'
        }
        
        color_choice = message.strip()
        if color_choice in color_map:
            cv_data['color_scheme'] = color_map[color_choice]
            
            # Get the selected template
            template = Template.query.get(cv_data['template_id'])
            
            # Generate CV with selected color
            from pdf_generator import PDFGenerator
            pdf_gen = PDFGenerator()
            
            cv_file_path = pdf_gen.generate_cv(user, cv_data, template)
            
            if cv_file_path:
                # Save CV to database
                new_cv = CV()
                new_cv.user_id = user.id
                new_cv.template_id = template.id
                new_cv.full_name = cv_data['full_name']
                new_cv.email = cv_data['email']
                new_cv.phone = cv_data['phone']
                new_cv.address = cv_data['address']
                new_cv.summary = cv_data['summary']
                new_cv.experience = json.dumps(cv_data['experience'])
                new_cv.education = json.dumps(cv_data['education'])
                new_cv.skills = json.dumps(cv_data['skills'])
                new_cv.profile_photo = cv_data.get('profile_photo')
                new_cv.file_path = cv_file_path
                new_cv.is_premium = template.is_premium
                new_cv.color_scheme = cv_data['color_scheme']
                
                db.session.add(new_cv)
                db.session.commit()
                
                # Reset conversation
                conv_state.state = 'idle'
                conv_state.data = ''
                db.session.commit()
                
                # Send CV file via WhatsApp
                from twilio.rest import Client
                import os
                
                client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
                
                try:
                    # Upload file and send
                    with open(cv_file_path, 'rb') as file:
                        message = client.messages.create(
                            body=f"🎉 Your premium CV is ready!\n\nTemplate: {template.name}\nColor: {color_map[color_choice].title()}\n\n{self.get_main_menu()}",
                            from_=os.environ.get('TWILIO_PHONE_NUMBER'),
                            to=user.phone_number,
                            media_url=f"data:application/pdf;base64,{file.read()}"
                        )
                    
                    return f"🎉 Perfect! Your CV has been generated with {color_map[color_choice]} colors and sent to you!\n\n{self.get_main_menu()}"
                    
                except Exception as e:
                    logging.error(f"Error sending CV file: {str(e)}")
                    return f"✅ Your CV has been generated successfully!\n\nTemplate: {template.name}\nColor: {color_map[color_choice].title()}\n\n{self.get_main_menu()}"
            
            else:
                return "❌ Sorry, there was an error generating your CV. Please try again.\n\n" + self.get_main_menu()
        
        else:
            return "Please select a valid color option (1-6):\n\n" + self.show_color_selection(Template.query.get(cv_data['template_id']))
    
    def get_main_menu(self):
        """Get the main menu options"""
        return """🎯 MAIN MENU:

1. 📄 Create New CV
2. 📋 View Templates  
3. 📁 My CVs
4. 💎 Premium Upgrade
5. 🆘 Help & Support

Type a number (1-5) or the action name:"""
