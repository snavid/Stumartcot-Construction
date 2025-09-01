from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from .models import User, Category, Product
from . import db
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/')
def home():
    categories = Category.query.all()
    products = Product.query.limit(8).all()  # Show latest 8 products
    return render_template("langingPage.html", categories=categories)

@views.route('/products')
def prodacts():
    categories = Category.query.all()
    products = Product.query.limit(8).all()  # Show latest 8 products
    return render_template("products.html",  categories=categories, products=products)


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

@views.route('construction-consultants')
def construction_consultants():
    return render_template("construction-consultants.html")

@views.route('technical-support')
def  technical_support():
    return render_template("technical-support.html")

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
    return render_template("product_detail.html", user=current_user, product=product)# Adm

@views.route('/manage-categories')
@login_required
def manage_categories():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', category='error')
        return redirect(url_for('views.dashboard'))
    
    categories = Category.query.all()
    return render_template("manage_categories.html", user=current_user, categories=categories)

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
                filename = secure_filename(file.filename)
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
        category_id = request.form.get('category_id')
        
        # Handle file upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename
        
        if len(name) < 1:
            flash('Product name is required.', category='error')
        elif not price or float(price) <= 0:
            flash('Valid price is required.', category='error')
        elif not category_id:
            flash('Category is required.', category='error')
        else:
            new_product = Product(
                name=name,
                description=description,
                price=float(price),
                category_id=int(category_id),
                user_id=current_user.id,
                image=image_filename
            )
            db.session.add(new_product)
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

@views.route('/delete-category/<int:category_id>')
@login_required
def delete_category(category_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', category='error')
        return redirect(url_for('views.dashboard'))
    
    category = Category.query.get_or_404(category_id)
    # Check if category has products
    if category.products:
        flash('Cannot delete category with existing products.', category='error')
    else:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!', category='success')
    
    return redirect(url_for('views.manage_categories'))

@views.route('/delete-product/<int:product_id>')
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Users can only delete their own products, admins can delete any
    if product.user_id != current_user.id and not current_user.is_admin:
        flash('Access denied.', category='error')
        return redirect(url_for('views.dashboard'))
    
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', category='success')
    
    return redirect(url_for('views.dashboard'))