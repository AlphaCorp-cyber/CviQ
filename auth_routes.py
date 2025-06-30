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

@auth_bp.route('/check-admin')
def check_admin():
    """Debug route to check admin accounts"""
    admin_count = Admin.query.count()
    admins = Admin.query.all()

    result = f"Total admin accounts: {admin_count}<br><br>"

    if admins:
        result += "Existing admins:<br>"
        for admin in admins:
            result += f"- ID: {admin.id}, Email: {admin.email}, Name: {getattr(admin, 'name', 'N/A')}, Active: {admin.is_active}, Created: {admin.created_at}<br>"
            result += f"  Password Hash: {'Set' if admin.password_hash else 'Missing'}<br><br>"
    else:
        result += "No admin accounts found. Visit /admin/setup to create one."

    result += f"<br><a href='/admin/fix-admin'>Fix Admin Account</a>"
    return result

@auth_bp.route('/fix-admin')
def fix_admin():
    """Fix admin account with None values"""
    admin = Admin.query.filter_by(email='admin@cvmaker.com').first()
    
    if admin:
        # Fix None values
        if admin.is_active is None:
            admin.is_active = True
        if admin.created_at is None:
            admin.created_at = datetime.utcnow()
        if not hasattr(admin, 'name') or admin.name is None:
            admin.name = 'Admin User'
            
        db.session.commit()
        return f"Fixed admin account: {admin.email}<br><a href='/admin/check-admin'>Check Admin</a><br><a href='/admin/set-password'>Set Password</a><br><a href='/admin/login'>Login</a>"
    else:
        return "No admin account found to fix.<br><a href='/admin/check-admin'>Check Admin</a>"

@auth_bp.route('/set-password', methods=['GET', 'POST'])
def set_password():
    """Set password for admin account"""
    admin = Admin.query.filter_by(email='admin@cvmaker.com').first()
    
    if not admin:
        return "No admin account found.<br><a href='/admin/check-admin'>Check Admin</a>"
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not password or not confirm_password:
            return "Both password fields are required.<br><a href='/admin/set-password'>Try Again</a>"
        
        if password != confirm_password:
            return "Passwords do not match.<br><a href='/admin/set-password'>Try Again</a>"
        
        if len(password) < 6:
            return "Password must be at least 6 characters long.<br><a href='/admin/set-password'>Try Again</a>"
        
        # Set the password
        admin.set_password(password)
        db.session.commit()
        
        return f"Password set successfully for {admin.email}!<br><a href='/admin/login'>Login Now</a>"
    
    return '''
    <html>
    <head><title>Set Admin Password</title></head>
    <body>
        <h2>Set Password for admin@cvmaker.com</h2>
        <form method="POST">
            <div>
                <label>New Password:</label><br>
                <input type="password" name="password" required minlength="6">
            </div><br>
            <div>
                <label>Confirm Password:</label><br>
                <input type="password" name="confirm_password" required minlength="6">
            </div><br>
            <button type="submit">Set Password</button>
        </form>
        <br>
        <a href="/admin/check-admin">Back to Check Admin</a>
    </body>
    </html>
    '''