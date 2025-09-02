#!/usr/bin/env python3
"""
Setup script for the Flask application
Installs dependencies and initializes the database
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"  Error: {e.stderr}")
        return False

def setup_project():
    """Set up the Flask project"""
    print("🚀 Setting up Flask Dynamic Store Project")
    print("=" * 50)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Please check your Python environment.")
        return False
    
    # Initialize Flask-Migrate
    print("\n📦 Setting up database migrations...")
    if not os.path.exists('migrations'):
        if run_command("flask db init", "Initializing Flask-Migrate"):
            print("✓ Flask-Migrate initialized")
        else:
            print("⚠️  Flask-Migrate initialization failed, continuing with basic setup...")
    else:
        print("✓ Flask-Migrate already initialized")
    
    # Create initial migration
    if os.path.exists('migrations'):
        if run_command("flask db migrate -m 'Initial migration'", "Creating initial migration"):
            print("✓ Initial migration created")
        else:
            print("⚠️  Migration creation failed, using basic database setup...")
    
    # Apply migrations or create tables
    if os.path.exists('migrations'):
        if run_command("flask db upgrade", "Applying migrations"):
            print("✓ Database migrations applied")
        else:
            print("⚠️  Migration failed, falling back to basic table creation...")
            run_command("python manage_db.py init-db", "Creating database tables")
    else:
        run_command("python manage_db.py init-db", "Creating database tables")
    
    # Seed database with sample data
    run_command("python manage_db.py seed-db", "Seeding database with sample data")
    
    # Create upload directory
    upload_dir = "website/static/uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir, exist_ok=True)
        print(f"✓ Created upload directory: {upload_dir}")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("  1. Run the application: python app.py")
    print("  2. Open your browser to: http://localhost:5000")
    print("  3. Login with admin credentials:")
    print("     Email: admin@admin.com")
    print("     Password: admin123")
    print("\n📚 Useful commands:")
    print("  python manage_db.py --help        # Database management")
    print("  flask db --help                   # Migration commands")
    print("  python app.py                     # Run the application")

if __name__ == "__main__":
    setup_project()