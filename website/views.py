from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from .models import User, Category, Product, ProductImage
from . import db
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'avif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(original_filename):
    """Generate a unique filename to prevent overwrites"""
    if not original_filename:
        return None
    
    # Get the file extension
    filename = secure_filename(original_filename)
    name, ext = os.path.splitext(filename)
    
    # Generate unique filename using timestamp and UUID
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]  # First 8 characters of UUID
    
    # Create new filename: originalname_timestamp_uniqueid.ext
    unique_filename = f"{name}_{timestamp}_{unique_id}{ext}"
    
    return unique_filename

@views.route('/')
def home():
    categories = Category.query.all()
    products = Product.query.limit(8).all()  # Show latest 8 products
    return render_template("langingPage.html", categories=categories)

@views.route('/products')
def products():
    categories = Category.query.all()
    products = Product.query.limit(8).all()  # Show latest 8 products
    return render_template("products.html", categories=categories, products=products)

@views.route('/blog')
def blogs():
    return render_template("blog.html")

@views.route('/contact')
def contact():
    return render_template("contact.html")

@views.route('/cart')
def cart():
    return render_template("cart.html")    

@views.route('/showrooms')
def showrooms():
    return render_template("showrooms.html")

@views.route('/factories')
def factories():
    return render_template("factories.html")

@views.route('/retail-shops')
def retail_shops():
    return render_template("retail-shops.html")

@views.route('/construction-consultants')
def construction_consultants():
    return render_template("construction-consultants.html")

@views.route('/technical-support')
def technical_support():
    return render_template("technical-support.html")

@views.route('/product-single/<int:product_id>')
def product_single(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product-single.html", product=product)

@views.route('/sitemap.xml')
def sitemap():
    # Generate dynamic sitemap with actual categories and products
    return render_template("sitemap.xml", categories=Category.query.all(), products=Product.query.all())

@views.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        total_users = User.query.count()
        total_categories = Category.query.count()
        total_products = Product.query.count()
        recent_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()
        
        return render_template("admin_dashboard.html", 
                             user=current_user,
                             total_users=total_users,
                             total_categories=total_categories,
                             total_products=total_products,
                             recent_products=recent_products)
    else:
        user_products = Product.query.filter_by(user_id=current_user.id).all()
        return render_template("user_dashboard.html", user=current_user, products=user_products)

@views.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template("categories.html", user=current_user, categories=categories)

@views.route('/category/<int:category_id>')
def category_products(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    return render_template("category_products.html", user=current_user, category=category, products=products)

@views.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product_detail.html", user=current_user, product=product)

@views.route('/manage-categories')
@login_required
def manage_categories():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', category='error')
        return redirect(url_for('views.dashboard'))
    
    categories = Category.query.all()
    return render_template("manage_categories.html", user=current_user, categories=categories)

@views.route('/manage-products')
@login_required
def manage_products():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', category='error')
        return redirect(url_for('views.dashboard'))
    
    products = Product.query.all()
    return render_template("manage_products.html", user=current_user, products=products)

@views.route('/add-category', methods=['GET', 'POST'])
@login_required
def add_category():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', category='error')
        return redirect(url_for('views.dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        # Handle file upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = generate_unique_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename
        
        if len(name) < 1:
            flash('Category name is required.', category='error')
        else:
            new_category = Category(name=name, description=description, image=image_filename)
            db.session.add(new_category)
            db.session.commit()
            flash('Category added successfully!', category='success')
            return redirect(url_for('views.manage_categories'))
    
    return render_template("add_category.html", user=current_user)

@views.route('/manage-users')
@login_required
def manage_users():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', category='error')
        return redirect(url_for('views.dashboard'))
    
    users = User.query.all()
    return render_template("manage_users.html", user=current_user, users=users)

@views.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        original_price = request.form.get('original_price')
        category_id = request.form.get('category_id')
        stock_quantity = request.form.get('stock_quantity', 0)
        weight = request.form.get('weight')
        dimensions = request.form.get('dimensions')
        features = request.form.get('features')
        available_sizes = request.form.get('available_sizes')
        available_colors = request.form.get('available_colors')
        tags = request.form.get('tags')
        
        # Validate inputs
        if len(name) < 1:
            flash('Product name is required.', category='error')
        elif not price or float(price) <= 0:
            flash('Valid price is required.', category='error')
        elif not category_id:
            flash('Category is required.', category='error')
        else:
            # Convert features to JSON format
            import json
            features_list = []
            if features:
                features_list = [f.strip() for f in features.split('\n') if f.strip()]
            
            # Convert sizes and colors to JSON format
            sizes_list = []
            if available_sizes:
                sizes_list = [s.strip() for s in available_sizes.split(',') if s.strip()]
            
            colors_list = []
            if available_colors:
                colors_list = [c.strip() for c in available_colors.split(',') if c.strip()]
            
            tags_list = []
            if tags:
                tags_list = [t.strip() for t in tags.split(',') if t.strip()]
            
            # Create new product
            new_product = Product(
                name=name,
                description=description,
                price=float(price),
                original_price=float(original_price) if original_price else None,
                category_id=int(category_id),
                user_id=current_user.id,
                stock_quantity=int(stock_quantity) if stock_quantity else 0,
                weight=float(weight) if weight else None,
                dimensions=dimensions,
                features=json.dumps(features_list) if features_list else None,
                available_sizes=json.dumps(sizes_list) if sizes_list else None,
                available_colors=json.dumps(colors_list) if colors_list else None,
                tags=json.dumps(tags_list) if tags_list else None
            )
            db.session.add(new_product)
            db.session.flush()  # Get product ID before committing
            
            # Handle multiple image uploads
            if 'images' in request.files:
                files = request.files.getlist('images')
                for file in files:
                    if file and file.filename != '' and allowed_file(file.filename):
                        filename = generate_unique_filename(file.filename)
                        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                        product_image = ProductImage(image=filename, product_id=new_product.id)
                        db.session.add(product_image)
            
            db.session.commit()
            flash('Product added successfully!', category='success')
            return redirect(url_for('views.dashboard'))
    
    categories = Category.query.all()
    return render_template("add_product.html", user=current_user, categories=categories)

@views.route('/delete-user/<int:user_id>')
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', category='error')
        return redirect(url_for('views.dashboard'))
    
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete your own account.', category='error')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', category='success')
    
    return redirect(url_for('views.manage_users'))

@views.route('/edit-category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', category='error')
        return redirect(url_for('views.dashboard'))
    
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        # Handle file upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = generate_unique_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                category.image = filename
        
        if len(name) < 1:
            flash('Category name is required.', category='error')
        else:
            category.name = name
            category.description = description
            db.session.commit()
            flash('Category updated successfully!', category='success')
            return redirect(url_for('views.manage_categories'))
    
    return render_template("edit_category.html", user=current_user, category=category)

@views.route('/edit-product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Users can only edit their own products, admins can edit any
    if product.user_id != current_user.id and not current_user.is_admin:
        flash('Access denied.', category='error')
        return redirect(url_for('views.dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        original_price = request.form.get('original_price')
        category_id = request.form.get('category_id')
        stock_quantity = request.form.get('stock_quantity', 0)
        weight = request.form.get('weight')
        dimensions = request.form.get('dimensions')
        features = request.form.get('features')
        available_sizes = request.form.get('available_sizes')
        available_colors = request.form.get('available_colors')
        tags = request.form.get('tags')
        delete_images = request.form.getlist('delete_images')  # Get list of images to delete
        
        # Validate inputs
        if len(name) < 1:
            flash('Product name is required.', category='error')
        elif not price or float(price) <= 0:
            flash('Valid price is required.', category='error')
        elif not category_id:
            flash('Category is required.', category='error')
        else:
            # Convert features to JSON format
            import json
            features_list = []
            if features:
                features_list = [f.strip() for f in features.split('\n') if f.strip()]
            
            # Convert sizes and colors to JSON format
            sizes_list = []
            if available_sizes:
                sizes_list = [s.strip() for s in available_sizes.split(',') if s.strip()]
            
            colors_list = []
            if available_colors:
                colors_list = [c.strip() for c in available_colors.split(',') if c.strip()]
            
            tags_list = []
            if tags:
                tags_list = [t.strip() for t in tags.split(',') if t.strip()]
            
            # Update product fields
            product.name = name
            product.description = description
            product.price = float(price)
            product.original_price = float(original_price) if original_price else None
            product.category_id = int(category_id)
            product.stock_quantity = int(stock_quantity) if stock_quantity else 0
            product.weight = float(weight) if weight else None
            product.dimensions = dimensions
            product.features = json.dumps(features_list) if features_list else None
            product.available_sizes = json.dumps(sizes_list) if sizes_list else None
            product.available_colors = json.dumps(colors_list) if colors_list else None
            product.tags = json.dumps(tags_list) if tags_list else None
            
            # Handle image deletions
            if delete_images:
                for image_id in delete_images:
                    image = ProductImage.query.get(int(image_id))
                    if image:
                        # Optionally, delete the file from the filesystem
                        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image.image)
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        db.session.delete(image)
            
            # Handle new image uploads
            if 'images' in request.files:
                files = request.files.getlist('images')
                for file in files:
                    if file and file.filename != '' and allowed_file(file.filename):
                        filename = generate_unique_filename(file.filename)
                        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                        product_image = ProductImage(image=filename, product_id=product.id)
                        db.session.add(product_image)
            
            db.session.commit()
            flash('Product updated successfully!', category='success')
            return redirect(url_for('views.dashboard'))
    
    categories = Category.query.all()
    return render_template("edit_product.html", user=current_user, product=product, categories=categories)

@views.route('/delete-category/<int:category_id>')
@login_required
def delete_category(category_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', category='error')
        return redirect(url_for('views.dashboard'))
    
    category = Category.query.get_or_404(category_id)
    
    # Delete all products in this category first
    if category.products:
        for product in category.products:
            db.session.delete(product)
    
    # Now delete the category
    db.session.delete(category)
    db.session.commit()
    flash('Category and all its products deleted successfully!', category='success')
    
    return redirect(url_for('views.manage_categories'))

@views.route('/delete-product/<int:product_id>')
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Users can only delete their own products, admins can delete any
    if product.user_id != current_user.id and not current_user.is_admin:
        flash('Access denied.', category='error')
        return redirect(url_for('views.dashboard'))
    
    # Delete associated images from filesystem
    for image in product.images:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image.image)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', category='success')
    
    return redirect(url_for('views.dashboard'))