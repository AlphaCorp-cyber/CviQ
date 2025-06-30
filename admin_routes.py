from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app import db
from models import User, Template, CV, Transaction
import json

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
def dashboard():
    """Admin dashboard with key metrics"""
    # Get key metrics
    total_users = User.query.count()
    total_cvs = CV.query.count()
    premium_users = User.query.filter_by(is_premium=True).count()
    recent_cvs = CV.query.order_by(CV.created_at.desc()).limit(10).all()
    
    # Get registration stats for the last 7 days
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_registrations = User.query.filter(User.created_at >= seven_days_ago).count()
    
    # Revenue calculation (mock)
    completed_transactions = Transaction.query.filter_by(status='completed').all()
    total_revenue = sum(t.amount for t in completed_transactions)
    
    # Template usage stats
    template_stats_query = db.session.query(
        Template.name,
        db.func.count(CV.id).label('usage_count')
    ).join(CV).group_by(Template.id, Template.name).all()
    
    # Convert to serializable format
    template_stats = [[stat.name, stat.usage_count] for stat in template_stats_query]
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_cvs=total_cvs,
                         premium_users=premium_users,
                         recent_registrations=recent_registrations,
                         total_revenue=total_revenue,
                         recent_cvs=recent_cvs,
                         template_stats=template_stats)

@admin_bp.route('/users')
@login_required
def users():
    """User management page"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<int:user_id>')
def user_detail(user_id):
    """User detail page"""
    user = User.query.get_or_404(user_id)
    user_cvs = CV.query.filter_by(user_id=user_id).order_by(CV.created_at.desc()).all()
    user_transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.created_at.desc()).all()
    
    return render_template('admin/user_detail.html',
                         user=user,
                         user_cvs=user_cvs,
                         user_transactions=user_transactions)

@admin_bp.route('/templates')
def templates():
    """Template management page"""
    templates = Template.query.order_by(Template.created_at.desc()).all()
    return render_template('admin/templates.html', templates=templates)

@admin_bp.route('/templates/add', methods=['GET', 'POST'])
def add_template():
    """Add new template"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        is_premium = request.form.get('is_premium') == 'on'
        template_file = request.form.get('template_file')
        
        if name and template_file:
            template = Template()
            template.name = name
            template.description = description
            template.is_premium = is_premium
            template.template_file = template_file
            
            db.session.add(template)
            db.session.commit()
            
            flash('Template added successfully!', 'success')
            return redirect(url_for('admin.templates'))
        else:
            flash('Name and template file are required!', 'error')
    
    return render_template('admin/add_template.html')

@admin_bp.route('/templates/<int:template_id>/edit', methods=['GET', 'POST'])
def edit_template(template_id):
    """Edit template details"""
    template = Template.query.get_or_404(template_id)
    
    if request.method == 'POST':
        template.name = request.form.get('name')
        template.description = request.form.get('description')
        template.is_premium = request.form.get('is_premium') == 'on'
        template.template_file = request.form.get('template_file')
        
        db.session.commit()
        flash(f'Template {template.name} updated successfully!', 'success')
        return redirect(url_for('admin.templates'))
    
    return render_template('admin/edit_template.html', template=template)

@admin_bp.route('/templates/<int:template_id>/toggle')
def toggle_template(template_id):
    """Toggle template active status"""
    template = Template.query.get_or_404(template_id)
    template.is_active = not template.is_active
    db.session.commit()
    
    status = 'activated' if template.is_active else 'deactivated'
    flash(f'Template {template.name} has been {status}!', 'success')
    
    return redirect(url_for('admin.templates'))

@admin_bp.route('/templates/<int:template_id>/toggle-premium')
def toggle_premium(template_id):
    """Toggle template premium status"""
    template = Template.query.get_or_404(template_id)
    template.is_premium = not template.is_premium
    db.session.commit()
    
    status = 'premium' if template.is_premium else 'free'
    flash(f'Template {template.name} is now {status}!', 'success')
    
    return redirect(url_for('admin.templates'))

@admin_bp.route('/templates/<int:template_id>/preview')
def preview_template(template_id):
    """Generate a preview CV for the template"""
    template = Template.query.get_or_404(template_id)
    
    # Sample CV data for preview
    sample_cv_data = {
        'full_name': 'John Smith',
        'email': 'john.smith@email.com',
        'phone': '+1 (555) 123-4567',
        'address': '123 Main Street, City, State 12345',
        'summary': 'Experienced professional with over 10 years in the industry. Proven track record of delivering high-quality results and leading successful teams. Passionate about innovation and continuous learning.',
        'experience': [
            'Senior Manager at Tech Corp\nJanuary 2020 - Present\nLead a team of 15 professionals in developing innovative solutions. Increased team productivity by 35% and reduced project delivery time by 20%. Managed multiple high-priority projects with budgets exceeding $2M.',
            'Project Manager at StartUp Inc\nMarch 2017 - December 2019\nOversaw product development lifecycle from conception to launch. Collaborated with cross-functional teams to deliver 5 successful product launches. Implemented agile methodologies that improved team efficiency by 25%.',
            'Business Analyst at Global Solutions\nJune 2014 - February 2017\nAnalyzed business requirements and translated them into technical specifications. Worked closely with stakeholders to identify process improvements. Contributed to a 15% increase in operational efficiency.'
        ],
        'education': [
            'Master of Business Administration\nHarvard Business School\n2014\nConcentration in Strategy and Operations',
            'Bachelor of Science in Computer Science\nStanford University\n2012\nGraduated Magna Cum Laude, GPA: 3.8/4.0'
        ],
        'skills': [
            'Project Management',
            'Strategic Planning',
            'Team Leadership',
            'Data Analysis',
            'Process Improvement',
            'Agile Methodologies',
            'Budget Management',
            'Stakeholder Relations',
            'Risk Assessment',
            'Performance Optimization'
        ]
    }
    
    try:
        from pdf_generator import PDFGenerator
        import tempfile
        import os
        from flask import send_file
        
        # Create temporary file for preview
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            temp_filepath = tmp_file.name
        
        # Generate preview PDF
        pdf_gen = PDFGenerator()
        
        # Get template generator
        import cv_templates
        template_module = getattr(cv_templates, template.template_file.replace('.py', ''))
        generator_class = getattr(template_module, 'TemplateGenerator')
        
        # Generate PDF
        generator = generator_class()
        success = generator.generate(sample_cv_data, temp_filepath)
        
        if success:
            def cleanup_file():
                try:
                    os.unlink(temp_filepath)
                except:
                    pass
            
            # Schedule cleanup after response
            from flask import after_this_request
            @after_this_request
            def remove_file(response):
                cleanup_file()
                return response
            
            return send_file(
                temp_filepath,
                as_attachment=False,
                download_name=f'{template.name}_preview.pdf',
                mimetype='application/pdf'
            )
        else:
            flash('Error generating template preview', 'error')
            return redirect(url_for('admin.templates'))
            
    except Exception as e:
        flash(f'Error generating preview: {str(e)}', 'error')
        return redirect(url_for('admin.templates'))

@admin_bp.route('/cvs')
def cvs():
    """CV management page"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    cvs = CV.query.order_by(CV.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/cvs.html', cvs=cvs)

@admin_bp.route('/transactions')
def transactions():
    """Transaction management page"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    transactions = Transaction.query.order_by(Transaction.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/transactions.html', transactions=transactions)

@admin_bp.route('/settings')
def settings():
    """System settings page"""
    return render_template('admin/settings.html')

@admin_bp.route('/settings/twilio', methods=['GET', 'POST'])
def twilio_settings():
    """Twilio configuration page"""
    if request.method == 'POST':
        account_sid = request.form.get('account_sid', '').strip()
        auth_token = request.form.get('auth_token', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        
        # Validate required fields
        if not account_sid or not auth_token or not phone_number:
            flash('All fields are required!', 'error')
            return render_template('admin/twilio_settings.html')
        
        # Validate account SID format
        if not account_sid.startswith('AC') or len(account_sid) != 34:
            flash('Invalid Account SID format. Should start with "AC" and be 34 characters long.', 'error')
            return render_template('admin/twilio_settings.html')
        
        # Validate phone number format
        if not phone_number.startswith('whatsapp:+'):
            flash('Phone number should start with "whatsapp:+" (e.g., whatsapp:+1234567890)', 'error')
            return render_template('admin/twilio_settings.html')
        
        # In Replit, we can write to a .env file that gets loaded
        import os
        
        # Create/update .env file
        env_content = f"""TWILIO_ACCOUNT_SID={account_sid}
TWILIO_AUTH_TOKEN={auth_token}
TWILIO_PHONE_NUMBER={phone_number}
DATABASE_URL={os.environ.get('DATABASE_URL', 'sqlite:///whatsapp_cv.db')}
SESSION_SECRET={os.environ.get('SESSION_SECRET', 'dev-secret-key')}
"""
        
        try:
            with open('.env', 'w') as f:
                f.write(env_content)
            
            # Update current environment
            os.environ['TWILIO_ACCOUNT_SID'] = account_sid
            os.environ['TWILIO_AUTH_TOKEN'] = auth_token
            os.environ['TWILIO_PHONE_NUMBER'] = phone_number
            
            # Update Flask app config
            from flask import current_app
            current_app.config['TWILIO_ACCOUNT_SID'] = account_sid
            current_app.config['TWILIO_AUTH_TOKEN'] = auth_token
            current_app.config['TWILIO_PHONE_NUMBER'] = phone_number
            
            flash('Twilio configuration saved successfully!', 'success')
        except Exception as e:
            flash(f'Error saving configuration: {str(e)}', 'error')
        
        return redirect(url_for('admin.twilio_settings'))
    
    return render_template('admin/twilio_settings.html')

@admin_bp.route('/api/stats')
def api_stats():
    """API endpoint for dashboard stats"""
    # Daily registration stats for the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    daily_registrations = db.session.query(
        db.func.date(User.created_at).label('date'),
        db.func.count(User.id).label('count')
    ).filter(User.created_at >= thirty_days_ago).group_by(
        db.func.date(User.created_at)
    ).all()
    
    # CV creation stats
    daily_cvs = db.session.query(
        db.func.date(CV.created_at).label('date'),
        db.func.count(CV.id).label('count')
    ).filter(CV.created_at >= thirty_days_ago).group_by(
        db.func.date(CV.created_at)
    ).all()
    
    return jsonify({
        'daily_registrations': [{'date': str(r.date), 'count': r.count} for r in daily_registrations],
        'daily_cvs': [{'date': str(r.date), 'count': r.count} for r in daily_cvs]
    })
