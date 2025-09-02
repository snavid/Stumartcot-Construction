#!/usr/bin/env python3
"""
Flask CLI commands for database management
"""

import click
from flask.cli import with_appcontext
from website import create_app, db
from website.models import User, Category, Product, ProductReview, ProductImage

app = create_app()

@app.cli.command()
@with_appcontext
def init_db():
    """Initialize the database with tables."""
    db.create_all()
    click.echo('Database tables created.')

@app.cli.command()
@with_appcontext
def reset_db():
    """Reset the database (drop all tables and recreate)."""
    db.drop_all()
    db.create_all()
    click.echo('Database reset complete.')

@app.cli.command()
@with_appcontext
def seed_db():
    """Seed the database with sample data."""
    from werkzeug.security import generate_password_hash
    import json
    
    # Create admin user if it doesn't exist
    admin = User.query.filter_by(email='admin@admin.com').first()
    if not admin:
        admin_user = User(
            email='admin@admin.com',
            username='admin',
            first_name='Admin',
            last_name='User',
            password=generate_password_hash('admin123', method='pbkdf2:sha256'),
            is_admin=True
        )
        db.session.add(admin_user)
    
    # Create sample categories
    categories_data = [
        {'name': 'Wall Tiles', 'description': 'Premium wall tiles for bathrooms and kitchens'},
        {'name': 'Floor Tiles', 'description': 'Durable floor tiles for all spaces'},
        {'name': 'Mosaic Tiles', 'description': 'Decorative mosaic tiles for accent walls'},
        {'name': 'Natural Stone', 'description': 'Natural stone tiles for elegant finishes'}
    ]
    
    for cat_data in categories_data:
        if not Category.query.filter_by(name=cat_data['name']).first():
            category = Category(**cat_data)
            db.session.add(category)
    
    db.session.commit()
    
    # Create sample products
    wall_tiles_cat = Category.query.filter_by(name='Wall Tiles').first()
    if wall_tiles_cat and not Product.query.filter_by(name='Premium Ceramic Wall Tiles').first():
        sample_features = [
            "Water resistant and easy to clean",
            "Durable ceramic construction", 
            "Multiple color options available",
            "Professional installation support",
            "5-year manufacturer warranty"
        ]
        
        sample_sizes = ["12x12", "18x18", "24x24"]
        sample_colors = ["White", "Beige", "Gray", "Blue"]
        sample_tags = ["ceramic", "tiles", "bathroom", "kitchen", "wall"]
        
        sample_product = Product(
            name='Premium Ceramic Wall Tiles',
            description='Premium ceramic wall tiles perfect for bathrooms and kitchens. These high-quality tiles offer excellent durability, water resistance, and easy maintenance.',
            price=45.00,
            original_price=55.00,
            category_id=wall_tiles_cat.id,
            user_id=admin.id if admin else 1,
            stock_quantity=100,
            weight=35.0,
            dimensions='12x12x0.3',
            features=json.dumps(sample_features),
            available_sizes=json.dumps(sample_sizes),
            available_colors=json.dumps(sample_colors),
            tags=json.dumps(sample_tags),
            is_active=True,
            is_featured=True
        )
        db.session.add(sample_product)
    
    db.session.commit()
    click.echo('Database seeded with sample data.')

if __name__ == '__main__':
    app.run(debug=True)