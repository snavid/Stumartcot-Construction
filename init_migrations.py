#!/usr/bin/env python3
"""
Initialize Flask-Migrate for the project
Run this script once to set up migrations
"""

import os
import sys
from flask import Flask
from flask_migrate import init, migrate, upgrade

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from website import create_app

def initialize_migrations():
    """Initialize Flask-Migrate for the project"""
    app = create_app()
    
    with app.app_context():
        print("Initializing Flask-Migrate...")
        
        # Check if migrations folder already exists
        if not os.path.exists('migrations'):
            print("Creating migrations repository...")
            init()
            print("✓ Migrations repository created")
        else:
            print("✓ Migrations repository already exists")
        
        # Create initial migration
        print("Creating initial migration...")
        try:
            migrate(message='Initial migration with all models')
            print("✓ Initial migration created")
        except Exception as e:
            print(f"Migration creation: {e}")
        
        # Apply migrations
        print("Applying migrations to database...")
        try:
            upgrade()
            print("✓ Migrations applied successfully")
        except Exception as e:
            print(f"Migration upgrade: {e}")
        
        print("\nFlask-Migrate setup complete!")
        print("\nUseful commands:")
        print("  flask db migrate -m 'description'  # Create new migration")
        print("  flask db upgrade                   # Apply migrations")
        print("  flask db downgrade                 # Rollback migrations")
        print("  flask db history                   # Show migration history")

if __name__ == "__main__":
    initialize_migrations()