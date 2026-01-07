/* ============================================
   Master SK Academy - JavaScript
   Mobile Menu, Smooth Scrolling, Form Handling
   ============================================ */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {

    // ============================================
    // Mobile Hamburger Menu Toggle
    // ============================================
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('navMenu');

    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function () {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // Close menu when clicking on a nav link
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function () {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', function (event) {
            const isClickInsideNav = navMenu.contains(event.target);
            const isClickOnHamburger = hamburger.contains(event.target);

            if (!isClickInsideNav && !isClickOnHamburger && navMenu.classList.contains('active')) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    }

    // ============================================
    // Smooth Scrolling for Anchor Links
    // ============================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');

            // Only prevent default if it's a hash link to an element on the same page
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                const target = document.querySelector(href);

                if (target) {
                    const headerOffset = 80;
                    const elementPosition = target.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // ============================================
    // Form Handling - Inquiry Form (Admissions Page)
    // ============================================
    const inquiryForm = document.getElementById('inquiryForm');

    if (inquiryForm) {
        inquiryForm.addEventListener('submit', function (e) {
            e.preventDefault();

            // Get form data
            const formData = {
                studentName: document.getElementById('studentName').value,
                parentName: document.getElementById('parentName').value,
                phone: document.getElementById('phone').value,
                email: document.getElementById('email').value,
                class: document.getElementById('class').value,
                message: document.getElementById('message').value
            };

            // Basic validation
            if (!formData.studentName || !formData.parentName || !formData.phone || !formData.class) {
                alert('Please fill in all required fields.');
                return;
            }

            // Phone number validation (basic)
            const phoneRegex = /^[0-9]{10}$/;
            if (!phoneRegex.test(formData.phone.replace(/\D/g, ''))) {
                alert('Please enter a valid 10-digit phone number.');
                return;
            }

            // Email validation (if provided)
            if (formData.email) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(formData.email)) {
                    alert('Please enter a valid email address.');
                    return;
                }
            }

            // Send data to backend
            fetch('http://localhost:8000/submit-admission', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    }
                    throw new Error('Network response was not ok.');
                })
                .then(data => {
                    alert('Thank you for your inquiry! We will contact you shortly.');
                    inquiryForm.reset();
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Sorry, there was an error submitting your form. Please try again later or contact us directly.');
                });
        });
    }

    // ============================================
    // Form Handling - Contact Form
    // ============================================
    const contactForm = document.getElementById('contactForm');

    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();

            // Get form data
            const formData = {
                name: document.getElementById('contactName').value,
                phone: document.getElementById('contactPhone').value,
                email: document.getElementById('contactEmail').value,
                subject: document.getElementById('contactSubject').value,
                message: document.getElementById('contactMessage').value
            };

            // Basic validation
            if (!formData.name || !formData.phone || !formData.email || !formData.subject || !formData.message) {
                alert('Please fill in all required fields.');
                return;
            }

            // Email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(formData.email)) {
                alert('Please enter a valid email address.');
                return;
            }

            // Phone number validation (basic)
            const phoneRegex = /^[0-9]{10}$/;
            if (!phoneRegex.test(formData.phone.replace(/\D/g, ''))) {
                alert('Please enter a valid 10-digit phone number.');
                return;
            }

            // Send data to backend
            fetch('http://localhost:8000/submit-contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    }
                    throw new Error('Network response was not ok.');
                })
                .then(data => {
                    alert('Thank you for contacting us! We will get back to you soon.');
                    contactForm.reset();
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Sorry, there was a problem sending your message. Please try again later.');
                });
        });
    }

    // ============================================
    // Scroll Animations (Fade in on scroll)
    // ============================================
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements for scroll animation
    const animateElements = document.querySelectorAll('.highlight-card, .course-card, .feature-box, .philosophy-item, .methodology-card, .detail-card, .contact-card');
    animateElements.forEach(el => {
        observer.observe(el);
    });

    // ============================================
    // Active Navigation Link Highlighting
    // ============================================
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        const linkHref = link.getAttribute('href');
        if (linkHref === currentPage || (currentPage === '' && linkHref === 'index.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // ============================================
    // Header Scroll Effect (Optional Enhancement)
    // ============================================
    const header = document.querySelector('.header');
    let lastScroll = 0;

    window.addEventListener('scroll', function () {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            header.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
        } else {
            header.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
        }

        lastScroll = currentScroll;
    });

    // ============================================
    // Button Hover Effects Enhancement
    // ============================================
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function () {
            this.style.transition = 'all 0.3s ease';
        });
    });

    // ============================================
    // Form Input Enhancement
    // ============================================
    const formInputs = document.querySelectorAll('input, textarea, select');
    formInputs.forEach(input => {
        // Add focus effect
        input.addEventListener('focus', function () {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function () {
            this.parentElement.classList.remove('focused');
        });
    });

    // ============================================
    // Console Welcome Message (for developers)
    // ============================================
    console.log('%cMaster SK Academy', 'color: #1a365d; font-size: 20px; font-weight: bold;');
    console.log('%cWebsite loaded successfully!', 'color: #6b7280; font-size: 12px;');
    console.log('%cFor inquiries, please contact us through the contact form.', 'color: #6b7280; font-size: 12px;');
});

// ============================================
// Utility Functions
// ============================================

// Function to validate phone number (can be used elsewhere)
function validatePhone(phone) {
    const cleaned = phone.replace(/\D/g, '');
    return cleaned.length === 10;
}

// Function to validate email (can be used elsewhere)
function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// Function to format phone number (optional enhancement)
function formatPhoneNumber(phone) {
    const cleaned = phone.replace(/\D/g, '');
    if (cleaned.length === 10) {
        return cleaned.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
    }
    return phone;
}

// ============================================
// Chat Widget Logic
// ============================================
document.addEventListener('DOMContentLoaded', function () {
    const chatBtn = document.getElementById('chatBtn');
    const chatContainer = document.getElementById('chatContainer');
    const closeChat = document.getElementById('closeChat');
    const chatInput = document.getElementById('chatInput');
    const sendMessage = document.getElementById('sendMessage');
    const chatMessages = document.getElementById('chatMessages');

    if (chatBtn && chatContainer) {
        // Toggle Chat
        chatBtn.addEventListener('click', () => {
            chatContainer.classList.toggle('active');
            if (chatContainer.classList.contains('active')) {
                chatInput.focus();
            }
        });

        closeChat.addEventListener('click', () => {
            chatContainer.classList.remove('active');
        });

        // Send Message Logic
        function handleSendMessage() {
            const message = chatInput.value.trim();
            if (!message) return;

            // Add User Message
            addMessage(message, 'user');
            chatInput.value = '';

            // Show specific loading or bot status could go here

            // Call Backend
            fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            })
                .then(response => response.json())
                .then(data => {
                    addMessage(data.answer, 'bot');
                })
                .catch(error => {
                    console.error('Error:', error);
                    addMessage("I'm sorry, I'm having trouble connecting to the server. Please check if the backend is running.", 'bot');
                });
        }

        sendMessage.addEventListener('click', handleSendMessage);

        chatInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                handleSendMessage();
            }
        });

        function addMessage(text, sender) {
            const msgDiv = document.createElement('div');
            msgDiv.classList.add('message', sender);

            // If bot, we might render simple markdown or newlines
            // For now, textContent is safer, but innerHTML allows formatting
            if (sender === 'bot') {
                // Convert newlines to <br> for basic formatting
                msgDiv.innerHTML = text.replace(/\n/g, '<br>');
            } else {
                msgDiv.textContent = text;
            }

            chatMessages.appendChild(msgDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
});

