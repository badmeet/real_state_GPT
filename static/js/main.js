// Property Search Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize property search if on search page
    if (document.querySelector('.search-section')) {
        initializePropertySearch();
    }
    
    // Initialize market analysis if on market page
    if (document.querySelector('.market-section')) {
        initializeMarketAnalysis();
    }
    
    // Initialize chat if on home page
    if (document.querySelector('.chat-section')) {
        initializeChat();
    }

    // Mobile Navigation
    const navContent = document.querySelector('.nav-content');
    const navLinks = document.querySelector('.nav-links');
    
    if (window.innerWidth <= 768) {
        const mobileMenuBtn = document.createElement('button');
        mobileMenuBtn.className = 'mobile-menu-btn';
        mobileMenuBtn.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <line x1="3" y1="12" x2="21" y2="12" stroke-width="2"/>
                <line x1="3" y1="6" x2="21" y2="6" stroke-width="2"/>
                <line x1="3" y1="18" x2="21" y2="18" stroke-width="2"/>
            </svg>
        `;
        navContent.insertBefore(mobileMenuBtn, navLinks);

        // Toggle mobile menu
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!navContent.contains(e.target)) {
                navLinks.classList.remove('active');
            }
        });
    }

    // Form Validation
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(contactForm);
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            
            // Add loading state
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;

            try {
                // Simulate form submission (replace with actual API call)
                await new Promise(resolve => setTimeout(resolve, 1500));
                
                // Show success message
                showNotification('Message sent successfully!', 'success');
                contactForm.reset();
            } catch (error) {
                // Show error message
                showNotification('Failed to send message. Please try again.', 'error');
            } finally {
                // Remove loading state
                submitBtn.classList.remove('loading');
                submitBtn.disabled = false;
            }
        });
    }

    // Smooth scrolling for anchor links
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

    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements with animation classes
    document.querySelectorAll('.about-content > div, .contact-content > div').forEach(el => {
        observer.observe(el);
    });
});

// Property Search Functions
function initializePropertySearch() {
    const searchForm = document.querySelector('.search-filters');
    const propertyGrid = document.querySelector('.property-grid');
    const resultsHeader = document.querySelector('.results-header h3');
    const sortSelect = document.querySelector('.results-header select');
    
    // Handle search form submission
    searchForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        await searchProperties();
    });
    
    // Handle sort change
    sortSelect.addEventListener('change', async function() {
        await searchProperties();
    });
    
    // Initial search
    searchProperties();
}

async function searchProperties() {
    const location = document.querySelector('select[name="location"]')?.value;
    const bhk = document.querySelector('select[name="property-type"]')?.value;
    const minPrice = document.querySelector('input[name="min-price"]')?.value;
    const maxPrice = document.querySelector('input[name="max-price"]')?.value;
    const minArea = document.querySelector('input[name="min-area"]')?.value;
    const maxArea = document.querySelector('input[name="max-area"]')?.value;
    const sortBy = document.querySelector('.results-header select')?.value;
    
    try {
        const response = await fetch(`/api/properties?${new URLSearchParams({
            location: location || '',
            bhk: bhk || '',
            min_price: minPrice || '',
            max_price: maxPrice || '',
            min_area: minArea || '',
            max_area: maxArea || '',
            sort_by: sortBy || 'relevance'
        })}`);
        
        const data = await response.json();
        updatePropertyGrid(data.properties);
        updateResultsCount(data.total);
    } catch (error) {
        console.error('Error fetching properties:', error);
    }
}

function updatePropertyGrid(properties) {
    const propertyGrid = document.querySelector('.property-grid');
    propertyGrid.innerHTML = '';
    
    properties.forEach(property => {
        const card = createPropertyCard(property);
        propertyGrid.appendChild(card);
    });
}

function createPropertyCard(property) {
    const card = document.createElement('div');
    card.className = 'property-card';
    
    card.innerHTML = `
        <div class="property-image">
            <img src="https://via.placeholder.com/300x200" alt="${property.property_name}">
            <span class="property-badge">${property.status}</span>
        </div>
        <div class="property-info">
            <h4>${property.property_name}</h4>
            <p class="property-location">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" stroke-width="2"/>
                    <circle cx="12" cy="10" r="3" stroke-width="2"/>
                </svg>
                ${property.location}
            </p>
            <div class="property-details">
                <span>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" stroke-width="2"/>
                        <polyline points="9 22 9 12 15 12 15 22" stroke-width="2"/>
                    </svg>
                    ${property.bhk}
                </span>
                <span>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2" stroke-width="2"/>
                    </svg>
                    ${property.area} sq ft
                </span>
            </div>
            <div class="property-price">
                <h4>₹${(property.price / 100000).toFixed(1)} Lakhs</h4>
                <span>₹${property.price_per_sqft}/sq ft</span>
            </div>
            <button class="btn-secondary">View Details</button>
        </div>
    `;
    
    return card;
}

function updateResultsCount(total) {
    const resultsHeader = document.querySelector('.results-header h3');
    resultsHeader.textContent = `${total} Properties Found`;
}

// Market Analysis Functions
function initializeMarketAnalysis() {
    loadMarketData();
    initializePriceTrendChart();
}

async function loadMarketData() {
    try {
        const response = await fetch('/api/market-data');
        const data = await response.json();
        updateMarketStats(data);
        updateLocationAnalysis(data.locations);
        updateMarketInsights();
    } catch (error) {
        console.error('Error loading market data:', error);
    }
}

function updateMarketStats(data) {
    // Update average price
    document.querySelector('.stat-value').textContent = `₹${data.average_price}/sqft`;
    document.querySelector('.stat-change.positive').textContent = `+${data.price_change}% YoY`;
    
    // Update properties listed
    document.querySelectorAll('.stat-value')[1].textContent = data.properties_listed.toLocaleString();
    document.querySelectorAll('.stat-change.positive')[1].textContent = `+${data.listings_change}% MoM`;
    
    // Update top location
    document.querySelectorAll('.stat-value')[2].textContent = data.top_location;
}

function updateLocationAnalysis(locations) {
    const locationGrid = document.querySelector('.location-grid');
    locationGrid.innerHTML = '';
    
    Object.entries(locations).forEach(([location, data]) => {
        const card = createLocationCard(location, data);
        locationGrid.appendChild(card);
    });
}

function createLocationCard(location, data) {
    const card = document.createElement('div');
    card.className = 'location-card';
    
    card.innerHTML = `
        <h3>${location}</h3>
        <div class="location-stats">
            <div class="location-stat">
                <span>Avg. Price</span>
                <strong>₹${data.avg_price}/sqft</strong>
            </div>
            <div class="location-stat">
                <span>Growth</span>
                <strong class="positive">+${data.growth}%</strong>
            </div>
            <div class="location-stat">
                <span>Demand</span>
                <strong>${data.demand}</strong>
            </div>
        </div>
        <button class="btn-secondary">View Properties</button>
    `;
    
    return card;
}

function initializePriceTrendChart() {
    // This would be implemented with a charting library like Chart.js
    // For now, we'll just show a placeholder
    const chartPlaceholder = document.querySelector('.chart-placeholder');
    chartPlaceholder.innerHTML = '<p>Loading price trend chart...</p>';
}

// Chat Functions
function initializeChat() {
    const chatOverlay = document.querySelector('.chat-overlay');
    const startChatButton = document.querySelector('.start-chat');
    const closeChat = document.querySelector('.close-chat');
    const chatContainer = document.querySelector('.chat-container');
    const messageInput = document.querySelector('.message-input');
    const sendButton = document.querySelector('.send-button');

    // Initialize send button icon
    if (sendButton) {
        sendButton.innerHTML = `<i class="fas fa-paper-plane"></i>`;
    }

    // Landing page interactions
    startChatButton?.addEventListener('click', () => {
        chatOverlay.classList.add('active');
        initChat();
    });

    closeChat?.addEventListener('click', () => {
        chatOverlay.classList.remove('active');
    });

    function initChat() {
        // Clear any existing messages
        if (chatContainer) {
            chatContainer.innerHTML = '';
            
            // Add initial greeting
            addMessage({
                type: 'assistant',
                content: "👋 Hello! I'm your AI real estate assistant powered by Google's Gemini. How can I help you find your perfect property today?\n\nYou can ask me questions like:\n- Find me a 2BHK apartment in Karapakkam under 60 lakhs\n- I'm looking for a property with a playground and gym\n- Show me spacious 3BHK apartments with parking in OMR"
            });

            // Enable input
            if (messageInput) {
                messageInput.value = '';
                messageInput.focus();
            }
        }
    }

    function addMessage({ type, content }) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const iconDiv = document.createElement('div');
        iconDiv.className = 'message-icon';
        iconDiv.innerHTML = type === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // Convert newlines to <br> and handle bullet points
        const formattedContent = content
            .split('\n')
            .map(line => {
                if (line.startsWith('- ')) {
                    return `<span class="bullet-point">•</span> ${line.substring(2)}`;
                }
                return line;
            })
            .join('<br>');
        
        contentDiv.innerHTML = formattedContent;
        
        messageDiv.appendChild(iconDiv);
        messageDiv.appendChild(contentDiv);
        
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function handleSendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        // Disable input and button while processing
        messageInput.disabled = true;
        sendButton.disabled = true;
        sendButton.innerHTML = `<i class="fas fa-spinner fa-spin"></i>`;

        // Add user message
        addMessage({
            type: 'user',
            content: message
        });

        try {
            // Send message to backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });

            if (!response.ok) throw new Error('Failed to send message');

            const data = await response.json();

            // Add assistant response
            addMessage({
                type: 'assistant',
                content: data.response || data.message
            });

            // If there are properties in the response, display them
            if (data.properties && data.properties.length > 0) {
                const propertiesList = document.createElement('div');
                propertiesList.className = 'properties-list';
                
                data.properties.forEach(property => {
                    const propertyCard = document.createElement('div');
                    propertyCard.className = 'property-card';
                    propertyCard.innerHTML = `
                        <h3>${property.location}</h3>
                        <p><i class="fas fa-rupee-sign"></i> ${property.price.toLocaleString('en-IN')}</p>
                        <p><i class="fas fa-vector-square"></i> ${property.area} sq ft</p>
                        <p><i class="fas fa-home"></i> ${property.bhk} BHK</p>
                        ${property.amenities ? `<p><i class="fas fa-star"></i> ${property.amenities.join(', ')}</p>` : ''}
                    `;
                    propertiesList.appendChild(propertyCard);
                });

                chatContainer.appendChild(propertiesList);
            }

        } catch (error) {
            console.error('Error:', error);
            addMessage({
                type: 'assistant',
                content: "I apologize, but I encountered an error processing your request. Please try again."
            });
        } finally {
            // Re-enable input and button
            messageInput.disabled = false;
            sendButton.disabled = false;
            sendButton.innerHTML = `<i class="fas fa-paper-plane"></i>`;
            messageInput.value = '';
            messageInput.focus();
        }
    }

    // Event listeners for sending messages
    sendButton?.addEventListener('click', handleSendMessage);
    
    messageInput?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });

    // Enable/disable send button based on input
    messageInput?.addEventListener('input', () => {
        if (sendButton) {
            sendButton.disabled = !messageInput.value.trim();
        }
        // Auto-resize textarea
        messageInput.style.height = 'auto';
        messageInput.style.height = messageInput.scrollHeight + 'px';
    });

    // Initialize chat if we're starting with the overlay active
    if (chatOverlay?.classList.contains('active')) {
        initChat();
    }
}

// Notification System
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    // Add notification styles
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 16px 24px;
        border-radius: 8px;
        background-color: ${type === 'success' ? '#00C851' : '#ff4444'};
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;

    document.body.appendChild(notification);

    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Add notification animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Handle window resize
let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        const navLinks = document.querySelector('.nav-links');
        if (window.innerWidth > 768) {
            navLinks.classList.remove('active');
        }
    }, 250);
}); 