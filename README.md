# Stumartcot Construction & Building Materials

A comprehensive e-commerce platform for Stumartcot Co Ltd, featuring product catalog management, user authentication, and admin dashboard functionality.

## Features

- **Product Management**: Add, edit, delete products with images, specifications, and features
- **Category Management**: Organize products into categories
- **User Management**: Admin and regular user roles
- **Review System**: Customer reviews and ratings
- **Inventory Tracking**: Stock quantity management
- **File Upload**: Unique filename generation to prevent overwrites
- **Responsive Design**: Mobile-friendly interface
- **Database Migrations**: Flask-Migrate for schema management

## Quick Setup

1. **Install and Setup**:
   ```bash
   python setup.py
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access the Application**:
   - Open your browser to: http://localhost:5000
   - Admin login: admin@admin.com / admin123

## Manual Setup

If you prefer manual setup:

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database**:
   ```bash
   # Using Flask-Migrate (recommended)
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   
   # Or using basic setup
   python manage_db.py init-db
   ```

3. **Seed Sample Data**:
   ```bash
   python manage_db.py seed-db
   ```

## Database Management

### Flask-Migrate Commands

```bash
# Initialize migrations (one time only)
flask db init

# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations to database
flask db upgrade

# Rollback last migration
flask db downgrade

# Show migration history
flask db history

# Show current migration
flask db current
```

### Custom Database Commands

```bash
# Initialize database tables
python manage_db.py init-db [--drop]

# Seed database with sample data
python manage_db.py seed-db

# Reset database (drop and recreate)
python manage_db.py reset-db

# Show all database tables
python manage_db.py show-tables
```

## Project Structure

```
├── website/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── views.py             # Main routes
│   ├── auth.py              # Authentication routes
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, images
├── migrations/              # Database migrations
├── instance/                # Database file
├── app.py                   # Application entry point
├── manage_db.py             # Database management CLI
├── setup.py                 # Project setup script
└── requirements.txt         # Python dependencies
```

## Models

### User
- Email, username, first_name, last_name
- Admin privileges
- Relationships with products and reviews

### Category
- Name, description, image
- Relationships with products

### Product
- Basic info: name, description, price, original_price
- Details: features, specifications, dimensions, weight
- Options: available_sizes, available_colors
- Inventory: stock_quantity
- Status: is_active, is_featured
- SEO: meta_title, meta_description, tags
- Relationships with category, user, reviews, images

### ProductReview
- Rating (1-5 stars), title, comment
- Verification and approval status
- Relationships with product and user

### ProductImage
- Multiple images per product
- Alt text and sort order
- Primary image designation

## File Upload

The system automatically generates unique filenames to prevent overwrites:
- Format: `originalname_YYYYMMDD_HHMMSS_uniqueid.ext`
- Example: `product_20250209_143052_a1b2c3d4.jpg`

## Admin Features

- User management (create, delete users)
- Category management (add, edit, delete categories)
- Product management (add, edit, delete products)
- Dashboard with statistics and recent activity

## User Features

- Product browsing and search
- Category filtering
- Product detail views with reviews
- Personal dashboard for managing own products

## Development

### Adding New Models

1. Update `models.py` with new model
2. Create migration: `flask db migrate -m "Add new model"`
3. Apply migration: `flask db upgrade`

### Database Schema Changes

1. Modify existing models in `models.py`
2. Generate migration: `flask db migrate -m "Description"`
3. Review the generated migration file
4. Apply migration: `flask db upgrade`

## Contact

Project by Mr. Stuart Kimaro  
Phone: +255769226111  
Company: Stumartcot Co Ltd
