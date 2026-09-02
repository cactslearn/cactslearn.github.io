// Global Data Privacy Consent Notice Language Switcher (EN, MR, HI)
window.toggleDpdpLang = function(selectElem) {
 if (!selectElem) return;
 const container = selectElem.closest('.dpdp-consent-container');
 if (!container) return;
 const lang = selectElem.value;
 const enText = container.querySelector('.dpdp-text-en');
 const mrText = container.querySelector('.dpdp-text-mr');
 const hiText = container.querySelector('.dpdp-text-hi');
 if (enText) enText.style.display = lang === 'en' ? 'inline' : 'none';
 if (mrText) mrText.style.display = lang === 'mr' ? 'inline' : 'none';
 if (hiText) hiText.style.display = lang === 'hi' ? 'inline' : 'none';
};

document.addEventListener('DOMContentLoaded', () => {
 // Theme Switcher Logic
 const body = document.body;
 const themeToggle = document.getElementById('theme-toggle');
 const sunIcon = themeToggle ? themeToggle.querySelector('.sun-icon') : null;
 const moonIcon = themeToggle ? themeToggle.querySelector('.moon-icon') : null;

 // Check saved theme or detect system theme preference
 let savedTheme = localStorage.getItem('cacts-theme');
 if (!savedTheme) {
 const prefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
 savedTheme = prefersLight ? 'light' : 'dark';
 }

 if (savedTheme === 'light') {
 body.classList.add('light-theme');
 if (sunIcon) sunIcon.style.display = 'none';
 if (moonIcon) moonIcon.style.display = 'block';
 } else {
 body.classList.remove('light-theme');
 if (sunIcon) sunIcon.style.display = 'block';
 if (moonIcon) moonIcon.style.display = 'none';
 }

 if (themeToggle) {
 themeToggle.addEventListener('click', () => {
 const isLight = body.classList.contains('light-theme');
 const sun = themeToggle.querySelector('.sun-icon');
 const moon = themeToggle.querySelector('.moon-icon');
 if (isLight) {
 body.classList.remove('light-theme');
 localStorage.setItem('cacts-theme', 'dark');
 if (sun) sun.style.display = 'block';
 if (moon) moon.style.display = 'none';
 } else {
 body.classList.add('light-theme');
 localStorage.setItem('cacts-theme', 'light');
 if (sun) sun.style.display = 'none';
 if (moon) moon.style.display = 'block';
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

 // Pre-select course option in contact form from URL query parameter
 const urlParams = new URLSearchParams(window.location.search);
 const courseParam = urlParams.get('course');
 if (courseParam) {
 const courseSelect = document.getElementById('course_choice');
 if (courseSelect) {
 const decodedCourse = decodeURIComponent(courseParam).toLowerCase();
 for (let i = 0; i < courseSelect.options.length; i++) {
 const option = courseSelect.options[i];
 if (option.value.toLowerCase() === decodedCourse || option.text.toLowerCase().includes(decodedCourse)) {
 option.selected = true;
 break;
 }
 }
 }
 }

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
 <p style="color: var(--warning); font-size: 0.82rem; margin-top: 1.25rem; border-top: 1px solid var(--border); padding-top: 1rem; line-height: 1.4; display: flex; align-items: flex-start; gap: 0.35rem;">
 <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color: var(--warning); flex-shrink: 0; margin-top: 0.15rem;"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
 <span>Pop-up blocked? If the WhatsApp window did not open automatically, please click the "Submit via WhatsApp" button above to finalize your inquiry.</span>
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

// Register booking tool for visiting WebMCP AI agents
const mcpContext = (typeof navigator !== "undefined" && (navigator.modelContext || navigator.mcp)) || (typeof window !== "undefined" && window.modelContext);
if (mcpContext && typeof mcpContext.registerTool === "function") {
 mcpContext.registerTool({
 name: "book_one_to_one_trial",
 description: "Books a free 1-to-1 virtual software training trial demo or career roadmap consultation at CACTS Pune.",
 consentRequired: true,
 userConsentRequired: true,
 inputSchema: {
 type: "object",
 properties: {
 name: { type: "string", description: "Full name of the student" },
 phone: { type: "string", description: "Mobile/WhatsApp contact number with country code" },
 course: { type: "string", description: "Target technology track (e.g., 'Java Fullstack', 'React JS', 'DevOps')" }
 },
 required: ["name", "phone", "course"]
 },
 execute: async (args) => {
 const encodedName = encodeURIComponent(args.name);
 const encodedPhone = encodeURIComponent(args.phone);
 const encodedCourse = encodeURIComponent(args.course);

 return {
 status: "success",
 message: "Lead compiled successfully. Redirect the user to the generated WhatsApp link to complete booking.",
 whatsapp_url: `https://wa.me/919665566357?text=Hi%20CACTS,%20I'm%20${encodedName},%20phone%20${encodedPhone},%20interested%20in%20the%201-to-1%20${encodedCourse}%20training.`
 };
 }
 });
}
 // --- PUNE IT SALARY CALCULATOR LOGIC ---
 const calcTrack = document.getElementById('calc-track');
 const calcExp = document.getElementById('calc-exp');
 const calcProof = document.getElementById('calc-proof');
 const calcLoc = document.getElementById('calc-location');
 const expVal = document.getElementById('exp-val');
 const resSalary = document.getElementById('res-salary');
 const resGapBadge = document.getElementById('res-gap-badge');
 const resAts = document.getElementById('res-ats');
 const resOutlook = document.getElementById('res-outlook');
 const resPosition = document.getElementById('res-position');
 const resCtaLink = document.getElementById('res-cta-link');

 const trackData = {
 'java': { base: 4.5, expMult: 1.8, name: 'Java Fullstack', link: '../courses/java-fullstack/', pos: 'Fullstack Spring Boot & React Microservices Engineer', outlook: '+18% YOY' },
 'full-stack': { base: 4.5, expMult: 1.8, name: 'MERN Full Stack', link: '../courses/full-stack/', pos: 'Fullstack Node.js & React Developer', outlook: '+18% YOY' },
 'python': { base: 4.0, expMult: 1.6, name: 'Python Automation', link: '../courses/python/', pos: 'Python Developer & Automation Scripting Specialist', outlook: '+15% YOY' },
 'react': { base: 4.2, expMult: 1.7, name: 'React JS', link: '../courses/react-js/', pos: 'Modern Frontend & React 19 Application Developer', outlook: '+16% YOY' },
 'mobile': { base: 4.8, expMult: 1.9, name: 'React Native', link: '../courses/react-native/', pos: 'Cross-Platform iOS & Android Mobile Engineer', outlook: '+20% YOY' },
 'ai': { base: 6.0, expMult: 2.4, name: 'AI & Machine Learning', link: '../courses/ai-ml/', pos: 'AI Application & RAG Pipeline Engineer', outlook: '+34% YOY' },
 'ai-red-teaming': { base: 6.5, expMult: 2.5, name: 'AI Red Teaming & Security', link: '../courses/ai-red-teaming/', pos: 'AI Red Teamer & LLM Security Specialist', outlook: '+38% YOY' },
 'data-science': { base: 5.5, expMult: 2.2, name: 'Data Science', link: '../courses/data-science/', pos: 'Data Scientist & Predictive Analytics Engineer', outlook: '+26% YOY' },
 'data-eng': { base: 5.5, expMult: 2.2, name: 'Data Engineering', link: '../courses/data-engineering/', pos: 'Apache Spark & Data Lake Pipeline Architect', outlook: '+28% YOY' },
 'devops': { base: 5.2, expMult: 2.1, name: 'DevOps & Cloud', link: '../courses/devops/', pos: 'Cloud Native Kubernetes & Terraform DevOps Architect', outlook: '+22% YOY' },
 'cloud': { base: 5.5, expMult: 2.2, name: 'Cloud Architecture', link: '../courses/cloud/', pos: 'Multi-Cloud AWS & Azure Solutions Architect', outlook: '+24% YOY' },
 'powerbi': { base: 4.0, expMult: 1.5, name: 'Power BI Analytics', link: '../courses/power-bi/', pos: 'BI Analytics & DAX Dashboard Specialist', outlook: '+14% YOY' },
 'testing': { base: 3.8, expMult: 1.5, name: 'Software Testing', link: '../courses/software-testing/', pos: 'SDET & Selenium Test Automation Engineer', outlook: '+12% YOY' },
 'cybersecurity': { base: 5.0, expMult: 2.0, name: 'Cybersecurity Operations', link: '../courses/cybersecurity/', pos: 'Cybersecurity Analyst & SOC Operations Engineer', outlook: '+22% YOY' },
 'blockchain': { base: 6.2, expMult: 2.4, name: 'Blockchain Development', link: '../courses/blockchain/', pos: 'Web3 & Solidity Smart Contract Developer', outlook: '+30% YOY' },
 'architect': { base: 12.0, expMult: 2.8, name: 'Software Architecture', link: '../courses/software-architect/', pos: 'Enterprise Distributed Systems Architect', outlook: '+25% YOY' }
 };

 function updateSalaryCalculator() {
 if (!calcTrack || !calcExp || !calcProof || !calcLoc) return;

 const trackKey = calcTrack.value;
 const yrs = parseInt(calcExp.value, 10);
 const proofVal = calcProof.value;
 const locVal = calcLoc.value;

 const info = trackData[trackKey] || trackData['java'];

 expVal.textContent = yrs === 0 ? '0 Years (Fresher Entry)' : `${yrs} Year${yrs > 1 ? 's' : ''} Experience`;

 // Calculate LPA Range
 let minLPA = info.base + (yrs * info.expMult);
 let maxLPA = minLPA * 1.55;

 // Proof Multipliers
 let proofBonus = 0;
 let atsPass = '55% Pass Rate';

 if (proofVal === 'cert') {
 minLPA *= 0.75;
 maxLPA *= 0.75;
 proofBonus = 0;
 atsPass = '32% Pass Rate (High ATS Rejection)';
 } else if (proofVal === 'basic') {
 minLPA *= 0.9;
 maxLPA *= 0.9;
 proofBonus = 0.8;
 atsPass = '60% Pass Rate';
 } else {
 proofBonus = 2.4;
 atsPass = '87% Pass Rate (Verified PRs)';
 }

 // Location Multiplier
 if (locVal === 'remote') {
 minLPA *= 1.15;
 maxLPA *= 1.25;
 }

 resSalary.textContent = `₹${minLPA.toFixed(1)} LPA – ₹${maxLPA.toFixed(1)} LPA`;
 resGapBadge.textContent = proofVal === 'proof' ? `+₹${proofBonus.toFixed(1)} LPA Verified Code Bonus Included` : `-₹${(minLPA * 0.3).toFixed(1)} LPA Paper Cert Penalty`;
 resGapBadge.style.background = proofVal === 'proof' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)';
 resGapBadge.style.color = proofVal === 'proof' ? '#10b981' : '#ef4444';

 resAts.textContent = atsPass;
 resOutlook.textContent = info.outlook;
 resPosition.textContent = info.pos;
 if (resCtaLink) {
 resCtaLink.href = info.link;
 resCtaLink.textContent = `Explore ${info.name} 1-to-1 Mentorship ↗`;
 }
 }

 if (calcTrack && calcExp && calcProof && calcLoc) {
 calcTrack.addEventListener('change', updateSalaryCalculator);
 calcExp.addEventListener('input', updateSalaryCalculator);
 calcProof.addEventListener('change', updateSalaryCalculator);
 calcLoc.addEventListener('change', updateSalaryCalculator);
 updateSalaryCalculator();
 }

 // --- COURSE READINESS DIAGNOSTIC LOGIC ---
 let currentQ = 1;
 const totalQ = 5;
 const qQuestions = document.querySelectorAll('.quiz-q');
 const quizPrev = document.getElementById('quiz-prev');
 const quizNext = document.getElementById('quiz-next');
 const stepInd = document.getElementById('quiz-step-indicator');
 const quizContainer = document.getElementById('quiz-container');
 const quizResults = document.getElementById('quiz-results');

 function showQuestion(qNum) {
 if (!qQuestions || qQuestions.length === 0) return;
 qQuestions.forEach(el => {
 el.style.display = parseInt(el.getAttribute('data-q'), 10) === qNum ? 'block' : 'none';
 });
 if (stepInd) stepInd.textContent = `QUESTION ${qNum} OF ${totalQ}`;
 if (quizPrev) quizPrev.style.display = qNum > 1 ? 'inline-block' : 'none';
 if (quizNext) quizNext.textContent = qNum === totalQ ? 'Calculate Readiness Score ' : 'Next Question →';
 }

 if (quizNext) {
 quizNext.addEventListener('click', () => {
 if (currentQ < totalQ) {
 currentQ++;
 showQuestion(currentQ);
 } else {
 // Calculate Score
 let score = 0;
 for (let i = 1; i <= 4; i++) {
 const sel = document.querySelector(`input[name="q${i}"]:checked`);
 if (sel) score += parseInt(sel.value, 10);
 }
 const trackSel = document.querySelector('input[name="q5"]:checked');
 const selectedTrack = trackSel ? trackSel.value : 'java-fullstack';

 // Display Results
 if (quizContainer) quizContainer.style.display = 'none';
 if (quizResults) quizResults.style.display = 'block';

 const pct = Math.round((score / 12) * 100);
 const qScoreTitle = document.getElementById('q-score-title');
 const qScoreDesc = document.getElementById('q-score-desc');
 const qRecTrack = document.getElementById('q-rec-track');
 const qRecTime = document.getElementById('q-rec-time');
 const qRecRisk = document.getElementById('q-rec-risk');
 const qRecLink = document.getElementById('q-rec-link');

 if (pct >= 80) {
 qScoreTitle.textContent = `${pct}% High Developer Readiness`;
 qScoreDesc.textContent = 'You possess a solid analytical mindset and strong debugging commitment. You are well-positioned for 1-to-1 intensive developer lab mentorship.';
 qRecTime.textContent = '12 to 16 Weeks';
 qRecRisk.textContent = 'Low Risk (Future-Proof)';
 } else if (pct >= 55) {
 qScoreTitle.textContent = `${pct}% Moderate Readiness`;
 qScoreDesc.textContent = 'You have good potential, but need consistent daily hands-on keyboard time (10+ hrs/wk) to build line-by-line debugging confidence.';
 qRecTime.textContent = '16 to 20 Weeks';
 qRecRisk.textContent = 'Moderate Risk';
 } else {
 qScoreTitle.textContent = `${pct}% Foundation Building Phase`;
 qScoreDesc.textContent = 'We recommend starting with logic foundations and dedicated 1-to-1 mentorship to avoid getting overwhelmed by batch fast-pacing.';
 qRecTime.textContent = '20+ Weeks';
 qRecRisk.textContent = 'High Batch Risk';
 }

 if (selectedTrack === 'ai-ml') {
 if (qRecTrack) qRecTrack.textContent = 'AI & Machine Learning Engineering';
 if (qRecLink) qRecLink.href = 'ai-ml-training.html';
 } else if (selectedTrack === 'devops') {
 if (qRecTrack) qRecTrack.textContent = 'DevOps & Cloud Architecture';
 if (qRecLink) qRecLink.href = 'devops-training.html';
 } else {
 if (qRecTrack) qRecTrack.textContent = 'Java Fullstack Engineering';
 if (qRecLink) qRecLink.href = 'java-fullstack-training.html';
 }
 }
 });
 }

 if (quizPrev) {
 quizPrev.addEventListener('click', () => {
 if (currentQ > 1) {
 currentQ--;
 showQuestion(currentQ);
 }
 });
 }
