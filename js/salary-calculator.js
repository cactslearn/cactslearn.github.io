/* ==========================================================================
   PUNE IT SALARY CALCULATOR LOGIC (js/salary-calculator.js)
   Interactive calculator calculating LPA ranges, ATS pass rate & proof bonuses
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
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

    if (expVal) {
      expVal.textContent = yrs === 0 ? '0 Years (Fresher Entry)' : `${yrs} Year${yrs > 1 ? 's' : ''} Experience`;
    }

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

    if (resSalary) {
      resSalary.textContent = `₹${minLPA.toFixed(1)} LPA – ₹${maxLPA.toFixed(1)} LPA`;
    }
    if (resGapBadge) {
      resGapBadge.textContent = proofVal === 'proof' ? `+₹${proofBonus.toFixed(1)} LPA Verified Code Bonus Included` : `-₹${(minLPA * 0.3).toFixed(1)} LPA Paper Cert Penalty`;
      resGapBadge.style.background = proofVal === 'proof' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)';
      resGapBadge.style.color = proofVal === 'proof' ? '#10b981' : '#ef4444';
    }

    if (resAts) resAts.textContent = atsPass;
    if (resOutlook) resOutlook.textContent = info.outlook;
    if (resPosition) resPosition.textContent = info.pos;
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
});
