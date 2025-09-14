# TODO will be done 

from flask_caching import Cache
import random
import numpy as np
from datetime import datetime
from sqlalchemy import func
from your_app.models import Category, Product
from your_app import db, app

# Initialize cache (configure based on your backend, e.g., Redis)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379/0'})

@cache.memoize(timeout=3600)  # Cache for 1 hour
def get_balanced_random_products(per_page=20, page=1, seed=None):
    """
    Get products with balanced representation from each category, cached and efficiently randomized.
    
    Args:
        per_page (int): Number of products per page
        page (int): Current page number
        seed (int, optional): Random seed for deterministic shuffling
    """
    # Use a default seed based on current day to ensure daily randomization
    if seed is None:
        seed = int(datetime.utcnow().strftime('%Y%m%d'))
    
    # Set random seed for reproducibility
    random.seed(seed)
    np.random.seed(seed)
    
    # Get all categories with their product counts
    category_stats = db.session.query(
        Category.id,
        Category.name,
        func.count(Product.id).label('product_count')
    ).join(Product).group_by(Category.id, Category.name).all()
    
    if not category_stats:
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
            # Fetch product IDs instead of full objects to reduce memory usage
            product_ids = db.session.query(Product.id)\
                .filter_by(category_id=cat_id)\
                .all()
            
            # Randomly select indices using numpy for efficiency
            selected_indices = np.random.choice(
                len(product_ids),
                size=products_from_this_category,
                replace=False
            )
            
            # Fetch only the selected products
            selected_ids = [product_ids[idx][0] for idx in selected_indices]
            category_products = Product.query.filter(Product.id.in_(selected_ids)).all()
            
            balanced_products.extend(category_products)
    
    # Shuffle the final list deterministically
    random.shuffle(balanced_products)
    
    # Calculate pagination info
    total_products = sum(stat.product_count for stat in category_stats)
    total_pages = (total_products + per_page - 1) // per_page
    
    # Slice for pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    return {
        'items': balanced_products[start_idx:end_idx],
        'pagination': create_mock_pagination(page, per_page, total_products, total_pages)
    }

def clear_cache():
    """Helper function to clear cache when products or categories change."""
    cache.delete_memoized(get_balanced_random_products)





















import json
import base64

def decode_jwt(token):
    parts = token.split('.')
    # Pad with '=' to make base64 decoding work
    header = json.loads(base64.urlsafe_b64decode(parts[0] + '===').decode('utf-8'))
    payload = json.loads(base64.urlsafe_b64decode(parts[1] + '===').decode('utf-8'))
    return header, payload

# Example usage
token_a = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiYzUxYzMyMy1jMzI1LTRiN2UtODFlOC01NDg1MThjMzQxNDQiLCJleHAiOjE3NTc3NzEzNjJ9.yGEVF5VOipwTfmnylwAiM7e4wInBR9__oTWwE8llTXc'
header_a, payload_a = decode_jwt(token_a)
print("Header A:", header_a)  # Output: {'alg': 'HS256', 'typ': 'JWT'}
print("Payload A:", payload_a)  # Output: {'sub': 'userA', 'role': 'user'}

token_b = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmNjhlZDM0Ny0xMzE2LTQ1YWMtOWQxMy00YjViNjIxZTFjZDAiLCJleHAiOjE3NTc3NzE0Mjh9.VfrNYAFO5GMjfN9Jr94oCZvsjS5ZCtWNqzXJv2TSdxs'
header_b, payload_b = decode_jwt(token_b)
print("Header B:", header_b)  # Output: {'alg': 'HS256', 'typ': 'JWT'}
print("Payload B:", payload_b)  # Output: {'sub': 'uuv runserB', 'role': 'user'}

