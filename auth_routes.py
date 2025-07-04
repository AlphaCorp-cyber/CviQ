from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import Admin
from app import db

# Create blueprint for authentication routes
auth_bp = Blueprint('admin_auth', __name__, url_prefix='/admin')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))

        if not email or not password:
            flash('Please provide both email and password.', 'error')
            return render_template('admin/login.html')

        admin = Admin.query.filter_by(email=email).first()

        if admin and admin.check_password(password) and admin.is_active:
            admin.last_login = datetime.utcnow()
            db.session.commit()
            login_user(admin, remember=remember)

            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/admin'):
                return redirect(next_page)
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('admin/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Admin logout"""
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('admin_auth.login'))

@auth_bp.route('/setup', methods=['GET', 'POST'])
def setup():
    """Initial admin setup - only available if no admins exist"""
    # Check if any admin exists
    if Admin.query.first():
        flash('Admin account already exists. Please log in.', 'info')
        return redirect(url_for('admin_auth.login'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validation
        if not all([name, email, password, confirm_password]):
            flash('All fields are required.', 'error')
            return render_template('admin/setup.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('admin/setup.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('admin/setup.html')

        # Check if email already exists
        if Admin.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return render_template('admin/setup.html')

        # Create new admin
        admin = Admin()
        admin.name = name
        admin.email = email
        admin.set_password(password)

        db.session.add(admin)
        db.session.commit()

        flash('Admin account created successfully! Please log in.', 'success')
        return redirect(url_for('admin_auth.login'))

    return render_template('admin/setup.html')

