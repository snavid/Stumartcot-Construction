from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'website/static/uploads'
    
    # Create upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .views import views
    from .auth import auth
    from .error_handlers import error_bp
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(error_bp, url_prefix='/')
    
    from .models import User, Category, Product
    
    # Add custom Jinja2 filters
    import json
    
    @app.template_filter('from_json')
    def from_json_filter(value):
        if value:
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    with app.app_context():
        db.create_all()
        
        # Create default admin user if it doesn't exist
        admin = User.query.filter_by(email='admin@admin.com').first()
        if not admin:
            from werkzeug.security import generate_password_hash
            admin_user = User(
                email='admin@admin.com',
                username='admin',
                first_name='Admin',
                last_name='User',
                password=generate_password_hash('admin123', method='pbkdf2:sha256'),
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
    
    return app