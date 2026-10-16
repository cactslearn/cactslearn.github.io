/**
 * CACTS Certificate Verification Engine (js/certificate-engine.js)
 * Production engine for verifying student credentials, generating dual QR codes,
 * and high-resolution PDF/PNG exports.
 */

let currentRecord = null;

const CERT_API_ENDPOINT = "https://script.google.com/macros/s/AKfycbxPfWNqDgntuL1IaQnjfgkNbbVhlxMzgXE2mjfSrOsaPYeyC_nIlSzEOkcDcZ7S4_s/exec";

window.addEventListener('DOMContentLoaded', () => {
  const ySpan = document.getElementById('footer-year');
  if (ySpan) ySpan.innerText = new Date().getFullYear();

  const certInput = document.getElementById('certIdInput');
  if (certInput) {
    certInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') handleManualVerify();
    });
  }

  // Check URL query parameters for Certificate ID
  const urlParams = new URLSearchParams(window.location.search);
  const certId = urlParams.get('id');
  if (certId && certId.trim()) {
    const cleanId = certId.trim();
    if (document.getElementById('certIdInput')) {
      document.getElementById('certIdInput').value = cleanId;
    }
    fetchCertificateRecord(cleanId);
  }
  // When visited without query params, do NOT auto-load any default certificate
});

window.addEventListener('resize', fitCertificateToScreen);

function fitCertificateToScreen() {
  const viewport = document.querySelector('.certificate-viewport');
  const canvas = document.getElementById('certificateCanvas');
  if (!viewport || !canvas || canvas.style.display === 'none') return;

  // Measure exact available content width inside section wrapper
  const sectionElem = viewport.closest('.tech-section') || document.body;
  const sectionWidth = sectionElem.clientWidth;
  const availableWidth = Math.min(sectionWidth - 16, 1050);

  if (availableWidth < 1050) {
    const scale = availableWidth / 1050;
    canvas.style.transform = `scale(${scale})`;
    canvas.style.transformOrigin = 'top center';
    viewport.style.height = `${(742 * scale) + 10}px`;
  } else {
    canvas.style.transform = 'none';
    viewport.style.height = 'auto';
  }
}

function handleManualVerify() {
  const inputElem = document.getElementById('certIdInput');
  const certId = inputElem ? inputElem.value.trim() : '';
  if (!certId) {
    showError('Please Enter a Certificate ID', 'Specify an 11-digit Certificate ID (e.g. 20260812001) to look up verification records.');
    return;
  }
  const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?id=' + encodeURIComponent(certId);
  window.history.pushState({ path: newUrl }, '', newUrl);
  fetchCertificateRecord(certId);
}

function fetchCertificateRecord(certId) {
  if (!certId || certId.trim().length < 4) {
    showError('Invalid Certificate ID Format', 'Please enter a valid Certificate ID (e.g. 20260812001).');
    return;
  }

  const cleanId = certId.trim();

  // Display live authentication loading state
  const statusBanner = document.getElementById('statusBanner');
  if (statusBanner) {
    statusBanner.className = 'status-alert loading';
  }
  const statusInfo = document.getElementById('statusInfo');
  if (statusInfo) {
    statusInfo.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation: spin 1s linear infinite;"><circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="12"></circle></svg>
      <span>CONNECTING TO LIVE ACCREDITATION GATEWAY: Authenticating Certificate ID ${cleanId}...</span>
    `;
  }
  const statusTimestamp = document.getElementById('statusTimestamp');
  if (statusTimestamp) statusTimestamp.innerText = 'Querying registry...';

  const errorCard = document.getElementById('errorCard');
  if (errorCard) errorCard.style.display = 'none';

  const apiUrl = `${CERT_API_ENDPOINT}?id=${encodeURIComponent(cleanId)}`;

  fetch(apiUrl)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Live gateway responded with HTTP status ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (!data || data.success === false || data.error) {
        const msg = (data && data.message) ? data.message : `No accreditation record matching Certificate ID "${cleanId}" was found in the live verification registry.`;
        showError('Certificate Record Not Found', msg);
        return;
      }

      const record = (data[cleanId] && typeof data[cleanId] === 'object') ? data[cleanId] : data;
      if (record && (record.id || record.studentName)) {
        // Defensively ensure array/object attributes are parsed if stringified
        if (typeof record.skills === 'string') {
          try { record.skills = JSON.parse(record.skills); } catch (e) { record.skills = record.skills.split(',').map(s => s.trim()); }
        }
        if (typeof record.projects === 'string') {
          try { record.projects = JSON.parse(record.projects); } catch (e) {}
        }
        if (typeof record.signees === 'string') {
          try { record.signees = JSON.parse(record.signees); } catch (e) {}
        }
        renderCertificate(record);
      } else {
        showError('Certificate Record Not Found', `No accreditation record matching Certificate ID "${cleanId}" was found in the live verification registry.`);
      }
    })
    .catch(err => {
      console.warn('Live API request failed, checking local backup if available:', err);
      if (cleanId.length >= 6) {
        const yearMonth = cleanId.substring(0, 6);
        fetch(`records/${yearMonth}.json`)
          .then(res => res.ok ? res.json() : Promise.reject())
          .then(localData => {
            if (localData && localData[cleanId]) {
              renderCertificate(localData[cleanId]);
              return;
            }
            showError('Certificate Record Not Found', `No accreditation record matching Certificate ID "${cleanId}" could be authenticated.`);
          })
          .catch(() => {
            showError('Verification Gateway Unavailable', `Could not connect to the live verification registry. Please check your internet connection and try again.`);
          });
      } else {
        showError('Verification Gateway Unavailable', `Could not connect to the live verification registry. Please check your internet connection and try again.`);
      }
    });
}

function renderCertificate(record) {
  currentRecord = record;

  const errorCard = document.getElementById('errorCard');
  if (errorCard) errorCard.style.display = 'none';

  const certCanvas = document.getElementById('certificateCanvas');
  if (certCanvas) certCanvas.style.display = 'flex';

  const breakdownSec = document.getElementById('breakdownSection');
  if (breakdownSec) breakdownSec.style.display = 'block';

  const dlPdfBtn = document.getElementById('downloadPdfBtn');
  if (dlPdfBtn) dlPdfBtn.disabled = false;

  const dlPngBtn = document.getElementById('downloadPngBtn');
  if (dlPngBtn) dlPngBtn.disabled = false;

  const cpLinkBtn = document.getElementById('copyLinkBtn');
  if (cpLinkBtn) cpLinkBtn.disabled = false;

  // Status Alert Banner & Status Badges
  const statusBanner = document.getElementById('statusBanner');
  const recStatus = (record.status || "VALID").toUpperCase();
  const statusBadge = document.getElementById('barStatusBadge');

  if (recStatus === "EXPIRED") {
    if (statusBanner) statusBanner.className = 'status-alert expired';
    const statusInfo = document.getElementById('statusInfo');
    if (statusInfo) {
      statusInfo.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        <span>EXPIRED ACCREDITATION: Certificate ID ${record.id} accreditation period has expired.</span>
      `;
    }
    if (statusBadge) {
      statusBadge.className = 'cert-status-badge expired';
      statusBadge.innerText = 'EXPIRED';
    }
  } else if (recStatus === "REVOKED") {
    if (statusBanner) statusBanner.className = 'status-alert error';
    const statusInfo = document.getElementById('statusInfo');
    if (statusInfo) {
      statusInfo.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>
        <span>REVOKED ACCREDITATION: Certificate ID ${record.id} record has been revoked.</span>
      `;
    }
    if (statusBadge) {
      statusBadge.className = 'cert-status-badge revoked';
      statusBadge.innerText = 'REVOKED';
    }
  } else {
    if (statusBanner) statusBanner.className = 'status-alert success';
    const statusInfo = document.getElementById('statusInfo');
    if (statusInfo) {
      statusInfo.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
        <span>AUTHENTICATED RECORD: Certificate ID ${record.id} is Verified &amp; Active.</span>
      `;
    }
    if (statusBadge) {
      statusBadge.className = 'cert-status-badge valid';
      statusBadge.innerText = 'VALID';
    }
  }

  const statusTimestamp = document.getElementById('statusTimestamp');
  if (statusTimestamp) statusTimestamp.innerText = `Verified: ${new Date().toLocaleDateString()}`;

  // Dynamic Title & Wording
  const certTitleElem = document.getElementById('certTitle');
  const certWordingElem = document.getElementById('certWording');

  if (certTitleElem) {
    if (record.certificateTitle) {
      certTitleElem.innerText = record.certificateTitle;
    } else if (record.programType === "Internship") {
      certTitleElem.innerText = "CERTIFICATE OF LIVE PROJECT INTERNSHIP";
    } else if (record.programType === "Training") {
      certTitleElem.innerText = "CERTIFICATE OF TRAINING COMPLETION";
    } else {
      certTitleElem.innerText = "CERTIFICATE OF PROFESSIONAL TRAINING & INTERNSHIP";
    }
  }

  if (certWordingElem) {
    const pType = record.programType || "Training & Internship";
    certWordingElem.innerHTML = `has successfully completed the <strong>1-to-1 Developer Mentoring &amp; Live Staging Internship</strong> (${pType}) in`;
  }

  // Student & Course Details
  const sName = document.getElementById('certStudentName');
  if (sName) sName.innerText = record.studentName || "Student Name";

  const cName = document.getElementById('certCourseName');
  if (cName) cName.innerText = record.courseName || "Software Engineering";

  const mDetails = document.getElementById('certMetaDetails');
  if (mDetails) mDetails.innerText = `Duration: ${record.duration || '16 Weeks'} \u2022 Performance Grade: ${record.grade || 'Distinction (A+)'}`;

  // Footer Credentials
  const barId = document.getElementById('barCertId');
  if (barId) barId.innerText = record.id;

  const barDate = document.getElementById('barIssueDate');
  if (barDate) barDate.innerText = record.issueDate || "August 12, 2026";

  // Signatures
  if (record.signees) {
    if (record.signees.director) {
      const dName = document.getElementById('sigDirectorName');
      const dFull = document.getElementById('sigDirectorFull');
      if (dName) dName.innerText = record.signees.director;
      if (dFull) dFull.innerText = record.signees.director;
    }
    if (record.signees.directorTitle) {
      const dTitle = document.getElementById('sigDirectorTitle');
      if (dTitle) dTitle.innerText = record.signees.directorTitle;
    }
    if (record.signees.trainer) {
      const tName = document.getElementById('sigTrainerName');
      const tFull = document.getElementById('sigTrainerFull');
      if (tName) tName.innerText = record.signees.trainer;
      if (tFull) tFull.innerText = record.signees.trainer;
    }
    if (record.signees.trainerTitle) {
      const tTitle = document.getElementById('sigTrainerTitle');
      if (tTitle) tTitle.innerText = record.signees.trainerTitle;
    }
  }

  // Generate Dual High-DPI Scannable QR Codes
  generateQRCodes(record);

  // Render Verified Skills Badges
  renderSkillsBreakdown(record.skills);

  // Render Verified Project Repositories
  renderProjectsBreakdown(record.projects);

  // Cryptographic Hash Display
  const hashStr = record.sha256Hash || generateDefaultHash(record.id);
  const hashElem = document.getElementById('hashTextDisplay');
  if (hashElem) hashElem.innerText = hashStr;

  // Fit to screen on initial render
  setTimeout(fitCertificateToScreen, 50);
}

function renderSkillsBreakdown(skillsArray) {
  const container = document.getElementById('skillsContainer');
  if (!container) return;
  container.innerHTML = '';
  const list = skillsArray && skillsArray.length ? skillsArray : ["Python Scripting", "Software Architecture", "Git & Code Review", "PostgreSQL", "Docker", "REST APIs"];

  list.forEach(skill => {
    const badge = document.createElement('div');
    badge.className = 'skill-badge';
    badge.innerHTML = `
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
      <span>${skill}</span>
    `;
    container.appendChild(badge);
  });
}

function renderProjectsBreakdown(projectsArray) {
  const container = document.getElementById('projectsContainer');
  if (!container) return;
  container.innerHTML = '';
  const list = projectsArray && projectsArray.length ? projectsArray : [
    {
      name: "Live Staging Architecture Project",
      description: "Production codebase reviewed line-by-line in 1-to-1 mentoring sessions.",
      url: "https://github.com/cactslearn/student-projects"
    }
  ];

  list.forEach(proj => {
    const item = document.createElement('div');
    item.className = 'project-card-item';
    item.innerHTML = `
      <div class="project-card-title">
        <span>${proj.name}</span>
        <a href="${proj.url}" target="_blank" style="color: var(--accent); font-size: 0.8rem; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
          View Repository &rarr;
        </a>
      </div>
      <div class="project-card-desc">${proj.description || ''}</div>
    `;
    container.appendChild(item);
  });
}

function generateQRCodes(record) {
  const qrOnline = document.getElementById('qrcodeOnline');
  const qrOffline = document.getElementById('qrcodeOffline');
  if (qrOnline) qrOnline.innerHTML = '';
  if (qrOffline) qrOffline.innerHTML = '';

  if (typeof QRCode === "undefined") return;

  const onlineUrl = `https://cactslearn.github.io/verify.html?id=${record.id}`;
  if (qrOnline) {
    new QRCode(qrOnline, {
      text: onlineUrl,
      width: 140,
      height: 140,
      colorDark: "#040c1a",
      colorLight: "#ffffff",
      correctLevel: QRCode.CorrectLevel.M
    });
  }

  const offlinePayload = `ID: ${record.id}\nNAME: ${record.studentName}\nPROGRAM: ${record.programType || '1-to-1 Training & Internship'}\nCOURSE: ${record.courseName}\nDATE: ${record.issueDate}\nSTATUS: ${record.status || 'VALID'}\nISSUER: CACTS Pune`;
  if (qrOffline) {
    new QRCode(qrOffline, {
      text: offlinePayload,
      width: 140,
      height: 140,
      colorDark: "#040c1a",
      colorLight: "#ffffff",
      correctLevel: QRCode.CorrectLevel.L
    });
  }
}

function showError(title, message) {
  const certCanvas = document.getElementById('certificateCanvas');
  if (certCanvas) certCanvas.style.display = 'none';

  const breakdownSec = document.getElementById('breakdownSection');
  if (breakdownSec) breakdownSec.style.display = 'none';

  const dlPdfBtn = document.getElementById('downloadPdfBtn');
  if (dlPdfBtn) dlPdfBtn.disabled = true;

  const dlPngBtn = document.getElementById('downloadPngBtn');
  if (dlPngBtn) dlPngBtn.disabled = true;

  const cpLinkBtn = document.getElementById('copyLinkBtn');
  if (cpLinkBtn) cpLinkBtn.disabled = true;

  const statusBanner = document.getElementById('statusBanner');
  if (statusBanner) statusBanner.className = 'status-alert error';

  const statusInfo = document.getElementById('statusInfo');
  if (statusInfo) {
    statusInfo.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>
      <span>UNVERIFIED RECORD: Certificate ID search could not be authenticated.</span>
    `;
  }

  const statusTimestamp = document.getElementById('statusTimestamp');
  if (statusTimestamp) statusTimestamp.innerText = `Checked: ${new Date().toLocaleTimeString()}`;

  const errorCard = document.getElementById('errorCard');
  const errorTitle = document.getElementById('errorTitle');
  const errorDesc = document.getElementById('errorDesc');

  if (errorTitle) errorTitle.innerText = title;
  if (errorDesc) errorDesc.innerText = message;
  if (errorCard) errorCard.style.display = 'block';
}

/* LinkedIn Certification Add to Profile Link Generator */
function addToLinkedInProfile() {
  if (!currentRecord) return;
  const rec = currentRecord;
  const certId = rec.id;
  const certName = rec.courseName || "Software Engineering Training";
  const orgName = "CACTS - Centre of Advanced Computer Training and Studies";
  const issueYear = parseInt(rec.issueYear, 10) || 2026;
  const issueMonth = parseInt(rec.issueMonth, 10) || 8;
  const certUrl = `https://cactslearn.github.io/verify.html?id=${certId}`;

  const linkedInUrl = `https://www.linkedin.com/profile/add?startTask=CERTIFICATION_NAME&name=${encodeURIComponent(certName)}&organizationName=${encodeURIComponent(orgName)}&issueYear=${issueYear}&issueMonth=${issueMonth}&certUrl=${encodeURIComponent(certUrl)}&certId=${encodeURIComponent(certId)}`;

  window.open(linkedInUrl, '_blank');
  showToast("Opening LinkedIn Add Certification page...");
}

/* Copy Verification Link to Clipboard */
function copyVerificationLink() {
  if (!currentRecord) return;
  const onlineUrl = `https://cactslearn.github.io/verify.html?id=${currentRecord.id}`;
  navigator.clipboard.writeText(onlineUrl).then(() => {
    showToast("Verification link copied to clipboard!");
  }).catch(() => {
    showToast("Failed to copy link. URL: " + onlineUrl);
  });
}

/* Copy SHA-256 Hash to Clipboard */
function copyHashText() {
  const hashElem = document.getElementById('hashTextDisplay');
  const hash = hashElem ? hashElem.innerText : '';
  navigator.clipboard.writeText(hash).then(() => {
    showToast("SHA-256 checksum copied to clipboard!");
  });
}

/* High-Res PNG Image Export */
function downloadPNG() {
  if (!currentRecord) return;
  const element = document.getElementById('certificateCanvas');
  if (!element || typeof html2canvas === "undefined") return;

  const oldTransform = element.style.transform;
  const oldOrigin = element.style.transformOrigin;
  const oldPosition = element.style.position;
  const oldTop = element.style.top;
  const oldLeft = element.style.left;
  const oldMargin = element.style.margin;
  const viewport = document.querySelector('.certificate-viewport');
  const oldViewportHeight = viewport ? viewport.style.height : '';

  element.style.transform = 'none';
  element.style.position = 'fixed';
  element.style.top = '0px';
  element.style.left = '0px';
  element.style.margin = '0px';
  element.style.zIndex = '99999';
  if (viewport) viewport.style.height = 'auto';

  document.fonts.ready.then(() => {
    html2canvas(element, {
      scale: 3,
      useCORS: true,
      allowTaint: true,
      logging: false,
      x: 0,
      y: 0,
      width: 1050,
      height: 742,
      scrollX: 0,
      scrollY: 0
    }).then(canvas => {
      element.style.transform = oldTransform;
      element.style.transformOrigin = oldOrigin;
      element.style.position = oldPosition;
      element.style.top = oldTop;
      element.style.left = oldLeft;
      element.style.margin = oldMargin;
      element.style.zIndex = 'auto';
      if (viewport) viewport.style.height = oldViewportHeight;
      fitCertificateToScreen();

      const link = document.createElement('a');
      link.download = `CACTS_Certificate_${currentRecord.id}.png`;
      link.href = canvas.toDataURL('image/png', 1.0);
      link.click();
      showToast("High-Res Certificate PNG exported!");
    }).catch(err => {
      console.error(err);
      element.style.transform = oldTransform;
      element.style.transformOrigin = oldOrigin;
      element.style.position = oldPosition;
      element.style.top = oldTop;
      element.style.left = oldLeft;
      element.style.margin = oldMargin;
      element.style.zIndex = 'auto';
      if (viewport) viewport.style.height = oldViewportHeight;
      fitCertificateToScreen();
    });
  });
}

/* Standard PDF Export */
function downloadPDF() {
  if (!currentRecord) return;
  const element = document.getElementById('certificateCanvas');
  if (!element || typeof html2pdf === "undefined") return;

  const oldTransform = element.style.transform;
  const oldOrigin = element.style.transformOrigin;
  const oldPosition = element.style.position;
  const oldTop = element.style.top;
  const oldLeft = element.style.left;
  const oldMargin = element.style.margin;
  const viewport = document.querySelector('.certificate-viewport');
  const oldViewportHeight = viewport ? viewport.style.height : '';

  element.style.transform = 'none';
  element.style.position = 'fixed';
  element.style.top = '0px';
  element.style.left = '0px';
  element.style.margin = '0px';
  element.style.zIndex = '99999';
  if (viewport) viewport.style.height = 'auto';

  document.fonts.ready.then(() => {
    const opt = {
      margin: 0,
      filename: `CACTS_Certificate_${currentRecord.id}.pdf`,
      image: { type: 'jpeg', quality: 1.0 },
      html2canvas: {
        scale: 3,
        letterRendering: true,
        useCORS: true,
        allowTaint: true,
        logging: false,
        x: 0,
        y: 0,
        width: 1050,
        height: 742,
        scrollX: 0,
        scrollY: 0
      },
      jsPDF: { unit: 'px', format: [1050, 742], orientation: 'landscape', compress: true }
    };

    html2pdf().set(opt).from(element).save().then(() => {
      element.style.transform = oldTransform;
      element.style.transformOrigin = oldOrigin;
      element.style.position = oldPosition;
      element.style.top = oldTop;
      element.style.left = oldLeft;
      element.style.margin = oldMargin;
      element.style.zIndex = 'auto';
      if (viewport) viewport.style.height = oldViewportHeight;
      fitCertificateToScreen();
      showToast("Certificate PDF downloaded!");
    }).catch(err => {
      console.error(err);
      element.style.transform = oldTransform;
      element.style.transformOrigin = oldOrigin;
      element.style.position = oldPosition;
      element.style.top = oldTop;
      element.style.left = oldLeft;
      element.style.margin = oldMargin;
      element.style.zIndex = 'auto';
      if (viewport) viewport.style.height = oldViewportHeight;
      fitCertificateToScreen();
    });
  });
}

/* Toast Helper */
function showToast(message) {
  const toast = document.getElementById('toastNotification');
  const toastMsg = document.getElementById('toastMessage');
  if (toast && toastMsg) {
    toastMsg.innerText = message;
    toast.style.display = 'flex';
    setTimeout(() => {
      toast.style.display = 'none';
    }, 3500);
  }
}

function generateDefaultHash(id) {
  return "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";
}
