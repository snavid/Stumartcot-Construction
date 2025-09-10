from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, Response
from flask_login import login_required, current_user
from .models import User, Category, Product, ProductImage
from . import db
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from sqlalchemy.sql.expression import func 
import random

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




def get_balanced_random_products(per_page=20, page=1):
    """
    Get products with balanced representation from each category
    """
    # Get all categories with their product counts
    category_stats = db.session.query(
        Category.id,
        Category.name,
        func.count(Product.id).label('product_count')
    ).join(Product).group_by(Category.id, Category.name).all()
    
    if not category_stats:
        # Fallback if no products
        return {
            'items': [],
            'pagination': create_mock_pagination(page, per_page, 0)
        }
    
    # Calculate how many products to get from each category
    total_categories = len(category_stats)
    base_per_category = per_page // total_categories
    remainder = per_page % total_categories
    
    balanced_products = []
    
    for i, (cat_id, cat_name, product_count) in enumerate(category_stats):
        # Distribute remainder among first few categories
        products_from_this_category = base_per_category
        if i < remainder:
            products_from_this_category += 1
        
        # Don't try to get more products than available in category
        products_from_this_category = min(products_from_this_category, product_count)
        
        if products_from_this_category > 0:
            # Get random products from this category
            category_products = Product.query.filter_by(category_id=cat_id)\
                .order_by(func.random())\
                .limit(products_from_this_category)\
                .all()
            
            balanced_products.extend(category_products)
    
    # Shuffle the final list to mix categories
    random.shuffle(balanced_products)
    
    # Calculate pagination info
    total_products = sum(stat.product_count for stat in category_stats)
    total_pages = (total_products + per_page - 1) // per_page
    
    # Handle pagination by getting different random samples for each page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    # For simplicity, we'll regenerate random products for each page
    # In production, you might want to use a seed or cache strategy
    
    return {
        'items': balanced_products[:per_page],  # Take only what we need for current page
        'pagination': create_mock_pagination(page, per_page, total_products, total_pages)
    }

def create_mock_pagination(page, per_page, total, total_pages=None):
    """
    Create a pagination-like object for balanced random products
    """
    if total_pages is None:
        total_pages = (total + per_page - 1) // per_page
    
    class MockPagination:
        def __init__(self, page, per_page, total, pages):
            self.page = page
            self.per_page = per_page
            self.total = total
            self.pages = pages
            self.has_prev = page > 1
            self.has_next = page < pages
            self.prev_num = page - 1 if self.has_prev else None
            self.next_num = page + 1 if self.has_next else None
        
        def iter_pages(self, left_edge=2, left_current=2, right_current=3, right_edge=2):
            """Generate page numbers for pagination display"""
            last = self.pages
            for num in range(1, last + 1):
                if num <= left_edge or \
                   (self.page - left_current - 1 < num < self.page + right_current) or \
                   num > last - right_edge:
                    yield num
    
    return MockPagination(page, per_page, total, total_pages)

# ALTERNATIVE APPROACH 1: Weighted Random Selection
def get_weighted_random_products(per_page=20, page=1):
    """
    Alternative approach: Use weighted selection to balance categories
    """
    # Get category product counts
    category_counts = db.session.query(
        Category.id,
        func.count(Product.id).label('count')
    ).join(Product).group_by(Category.id).all()
    
    if not category_counts:
        return {'items': [], 'pagination': create_mock_pagination(page, per_page, 0)}
    
    # Calculate weights (inverse of product count for balance)
    max_count = max(count for _, count in category_counts)
    category_weights = {
        cat_id: max_count / count for cat_id, count in category_counts
    }
    
    # Get weighted random products
    products = []
    for _ in range(per_page):
        # Choose category based on weights
        categories_list = list(category_weights.keys())
        weights_list = list(category_weights.values())
        
        selected_category = random.choices(categories_list, weights=weights_list)[0]
        
        # Get random product from selected category
        product = Product.query.filter_by(category_id=selected_category)\
            .order_by(func.random())\
            .first()
        
        if product and product not in products:
            products.append(product)
    
    total_products = sum(count for _, count in category_counts)
    return {
        'items': products,
        'pagination': create_mock_pagination(page, per_page, total_products)
    }

# ALTERNATIVE APPROACH 2: Round-Robin Selection
def get_round_robin_products(per_page=20, page=1):
    """
    Alternative approach: Round-robin selection from categories
    """
    # Get random products from each category
    category_products = {}
    categories = Category.query.join(Product).distinct().all()
    
    for category in categories:
        products = Product.query.filter_by(category_id=category.id)\
            .order_by(func.random())\
            .limit(per_page)\
            .all()
        category_products[category.id] = products
    
    # Round-robin selection
    selected_products = []
    max_iterations = per_page
    iteration = 0
    
    while len(selected_products) < per_page and iteration < max_iterations:
        for cat_id, products in category_products.items():
            if len(selected_products) >= per_page:
                break
            if iteration < len(products):
                selected_products.append(products[iteration])
        iteration += 1
    
    # Shuffle final selection
    random.shuffle(selected_products)
    
    total_products = sum(len(products) for products in category_products.values())
    return {
        'items': selected_products,
        'pagination': create_mock_pagination(page, per_page, total_products)
    }






@views.route('/')
def home():
    categories = Category.query.all()
    products = Product.query.limit(8).all()  # Show latest 8 products
    return render_template("langingPage.html", categories=categories)

@views.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', 'all', type=str)
    
    categories = Category.query.all()
    
    # Base query
    query = Product.query
    
    # Convert category_id to integer if not 'all'
    selected_category = None
    if category_id != 'all':
        try:
            selected_category = int(category_id)
            query = query.filter_by(category_id=selected_category)
        except ValueError:
            selected_category = None
    else:
        # IMPROVED: Balanced randomization when showing all categories
        products = get_balanced_random_products(per_page=20, page=page)
        return render_template(
            "products.html",
            categories=categories,
            products=products['items'],
            pagination=products['pagination'],
            selected_category=selected_category
        )
    
    # For specific category, use regular pagination
    per_page = 20
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items
    
    return render_template(
        "products.html",
        categories=categories,
        products=products,
        pagination=pagination,
        selected_category=selected_category
    )


@views.route('/blog')
def blogs():
    return render_template("blog.html")

@views.route('/contact')
def contact():
    return render_template("contact.html")

# @views.route('/cart')
# def cart():
#     return render_template("cart.html")    

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
    
    # Get random related products from the same category (excluding current product)
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id
    ).order_by(func.random()).limit(4).all()
    
    # If no products in same category, get random products from all categories
    if not related_products:
        related_products = Product.query.filter(
            Product.id != product.id
        ).order_by(func.random()).limit(4).all()
    
    return render_template("product-single.html", 
                         product=product, 
                         related_products=related_products)

@views.route('/sitemap.xml')
def sitemap():
    current_time = datetime.utcnow()
    sitemap_xml = render_template("sitemap.xml", 
                                categories=Category.query.all(), 
                                products=Product.query.all(),
                                current_time=current_time,
                                moment = current_time)
    response = Response(sitemap_xml, mimetype='application/xml')
    return response

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

@views.route('/about')
def about_page():
    return render_template("about.html")

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
        #original_price = request.form.get('original_price')
        category_id = request.form.get('category_id')
        #stock_quantity = request.form.get('stock_quantity', 0)
        #weight = request.form.get('weight')
        #dimensions = request.form.get('dimensions')
        #features = request.form.get('features')
        #available_sizes = request.form.get('available_sizes')
        #available_colors = request.form.get('available_colors')
        #tags = request.form.get('tags')
        
        # Validate inputs
        if len(name) < 1:
            flash('Product name is required.', category='error')
        elif not price or float(price) <= 0:
            flash('Valid price is required.', category='error')
        elif not category_id:
            flash('Category is required.', category='error')
        else:
            # # Convert features to JSON format
            # import json
            # features_list = []
            # if features:
            #     features_list = [f.strip() for f in features.split('\n') if f.strip()]
            
            # # Convert sizes and colors to JSON format
            # sizes_list = []
            # if available_sizes:
            #     sizes_list = [s.strip() for s in available_sizes.split(',') if s.strip()]
            
            # colors_list = []
            # if available_colors:
            #     colors_list = [c.strip() for c in available_colors.split(',') if c.strip()]
            
            # tags_list = []
            # if tags:
            #     tags_list = [t.strip() for t in tags.split(',') if t.strip()]
            
            # Create new product
            new_product = Product(
                name=name,
                description=description,
                price=float(price),
                #original_price=float(original_price) if original_price else None,
                category_id=int(category_id),
                user_id=current_user.id,
                #stock_quantity=int(stock_quantity) if stock_quantity else 0,
                #weight=float(weight) if weight else None,
                #dimensions=dimensions,
                #features=json.dumps(features_list) if features_list else None,
                #available_sizes=json.dumps(sizes_list) if sizes_list else None,
                #available_colors=json.dumps(colors_list) if colors_list else None,
                #tags=json.dumps(tags_list) if tags_list else None
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

@views.route("/robots.txt")
def robots_txt():
    robots_text = """User-agent: *
Disallow: /admin/
Disallow: /dashboard
Disallow: /categories/
Disallow: /category/
Disallow: /manage-categories
Disallow: /manage-products
Disallow: /add-category
Disallow: /manage-users
Disallow: /manage-products
Disallow: /add-product
Disallow: /delete-user/
Disallow: /edit-category/
Disallow: /edit-product/
Disallow: /delete-category/
Disallow: /delete-product/
Disallow: /login
Disallow: /sign-up
Allow: /
Sitemap: https://stumarcot.co.tz/sitemap.xml
"""
    return Response(robots_text, mimetype="text/plain")