
// Enhanced Hero Section Functionality

// Smooth scrolling with enhanced easing
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const headerOffset = 80;
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Enhanced navbar with glassmorphism effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    const scrolled = window.pageYOffset;
    
    if (scrolled > 50) {
        navbar.style.background = 'rgba(26, 26, 26, 0.98)';
        navbar.style.backdropFilter = 'blur(20px)';
        navbar.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.3)';
    } else {
        navbar.style.background = 'rgba(26, 26, 26, 0.95)';
        navbar.style.backdropFilter = 'blur(10px)';
        navbar.style.boxShadow = 'none';
    }
});

// Enhanced Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            
            // Trigger counter animation for stats
            if (entry.target.classList.contains('hero-stats')) {
                animateStats();
            }
        }
    });
}, observerOptions);

// Observe all animated elements
document.querySelectorAll('.fade-in-up, .fade-in-left, .fade-in-right, .hero-stats').forEach(el => {
    observer.observe(el);
});

// Enhanced counter animation for hero stats
function animateStats() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const target = parseInt(stat.dataset.target);
        const duration = 2000; // 2 seconds
        const increment = target / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                stat.textContent = target.toLocaleString();
                clearInterval(timer);
            } else {
                stat.textContent = Math.floor(current).toLocaleString();
            }
        }, 16);
    });
}

// Interactive product showcase
document.addEventListener('DOMContentLoaded', function() {
    const showcaseItems = document.querySelectorAll('.showcase-item');
    
    showcaseItems.forEach(item => {
        item.addEventListener('click', function() {
            const product = this.dataset.product;
            
            // Add ripple effect
            createShowcaseRipple(this);
            
            // Scroll to products section with highlight
            setTimeout(() => {
                const productsSection = document.getElementById('products');
                if (productsSection) {
                    productsSection.scrollIntoView({ behavior: 'smooth' });
                    
                    // Highlight relevant product
                    highlightProduct(product);
                }
            }, 300);
        });
        
        // Add hover sound effect (optional)
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.05)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0px) scale(1)';
        });
    });
});

// Create ripple effect for showcase items
function createShowcaseRipple(element) {
    const ripple = document.createElement('div');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    
    ripple.style.cssText = `
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 215, 0, 0.6);
        transform: scale(0);
        animation: showcaseRipple 0.6s linear;
        width: ${size}px;
        height: ${size}px;
        left: ${rect.width / 2 - size / 2}px;
        top: ${rect.height / 2 - size / 2}px;
        pointer-events: none;
    `;
    
    element.style.position = 'relative';
    element.appendChild(ripple);
    
    // Add ripple animation
    if (!document.querySelector('#showcase-ripple-style')) {
        const style = document.createElement('style');
        style.id = 'showcase-ripple-style';
        style.textContent = `
            @keyframes showcaseRipple {
                to {
                    transform: scale(2);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    setTimeout(() => ripple.remove(), 600);
}

// Highlight specific product in products section
function highlightProduct(productType) {
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        const cardContent = card.textContent.toLowerCase();
        let shouldHighlight = false;
        
        switch(productType) {
            case 'tiles':
                shouldHighlight = cardContent.includes('tile');
                break;
            case 'blocks':
                shouldHighlight = cardContent.includes('block');
                break;
            case 'tools':
                shouldHighlight = cardContent.includes('tool');
                break;
        }
        
        if (shouldHighlight) {
            card.style.transform = 'translateY(-15px) scale(1.05)';
            card.style.boxShadow = '0 25px 60px rgba(255, 215, 0, 0.4)';
            
            setTimeout(() => {
                card.style.transform = '';
                card.style.boxShadow = '';
            }, 3000);
        }
    });
}

// Enhanced CTA button interactions
document.addEventListener('DOMContentLoaded', function() {
    const ctaButtons = document.querySelectorAll('.cta-button');
    
    ctaButtons.forEach(button => {
        // Enhanced hover effect with magnetic attraction
        button.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            const moveX = x * 0.15;
            const moveY = y * 0.15;
            
            this.style.transform = `translate(${moveX}px, ${moveY}px) translateY(-8px) scale(1.05)`;
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(-8px) scale(1.05)';
        });
        
        // Enhanced click effect
        button.addEventListener('click', function(e) {
            const ripple = this.querySelector('.btn-ripple');
            if (ripple) {
                ripple.style.width = '300px';
                ripple.style.height = '300px';
                
                setTimeout(() => {
                    ripple.style.width = '0';
                    ripple.style.height = '0';
                }, 600);
            }
        });
    });
});

// Dynamic particle system for hero background
class ParticleSystem {
    constructor() {
        this.particles = [];
        this.canvas = null;
        this.ctx = null;
        this.init();
    }
    
    init() {
        // Create canvas for particles
        this.canvas = document.createElement('canvas');
        this.canvas.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        `;
        
        const heroBackground = document.querySelector('.hero-background');
        if (heroBackground) {
            heroBackground.appendChild(this.canvas);
            this.ctx = this.canvas.getContext('2d');
            this.resize();
            this.createParticles();
            this.animate();
        }
        
        window.addEventListener('resize', () => this.resize());
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    createParticles() {
        for (let i = 0; i < 50; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: Math.random() * 2 + 1,
                opacity: Math.random() * 0.5 + 0.1,
                color: `rgba(255, 215, 0, ${Math.random() * 0.3 + 0.1})`
            });
        }
    }
    
    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.particles.forEach(particle => {
            // Update position
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // Wrap around edges
            if (particle.x < 0) particle.x = this.canvas.width;
            if (particle.x > this.canvas.width) particle.x = 0;
            if (particle.y < 0) particle.y = this.canvas.height;
            if (particle.y > this.canvas.height) particle.y = 0;
            
            // Draw particle
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fillStyle = particle.color;
            this.ctx.fill();
        });
        
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize particle system
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.hero')) {
        new ParticleSystem();
    }
});

// Mouse parallax effect for hero elements
document.addEventListener('mousemove', function(e) {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;
    
    // Parallax for geometric shapes
    const shapes = document.querySelectorAll('.shape');
    shapes.forEach((shape, index) => {
        const speed = (index + 1) * 0.02;
        const x = (mouseX - 0.5) * speed * 100;
        const y = (mouseY - 0.5) * speed * 100;
        
        shape.style.transform += ` translate(${x}px, ${y}px)`;
    });
    
    // Parallax for building animation
    const buildingContainer = document.querySelector('.building-container');
    if (buildingContainer) {
        const x = (mouseX - 0.5) * 20;
        const y = (mouseY - 0.5) * 20;
        
        buildingContainer.style.transform += ` translate(${x}px, ${y}px)`;
    }
});

// Typewriter effect for hero title (enhanced)
function initTypewriterEffect() {
    const titleLines = document.querySelectorAll('.title-line');
    
    titleLines.forEach((line, index) => {
        const text = line.textContent;
        line.textContent = '';
        line.style.opacity = '1';
        
        setTimeout(() => {
            typeText(line, text, 100);
        }, index * 800 + 500);
    });
}

function typeText(element, text, speed) {
    let i = 0;
    const timer = setInterval(() => {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
        } else {
            clearInterval(timer);
        }
    }, speed);
}

// Initialize enhanced effects
document.addEventListener('DOMContentLoaded', function() {
    // Add loading screen
    const loadingScreen = document.createElement('div');
    loadingScreen.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 25%, #2c3e50 50%, #1a1a1a 75%, #0a0a0a 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        transition: opacity 0.5s ease;
    `;
    
    loadingScreen.innerHTML = `
        <div style="text-align: center; color: #FFD700;">
            <div style="width: 60px; height: 60px; border: 3px solid rgba(255, 215, 0, 0.3); border-top: 3px solid #FFD700; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 20px;"></div>
            <h3 style="font-family: Inter, sans-serif; font-weight: 600; margin: 0;">Building Excellence...</h3>
        </div>
    `;
    
    // Add spin animation
    const spinStyle = document.createElement('style');
    spinStyle.textContent = `
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(spinStyle);
    
    document.body.appendChild(loadingScreen);
    
    // Remove loading screen after page load
    window.addEventListener('load', function() {
        setTimeout(() => {
            loadingScreen.style.opacity = '0';
            setTimeout(() => {
                loadingScreen.remove();
                // Initialize typewriter effect after loading
                // initTypewriterEffect();
            }, 500);
        }, 1000);
    });
});

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