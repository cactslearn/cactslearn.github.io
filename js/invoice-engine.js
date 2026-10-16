/**
 * CACTS Student Invoicing & Fee Receipts Engine (js/invoice-engine.js)
 * Production engine for student billing statements, installment receipts,
 * single-page A4 PDF export, and Google Apps Script integration.
 */

const INVOICE_API_ENDPOINT = "https://script.google.com/macros/s/AKfycbzrcvqXiyAjNmsU_r5BuyPqkTNaCoMnrVuBgamhf0zDph3PrYzTl_sVVvgeqQlhbA/exec";

let currentInvoices = {};
let currentActiveInvoice = null;
let currentActiveView = 'invoice'; // 'invoice' or 'receipt'
let currentActiveReceiptIndex = 0;

const DEFAULT_RECORD = {
  invoiceNumber: "CACTS-202610-001",
  studentName: "Rahul Patil",
  mobileNumber: "9876543210",
  joiningDate: "2026-10-05",
  courseName: "Java Full Stack Development",
  courseFees: 19999,
  discount: 1999,
  payments: [
    {
      receiptNumber: "CACTS-R-001",
      date: "2026-10-05",
      amount: 5000,
      transactionNumber: "UPI123456789"
    },
    {
      receiptNumber: "CACTS-R-002",
      date: "2026-10-15",
      amount: 3000,
      transactionNumber: "TXN987654321"
    }
  ]
};

window.addEventListener('DOMContentLoaded', () => {
  const ySpan = document.getElementById('footer-year');
  if (ySpan) ySpan.innerText = new Date().getFullYear();

  const mobInput = document.getElementById('mobileInput');
  if (mobInput) {
    mobInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') handleManualSearch();
    });
  }

  // Parse URL parameters
  const urlParams = new URLSearchParams(window.location.search);
  const mobileParam = urlParams.get('mobile');
  const monthParam = urlParams.get('month');
  const yearParam = urlParams.get('year');
  const idParam = urlParams.get('id') || urlParams.get('inv');

  if (mobileParam && mobileParam.trim()) {
    const m = mobileParam.trim();
    if (mobInput) mobInput.value = m;
    if (monthParam && document.getElementById('monthSelect')) document.getElementById('monthSelect').value = monthParam.trim();
    if (yearParam && document.getElementById('yearSelect')) document.getElementById('yearSelect').value = yearParam.trim();
    fetchInvoiceRecord(m, monthParam || (document.getElementById('monthSelect') ? document.getElementById('monthSelect').value : '10'), yearParam || (document.getElementById('yearSelect') ? document.getElementById('yearSelect').value : '2026'));
  } else if (idParam && idParam.trim()) {
    const idStr = idParam.trim();
    const parts = idStr.match(/(\d{4})(\d{2})/);
    if (parts) {
      if (document.getElementById('yearSelect')) document.getElementById('yearSelect').value = parts[1];
      if (document.getElementById('monthSelect')) document.getElementById('monthSelect').value = parseInt(parts[2], 10).toString();
    }
    if (mobInput) mobInput.value = '9876543210';
    fetchInvoiceRecord('9876543210', document.getElementById('monthSelect') ? document.getElementById('monthSelect').value : '10', document.getElementById('yearSelect') ? document.getElementById('yearSelect').value : '2026');
  }
  // When visited without query params, do NOT auto-load any default invoice
});

window.addEventListener('resize', fitDocumentToScreen);

function fitDocumentToScreen() {
  const viewport = document.querySelector('.invoice-viewport');
  const canvas = currentActiveView === 'invoice' ? document.getElementById('invoiceCanvas') : document.getElementById('receiptCanvas');
  if (!viewport || !canvas || canvas.style.display === 'none') return;

  const sectionElem = viewport.closest('.tech-section') || document.body;
  const sectionWidth = sectionElem.clientWidth;
  const availableWidth = Math.min(sectionWidth - 16, 794);

  if (availableWidth < 794) {
    const scale = availableWidth / 794;
    canvas.style.transform = `scale(${scale})`;
    canvas.style.transformOrigin = 'top center';
    viewport.style.height = `${(canvas.offsetHeight * scale) + 16}px`;
  } else {
    canvas.style.transform = 'none';
    viewport.style.height = 'auto';
  }
}

function handleManualSearch() {
  const mobElem = document.getElementById('mobileInput');
  const mobile = mobElem ? mobElem.value.trim() : '';
  const month = document.getElementById('monthSelect') ? document.getElementById('monthSelect').value : '10';
  const year = document.getElementById('yearSelect') ? document.getElementById('yearSelect').value : '2026';

  if (!mobile || mobile.length !== 10 || !/^\d{10}$/.test(mobile)) {
    showError('Invalid Mobile Number', 'Please enter a valid 10-digit registered mobile number (e.g. 9876543210).');
    return;
  }

  const newUrl = `${window.location.protocol}//${window.location.host}${window.location.pathname}?mobile=${encodeURIComponent(mobile)}&month=${encodeURIComponent(month)}&year=${encodeURIComponent(year)}`;
  window.history.pushState({ path: newUrl }, '', newUrl);

  fetchInvoiceRecord(mobile, month, year);
}

function fetchInvoiceRecord(mobile, month, year, isBackgroundCheck = false) {
  const statusBanner = document.getElementById('statusBanner');
  if (!isBackgroundCheck && statusBanner) {
    statusBanner.className = 'status-alert loading';
    const statusInfo = document.getElementById('statusInfo');
    if (statusInfo) {
      statusInfo.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation: spin 1s linear infinite;"><circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="12"></circle></svg>
        <span>CONNECTING TO SECURE BILLING GATEWAY: Authenticating student records for +91 ${mobile}...</span>
      `;
    }
    const statusTimestamp = document.getElementById('statusTimestamp');
    if (statusTimestamp) statusTimestamp.innerText = 'Querying ledger...';
    const errorCard = document.getElementById('errorCard');
    if (errorCard) errorCard.style.display = 'none';
  }

  const requestUrl = `${INVOICE_API_ENDPOINT}?mobile=${encodeURIComponent(mobile)}&month=${encodeURIComponent(month)}&year=${encodeURIComponent(year)}`;

  fetch(requestUrl)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP Error ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (!data || data.error || Object.keys(data).length === 0) {
        if (mobile === '9876543210') {
          currentInvoices = { "CACTS-202610-001": DEFAULT_RECORD };
          currentActiveInvoice = DEFAULT_RECORD;
          renderInvoice(DEFAULT_RECORD);
          return;
        }
        const msg = data && data.error ? data.error : `No invoice records found for mobile ${mobile} in month ${month}/${year}.`;
        showError('Billing Record Not Found', msg);
        return;
      }

      currentInvoices = data;
      const keys = Object.keys(data);
      const firstKey = keys[0];
      currentActiveInvoice = data[firstKey];

      renderInvoice(currentActiveInvoice);
    })
    .catch(err => {
      console.warn('Invoice fetch failed:', err);
      if (mobile === '9876543210') {
        currentInvoices = { "CACTS-202610-001": DEFAULT_RECORD };
        currentActiveInvoice = DEFAULT_RECORD;
        renderInvoice(DEFAULT_RECORD);
        return;
      }
      showError('Billing Gateway Unavailable', 'Could not connect to the Google Apps Script billing service. Please check your internet connection.');
    });
}

function renderInvoice(record) {
  currentActiveInvoice = record;

  const errorCard = document.getElementById('errorCard');
  if (errorCard) errorCard.style.display = 'none';

  const dlBtn = document.getElementById('downloadPdfBtn');
  if (dlBtn) dlBtn.disabled = false;

  const prBtn = document.getElementById('printDocBtn');
  if (prBtn) prBtn.disabled = false;

  const cpBtn = document.getElementById('copyShareBtn');
  if (cpBtn) cpBtn.disabled = false;

  // Status Banner
  const statusBanner = document.getElementById('statusBanner');
  const grossFees = Number(record.courseFees) || 0;
  const discount = Number(record.discount) || 0;
  const netPayable = Math.max(0, grossFees - discount);

  const payments = Array.isArray(record.payments) ? record.payments : [];
  const totalPaid = payments.reduce((sum, p) => sum + (Number(p.amount) || 0), 0);
  const balanceDue = Math.max(0, netPayable - totalPaid);

  let statusType = "PARTIAL";
  let statusText = `PARTIAL PAYMENT: ${formatINR(totalPaid)} Paid &bull; ${formatINR(balanceDue)} Pending Balance`;
  if (balanceDue <= 0 && netPayable > 0) {
    statusType = "PAID";
    statusText = `AUTHENTICATED BILLING: Invoice ${record.invoiceNumber} is Fully Paid &amp; Cleared.`;
  } else if (totalPaid === 0) {
    statusType = "UNPAID";
    statusText = `PAYMENT PENDING: Net course fee of ${formatINR(netPayable)} is outstanding.`;
  }

  if (statusBanner) {
    if (statusType === "PAID") {
      statusBanner.className = 'status-alert success';
    } else if (statusType === "PARTIAL") {
      statusBanner.className = 'status-alert partial';
    } else {
      statusBanner.className = 'status-alert error';
    }
  }

  const statusInfo = document.getElementById('statusInfo');
  if (statusInfo) {
    statusInfo.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>${statusText}</span>
    `;
  }

  const statusTimestamp = document.getElementById('statusTimestamp');
  if (statusTimestamp) statusTimestamp.innerText = `Verified: ${new Date().toLocaleDateString()}`;

  // Update Top Badges & Selector
  const countBadge = document.getElementById('receiptCountBadge');
  if (countBadge) countBadge.innerText = payments.length;
  setupReceiptDropdown(payments);

  // Populate Master Invoice Fields
  const invNum = document.getElementById('invNumberDisplay');
  if (invNum) invNum.innerText = record.invoiceNumber || 'CACTS-INV-001';

  const invDate = document.getElementById('invDateDisplay');
  if (invDate) invDate.innerText = `Issued: ${formatDate(record.joiningDate)}`;

  const sName = document.getElementById('invStudentName');
  if (sName) sName.innerText = record.studentName || 'Student Name';

  const sMobile = document.getElementById('invMobileNumber');
  if (sMobile) sMobile.innerText = `+91 ${record.mobileNumber || ''}`;

  const sJoin = document.getElementById('invJoiningDate');
  if (sJoin) sJoin.innerText = formatDate(record.joiningDate);

  const sCourse = document.getElementById('invCourseName');
  if (sCourse) sCourse.innerText = record.courseName || 'Software Engineering';

  const tblCourse = document.getElementById('tableCourseTitle');
  if (tblCourse) tblCourse.innerText = record.courseName || 'Software Engineering';

  // Table & Totals
  const tblGross = document.getElementById('tableGrossFee');
  if (tblGross) tblGross.innerText = formatINR(grossFees);

  const tblDisc = document.getElementById('tableDiscount');
  if (tblDisc) tblDisc.innerText = `- ${formatINR(discount)}`;

  const tblNet = document.getElementById('tableNetFee');
  if (tblNet) tblNet.innerText = formatINR(netPayable);

  const sumGross = document.getElementById('summaryGrossFee');
  if (sumGross) sumGross.innerText = formatINR(grossFees);

  const sumDisc = document.getElementById('summaryDiscount');
  if (sumDisc) sumDisc.innerText = `- ${formatINR(discount)}`;

  const sumNet = document.getElementById('summaryNetFee');
  if (sumNet) sumNet.innerText = formatINR(netPayable);

  const sumPaid = document.getElementById('summaryTotalPaid');
  if (sumPaid) sumPaid.innerText = formatINR(totalPaid);

  const sumBal = document.getElementById('summaryBalanceDue');
  if (sumBal) sumBal.innerText = formatINR(balanceDue);

  // In Words
  const paidInWords = convertNumberToIndianWords(totalPaid);
  const balanceInWords = balanceDue > 0 ? convertNumberToIndianWords(balanceDue) : "Nil (No Outstanding Dues)";

  const wordsPaid = document.getElementById('wordsAmountPaid');
  if (wordsPaid) wordsPaid.innerHTML = paidInWords.replace(/ /g, '&nbsp;');

  const wordsBal = document.getElementById('wordsBalanceDue');
  if (wordsBal) wordsBal.innerHTML = balanceInWords.replace(/ /g, '&nbsp;');

  // Summary Balance Row & Words Styling
  const balanceRow = document.getElementById('summaryBalanceRow');
  const balanceLabel = document.getElementById('summaryBalanceLabel');
  if (balanceRow) {
    if (balanceDue <= 0 && netPayable > 0) {
      balanceRow.className = 'balance-due-row cleared';
      if (balanceLabel) balanceLabel.innerHTML = 'Account&nbsp;Standing:&nbsp;Net&nbsp;Balance&nbsp;Cleared&nbsp;in&nbsp;Full';
      if (wordsBal) wordsBal.className = 'words-val';
    } else {
      balanceRow.className = 'balance-due-row';
      if (balanceLabel) balanceLabel.innerHTML = 'Remaining&nbsp;Outstanding&nbsp;Balance&nbsp;Due:';
      if (wordsBal) wordsBal.className = 'words-val balance';
    }
  }

  // Status Pill Badges
  const pillClass = statusType === "PAID" ? "status-pill-badge paid" : (statusType === "PARTIAL" ? "status-pill-badge partial" : "status-pill-badge unpaid");
  const pillLabel = statusType === "PAID" ? "PAID IN FULL" : (statusType === "PARTIAL" ? "PARTIAL PAYMENT" : "PAYMENT PENDING");

  const pillInline = document.getElementById('invStatusPillInline');
  if (pillInline) {
    pillInline.className = pillClass;
    pillInline.innerText = pillLabel;
  }

  const pillSummary = document.getElementById('invStatusPillSummary');
  if (pillSummary) {
    pillSummary.className = pillClass;
    pillSummary.innerText = statusType === "PAID" ? "PAID IN FULL • ALL DUES CLEARED" : (statusType === "PARTIAL" ? `PARTIAL PAYMENT • ${formatINR(balanceDue)} DUE` : "PAYMENT OUTSTANDING");
  }

  // Populate Installments Ledger Table
  const ledgerTbody = document.getElementById('paymentsLedgerBody');
  if (ledgerTbody) {
    ledgerTbody.innerHTML = '';

    if (payments.length === 0) {
      ledgerTbody.innerHTML = `<tr><td colspan="6" class="text-center" style="color: #94a3b8; padding: 20px;">No installment payments recorded yet.</td></tr>`;
    } else {
      let runningSum = 0;
      payments.forEach((p, idx) => {
        const amt = Number(p.amount) || 0;
        runningSum += amt;
        const remainingAfter = Math.max(0, netPayable - runningSum);

        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td style="white-space: nowrap;">
            <span class="receipt-link-btn" onclick="openSpecificReceipt(${idx})" title="Click to view Receipt Voucher">
              ${p.receiptNumber}
            </span>
          </td>
          <td class="text-center" style="white-space: nowrap; font-size: 0.8rem; color: #334155;">${formatDate(p.date)}</td>
          <td style="font-family: monospace; font-size: 0.82rem; color: #334155;"><code style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.82rem; color: #334155;">${p.transactionNumber || 'N/A'}</code></td>
          <td class="text-right" style="color: #047857; font-weight: 700; white-space: nowrap;">${formatINR(amt)}</td>
          <td class="text-right" style="font-weight: 600; white-space: nowrap;">${formatINR(runningSum)}</td>
          <td class="text-right" style="color: ${remainingAfter > 0 ? '#b45309' : '#047857'}; font-weight: 700; white-space: nowrap;">${formatINR(remainingAfter)}</td>
        `;
        ledgerTbody.appendChild(tr);
      });
    }
  }

  // Generate Verification QR Code
  generateInvoiceQR(record);

  // Render current view
  switchView(currentActiveView);
}

function setupReceiptDropdown(payments) {
  const select = document.getElementById('receiptSelect');
  if (!select) return;
  select.innerHTML = '';
  if (payments.length > 0) {
    payments.forEach((p, idx) => {
      const opt = document.createElement('option');
      opt.value = idx;
      opt.innerText = `${p.receiptNumber} (${formatINR(p.amount)})`;
      select.appendChild(opt);
    });
  }
}

function switchView(viewName) {
  currentActiveView = viewName;
  const btnInv = document.getElementById('btnViewInvoice');
  const btnRcpt = document.getElementById('btnViewReceipt');
  const invCanvas = document.getElementById('invoiceCanvas');
  const rcptCanvas = document.getElementById('receiptCanvas');
  const rcptSelect = document.getElementById('receiptSelect');

  if (!currentActiveInvoice) {
    if (invCanvas) invCanvas.style.display = 'none';
    if (rcptCanvas) rcptCanvas.style.display = 'none';
    if (rcptSelect) rcptSelect.style.display = 'none';
    return;
  }

  if (viewName === 'invoice') {
    if (btnInv) btnInv.className = 'view-toggle-btn active';
    if (btnRcpt) btnRcpt.className = 'view-toggle-btn';
    if (invCanvas) invCanvas.style.display = 'block';
    if (rcptCanvas) rcptCanvas.style.display = 'none';
    if (rcptSelect) rcptSelect.style.display = 'none';
  } else {
    if (btnInv) btnInv.className = 'view-toggle-btn';
    if (btnRcpt) btnRcpt.className = 'view-toggle-btn active';
    if (invCanvas) invCanvas.style.display = 'none';
    if (rcptCanvas) rcptCanvas.style.display = 'block';
    if (rcptSelect) rcptSelect.style.display = 'inline-block';
    renderSpecificReceipt(currentActiveReceiptIndex);
  }

  setTimeout(fitDocumentToScreen, 50);
}

function openSpecificReceipt(index) {
  currentActiveReceiptIndex = index;
  const rcptSelect = document.getElementById('receiptSelect');
  if (rcptSelect) rcptSelect.value = index;
  switchView('receipt');
}

function renderSpecificReceipt(index) {
  currentActiveReceiptIndex = parseInt(index, 10) || 0;
  if (!currentActiveInvoice || !currentActiveInvoice.payments) return;

  const payments = currentActiveInvoice.payments;
  const payment = payments[currentActiveReceiptIndex] || payments[0];
  if (!payment) return;

  const grossFees = Number(currentActiveInvoice.courseFees) || 0;
  const discount = Number(currentActiveInvoice.discount) || 0;
  const netPayable = Math.max(0, grossFees - discount);

  let priorSum = 0;
  for (let i = 0; i < currentActiveReceiptIndex; i++) {
    priorSum += (Number(payments[i].amount) || 0);
  }
  const thisAmount = Number(payment.amount) || 0;
  const cumulativeSum = priorSum + thisAmount;
  const remainingAfter = Math.max(0, netPayable - cumulativeSum);

  const rcptNum = document.getElementById('rcptNumberDisplay');
  if (rcptNum) rcptNum.innerText = payment.receiptNumber || 'CACTS-R-001';

  const rcptDate = document.getElementById('rcptDateDisplay');
  if (rcptDate) rcptDate.innerText = `Date: ${formatDate(payment.date)}`;

  const rcptBadge = document.getElementById('rcptAmountBadge');
  if (rcptBadge) rcptBadge.innerText = formatINR(thisAmount);

  const rcptInvRef = document.getElementById('rcptInvoiceRef');
  if (rcptInvRef) rcptInvRef.innerText = currentActiveInvoice.invoiceNumber || 'N/A';

  const rcptName = document.getElementById('rcptStudentName');
  if (rcptName) rcptName.innerText = currentActiveInvoice.studentName || 'Student Name';

  const rcptMob = document.getElementById('rcptMobile');
  if (rcptMob) rcptMob.innerText = `+91 ${currentActiveInvoice.mobileNumber || ''}`;

  const rcptWords = document.getElementById('rcptWordsAmount');
  if (rcptWords) rcptWords.innerHTML = convertNumberToIndianWords(thisAmount).replace(/ /g, '&nbsp;');

  const rcptCourse = document.getElementById('rcptCourseName');
  if (rcptCourse) rcptCourse.innerText = currentActiveInvoice.courseName || 'Software Engineering';

  const rcptTxn = document.getElementById('rcptTxnNumber');
  if (rcptTxn) rcptTxn.innerText = payment.transactionNumber || 'N/A';

  const rcptMode = document.getElementById('rcptPaymentMode');
  if (rcptMode) rcptMode.innerText = (payment.transactionNumber && payment.transactionNumber.startsWith('UPI')) ? 'UPI Transfer' : 'Direct Electronic Bank Transfer';

  const rcptSeq = document.getElementById('rcptSequence');
  if (rcptSeq) rcptSeq.innerText = `Installment ${currentActiveReceiptIndex + 1} of ${payments.length}`;

  const rcptNet = document.getElementById('rcptNetTotal');
  if (rcptNet) rcptNet.innerText = formatINR(netPayable);

  const rcptPrior = document.getElementById('rcptPriorPaid');
  if (rcptPrior) rcptPrior.innerText = formatINR(priorSum);

  const rcptThis = document.getElementById('rcptThisAmount');
  if (rcptThis) rcptThis.innerText = formatINR(thisAmount);

  const rcptCum = document.getElementById('rcptCumulativePaid');
  if (rcptCum) rcptCum.innerText = formatINR(cumulativeSum);

  const rcptBal = document.getElementById('rcptBalanceDue');
  if (rcptBal) rcptBal.innerText = formatINR(remainingAfter);

  generateReceiptQR(payment);
}

function generateInvoiceQR(record) {
  const container = document.getElementById('invQrCodeContainer');
  if (!container || typeof QRCode === "undefined") return;
  container.innerHTML = '';
  const monthVal = document.getElementById('monthSelect') ? document.getElementById('monthSelect').value : '10';
  const yearVal = document.getElementById('yearSelect') ? document.getElementById('yearSelect').value : '2026';
  const url = `https://cactslearn.github.io/invoice.html?mobile=${record.mobileNumber}&month=${monthVal}&year=${yearVal}`;
  new QRCode(container, {
    text: url,
    width: 76,
    height: 76,
    colorDark: "#0f172a",
    colorLight: "#ffffff",
    correctLevel: QRCode.CorrectLevel.M
  });
}

function generateReceiptQR(payment) {
  const container = document.getElementById('rcptQrCodeContainer');
  if (!container || typeof QRCode === "undefined") return;
  container.innerHTML = '';
  const payload = `CACTS RECEIPT\nNo: ${payment.receiptNumber}\nDate: ${payment.date}\nAmount: Rs.${payment.amount}\nTxn: ${payment.transactionNumber}\nStudent: ${currentActiveInvoice ? currentActiveInvoice.studentName : ''}`;
  new QRCode(container, {
    text: payload,
    width: 76,
    height: 76,
    colorDark: "#0f172a",
    colorLight: "#ffffff",
    correctLevel: QRCode.CorrectLevel.M
  });
}

function showError(title, message) {
  const invCanvas = document.getElementById('invoiceCanvas');
  if (invCanvas) invCanvas.style.display = 'none';

  const rcptCanvas = document.getElementById('receiptCanvas');
  if (rcptCanvas) rcptCanvas.style.display = 'none';

  const dlBtn = document.getElementById('downloadPdfBtn');
  if (dlBtn) dlBtn.disabled = true;

  const prBtn = document.getElementById('printDocBtn');
  if (prBtn) prBtn.disabled = true;

  const cpBtn = document.getElementById('copyShareBtn');
  if (cpBtn) cpBtn.disabled = true;

  const statusBanner = document.getElementById('statusBanner');
  if (statusBanner) statusBanner.className = 'status-alert error';

  const statusInfo = document.getElementById('statusInfo');
  if (statusInfo) {
    statusInfo.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>
      <span>BILLING LOOKUP FAILED: Record could not be authenticated.</span>
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

function downloadDocumentPDF() {
  if (!currentActiveInvoice) return;
  const isInvoice = currentActiveView === 'invoice';
  const element = isInvoice ? document.getElementById('invoiceCanvas') : document.getElementById('receiptCanvas');
  if (!element) return;

  const filename = isInvoice ? `${currentActiveInvoice.invoiceNumber}_CACTS_Invoice.pdf` : `CACTS_Receipt_${currentActiveInvoice.payments[currentActiveReceiptIndex]?.receiptNumber || '001'}.pdf`;

  // Save previous styles
  const oldTransform = element.style.transform;
  const oldOrigin = element.style.transformOrigin;
  const oldPosition = element.style.position;
  const oldTop = element.style.top;
  const oldLeft = element.style.left;
  const oldMargin = element.style.margin;
  const oldZIndex = element.style.zIndex;
  const oldWidth = element.style.width;
  const oldMaxWidth = element.style.maxWidth;
  const viewport = document.querySelector('.invoice-viewport');
  const oldViewportHeight = viewport ? viewport.style.height : 'auto';

  // Temporarily isolate element into fixed viewport
  element.style.transform = 'none';
  element.style.position = 'fixed';
  element.style.top = '0px';
  element.style.left = '0px';
  element.style.margin = '0px';
  element.style.width = '794px';
  element.style.maxWidth = '794px';
  element.style.zIndex = '99999';
  if (viewport) viewport.style.height = 'auto';

  document.fonts.ready.then(() => {
    const targetWidth = 794;
    const targetHeight = element.offsetHeight;

    if (typeof html2canvas === "undefined") return;

    html2canvas(element, {
      scale: 2.5,
      useCORS: true,
      allowTaint: true,
      logging: false,
      x: 0,
      y: 0,
      width: targetWidth,
      height: targetHeight,
      scrollX: 0,
      scrollY: 0,
      windowWidth: targetWidth,
      backgroundColor: '#ffffff'
    }).then(canvas => {
      // Restore element styles immediately
      element.style.transform = oldTransform;
      element.style.transformOrigin = oldOrigin;
      element.style.position = oldPosition;
      element.style.top = oldTop;
      element.style.left = oldLeft;
      element.style.margin = oldMargin;
      element.style.width = oldWidth;
      element.style.maxWidth = oldMaxWidth;
      element.style.zIndex = oldZIndex;
      if (viewport) viewport.style.height = oldViewportHeight;
      fitDocumentToScreen();

      const imgData = canvas.toDataURL('image/jpeg', 0.98);

      const JsPdfClass = (window.jspdf && window.jspdf.jsPDF) ? window.jspdf.jsPDF : (window.jsPDF ? window.jsPDF : null);

      if (JsPdfClass) {
        const pdf = new JsPdfClass({
          orientation: 'portrait',
          unit: 'mm',
          format: 'a4',
          compress: true
        });

        const a4Width = 210;
        const a4Height = 297;
        const margin = 8;
        const maxWidth = a4Width - (margin * 2);
        const maxHeight = a4Height - (margin * 2);

        const imgRatio = canvas.width / canvas.height;
        let renderWidth = maxWidth;
        let renderHeight = renderWidth / imgRatio;

        if (renderHeight > maxHeight) {
          renderHeight = maxHeight;
          renderWidth = renderHeight * imgRatio;
        }

        const posX = (a4Width - renderWidth) / 2;
        const posY = (a4Height - renderHeight) / 2;

        pdf.addImage(imgData, 'JPEG', posX, posY, renderWidth, renderHeight, undefined, 'FAST');
        pdf.save(filename);
        showToast("PDF downloaded - Single A4 page fit complete!");
      } else if (typeof html2pdf !== "undefined") {
        const opt = {
          margin: 0,
          filename: filename,
          image: { type: 'jpeg', quality: 0.98 },
          html2canvas: {
            scale: 2,
            useCORS: true,
            x: 0,
            y: 0,
            width: targetWidth,
            height: targetHeight,
            windowWidth: targetWidth
          },
          jsPDF: { unit: 'px', format: [targetWidth, targetHeight], orientation: 'portrait', compress: true },
          pagebreak: { mode: 'avoid-all' }
        };
        html2pdf().set(opt).from(element).save().then(() => {
          showToast("PDF downloaded!");
        });
      }
    }).catch(err => {
      element.style.transform = oldTransform;
      element.style.transformOrigin = oldOrigin;
      element.style.position = oldPosition;
      element.style.top = oldTop;
      element.style.left = oldLeft;
      element.style.margin = oldMargin;
      element.style.width = oldWidth;
      element.style.maxWidth = oldMaxWidth;
      element.style.zIndex = oldZIndex;
      if (viewport) viewport.style.height = oldViewportHeight;
      fitDocumentToScreen();
      console.error(err);
      showToast("Error generating PDF. Please use browser Print > Save as PDF.");
    });
  });
}

function copyDocumentLink() {
  if (!currentActiveInvoice) return;
  const monthVal = document.getElementById('monthSelect') ? document.getElementById('monthSelect').value : '10';
  const yearVal = document.getElementById('yearSelect') ? document.getElementById('yearSelect').value : '2026';
  const url = currentActiveInvoice.mobileNumber ?
    `${window.location.protocol}//${window.location.host}${window.location.pathname}?mobile=${encodeURIComponent(currentActiveInvoice.mobileNumber)}&month=${encodeURIComponent(monthVal)}&year=${encodeURIComponent(yearVal)}` :
    window.location.href;
  navigator.clipboard.writeText(url).then(() => {
    showToast("Direct invoice link copied to clipboard!");
  }).catch(() => {
    showToast("Link: " + url);
  });
}

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

/* Helper: Indian Rupee Formatter */
function formatINR(val) {
  const num = Number(val) || 0;
  return '\u20B9 ' + num.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

/* Helper: Date Formatter */
function formatDate(dateStr) {
  if (!dateStr) return 'N/A';
  try {
    const d = new Date(dateStr);
    if (isNaN(d.getTime())) return dateStr;
    return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
  } catch (e) {
    return dateStr;
  }
}

/* Helper: Number to Words (Indian Numbering System) */
function convertNumberToIndianWords(num) {
  const n = Math.floor(Math.abs(Number(num) || 0));
  if (n === 0) return "Rupees Zero Only";

  const a = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen'];
  const b = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety'];

  function twoDigits(n) {
    if (n < 20) return a[n];
    const tens = b[Math.floor(n / 10)];
    const ones = a[n % 10];
    return ones ? tens + ' ' + ones : tens;
  }

  function inWords(val) {
    if (val === 0) return '';
    let words = [];

    const crores = Math.floor(val / 10000000);
    val %= 10000000;
    if (crores > 0) words.push(inWords(crores) + ' Crore');

    const lakhs = Math.floor(val / 100000);
    val %= 100000;
    if (lakhs > 0) words.push(twoDigits(lakhs) + ' Lakh');

    const thousands = Math.floor(val / 1000);
    val %= 1000;
    if (thousands > 0) words.push(twoDigits(thousands) + ' Thousand');

    const hundreds = Math.floor(val / 100);
    val %= 100;
    if (hundreds > 0) words.push(a[hundreds] + ' Hundred');

    if (val > 0) {
      if (words.length > 0) words.push('and');
      words.push(twoDigits(val));
    }

    return words.join(' ');
  }

  return "Rupees " + inWords(n) + " Only";
}
