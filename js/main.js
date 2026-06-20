document.addEventListener('DOMContentLoaded', () => {
    // Theme Switcher Logic
    const body = document.body;
    const themeToggle = document.getElementById('theme-toggle');
    
    // Check saved theme or default to dark
    const savedTheme = localStorage.getItem('cacts-theme') || 'dark';
    if (savedTheme === 'light') {
        body.classList.add('light-theme');
        if (themeToggle) themeToggle.textContent = '🌙'; // Moon to switch to dark
    } else {
        body.classList.remove('light-theme');
        if (themeToggle) themeToggle.textContent = '☀️'; // Sun to switch to light
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const isLight = body.classList.contains('light-theme');
            if (isLight) {
                body.classList.remove('light-theme');
                localStorage.setItem('cacts-theme', 'dark');
                themeToggle.textContent = '☀️';
            } else {
                body.classList.add('light-theme');
                localStorage.setItem('cacts-theme', 'light');
                themeToggle.textContent = '🌙';
            }
        });
    }

    // 1. Sticky Header scroll effect
    const header = document.querySelector('.site-header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // 2. Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            const isVisible = navLinks.style.display === 'flex';
            navLinks.style.display = isVisible ? 'none' : 'flex';
            navLinks.style.flexDirection = 'column';
            navLinks.style.position = 'absolute';
            navLinks.style.top = '100%';
            navLinks.style.left = '0';
            navLinks.style.width = '100%';
            navLinks.style.background = 'var(--bg-main)';
            navLinks.style.borderBottom = '1px solid var(--border)';
            navLinks.style.padding = '1.5rem';
            navLinks.style.gap = '1.5rem';
        });
    }

    // 3. Dynamic Footer Year
    const yearElement = document.getElementById('footer-year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }

    // 4. Accordion Toggle (for Curriculum & FAQs)
    document.addEventListener('click', (e) => {
        const headerToggle = e.target.closest('.module-header') || e.target.closest('.faq-header');
        if (headerToggle) {
            const content = headerToggle.nextElementSibling;
            if (content) {
                const isOpen = content.classList.contains('active');
                
                // Close other elements in the same parent if needed
                const container = headerToggle.parentElement.parentElement;
                container.querySelectorAll('.module-content, .faq-content').forEach(c => {
                    c.classList.remove('active');
                    c.style.maxHeight = null;
                });
                
                const icon = headerToggle.querySelector('.accordion-icon');
                container.querySelectorAll('.accordion-icon').forEach(i => {
                    if (i) i.textContent = '+';
                });

                if (!isOpen) {
                    content.classList.add('active');
                    content.style.maxHeight = content.scrollHeight + "px";
                    if (icon) icon.textContent = '−';
                }
            }
        }
    });

    // 5. Contact Lead Form submission handling
    const leadForms = document.querySelectorAll('.lead-form, #inquiry-form');
    leadForms.forEach(form => {
        const phoneInput = form.querySelector('input[name="phone"]');
        if (phoneInput) {
            phoneInput.addEventListener('input', () => {
                phoneInput.setCustomValidity("");
            });
        }

        form.addEventListener('submit', (e) => {
            e.preventDefault();

            // Validate phone number regex
            if (phoneInput) {
                const phoneVal = phoneInput.value.replace(/\s+/g, '').replace(/^\+91/, '');
                const phoneRegex = /^[6-9]\d{9}$/;
                if (!phoneRegex.test(phoneVal)) {
                    phoneInput.setCustomValidity("Please enter a valid 10-digit Indian mobile number (starting with 6-9).");
                    phoneInput.reportValidity();
                    return;
                } else {
                    phoneInput.setCustomValidity("");
                }
            }

            const formData = new FormData(form);
            const data = {};
            formData.forEach((value, key) => { data[key] = value; });

            // Store inquiry locally to simulate persistence
            const inquiries = JSON.parse(localStorage.getItem('cacts_inquiries') || '[]');
            data.timestamp = new Date().toISOString();
            inquiries.push(data);
            localStorage.setItem('cacts_inquiries', JSON.stringify(inquiries));

            // Construct WhatsApp/SMS query string details
            const messageText = `Hi CACTS, I want to inquire for a Free 1-to-1 Trial Demo.\n\n` +
                                `• Name: ${data.name || ''}\n` +
                                `• Course: ${data.course || ''}\n` +
                                `• Phone: ${data.phone || ''}\n` +
                                `• Email: ${data.email || ''}\n` +
                                `• Exp: ${data.experience || 'Student'}\n` +
                                `• Notes: ${data.notes || 'None'}`;
            
            const waUrl = `https://wa.me/919665566357?text=${encodeURIComponent(messageText)}`;
            const smsUrl = `sms:+919665566357?body=${encodeURIComponent(messageText)}`;

            // Show customized redirect confirmation box
            const container = form.parentElement;
            container.innerHTML = `
                <div style="text-align: center; padding: 2rem 1rem;">
                    <div style="width: 64px; height: 64px; background: var(--accent-glow); border: 2px solid var(--accent); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem auto;">
                        <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" style="color: var(--accent-light);"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg>
                    </div>
                    <h3 style="font-size: 1.5rem; margin-bottom: 0.5rem; font-family: var(--font-heading); color: var(--text-primary);">Inquiry Compiled!</h3>
                    <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 1.5rem;">Redirecting you to WhatsApp to complete submission...</p>
                    
                    <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                        <a href="${waUrl}" class="btn btn-accent" target="_blank" style="color: #0b0f19; width: 100%; text-align: center; font-weight:700;">
                            Submit via WhatsApp (Manual Link)
                        </a>
                        <a href="${smsUrl}" class="btn btn-secondary" style="width: 100%; text-align: center;">
                            Submit via SMS Text
                        </a>
                    </div>
                    <p style="color: var(--warning); font-size: 0.82rem; margin-top: 1.25rem; border-top: 1px solid var(--border); padding-top: 1rem; line-height: 1.4;">
                        ⚠️ Pop-up blocked? If the WhatsApp window did not open automatically, please click the "Submit via WhatsApp" button above to finalize your inquiry.
                    </p>
                </div>
            `;

            // Auto-redirect to WhatsApp
            setTimeout(() => {
                window.open(waUrl, '_blank');
            }, 1200);
        });
    });
});
