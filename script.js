
// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar background on scroll
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(26, 26, 26, 0.98)';
    } else {
        navbar.style.background = 'rgba(26, 26, 26, 0.95)';
    }
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// Observe all animated elements
document.querySelectorAll('.fade-in-up, .fade-in-left, .fade-in-right').forEach(el => {
    observer.observe(el);
});

// Counter animation for stats (if you want to add stats later)
function animateCounter(element, target, duration) {
    let start = 0;
    const increment = target / (duration / 16);
    
    function updateCounter() {
        start += increment;
        if (start < target) {
            element.textContent = Math.floor(start);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    }
    updateCounter();
}

// Parallax effect for floating icons
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('.floating-icon');
    
    parallaxElements.forEach((element, index) => {
        const speed = (index + 1) * 0.5;
        element.style.transform = `translateY(${scrolled * speed}px)`;
    });
});

// Add loading animation
window.addEventListener('load', function() {
    document.body.style.overflow = 'visible';
});

// Typing effect for hero title (optional enhancement)
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    type();
}

// Particle background effect
function createParticle() {
    const particle = document.createElement('div');
    particle.style.cssText = `
        position: absolute;
        width: 4px;
        height: 4px;
        background: rgba(255, 215, 0, 0.6);
        border-radius: 50%;
        pointer-events: none;
        animation: particleFloat 8s linear infinite;
    `;
    
    particle.style.left = Math.random() * 100 + 'vw';
    particle.style.animationDelay = Math.random() * 8 + 's';
    
    document.querySelector('.hero').appendChild(particle);
    
    setTimeout(() => {
        particle.remove();
    }, 8000);
}

// Add particle animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes particleFloat {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100px) rotate(360deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Create particles periodically
setInterval(createParticle, 3000);

// Magnetic effect for CTA buttons
document.querySelectorAll('.cta-button').forEach(button => {
    button.addEventListener('mousemove', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        
        this.style.transform = `translate(${x * 0.1}px, ${y * 0.1}px) translateY(-5px)`;
    });
    
    button.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(-5px)';
    });
});

// Product card tilt effect
document.querySelectorAll('.product-card').forEach(card => {
    card.addEventListener('mousemove', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;
        
        this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(-10px)';
    });
});

// Add scroll progress indicator
const progressBar = document.createElement('div');
progressBar.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 0%;
    height: 3px;
    background: linear-gradient(90deg, #FFD700, #FFA500);
    z-index: 9999;
    transition: width 0.3s ease;
`;
document.body.appendChild(progressBar);

window.addEventListener('scroll', function() {
    const scrolled = (window.pageYOffset / (document.body.scrollHeight - window.innerHeight)) * 100;
    progressBar.style.width = scrolled + '%';
});

// Add ripple effect to buttons
function createRipple(event) {
    const button = event.currentTarget;
    const circle = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
    circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
    circle.classList.add('ripple');

    const rippleStyle = document.createElement('style');
    if (!document.querySelector('#ripple-style')) {
        rippleStyle.id = 'ripple-style';
        rippleStyle.textContent = `
            .ripple {
                position: absolute;
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 600ms linear;
                background-color: rgba(255, 255, 255, 0.6);
            }
            @keyframes ripple {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(rippleStyle);
    }

    const rippleElement = button.getElementsByClassName('ripple')[0];
    if (rippleElement) {
        rippleElement.remove();
    }

    button.appendChild(circle);
}

document.querySelectorAll('.cta-button, .feature-card, .product-card').forEach(button => {
    button.addEventListener('click', createRipple);
});
// Ecommerce Functionality

// Cart management
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Update cart count in navigation
function updateCartCount() {
    const cartCount = document.querySelector('.cart-count');
    if (cartCount) {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        cartCount.textContent = totalItems;
        cartCount.style.display = totalItems > 0 ? 'flex' : 'none';
    }
}

// Add item to cart
function addToCart(id, name, price, quantity = 1) {
    const existingItem = cart.find(item => item.id === id);
    
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({
            id: id,
            name: name,
            price: price,
            quantity: quantity,
            image: getProductImage(id)
        });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    showCartNotification(name, quantity);
}

// Get product image icon based on ID
function getProductImage(id) {
    const imageMap = {
        'ceramic-wall-tiles': 'fas fa-th-large',
        'porcelain-floor-tiles': 'fas fa-layer-group',
        'pelvin-blocks': 'fas fa-cube',
        'hollow-blocks': 'fas fa-cubes',
        'clay-roof-tiles': 'fas fa-home',
        'metal-roofing-sheets': 'fas fa-warehouse',
        'construction-hammer': 'fas fa-hammer',
        'tool-set': 'fas fa-tools',
        'premium-paint': 'fas fa-paint-roller',
        'mosaic-tiles': 'fas fa-th',
        'natural-stone-tiles': 'fas fa-square',
        'subway-tiles': 'fas fa-grip-horizontal'
    };
    return imageMap[id] || 'fas fa-box';
}

// Show cart notification
function showCartNotification(productName, quantity) {
    // Remove existing notification
    const existingNotification = document.querySelector('.cart-notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = 'cart-notification';
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-check-circle"></i>
            <span>${quantity} x ${productName} added to cart</span>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: var(--gradient-1);
        color: var(--text-dark);
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        font-weight: 600;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Animate out and remove
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Remove item from cart
function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    renderCartItems();
    updateOrderSummary();
}

// Update item quantity
function updateQuantity(id, newQuantity) {
    if (newQuantity <= 0) {
        removeFromCart(id);
        return;
    }
    
    const item = cart.find(item => item.id === id);
    if (item) {
        item.quantity = newQuantity;
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartCount();
        renderCartItems();
        updateOrderSummary();
    }
}

// Clear entire cart
function clearCart() {
    if (cart.length === 0) return;
    
    if (confirm('Are you sure you want to clear your cart?')) {
        cart = [];
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartCount();
        renderCartItems();
        updateOrderSummary();
    }
}

// Render cart items on cart page
function renderCartItems() {
    const cartContainer = document.getElementById('cartItemsContainer');
    const emptyCart = document.getElementById('emptyCart');
    const checkoutBtn = document.getElementById('checkoutBtn');
    
    if (!cartContainer) return;
    
    if (cart.length === 0) {
        emptyCart.style.display = 'block';
        checkoutBtn.disabled = true;
        cartContainer.innerHTML = '<div class="empty-cart" id="emptyCart"><div class="empty-cart-icon"><i class="fas fa-shopping-cart"></i></div><h3>Your cart is empty</h3><p>Add some construction materials to get started</p><a href="products.html" class="btn-continue-shopping"><i class="fas fa-arrow-left me-2"></i>Continue Shopping</a></div>';
        return;
    }
    
    emptyCart.style.display = 'none';
    checkoutBtn.disabled = false;
    
    const cartHTML = cart.map(item => `
        <div class="cart-item" data-id="${item.id}">
            <div class="cart-item-image">
                <i class="${item.image}"></i>
            </div>
            <div class="cart-item-details">
                <h5>${item.name}</h5>
                <p class="item-price">$${item.price.toFixed(2)} each</p>
            </div>
            <div class="cart-item-quantity">
                <button class="btn-quantity" onclick="updateQuantity('${item.id}', ${item.quantity - 1})">-</button>
                <span class="quantity">${item.quantity}</span>
                <button class="btn-quantity" onclick="updateQuantity('${item.id}', ${item.quantity + 1})">+</button>
            </div>
            <div class="cart-item-total">
                <span class="item-total">$${(item.price * item.quantity).toFixed(2)}</span>
            </div>
            <div class="cart-item-remove">
                <button class="btn-remove" onclick="removeFromCart('${item.id}')">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
    
    cartContainer.innerHTML = cartHTML;
    
    // Add cart item styles
    if (!document.querySelector('#cart-item-styles')) {
        const cartStyles = document.createElement('style');
        cartStyles.id = 'cart-item-styles';
        cartStyles.textContent = `
            .cart-item {
                display: flex;
                align-items: center;
                padding: 20px 0;
                border-bottom: 1px solid #eee;
                gap: 20px;
            }
            .cart-item:last-child {
                border-bottom: none;
            }
            .cart-item-image {
                width: 80px;
                height: 80px;
                background: var(--gradient-1);
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2rem;
                color: var(--text-dark);
                flex-shrink: 0;
            }
            .cart-item-details {
                flex: 1;
            }
            .cart-item-details h5 {
                margin: 0 0 5px 0;
                color: var(--text-dark);
                font-weight: 600;
            }
            .item-price {
                margin: 0;
                color: #6c757d;
                font-size: 0.9rem;
            }
            .cart-item-quantity {
                display: flex;
                align-items: center;
                gap: 10px;
                background: var(--light-bg);
                padding: 8px 12px;
                border-radius: 8px;
            }
            .cart-item-quantity .btn-quantity {
                background: var(--primary-yellow);
                color: var(--text-dark);
                border: none;
                width: 30px;
                height: 30px;
                border-radius: 6px;
                font-weight: 600;
                cursor: pointer;
            }
            .cart-item-quantity .quantity {
                font-weight: 600;
                min-width: 20px;
                text-align: center;
            }
            .cart-item-total {
                min-width: 100px;
                text-align: right;
            }
            .item-total {
                font-size: 1.2rem;
                font-weight: 700;
                color: var(--text-dark);
            }
            .cart-item-remove {
                flex-shrink: 0;
            }
            .btn-remove {
                background: transparent;
                border: 2px solid #e74c3c;
                color: #e74c3c;
                width: 40px;
                height: 40px;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .btn-remove:hover {
                background: #e74c3c;
                color: white;
            }
            @media (max-width: 768px) {
                .cart-item {
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 15px;
                }
                .cart-item-details {
                    width: 100%;
                }
                .cart-item-quantity,
                .cart-item-total,
                .cart-item-remove {
                    width: 100%;
                    justify-content: center;
                }
            }
        `;
        document.head.appendChild(cartStyles);
    }
}

// Update order summary
function updateOrderSummary() {
    const subtotalEl = document.getElementById('subtotal');
    const shippingEl = document.getElementById('shipping');
    const taxEl = document.getElementById('tax');
    const totalEl = document.getElementById('total');
    
    if (!subtotalEl) return;
    
    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const shippingCost = getShippingCost();
    const tax = subtotal * 0.08; // 8% tax
    const total = subtotal + shippingCost + tax;
    
    subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
    shippingEl.textContent = shippingCost === 0 ? 'Free' : `$${shippingCost.toFixed(2)}`;
    taxEl.textContent = `$${tax.toFixed(2)}`;
    totalEl.textContent = `$${total.toFixed(2)}`;
}

// Get shipping cost based on selected option
function getShippingCost() {
    const shippingOptions = document.querySelectorAll('input[name="shipping"]');
    let selectedShipping = 0;
    
    shippingOptions.forEach(option => {
        if (option.checked) {
            selectedShipping = parseFloat(option.value);
        }
    });
    
    return selectedShipping;
}

// Apply promo code
function applyPromoCode() {
    const promoInput = document.getElementById('promoCode');
    const promoCode = promoInput.value.trim().toUpperCase();
    
    const validCodes = {
        'SAVE10': 0.10,
        'WELCOME15': 0.15,
        'BUILD20': 0.20
    };
    
    if (validCodes[promoCode]) {
        const discount = validCodes[promoCode];
        // Apply discount logic here
        alert(`Promo code applied! You saved ${(discount * 100)}%`);
        promoInput.value = '';
    } else {
        alert('Invalid promo code. Please try again.');
    }
}

// Proceed to checkout
function proceedToCheckout() {
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }
    
    // In a real application, this would redirect to a checkout page
    alert('Redirecting to checkout... (This would be implemented with your backend)');
}

// Product filtering and sorting
function filterProducts() {
    const categoryFilter = document.getElementById('categoryFilter');
    const priceFilter = document.getElementById('priceFilter');
    const sortFilter = document.getElementById('sortFilter');
    
    if (!categoryFilter) return;
    
    const products = document.querySelectorAll('.product-item');
    const selectedCategory = categoryFilter.value;
    const selectedPriceRange = priceFilter.value;
    const selectedSort = sortFilter.value;
    
    // Filter products
    products.forEach(product => {
        const category = product.dataset.category;
        const price = parseFloat(product.dataset.price);
        
        let showProduct = true;
        
        // Category filter
        if (selectedCategory !== 'all' && category !== selectedCategory) {
            showProduct = false;
        }
        
        // Price filter
        if (selectedPriceRange !== 'all') {
            const [min, max] = selectedPriceRange.split('-').map(p => p === '+' ? Infinity : parseFloat(p));
            if (price < min || price > max) {
                showProduct = false;
            }
        }
        
        product.style.display = showProduct ? 'block' : 'none';
    });
    
    // Sort products (simplified - in real app you'd sort the actual data)
    // This is a basic implementation for demonstration
}

// Product detail page functionality
function changeQuantity(change) {
    const quantityInput = document.getElementById('quantity');
    if (!quantityInput) return;
    
    let currentQuantity = parseInt(quantityInput.value);
    currentQuantity += change;
    
    if (currentQuantity < 1) currentQuantity = 1;
    if (currentQuantity > 100) currentQuantity = 100;
    
    quantityInput.value = currentQuantity;
}

// Add to cart from product detail page
function addToCartFromDetail() {
    const productTitle = document.getElementById('productTitle');
    const productPrice = document.getElementById('productPrice');
    const quantityInput = document.getElementById('quantity');
    
    if (!productTitle || !productPrice || !quantityInput) return;
    
    const name = productTitle.textContent;
    const price = parseFloat(productPrice.textContent.replace('$', ''));
    const quantity = parseInt(quantityInput.value);
    
    // Generate ID from title (simplified)
    const id = name.toLowerCase().replace(/\s+/g, '-');
    
    addToCart(id, name, price, quantity);
}

// Color option selection
document.addEventListener('DOMContentLoaded', function() {
    // Color options
    const colorOptions = document.querySelectorAll('.color-option');
    colorOptions.forEach(option => {
        option.addEventListener('click', function() {
            colorOptions.forEach(opt => opt.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Thumbnail selection
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            thumbnails.forEach(thumb => thumb.classList.remove('active'));
            this.classList.add('active');
            
            // Update main image (in real app, you'd change the actual image)
            const mainImage = document.querySelector('#mainProductImage');
            if (mainImage) {
                mainImage.innerHTML = this.innerHTML;
            }
        });
    });
    
    // Shipping option change
    const shippingOptions = document.querySelectorAll('input[name="shipping"]');
    shippingOptions.forEach(option => {
        option.addEventListener('change', updateOrderSummary);
    });
    
    // Filter change events
    const filters = ['categoryFilter', 'priceFilter', 'sortFilter'];
    filters.forEach(filterId => {
        const filter = document.getElementById(filterId);
        if (filter) {
            filter.addEventListener('change', filterProducts);
        }
    });
    
    // Initialize cart
    updateCartCount();
    
    // Initialize cart page if we're on it
    if (document.getElementById('cartItemsContainer')) {
        renderCartItems();
        updateOrderSummary();
    }
    
    // Load product details if we're on product detail page
    loadProductDetails();
});

// Load product details based on URL parameters
function loadProductDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');
    
    if (!productId) return;
    
    // Product data (in real app, this would come from an API)
    const productData = {
        'ceramic-wall-tiles': {
            title: 'Ceramic Wall Tiles',
            price: 45.00,
            originalPrice: 55.00,
            description: 'Premium ceramic wall tiles perfect for bathrooms and kitchens. These high-quality tiles offer excellent durability, water resistance, and easy maintenance.',
            features: [
                'Water resistant and easy to clean',
                'Durable ceramic construction',
                'Multiple color options available',
                'Professional installation support',
                '5-year manufacturer warranty'
            ],
            icon: 'fas fa-th-large'
        },
        'porcelain-floor-tiles': {
            title: 'Porcelain Floor Tiles',
            price: 65.00,
            description: 'Durable porcelain tiles for high-traffic areas with superior strength and style.',
            features: [
                'High durability for heavy traffic',
                'Scratch and stain resistant',
                'Available in multiple sizes',
                'Easy maintenance',
                '10-year warranty'
            ],
            icon: 'fas fa-layer-group'
        },
        'pelvin-blocks': {
            title: 'Pelvin Blocks',
            price: 25.00,
            description: 'High-strength concrete blocks for structural construction with excellent load-bearing capacity.',
            features: [
                'Superior compressive strength',
                'Weather resistant',
                'Consistent dimensions',
                'Eco-friendly production',
                'Meets building standards'
            ],
            icon: 'fas fa-cube'
        }
        // Add more products as needed
    };
    
    const product = productData[productId];
    if (!product) return;
    
    // Update page elements
    const elements = {
        productTitle: product.title,
        productPrice: `$${product.price.toFixed(2)}`,
        originalPrice: product.originalPrice ? `$${product.originalPrice.toFixed(2)}` : '',
        productDescription: product.description,
        productBreadcrumb: product.title,
        mainProductImage: `<i class="${product.icon}"></i>`
    };
    
    Object.keys(elements).forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.innerHTML = elements[id];
        }
    });
    
    // Update features list
    const featuresList = document.getElementById('productFeatures');
    if (featuresList && product.features) {
        featuresList.innerHTML = product.features.map(feature => 
            `<li><i class="fas fa-check text-success me-2"></i>${feature}</li>`
        ).join('');
    }
    
    // Update page title
    document.title = `${product.title} - Stumarcot Construction Materials`;
}

// Contact form submission
function handleContactForm() {
    const contactForm = document.getElementById('contactForm');
    if (!contactForm) return;
    
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(contactForm);
        const data = Object.fromEntries(formData);
        
        // Validate required fields
        const requiredFields = ['firstName', 'lastName', 'email', 'subject', 'message'];
        const missingFields = requiredFields.filter(field => !data[field]);
        
        if (missingFields.length > 0) {
            alert('Please fill in all required fields.');
            return;
        }
        
        // Simulate form submission
        alert('Thank you for your message! We will get back to you within 24 hours.');
        contactForm.reset();
    });
}

// Newsletter subscription
function handleNewsletterForm() {
    const newsletterForm = document.querySelector('.newsletter-form');
    if (!newsletterForm) return;
    
    newsletterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = this.querySelector('input[type="email"]').value;
        if (!email) {
            alert('Please enter a valid email address.');
            return;
        }
        
        alert('Thank you for subscribing to our newsletter!');
        this.reset();
    });
}

// Initialize contact and newsletter forms
document.addEventListener('DOMContentLoaded', function() {
    handleContactForm();
    handleNewsletterForm();
});

// Search functionality for blog
function handleBlogSearch() {
    const searchInput = document.querySelector('.search-box input');
    if (!searchInput) return;
    
    const searchButton = document.querySelector('.btn-search');
    
    function performSearch() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        if (!searchTerm) return;
        
        // In a real application, this would search through blog posts
        alert(`Searching for: "${searchTerm}"`);
    }
    
    searchButton.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
}

// Initialize blog search
document.addEventListener('DOMContentLoaded', handleBlogSearch);

// Wishlist functionality (basic implementation)
let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];

function toggleWishlist(productId, productName) {
    const index = wishlist.findIndex(item => item.id === productId);
    
    if (index > -1) {
        wishlist.splice(index, 1);
        showNotification(`${productName} removed from wishlist`, 'info');
    } else {
        wishlist.push({ id: productId, name: productName });
        showNotification(`${productName} added to wishlist`, 'success');
    }
    
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
    updateWishlistButtons();
}

function updateWishlistButtons() {
    const wishlistButtons = document.querySelectorAll('.btn-wishlist');
    wishlistButtons.forEach(button => {
        const productId = button.dataset.productId;
        const isInWishlist = wishlist.some(item => item.id === productId);
        
        if (isInWishlist) {
            button.innerHTML = '<i class="fas fa-heart"></i>';
            button.style.color = '#e74c3c';
        } else {
            button.innerHTML = '<i class="far fa-heart"></i>';
            button.style.color = '#6c757d';
        }
    });
}

// Generic notification function
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    const colors = {
        success: 'var(--gradient-1)',
        info: '#3498db',
        warning: '#f39c12',
        error: '#e74c3c'
    };
    
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${colors[type]};
        color: ${type === 'success' ? 'var(--text-dark)' : 'white'};
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        font-weight: 600;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Initialize wishlist on page load
document.addEventListener('DOMContentLoaded', function() {
    updateWishlistButtons();
});