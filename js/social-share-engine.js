/**
 * CACTS Pune - 10-Platform Dynamic Client-Side Social Syndication Engine
 * Filename: js/social-share-engine.js
 * Description: Zero-dependency client-side social sharing engine featuring dynamic JSON-LD/OG content
 *              recognition, human-centric non-robotic social captions, audience-tailored problem statements,
 *              perfectly matched expanded schema badges & explicit "SCAN QR CODE TO..." CTA buttons for all page categories & course bifurcations (Fees, Syllabus, Beginner, Roadmap, Comparison, Main Course),
 *              removal of sub-QR label for clean uncluttered QR code display,
 *              audience-specific targeted topic hashtags (Recruiters, HRs, CS Graduates, Freshers, Local Residents),
 *              platform-specific hashtag suppression (WhatsApp, Google Business Profile, and Reddit explicitly avoid hashtags to prevent spammy/unsupported clutter),
 *              strict schema-type-to-platform suitability filtering (only relevant platforms shown),
 *              clean hashtag-free socialCaptionText textarea (hashtags displayed in interactive pills for supported platforms only),
 *              automatic 100% full canonical text share URLs, pre-filled intent composers,
 *              dedicated Copy Text Only, Copy Full Caption (Text + Hashtags), & Copy Hashtags Only controls,
 *              clipboard image binary copy, mobile share sheet clipboard preservation,
 *              live graphic preview re-rendering, format-proportional font sizing, radial background lighting,
 *              16-theme rich dark gradient palettes with index-dispersed background variation,
 *              multi-paragraph line wrapping with strict left alignment, clean content-only canvas layout,
 *              real QR code generation via qrcode.js CDN & ISO/IEC 18004 Reed-Solomon GF(256) encoder,
 *              *T&C Apply disclaimer footer protection for price/offer updates, & Web Share API execution.
 */

window.CactsSocialShareEngine = (function() {
  'use strict';

  // Base Production Canonical Domain
  const BASE_CANONICAL_DOMAIN = 'https://cactslearn.github.io';

  // State Management
  let currentMetadata = null;
  let activePlatformId = 'linkedin-feed';
  let activeFormat = '1200x630';
  let currentBlob = null;
  let currentObjectUrl = null;
  let isLightFeed = false;
  let captionDebounceTimer = null;
  let qrLibPromise = null;

  // Platforms where Hashtags are explicitly unsupported or counter-productive (spams chats or breaks formatting)
  const NO_HASHTAG_PLATFORMS = ['whatsapp-chat', 'whatsapp-enroll', 'gbp-post', 'reddit-post'];

  // Platform Formats Mapping
  const PLATFORM_FORMATS = {
    'linkedin-feed': '1200x630',
    'instagram-story': '1080x1920',
    'whatsapp-chat': '1080x1920',
    'whatsapp-enroll': '1200x630',
    'twitter-tweet': '1200x630',
    'facebook-feed': '1200x630',
    'gbp-post': '1200x900',
    'reddit-post': '1200x630',
    'bluesky-post': '1200x630',
    'native-os-share': '1200x630'
  };

  // 16-Theme Rich Dark Gradient Palettes Collection for Maximum Grid Color Variation
  const RICH_PALETTES_16 = [
    { bgGradStart: '#78350f', bgGradEnd: '#1c1917', accentTabBg: '#f59e0b', accentTabTextColor: '#1c1917', subheadColor: '#fbbf24' },
    { bgGradStart: '#4c1d95', bgGradEnd: '#1e1b4b', accentTabBg: '#c084fc', accentTabTextColor: '#1e1b4b', subheadColor: '#e879f9' },
    { bgGradStart: '#064e3b', bgGradEnd: '#022c22', accentTabBg: '#10b981', accentTabTextColor: '#022c22', subheadColor: '#34d399' },
    { bgGradStart: '#1e3a8a', bgGradEnd: '#0f172a', accentTabBg: '#06b6d4', accentTabTextColor: '#0f172a', subheadColor: '#38bdf8' },
    { bgGradStart: '#881337', bgGradEnd: '#1c1917', accentTabBg: '#f43f5e', accentTabTextColor: '#1c1917', subheadColor: '#fb7185' },
    { bgGradStart: '#312e81', bgGradEnd: '#09090b', accentTabBg: '#84cc16', accentTabTextColor: '#09090b', subheadColor: '#a3e635' },
    { bgGradStart: '#451a03', bgGradEnd: '#0f172a', accentTabBg: '#f97316', accentTabTextColor: '#0f172a', subheadColor: '#fb923c' },
    { bgGradStart: '#701a75', bgGradEnd: '#0f172a', accentTabBg: '#f472b6', accentTabTextColor: '#0f172a', subheadColor: '#f472b6' },
    { bgGradStart: '#1e40af', bgGradEnd: '#030712', accentTabBg: '#38bdf8', accentTabTextColor: '#030712', subheadColor: '#60a5fa' },
    { bgGradStart: '#14532d', bgGradEnd: '#052e16', accentTabBg: '#4ade80', accentTabTextColor: '#052e16', subheadColor: '#86efac' },
    { bgGradStart: '#713f12', bgGradEnd: '#0f172a', accentTabBg: '#facc15', accentTabTextColor: '#0f172a', subheadColor: '#fde047' },
    { bgGradStart: '#164e63', bgGradEnd: '#083344', accentTabBg: '#22d3ee', accentTabTextColor: '#083344', subheadColor: '#67e8f9' },
    { bgGradStart: '#7f1d1d', bgGradEnd: '#450a0a', accentTabBg: '#ef4444', accentTabTextColor: '#450a0a', subheadColor: '#f87171' },
    { bgGradStart: '#581c87', bgGradEnd: '#2e1065', accentTabBg: '#a855f7', accentTabTextColor: '#2e1065', subheadColor: '#c084fc' },
    { bgGradStart: '#27272a', bgGradEnd: '#09090b', accentTabBg: '#e4e4e7', accentTabTextColor: '#09090b', subheadColor: '#fafafa' },
    { bgGradStart: '#0c4a6e', bgGradEnd: '#032830', accentTabBg: '#38bdf8', accentTabTextColor: '#032830', subheadColor: '#7dd3fc' }
  ];

  // Platform Hashtags Base Matrix (For Platforms that Support Hashtags)
  const PLATFORM_HASHTAGS = {
    'linkedin-feed': ['#CACTSPune', '#SoftwareEngineering', '#PuneITJobs'],
    'instagram-story': ['#cactspune', '#fullstackdeveloper', '#punestudents', '#learncoding'],
    'twitter-tweet': ['#CACTSPune', '#DevCommunity', '#TechJobs'],
    'facebook-feed': ['#CACTSPune', '#PuneITJobs', '#SoftwareTraining'],
    'bluesky-post': ['#CACTSPune', '#TechUpdate', '#WebDev'],
    'native-os-share': ['#CACTSPune', '#FullStackDeveloper', '#PuneITJobs']
  };

  // Audience & Content-Specific Hashtags Matrix
  const TOPIC_HASHTAGS = {
    'cert': ['#TechHiring', '#Recruitment', '#VerifiedDeveloper', '#HRTech', '#CACTSPune'],
    'job': ['#PuneITJobs', '#TechHiring', '#DeveloperJobs', '#PuneJobs', '#SoftwareEngineer'],
    'fees': ['#ITTrainingPune', '#SoftwareCourseFees', '#EMIOption', '#CareerGuidance', '#CACTSPune'],
    'syllabus': ['#SoftwareSyllabus', '#PracticalCoding', '#FullStackCourse', '#1to1Mentorship'],
    'beginner': ['#CodingForBeginners', '#LearnToCode', '#ZeroExperience', '#TechCareer'],
    'roadmap': ['#DeveloperRoadmap', '#CareerPath', '#TechSkills2026', '#SoftwareEngineering'],
    'comparison': ['#TechComparison', '#SoftwareArchitecture', '#WebDevelopment', '#Frameworks'],
    'course': ['#PuneITInstitute', '#SoftwareTraining', '#1to1Mentorship', '#FullStackDeveloper'],
    'tool': ['#DevTools', '#WebDevelopment', '#DeveloperProductivity', '#CodingTools'],
    'review': ['#StudentSuccess', '#AlumniReviews', '#PuneInstitute', '#CACTSPune'],
    'location': ['#PuneITInstitute', '#SoftwareTrainingPune', '#DhankawadiPune', '#KatrajPune'],
    'policy': ['#CACTSPune', '#DataProtection', '#PrivacyPolicy'],
    'guide': ['#DevCommunity', '#TechGuide', '#CareerRoadmap', '#WebDev']
  };

  // Format Dimensions Matrix
  const FORMAT_SPECS = {
    '1200x630': { width: 1200, height: 630, label: '1200x630 Banner' },
    '1080x1080': { width: 1080, height: 1080, label: '1080x1080 Feed' },
    '1080x1920': { width: 1080, height: 1920, label: '1080x1920 Story' },
    '1920x1080': { width: 1920, height: 1080, label: '1920x1080 HD' },
    '1200x900': { width: 1200, height: 900, label: '1200x900 GBP' }
  };

  // Helper: Dynamically Load QRCode JS Library from CDN
  function loadQRCodeLibrary() {
    if (window.QRCode) return Promise.resolve(true);
    if (qrLibPromise) return qrLibPromise;

    qrLibPromise = new Promise((resolve) => {
      const script = document.createElement('script');
      script.src = 'https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js';
      script.onload = () => resolve(true);
      script.onerror = () => resolve(false);
      document.head.appendChild(script);
    });

    return qrLibPromise;
  }

  /* ==========================================================================
     ISO/IEC 18004 Standards-Compliant Reed-Solomon GF(256) QR Code Encoder
     ========================================================================== */
  const QRCodeGen = (function() {
    const EXP_TABLE = new Array(256);
    const LOG_TABLE = new Array(256);
    for (let i = 0; i < 8; i++) EXP_TABLE[i] = 1 << i;
    for (let i = 8; i < 256; i++) {
      EXP_TABLE[i] = EXP_TABLE[i - 1] ^ (EXP_TABLE[i - 1] << 1) ^ ((EXP_TABLE[i - 1] & 0x80) ? 0x11d : 0);
    }
    for (let i = 0; i < 255; i++) LOG_TABLE[EXP_TABLE[i]] = i;

    function glog(n) {
      if (n < 1) throw new Error("glog(" + n + ")");
      return LOG_TABLE[n];
    }
    function gexp(n) {
      while (n < 0) n += 255;
      while (n >= 255) n -= 255;
      return EXP_TABLE[n];
    }

    function Polynomial(num, shift) {
      if (num.length == undefined) throw new Error(num.length + "/" + shift);
      let offset = 0;
      while (offset < num.length && num[offset] == 0) offset++;
      this.num = new Array(num.length - offset + shift);
      for (let i = 0; i < num.length - offset; i++) this.num[i] = num[offset + i];
    }
    Polynomial.prototype = {
      get: function(index) { return this.num[index]; },
      getLength: function() { return this.num.length; },
      multiply: function(e) {
        const num = new Array(this.getLength() + e.getLength() - 1).fill(0);
        for (let i = 0; i < this.getLength(); i++) {
          for (let j = 0; j < e.getLength(); j++) {
            num[i + j] ^= gexp(glog(this.get(i)) + glog(e.get(j)));
          }
        }
        return new Polynomial(num, 0);
      },
      mod: function(e) {
        if (this.getLength() - e.getLength() < 0) return this;
        const ratio = glog(this.get(0)) - glog(e.get(0));
        const num = new Array(this.getLength());
        for (let i = 0; i < this.getLength(); i++) num[i] = this.get(i);
        for (let i = 0; i < e.getLength(); i++) {
          num[i] ^= gexp(glog(e.get(i)) + ratio);
        }
        return new Polynomial(num, 0).mod(e);
      }
    };

    function BitBuffer() {
      this.buffer = [];
      this.length = 0;
    }
    BitBuffer.prototype = {
      put: function(num, length) {
        for (let i = 0; i < length; i++) {
          this.putBit(((num >>> (length - i - 1)) & 1) == 1);
        }
      },
      putBit: function(bit) {
        const bufIndex = Math.floor(this.length / 8);
        if (this.buffer.length <= bufIndex) this.buffer.push(0);
        if (bit) this.buffer[bufIndex] |= (0x80 >>> (this.length % 8));
        this.length++;
      }
    };

    const RS_BLOCKS = {
      1: { totalData: 19, ecBytes: 7, maxCap: 17 },
      2: { totalData: 34, ecBytes: 10, maxCap: 32 },
      3: { totalData: 55, ecBytes: 15, maxCap: 53 },
      4: { totalData: 80, ecBytes: 20, maxCap: 78 },
      5: { totalData: 108, ecBytes: 26, maxCap: 106 },
      6: { totalData: 136, ecBytes: 18, maxCap: 134 },
      7: { totalData: 156, ecBytes: 20, maxCap: 154 },
      8: { totalData: 194, ecBytes: 24, maxCap: 192 },
      9: { totalData: 232, ecBytes: 30, maxCap: 230 },
      10: { totalData: 274, ecBytes: 18, maxCap: 271 }
    };

    function getErrorCorrectionPolynomial(errorCorrectionLength) {
      let a = new Polynomial([1], 0);
      for (let i = 0; i < errorCorrectionLength; i++) {
        a = a.multiply(new Polynomial([1, gexp(i)], 0));
      }
      return a;
    }

    function generateMatrix(textData) {
      const utf8Bytes = [];
      for (let i = 0; i < textData.length; i++) {
        let code = textData.charCodeAt(i);
        if (code < 0x80) utf8Bytes.push(code);
        else if (code < 0x800) {
          utf8Bytes.push(0xc0 | (code >> 6), 0x80 | (code & 0x3f));
        } else {
          utf8Bytes.push(0xe0 | (code >> 12), 0x80 | ((code >> 6) & 0x3f), 0x80 | (code & 0x3f));
        }
      }

      let version = 1;
      while (version <= 10 && RS_BLOCKS[version].maxCap < utf8Bytes.length + 3) {
        version++;
      }
      if (version > 10) version = 10;

      const spec = RS_BLOCKS[version];
      const buffer = new BitBuffer();
      buffer.put(4, 4); // Mode byte: 0100
      buffer.put(utf8Bytes.length, 8);
      for (let i = 0; i < utf8Bytes.length; i++) {
        buffer.put(utf8Bytes[i], 8);
      }

      const totalDataBits = spec.totalData * 8;
      if (buffer.length + 4 <= totalDataBits) buffer.put(0, 4);
      while (buffer.length % 8 != 0) buffer.putBit(false);
      const padBytes = [0xec, 0x11];
      let padIdx = 0;
      while (buffer.length < totalDataBits) {
        buffer.put(padBytes[padIdx % 2], 8);
        padIdx++;
      }

      const dataBytes = buffer.buffer;
      const rsPoly = getErrorCorrectionPolynomial(spec.ecBytes);
      const rawPoly = new Polynomial(dataBytes, spec.ecBytes);
      const modPoly = rawPoly.mod(rsPoly);

      const ecBytes = new Array(spec.ecBytes).fill(0);
      for (let i = 0; i < ecBytes.length; i++) {
        const idx = i + modPoly.getLength() - spec.ecBytes;
        ecBytes[i] = (idx >= 0) ? modPoly.get(idx) : 0;
      }

      const finalCodewords = dataBytes.concat(ecBytes);
      const moduleCount = version * 4 + 17;
      const matrix = new Array(moduleCount);
      const isReserved = new Array(moduleCount);
      for (let i = 0; i < moduleCount; i++) {
        matrix[i] = new Array(moduleCount).fill(false);
        isReserved[i] = new Array(moduleCount).fill(false);
      }

      function setupFinder(r, c) {
        for (let y = -1; y <= 7; y++) {
          if (r + y < -1 || moduleCount <= r + y) continue;
          for (let x = -1; x <= 7; x++) {
            if (c + x < -1 || moduleCount <= c + x) continue;
            if (0 <= y && y <= 6 && 0 <= x && x <= 6) {
              const isDark = (y == 0 || y == 6 || x == 0 || x == 6 || (2 <= y && y <= 4 && 2 <= x && x <= 4));
              matrix[r + y][c + x] = isDark;
            }
            if (0 <= r + y && r + y < moduleCount && 0 <= c + x && c + x < moduleCount) {
              isReserved[r + y][c + x] = true;
            }
          }
        }
      }
      setupFinder(0, 0);
      setupFinder(moduleCount - 7, 0);
      setupFinder(0, moduleCount - 7);

      if (version >= 2) {
        const alignPos = moduleCount - 7;
        for (let y = -2; y <= 2; y++) {
          for (let x = -2; x <= 2; x++) {
            const isDark = (Math.abs(y) == 2 || Math.abs(x) == 2 || (y == 0 && x == 0));
            matrix[alignPos + y][alignPos + x] = isDark;
            isReserved[alignPos + y][alignPos + x] = true;
          }
        }
      }

      for (let i = 8; i < moduleCount - 8; i++) {
        if (!isReserved[i][6]) {
          matrix[i][6] = (i % 2 == 0);
          isReserved[i][6] = true;
        }
        if (!isReserved[6][i]) {
          matrix[6][i] = (i % 2 == 0);
          isReserved[6][i] = true;
        }
      }

      for (let i = 8; i < 9; i++) {
        if (!isReserved[i][8]) isReserved[i][8] = true;
        if (!isReserved[8][i]) isReserved[8][i] = true;
        if (!isReserved[moduleCount - 1 - i][8]) isReserved[moduleCount - 1 - i][8] = true;
        if (!isReserved[8][moduleCount - 1 - i]) isReserved[8][moduleCount - 1 - i] = true;
      }

      let bitIdx = 0;
      const totalBits = finalCodewords.length * 8;
      let dir = -1;
      let col = moduleCount - 1;
      let row = moduleCount - 1;

      while (col > 0) {
        if (col == 6) col--;
        while (true) {
          for (let c = 0; c < 2; c++) {
            const currentCol = col - c;
            if (!isReserved[row][currentCol]) {
              let dark = false;
              if (bitIdx < totalBits) {
                const bytePos = Math.floor(bitIdx / 8);
                const bitPos = 7 - (bitIdx % 8);
                dark = ((finalCodewords[bytePos] >>> bitPos) & 1) == 1;
              }
              if ((row + currentCol) % 2 == 0) dark = !dark;
              matrix[row][currentCol] = dark;
              isReserved[row][currentCol] = true;
              bitIdx++;
            }
          }
          row += dir;
          if (row < 0 || moduleCount <= row) {
            row -= dir;
            dir = -dir;
            break;
          }
        }
        col -= 2;
      }

      const formatBits = [true, true, true, false, true, true, true, true, true, false, false, false, true, false, false];
      for (let i = 0; i < 15; i++) {
        const val = formatBits[i];
        if (i < 6) matrix[i][8] = val;
        else if (i < 8) matrix[i + 1][8] = val;
        else matrix[moduleCount - 15 + i][8] = val;

        if (i < 8) matrix[8][moduleCount - 1 - i] = val;
        else if (i == 8) matrix[8][15 - i] = val;
        else matrix[8][15 - 1 - i] = val;
      }

      return { matrix: matrix, count: moduleCount };
    }

    return { generateMatrix: generateMatrix };
  })();

  // Helper: Guarantees 100% Full Absolute Canonical URL
  function ensureFullAbsoluteUrl(urlStr) {
    if (!urlStr) return `${BASE_CANONICAL_DOMAIN}/`;
    try {
      if (urlStr.startsWith('http://') || urlStr.startsWith('https://')) {
        const u = new URL(urlStr);
        if (u.hostname === 'localhost' || u.hostname === '127.0.0.1') {
          return `${BASE_CANONICAL_DOMAIN}${u.pathname}${u.search}${u.hash}`;
        }
        return u.href;
      }
      const cleanPath = urlStr.startsWith('/') ? urlStr : '/' + urlStr;
      return new URL(cleanPath, BASE_CANONICAL_DOMAIN).href;
    } catch (e) {
      return urlStr;
    }
  }

  /* ==========================================================================
     MODULE A: Content Recognition & Audience-Tailored Social Captions Engine
     ========================================================================== */
  function extractPageMetadata(htmlDoc = document, targetUrl = window.location.href, pageItemData = null) {
    let fullUrl = ensureFullAbsoluteUrl(targetUrl);
    if (pageItemData && pageItemData.url) {
      fullUrl = ensureFullAbsoluteUrl(pageItemData.url);
    }

    const meta = {
      url: fullUrl,
      title: '',
      description: '',
      customTitle: '',
      customDescription: '',
      canonicalUrl: fullUrl,
      ogImage: `${BASE_CANONICAL_DOMAIN}/images/cacts-logo.png`,
      schemaType: 'WebPage',
      badgeTitle: '[Recognized: Web Page]',
      presetKey: 'guide',
      ldData: {},
      ldCaption: '',
      pageItemData: pageItemData
    };

    // Extract Title & Description
    if (pageItemData) {
      meta.title = pageItemData.title || '';
      meta.description = pageItemData.description || '';
    } else {
      const titleElem = htmlDoc.querySelector('title');
      meta.title = titleElem ? titleElem.innerText.trim() : 'CACTS Pune Software Training';

      const descElem = htmlDoc.querySelector('meta[name="description"]') || htmlDoc.querySelector('meta[property="og:description"]');
      meta.description = descElem ? descElem.getAttribute('content').trim() : meta.title;

      const ogImgElem = htmlDoc.querySelector('meta[property="og:image"]');
      if (ogImgElem) meta.ogImage = ensureFullAbsoluteUrl(ogImgElem.getAttribute('content'));

      const canonElem = htmlDoc.querySelector('link[rel="canonical"]');
      if (canonElem) meta.canonicalUrl = ensureFullAbsoluteUrl(canonElem.getAttribute('href'));
    }

    const cleanTitle = meta.title.replace(/\s*[|\-–—:]\s*(?:CACTS(?:\s+Pune|\s+Institute|\s+Training|\s+Careers)?|Centre\s+of\s+Advanced\s+Computer\s+Training\s+and\s+Studies).*$/i, '').trim();

    // 1. Certificate Verification Portal & Credentials (Target Audience: Candidates, Recruiters & HR Managers)
    if (fullUrl.includes('verify.html') || (pageItemData && (pageItemData.schema_type || '').toLowerCase().includes('credential'))) {
      meta.schemaType = 'EducationalOccupationalCredential';
      meta.badgeTitle = '[Recognized: Certificate Verification Portal]';
      meta.presetKey = 'cert';

      // Dynamically inspect URL query parameters or active DOM on verify.html for candidate certificate details
      let certId = '';
      let studentName = '';
      let courseName = '';

      try {
        if (typeof window !== 'undefined') {
          const urlObj = new URL(fullUrl);
          if (urlObj.searchParams.has('id')) {
            certId = urlObj.searchParams.get('id').trim();
          }
        }
      } catch(e) {}

      if (typeof document !== 'undefined') {
        const nameElem = document.getElementById('certStudentName');
        const courseElem = document.getElementById('certCourseName');
        const barIdElem = document.getElementById('barCertId');

        if (nameElem && nameElem.innerText && nameElem.innerText.trim()) {
          studentName = nameElem.innerText.trim();
        }
        if (courseElem && courseElem.innerText && courseElem.innerText.trim()) {
          courseName = courseElem.innerText.trim();
        }
        if (!certId && barIdElem && barIdElem.innerText && barIdElem.innerText.trim()) {
          certId = barIdElem.innerText.trim();
        }
      }

      if (studentName || certId || courseName) {
        const displayStudent = studentName || 'Candidate';
        const displayCourse = courseName || 'Software Architecture & Development';
        const displayCertId = certId ? ` (Certificate ID: ${certId})` : '';

        meta.customTitle = `Congratulations ${displayStudent}! Verified Certificate`;
        meta.customDescription = `Official Digital Accreditation: ${displayCourse}${displayCertId} at CACTS Pune. 1-to-1 live mentor code reviews & real company project internships.`;
        meta.ldCaption = `Congratulations ${displayStudent} on successfully completing the ${displayCourse} program at CACTS Pune!\n\nOfficial Verified Credential${displayCertId}\nAccreditation Status: VALID & AUTHENTIC\nProgram Highlights: 1-to-1 Live Mentor Code Reviews & Real Company Project Internships.\n\nRecruiters & HR Managers: Validate candidate credentials online in under 10 seconds:\n${meta.url}`;
      } else {
        meta.ldCaption = `Hiring managers & recruiters: Need to verify a candidate's CACTS credentials in under 10 seconds?\n\nOur official accreditation portal allows tech employers to instantly validate live project completion, 1-to-1 mentorship hours, and verified student certifications.\n\nVerify Credentials Online: ${meta.url}`;
      }
      return meta;
    }

    // 2. Tech Job Postings (Target Audience: Pune Developers & CS Graduates)
    if (fullUrl.includes('/jobs/') || (pageItemData && (pageItemData.schema_type || '').toLowerCase().includes('job'))) {
      meta.schemaType = 'JobPosting';
      meta.badgeTitle = '[Recognized: Tech Job Posting]';
      meta.presetKey = 'job';

      if (pageItemData && pageItemData.jobTitle) {
        const jTitle = pageItemData.jobTitle;
        const jStipend = pageItemData.stipend ? ` (${pageItemData.stipend})` : '';
        const jDesc = truncateText(pageItemData.jobDesc || pageItemData.description, 140);

        meta.customTitle = `Hiring: ${jTitle}`;
        meta.customDescription = `${jTitle}${jStipend} at CACTS Pune. ${jDesc}`;
        meta.ldCaption = `Hiring Alert for Pune Developers & Engineering Graduates!\n\nRole: ${jTitle}${jStipend}\nLocation: CACTS Pune\n\n${jDesc}\n\n1-to-1 Live Mentor Code Reviews, Production Codebase Access & Career Placement Support.\n\nApply Online: ${meta.url}`;
      } else {
        meta.ldCaption = `Hiring Alert for Pune Tech Developers & Engineering Graduates!\n\n${cleanTitle} at CACTS Pune. Gain 1-to-1 live mentor code reviews, production codebase access & career guidance.\n\nApply Now: ${meta.url}`;
      }
      return meta;
    }

    // 3. Course Subpages & Syllabi (Bifurcated: Fees, Syllabus, Beginner, Roadmap, Comparison, Main)
    if (fullUrl.includes('/courses/') || (pageItemData && (pageItemData.schema_type || '').toLowerCase().includes('course'))) {
      meta.schemaType = 'Course';

      if (fullUrl.includes('fees.html') || fullUrl.includes('/fees/')) {
        meta.badgeTitle = '[Recognized: Course Fee Structure]';
        meta.presetKey = 'fees';
        meta.ldCaption = `Want to check course fees & flexible installment plans for ${cleanTitle} at CACTS Pune?\n\nRead complete fee breakdown, 1-to-1 mentorship details & enrollment plans.\n\nView Fee Structure: ${meta.url}`;
      } else if (fullUrl.includes('syllabus.html') || fullUrl.includes('/syllabus/')) {
        meta.badgeTitle = '[Recognized: Course Syllabus Breakdown]';
        meta.presetKey = 'syllabus';
        meta.ldCaption = `Explore the complete module-by-module syllabus for ${cleanTitle} at CACTS Pune.\n\nMaster live company projects & 1-to-1 mentor code reviews.\n\nView Full Syllabus: ${meta.url}`;
      } else if (fullUrl.includes('beginner.html') || fullUrl.includes('/beginner/')) {
        meta.badgeTitle = '[Recognized: Beginner Tech Guide]';
        meta.presetKey = 'beginner';
        meta.ldCaption = `Starting your software development journey from scratch?\n\nRead our step-by-step beginner guide for ${cleanTitle} at CACTS Pune.\n\nStart Learning: ${meta.url}`;
      } else if (fullUrl.includes('roadmap.html') || fullUrl.includes('/roadmap/')) {
        meta.badgeTitle = '[Recognized: Developer Career Roadmap]';
        meta.presetKey = 'roadmap';
        meta.ldCaption = `Planning your tech career roadmap?\n\nDiscover the developer career path & skills required for ${cleanTitle} at CACTS Pune.\n\nExplore Roadmap: ${meta.url}`;
      } else if (fullUrl.includes('comparison.html') || fullUrl.includes('/comparison/')) {
        meta.badgeTitle = '[Recognized: Tech Comparison Guide]';
        meta.presetKey = 'comparison';
        meta.ldCaption = `Confused between tech stacks?\n\nRead our in-depth comparative breakdown for ${cleanTitle} by CACTS Pune engineering mentors.\n\nRead Comparison: ${meta.url}`;
      } else {
        meta.badgeTitle = '[Recognized: 1-to-1 Course Training]';
        meta.presetKey = 'course';
        meta.ldCaption = `Want to master full-stack software development with 1-to-1 live mentor code reviews?\n\nExplore ${cleanTitle} at CACTS Pune with practical hands-on curriculum, production company projects & career guidance.\n\nSyllabus & Enrollment Details: ${meta.url}`;
      }
      return meta;
    }

    // 4. Interactive Developer Tools (Target Audience: Web Developers)
    if (fullUrl.includes('/tools/') || (pageItemData && (pageItemData.schema_type || '').toLowerCase().includes('tool'))) {
      meta.schemaType = 'WebApplication';
      meta.badgeTitle = '[Recognized: Interactive Developer Tool]';
      meta.presetKey = 'tool';
      meta.ldCaption = `Boost your developer productivity with free interactive tools by CACTS Pune!\n\n${cleanTitle}: ${truncateText(meta.description, 130)}\n\nTry Tool Online: ${meta.url}`;
      return meta;
    }

    // 5. Student Reviews & Alumni Success (Target Audience: Prospective Students & Parents)
    if (fullUrl.includes('reviews.html') || (pageItemData && (pageItemData.schema_type || '').toLowerCase().includes('review'))) {
      meta.schemaType = 'StudentReviews';
      meta.badgeTitle = '[Recognized: Student Reviews & Alumni Ratings]';
      meta.presetKey = 'review';

      if (pageItemData && pageItemData.studentName) {
        const sName = pageItemData.studentName;
        const sRole = pageItemData.studentRole || 'CACTS Pune Alumni';
        const rText = truncateText(pageItemData.reviewText || pageItemData.description, 140);

        meta.customTitle = `Alumni Story: ${sName}`;
        meta.customDescription = `"${rText}" - ${sName} (${sRole})`;
        meta.ldCaption = `Alumni Career Transformation Story at CACTS Pune:\n\n${sName} (${sRole}):\n"${rText}"\n\nDiscover how 1-to-1 live mentor code reviews & real company project internships help developers land tech roles.\n\nRead Full Alumni Reviews: ${meta.url}`;
      } else {
        meta.ldCaption = `Discover authentic career transformations & student reviews at CACTS Pune.\n\nSee how 1-to-1 live code reviews & real company project internships help developers land tech roles.\n\nRead Alumni Reviews: ${meta.url}`;
      }
      return meta;
    }

    // 6. Branch Location Pages (Target Audience: Pune Local Area Residents)
    if (fullUrl.includes('/locations/')) {
      meta.schemaType = 'LocalBusiness';
      meta.badgeTitle = '[Recognized: Pune Branch Location]';
      meta.presetKey = 'location';
      meta.ldCaption = `Looking for top-rated software & IT training institutes in Pune?\n\nVisit CACTS Pune (${cleanTitle}) for 1-to-1 developer mentorship, practical labs, and live company projects.\n\nExplore Branch Details: ${meta.url}`;
      return meta;
    }

    // 7. Privacy Policy Page
    if (fullUrl.includes('privacy')) {
      meta.schemaType = 'PrivacyPolicy';
      meta.badgeTitle = '[Recognized: Institutional Privacy Policy]';
      meta.presetKey = 'policy';
      meta.ldCaption = `Official Privacy Policy & Data Protection Guidelines for CACTS Pune students, applicants, and site visitors.\n\nRead Privacy Policy: ${meta.url}`;
      return meta;
    }

    // 8. Terms & Conditions Page
    if (fullUrl.includes('terms')) {
      meta.schemaType = 'TermsAndConditions';
      meta.badgeTitle = '[Recognized: Legal Terms & Conditions]';
      meta.presetKey = 'policy';
      meta.ldCaption = `Official Terms & Conditions, Enrollment Rules, and Institutional Guidelines for CACTS Pune.\n\nRead Terms & Conditions: ${meta.url}`;
      return meta;
    }

    // 9. About Us Page
    if (fullUrl.includes('about')) {
      meta.schemaType = 'AboutPage';
      meta.badgeTitle = '[Recognized: Institutional Profile]';
      meta.presetKey = 'guide';
      meta.ldCaption = `Discover CACTS Pune - Centre of Advanced Computer Training and Studies. 1-to-1 live developer mentorship, ISO 9001:2015 compliant standards & real company project internships.\n\nVisit Profile: ${meta.url}`;
      return meta;
    }

    // 10. Contact Us Page
    if (fullUrl.includes('contact')) {
      meta.schemaType = 'ContactPage';
      meta.badgeTitle = '[Recognized: Official Contact Desk]';
      meta.presetKey = 'guide';
      meta.ldCaption = `Get in touch with CACTS Pune admissions, student support & technical training counselors.\n\nContact Support Desk: ${meta.url}`;
      return meta;
    }

    // 11. FAQ Page
    if (fullUrl.includes('faq')) {
      meta.schemaType = 'FAQPage';
      meta.badgeTitle = '[Recognized: Frequently Asked Questions]';
      meta.presetKey = 'guide';
      meta.ldCaption = `Have questions about 1-to-1 mentorship, course fees, syllabus, or placement assistance at CACTS Pune? Find clear answers here.\n\nVisit Help FAQ: ${meta.url}`;
      return meta;
    }

    // 12. Careers Overview Page
    if (fullUrl.includes('careers')) {
      meta.schemaType = 'CareersPage';
      meta.badgeTitle = '[Recognized: Career Opportunities & Hiring]';
      meta.presetKey = 'job';
      meta.ldCaption = `Explore tech career opportunities, hiring alerts & developer placement support at CACTS Pune.\n\nVisit Career Center: ${meta.url}`;
      return meta;
    }

    // 13. Sitemap Directory Page
    if (fullUrl.includes('sitemap')) {
      meta.schemaType = 'SiteNavigation';
      meta.badgeTitle = '[Recognized: Site Directory]';
      meta.presetKey = 'guide';
      meta.ldCaption = `Explore the complete directory of courses, tech career roadmaps, locations & developer tools by CACTS Pune.\n\nVisit Sitemap: ${meta.url}`;
      return meta;
    }

    // 14. Developer Tech Articles & Guides (/guides/, /comparisons/)
    if (fullUrl.includes('/guides/') || fullUrl.includes('/comparisons/')) {
      meta.schemaType = 'Article';
      meta.badgeTitle = '[Recognized: Tech Engineering Guide]';
      meta.presetKey = 'guide';
      meta.ldCaption = `Looking to solve complex software engineering challenges?\n\nRead ${cleanTitle} written by CACTS Pune engineering mentors.\n\nVisit Guide: ${meta.url}`;
      return meta;
    }

    // 15. Generic Web Page Fallback
    meta.schemaType = 'WebPage';
    meta.badgeTitle = '[Recognized: Official Web Page]';
    meta.presetKey = 'guide';
    meta.ldCaption = `${cleanTitle} - CACTS Pune Centre of Advanced Computer Training and Studies.\n\nVisit: ${meta.url}`;
    return meta;
  }

  /* ==========================================================================
     MODULE B: Strict Schema-Type-to-Platform Relevance Filtering Engine
     ========================================================================== */
  function getPlatformSuitability(meta) {
    const targetUrl = ensureFullAbsoluteUrl(meta.url);
    const captionElem = document.getElementById('socialCaptionText');
    const liveCaption = captionElem ? captionElem.value : (meta.ldCaption || meta.title);

    const encUrl = encodeURIComponent(appendUtmParams(targetUrl, 'social_syndication'));
    const encTitle = encodeURIComponent(meta.title);
    const encFullCaption = encodeURIComponent(liveCaption);

    // Master Platform Library Dictionary
    const allPlatforms = [
      {
        id: 'linkedin-feed',
        name: 'LinkedIn Feed',
        icon: 'IN',
        color: '#0077b5',
        recommended: true,
        formatTag: '1200x630 Feed Banner',
        actionType: 'intent',
        intentUrl: `https://www.linkedin.com/sharing/share-offsite/?url=${encUrl}`,
        actionLabel: 'Share to LinkedIn Feed'
      },
      {
        id: 'twitter-tweet',
        name: 'X (Twitter)',
        icon: 'X',
        color: '#1da1f2',
        recommended: true,
        formatTag: '1200x630 Tech Tweet',
        actionType: 'intent',
        intentUrl: `https://twitter.com/intent/tweet?text=${encFullCaption}`,
        actionLabel: 'Post Pre-filled Tweet on X'
      },
      {
        id: 'instagram-story',
        name: 'Instagram Story',
        icon: 'IG',
        color: '#e1306c',
        recommended: true,
        formatTag: '1080x1920 Story Card',
        actionType: 'intent',
        formatKey: '1080x1920',
        actionLabel: 'Copy Caption & Open Instagram'
      },
      {
        id: 'whatsapp-chat',
        name: 'WhatsApp Chat',
        icon: 'WA',
        color: '#25d366',
        recommended: true,
        formatTag: 'Text & Link Share',
        actionType: 'intent',
        intentUrl: `https://api.whatsapp.com/send?text=${encFullCaption}`,
        actionLabel: 'Share Full Text & Link to WhatsApp'
      },
      {
        id: 'whatsapp-enroll',
        name: 'WhatsApp Desk',
        icon: 'WA',
        color: '#128c7e',
        recommended: true,
        formatTag: 'Direct Desk Inquiry',
        actionType: 'intent',
        intentUrl: `https://wa.me/919665566357?text=${encodeURIComponent('Hello CACTS Pune, I am inquiring about: ' + meta.title + ' (' + targetUrl + ')')}`,
        actionLabel: 'Open Direct WhatsApp Desk Inquiry'
      },
      {
        id: 'facebook-feed',
        name: 'Facebook Feed',
        icon: 'FB',
        color: '#1877f2',
        recommended: true,
        formatTag: '1200x630 Link Post',
        actionType: 'intent',
        intentUrl: `https://www.facebook.com/sharer/sharer.php?u=${encUrl}`,
        actionLabel: 'Share to Facebook'
      },
      {
        id: 'gbp-post',
        name: 'Google Business',
        icon: 'G',
        color: '#ea4335',
        recommended: true,
        formatTag: '1200x900 Promo Card',
        actionType: 'intent',
        formatKey: '1200x900',
        actionLabel: 'Copy Caption & Open Google Business'
      },
      {
        id: 'reddit-post',
        name: 'Reddit Post',
        icon: 'RD',
        color: '#ff4500',
        recommended: true,
        formatTag: 'Discussion Link',
        actionType: 'intent',
        intentUrl: `https://www.reddit.com/submit?url=${encUrl}&title=${encTitle}`,
        actionLabel: 'Post to Reddit'
      },
      {
        id: 'bluesky-post',
        name: 'Bluesky Tech',
        icon: 'BS',
        color: '#0085ff',
        recommended: true,
        formatTag: 'Tech Update',
        actionType: 'intent',
        intentUrl: `https://bsky.app/intent/compose?text=${encFullCaption}`,
        actionLabel: 'Post Pre-filled Text to Bluesky'
      }
    ];

    // Mobile System Share Sheet (Always Available on Supported Devices)
    if (navigator.share) {
      allPlatforms.unshift({
        id: 'native-os-share',
        name: 'Mobile Share Sheet',
        icon: 'OS',
        color: '#8b5cf6',
        recommended: true,
        formatTag: 'Native Image & Text Share',
        actionType: 'native-share',
        actionLabel: 'Open Mobile System Share Sheet'
      });
    }

    // Determine Strict Allowed Platform IDs Based on Content Schema & Category
    let allowedIds = [];

    const urlLower = targetUrl.toLowerCase();
    const schema = (meta.schemaType || '').toLowerCase();

    if (urlLower.includes('verify.html') || schema.includes('credential')) {
      // 1. Certificate Verification (Strictly Trust & Employer Centric)
      allowedIds = ['linkedin-feed', 'twitter-tweet', 'whatsapp-chat', 'native-os-share'];
    } else if (urlLower.includes('/jobs/') || schema.includes('job') || schema.includes('careers')) {
      // 2. Job Postings & Hiring Alerts
      allowedIds = ['linkedin-feed', 'twitter-tweet', 'reddit-post', 'bluesky-post', 'whatsapp-chat', 'whatsapp-enroll', 'native-os-share'];
    } else if (urlLower.includes('/courses/') || schema.includes('course')) {
      // 3. Course Syllabi & Admissions (including subpages: fees, syllabus, beginner, roadmap, comparison)
      if (urlLower.includes('beginner') || urlLower.includes('roadmap') || urlLower.includes('comparison')) {
        allowedIds = ['linkedin-feed', 'twitter-tweet', 'reddit-post', 'bluesky-post', 'whatsapp-chat', 'instagram-story', 'native-os-share'];
      } else {
        allowedIds = ['instagram-story', 'whatsapp-enroll', 'whatsapp-chat', 'facebook-feed', 'gbp-post', 'linkedin-feed', 'native-os-share'];
      }
    } else if (urlLower.includes('/tools/') || schema.includes('application') || schema.includes('tool')) {
      // 4. Interactive Developer Tools
      allowedIds = ['twitter-tweet', 'reddit-post', 'bluesky-post', 'linkedin-feed', 'whatsapp-chat', 'native-os-share'];
    } else if (urlLower.includes('reviews.html') || schema.includes('review')) {
      // 5. Student Reviews & Alumni Ratings
      allowedIds = ['instagram-story', 'facebook-feed', 'gbp-post', 'whatsapp-chat', 'native-os-share'];
    } else if (urlLower.includes('/locations/') || schema.includes('localbusiness')) {
      // 6. Branch Location Pages & Hubs
      allowedIds = ['gbp-post', 'facebook-feed', 'instagram-story', 'whatsapp-chat', 'native-os-share'];
    } else if (urlLower.includes('report') || schema.includes('report')) {
      // 7. Industry Benchmark Reports & Salary Index
      allowedIds = ['linkedin-feed', 'twitter-tweet', 'reddit-post', 'bluesky-post', 'whatsapp-chat', 'native-os-share'];
    } else if (urlLower.includes('privacy') || urlLower.includes('terms') || urlLower.includes('policy')) {
      // 8. Legal & Policy Pages
      allowedIds = ['linkedin-feed', 'whatsapp-chat', 'native-os-share'];
    } else if (urlLower.includes('about') || urlLower.includes('contact') || urlLower.includes('faq') || urlLower.includes('sitemap')) {
      // 9. Institutional Informational Pages
      allowedIds = ['linkedin-feed', 'facebook-feed', 'whatsapp-chat', 'whatsapp-enroll', 'native-os-share'];
    } else {
      // 10. Developer Tech Articles & Guides (Default Fallback)
      allowedIds = ['linkedin-feed', 'twitter-tweet', 'reddit-post', 'bluesky-post', 'whatsapp-chat', 'native-os-share'];
    }

    // Return ONLY the relevant platforms for this specific content schema
    return allPlatforms.filter(p => allowedIds.includes(p.id));
  }

  function appendUtmParams(urlStr, platformSource) {
    const fullUrl = ensureFullAbsoluteUrl(urlStr);
    try {
      const u = new URL(fullUrl);
      u.searchParams.set('utm_source', platformSource);
      u.searchParams.set('utm_medium', 'social_syndication');
      u.searchParams.set('utm_campaign', 'cacts_share');
      return u.href;
    } catch (e) {
      return fullUrl;
    }
  }

  function truncateText(str, maxLen) {
    if (!str || str.length <= maxLen) return str;
    return str.substring(0, maxLen - 3) + '...';
  }

  // Fixed Schema & Sub-Schema Category Palettes Map
  const SCHEMA_PALETTES = {
    'cert':       { bgGradStart: '#78350f', bgGradEnd: '#1c1917', accentTabBg: '#f59e0b', accentTabTextColor: '#1c1917', subheadColor: '#fbbf24' },
    'job':        { bgGradStart: '#312e81', bgGradEnd: '#09090b', accentTabBg: '#818cf8', accentTabTextColor: '#09090b', subheadColor: '#c7d2fe' },
    'fees':       { bgGradStart: '#064e3b', bgGradEnd: '#022c22', accentTabBg: '#10b981', accentTabTextColor: '#022c22', subheadColor: '#34d399' },
    'syllabus':   { bgGradStart: '#1e3a8a', bgGradEnd: '#0f172a', accentTabBg: '#38bdf8', accentTabTextColor: '#0f172a', subheadColor: '#7dd3fc' },
    'beginner':   { bgGradStart: '#451a03', bgGradEnd: '#0f172a', accentTabBg: '#f97316', accentTabTextColor: '#0f172a', subheadColor: '#fb923c' },
    'roadmap':    { bgGradStart: '#4c1d95', bgGradEnd: '#1e1b4b', accentTabBg: '#c084fc', accentTabTextColor: '#1e1b4b', subheadColor: '#e879f9' },
    'comparison': { bgGradStart: '#164e63', bgGradEnd: '#083344', accentTabBg: '#22d3ee', accentTabTextColor: '#083344', subheadColor: '#67e8f9' },
    'course':     { bgGradStart: '#1e40af', bgGradEnd: '#030712', accentTabBg: '#60a5fa', accentTabTextColor: '#030712', subheadColor: '#93c5fd' },
    'tool':       { bgGradStart: '#14532d', bgGradEnd: '#052e16', accentTabBg: '#84cc16', accentTabTextColor: '#052e16', subheadColor: '#a3e635' },
    'review':     { bgGradStart: '#701a75', bgGradEnd: '#0f172a', accentTabBg: '#f472b6', accentTabTextColor: '#0f172a', subheadColor: '#fbcfe8' },
    'location':   { bgGradStart: '#0c4a6e', bgGradEnd: '#032830', accentTabBg: '#38bdf8', accentTabTextColor: '#032830', subheadColor: '#7dd3fc' },
    'report':     { bgGradStart: '#7f1d1d', bgGradEnd: '#450a0a', accentTabBg: '#f87171', accentTabTextColor: '#450a0a', subheadColor: '#fca5a5' },
    'policy':     { bgGradStart: '#27272a', bgGradEnd: '#09090b', accentTabBg: '#e4e4e7', accentTabTextColor: '#09090b', subheadColor: '#fafafa' },
    'info':       { bgGradStart: '#18181b', bgGradEnd: '#09090b', accentTabBg: '#fbbf24', accentTabTextColor: '#09090b', subheadColor: '#fef08a' },
    'guide':      { bgGradStart: '#064e3b', bgGradEnd: '#0f172a', accentTabBg: '#34d399', accentTabTextColor: '#0f172a', subheadColor: '#a7f3d0' }
  };

  // Fixed Category-Specific Background Palette & Badge Selection Engine
  function getItemPalette(meta) {
    let tabTop = 'OFFICIAL PORTAL';
    let tabBottom = 'CACTS Pune Web Page';
    let cta = 'SCAN QR CODE TO VISIT PAGE';
    let catKey = 'guide';

    const targetUrl = (meta.url || '').toLowerCase();
    const schema = (meta.schemaType || '').toLowerCase();

    if (schema.includes('credential') || targetUrl.includes('verify.html')) {
      tabTop = 'OFFICIAL ACCREDITATION';
      tabBottom = 'Certificate Verification';
      cta = 'SCAN QR CODE TO VERIFY CREDENTIALS';
      catKey = 'cert';
    } else if (schema.includes('job') || targetUrl.includes('/jobs/')) {
      tabTop = 'CAREER OPPORTUNITY';
      tabBottom = 'Developer Job Posting';
      cta = 'SCAN QR CODE TO APPLY ONLINE';
      catKey = 'job';
    } else if (targetUrl.includes('fees.html') || targetUrl.includes('/fees/')) {
      tabTop = 'COURSE FEES';
      tabBottom = 'Fees & Installments';
      cta = 'SCAN QR CODE FOR FEES & EMI';
      catKey = 'fees';
    } else if (targetUrl.includes('syllabus.html') || targetUrl.includes('/syllabus/')) {
      tabTop = 'COURSE SYLLABUS';
      tabBottom = 'Complete Module Breakdown';
      cta = 'SCAN QR CODE FOR FULL SYLLABUS';
      catKey = 'syllabus';
    } else if (targetUrl.includes('beginner.html') || targetUrl.includes('/beginner/')) {
      tabTop = 'BEGINNER ROADMAP';
      tabBottom = 'Zero-Experience Guide';
      cta = 'SCAN QR CODE FOR BEGINNER GUIDE';
      catKey = 'beginner';
    } else if (targetUrl.includes('roadmap.html') || targetUrl.includes('/roadmap/')) {
      tabTop = 'CAREER ROADMAP';
      tabBottom = 'Developer Career Path';
      cta = 'SCAN QR CODE FOR CAREER ROADMAP';
      catKey = 'roadmap';
    } else if (targetUrl.includes('comparison.html') || targetUrl.includes('/comparison/')) {
      tabTop = 'TECH COMPARISON';
      tabBottom = 'Framework Breakdown';
      cta = 'SCAN QR CODE FOR TECH COMPARISON';
      catKey = 'comparison';
    } else if (schema.includes('course') || targetUrl.includes('/courses/')) {
      tabTop = '1-TO-1 COURSE';
      tabBottom = 'Live Mentor Training';
      cta = 'SCAN QR CODE FOR COURSE DETAILS';
      catKey = 'course';
    } else if (schema.includes('tool') || schema.includes('application') || targetUrl.includes('/tools/')) {
      tabTop = 'DEVELOPER TOOL';
      tabBottom = 'Interactive Utility';
      cta = 'SCAN QR CODE TO LAUNCH TOOL';
      catKey = 'tool';
    } else if (schema.includes('review') || targetUrl.includes('reviews.html')) {
      tabTop = 'ALUMNI REVIEWS';
      tabBottom = 'Verified Student Ratings';
      cta = 'SCAN QR CODE FOR ALUMNI REVIEWS';
      catKey = 'review';
    } else if (schema.includes('localbusiness') || targetUrl.includes('/locations/')) {
      tabTop = 'TRAINING INSTITUTE';
      tabBottom = 'Pune Branch Location';
      cta = 'SCAN QR CODE FOR BRANCH DETAILS';
      catKey = 'location';
    } else if (schema.includes('report') || targetUrl.includes('report')) {
      tabTop = 'INDUSTRY REPORT';
      tabBottom = 'Salary & Tech Index';
      cta = 'SCAN QR CODE FOR FULL REPORT';
      catKey = 'report';
    } else if (targetUrl.includes('privacy')) {
      tabTop = 'INSTITUTIONAL POLICY';
      tabBottom = 'Privacy Policy';
      cta = 'SCAN QR CODE FOR PRIVACY POLICY';
      catKey = 'policy';
    } else if (targetUrl.includes('terms')) {
      tabTop = 'LEGAL TERMS';
      tabBottom = 'Terms & Conditions';
      cta = 'SCAN QR CODE FOR LEGAL TERMS';
      catKey = 'policy';
    } else if (targetUrl.includes('about')) {
      tabTop = 'INSTITUTION PROFILE';
      tabBottom = 'About CACTS Pune';
      cta = 'SCAN QR CODE FOR ABOUT DETAILS';
      catKey = 'info';
    } else if (targetUrl.includes('contact')) {
      tabTop = 'OFFICIAL CONTACT';
      tabBottom = 'Support & Help Desk';
      cta = 'SCAN QR CODE FOR CONTACT DESK';
      catKey = 'info';
    } else if (targetUrl.includes('faq')) {
      tabTop = 'KNOWLEDGE DESK';
      tabBottom = 'Frequently Asked Questions';
      cta = 'SCAN QR CODE FOR HELP FAQ';
      catKey = 'info';
    } else if (targetUrl.includes('careers')) {
      tabTop = 'CAREER CENTER';
      tabBottom = 'Job Openings & Placement';
      cta = 'SCAN QR CODE FOR CAREER OPENINGS';
      catKey = 'job';
    } else if (targetUrl.includes('sitemap')) {
      tabTop = 'SITE DIRECTORY';
      tabBottom = 'Full Course Sitemap';
      cta = 'SCAN QR CODE FOR SITE MAP';
      catKey = 'info';
    } else if (targetUrl.includes('/guides/') || targetUrl.includes('/comparisons/') || schema.includes('article')) {
      tabTop = 'ENGINEERING GUIDE';
      tabBottom = 'Tech Career Roadmap';
      cta = 'SCAN QR CODE TO READ GUIDE';
      catKey = 'guide';
    } else {
      tabTop = 'OFFICIAL PORTAL';
      tabBottom = 'CACTS Pune Web Page';
      cta = 'SCAN QR CODE TO VISIT PAGE';
      catKey = 'guide';
    }

    // Get the fixed signature palette for this specific category
    const p = SCHEMA_PALETTES[catKey] || SCHEMA_PALETTES['guide'];

    return {
      bgGradStart: p.bgGradStart,
      bgGradEnd: p.bgGradEnd,
      accentTabBg: p.accentTabBg,
      accentTabTextColor: p.accentTabTextColor,
      accentTabTextTop: tabTop,
      accentTabTextBottom: tabBottom,
      subheadColor: p.subheadColor,
      borderRing: p.accentTabBg,
      ctaLabel: cta
    };
  }

  /* ==========================================================================
     MODULE C: High-Impact Format-Proportional Canvas Media Generator
     ========================================================================== */
  async function renderBrandedCanvas(meta, formatKey = '1200x630') {
    // Ensure QRCode JS library from CDN is requested
    await loadQRCodeLibrary();

    const canvas = document.createElement('canvas');
    const spec = FORMAT_SPECS[formatKey] || FORMAT_SPECS['1200x630'];
    
    const scale = 2;
    canvas.width = spec.width * scale;
    canvas.height = spec.height * scale;
    
    const ctx = canvas.getContext('2d');
    ctx.scale(scale, scale);

    const width = spec.width;
    const height = spec.height;

    const palette = getItemPalette(meta);
    const displayTitle = meta.customTitle || meta.title;
    const displayDesc = meta.customDescription || meta.description;

    // 1. Multi-Stop Dark Linear Gradient Background
    const bgGrad = ctx.createLinearGradient(0, 0, width, height);
    bgGrad.addColorStop(0, palette.bgGradStart);
    bgGrad.addColorStop(0.65, palette.bgGradEnd);
    bgGrad.addColorStop(1, '#05070d');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, width, height);

    // Subtle Radial Background Lighting Glow
    const radialGlow = ctx.createRadialGradient(width / 2, height / 2, 40, width / 2, height / 2, width * 0.85);
    radialGlow.addColorStop(0, 'rgba(255, 255, 255, 0.09)');
    radialGlow.addColorStop(1, 'transparent');
    ctx.fillStyle = radialGlow;
    ctx.fillRect(0, 0, width, height);

    // Frame Border Ring
    ctx.strokeStyle = palette.accentTabBg;
    ctx.lineWidth = formatKey === '1080x1920' ? 6 : 4;
    ctx.strokeRect(3, 3, width - 6, height - 6);

    // Load Logo Image
    let logoLoaded = false;
    let logoSize = 75;
    let logoY = 36;
    if (formatKey === '1080x1080') {
      logoSize = 85;
      logoY = 42;
    } else if (formatKey === '1080x1920') {
      logoSize = 110;
      logoY = 70;
    }

    let logoImg = new Image();
    try {
      logoImg.crossOrigin = 'anonymous';
      const loadPromise = new Promise((resolve, reject) => {
        logoImg.onload = () => resolve(true);
        logoImg.onerror = () => reject(false);
        logoImg.src = ensureFullAbsoluteUrl('images/cacts-logo.png');
      });
      const timeoutPromise = new Promise(resolve => setTimeout(() => resolve(false), 1500));
      logoLoaded = await Promise.race([loadPromise, timeoutPromise]);
    } catch (e) {
      logoLoaded = false;
    }

    /* ==========================================================================
       SPECIALIZED DEDICATED RENDERER FOR 1080x1920 VERTICAL STORY FORMAT
       ========================================================================== */
    if (formatKey === '1080x1920') {
      // 1. Top Header Branding
      if (logoLoaded) {
        ctx.drawImage(logoImg, 50, 70, 110, 110);
      } else {
        ctx.fillStyle = palette.accentTabBg;
        ctx.beginPath();
        ctx.roundRect(50, 70, 110, 110, 18);
        ctx.fill();
        ctx.fillStyle = palette.accentTabTextColor;
        ctx.font = 'bold 54px Montserrat, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('C', 105, 125);
      }

      ctx.textAlign = 'left';
      ctx.textBaseline = 'alphabetic';
      ctx.fillStyle = '#FFFFFF';
      ctx.font = '800 44px Montserrat, sans-serif';
      ctx.fillText('CACTS Pune', 180, 116);

      ctx.fillStyle = '#cbd5e1';
      ctx.font = '500 19px Montserrat, sans-serif';
      ctx.fillText('Centre of Advanced Computer Training and Studies', 180, 148);

      ctx.fillStyle = palette.subheadColor;
      ctx.font = '600 17px Montserrat, sans-serif';
      ctx.fillText('ISO 9001:2015 Compliant IT Institute  •  Call/WA: +91 96655 66357', 180, 176);

      // Header Divider Glow Line
      const headGrad = ctx.createLinearGradient(50, 0, width - 200, 0);
      headGrad.addColorStop(0, 'rgba(255, 255, 255, 0.35)');
      headGrad.addColorStop(1, 'transparent');
      ctx.fillStyle = headGrad;
      ctx.fillRect(50, 210, width - 280, 3);

      // Top Right Overhanging Badge Tab (Expanded Schema Text Box)
      const tabX = width - 330;
      ctx.save();
      ctx.shadowColor = 'rgba(0, 0, 0, 0.6)';
      ctx.shadowBlur = 18;
      ctx.shadowOffsetY = 8;
      ctx.fillStyle = palette.accentTabBg;
      ctx.beginPath();
      ctx.roundRect(tabX, 0, 295, 92, [0, 0, 18, 18]);
      ctx.fill();
      ctx.restore();

      ctx.fillStyle = palette.accentTabTextColor;
      ctx.textAlign = 'center';
      ctx.font = 'bold 16px Montserrat, sans-serif';
      ctx.fillText(palette.accentTabTextTop, tabX + 147, 38);
      ctx.font = '800 20px Montserrat, sans-serif';
      ctx.fillText(palette.accentTabTextBottom, tabX + 147, 68);

      // 2. Title Section (Large, Highly Readable Content-Focused Typography)
      let titleY = 280;
      let baseTitleSize = 72;
      ctx.font = `800 ${baseTitleSize}px Montserrat, sans-serif`;
      while (ctx.measureText(displayTitle).width > (width - 100) * 4.2 && baseTitleSize > 38) {
        baseTitleSize -= 2;
        ctx.font = `800 ${baseTitleSize}px Montserrat, sans-serif`;
      }

      ctx.save();
      ctx.shadowColor = 'rgba(0, 0, 0, 0.85)';
      ctx.shadowBlur = 14;
      ctx.shadowOffsetY = 5;
      ctx.textAlign = 'left';
      ctx.textBaseline = 'alphabetic';
      ctx.fillStyle = '#FFFFFF';
      const titleLinesDrawn = wrapText(ctx, displayTitle, 50, titleY, width - 100, baseTitleSize * 1.28, 5);
      ctx.restore();

      // Title Divider Accent Line
      const titleDividerY = titleY + (titleLinesDrawn * baseTitleSize * 1.28) + 20;
      const divGrad = ctx.createLinearGradient(50, 0, width - 100, 0);
      divGrad.addColorStop(0, palette.accentTabBg);
      divGrad.addColorStop(1, 'transparent');
      ctx.fillStyle = divGrad;
      ctx.fillRect(50, titleDividerY, width - 100, 5);

      // 3. Description Section (Generous Vertical Content Space)
      const descY = titleDividerY + 64;
      const descFontSize = 40;
      const descLineHeight = 64;
      ctx.fillStyle = '#f1f5f9';
      ctx.font = `400 ${descFontSize}px Montserrat, sans-serif`;
      wrapText(ctx, displayDesc, 50, descY, width - 100, descLineHeight, 12);

      // 4. Solid "SCAN QR CODE TO..." CTA Button & Real QRCode Renderer
      const btnY = 1680;
      const btnW = 680;
      const btnH = 88;

      ctx.save();
      ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
      ctx.shadowBlur = 14;
      ctx.shadowOffsetY = 6;
      ctx.fillStyle = palette.accentTabBg;
      ctx.beginPath();
      ctx.roundRect(50, btnY, btnW, btnH, btnH / 2);
      ctx.fill();
      ctx.restore();

      ctx.fillStyle = palette.accentTabTextColor;
      ctx.font = 'bold 24px Montserrat, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(palette.ctaLabel, 50 + btnW / 2, btnY + 54);

      await renderRealQrCodeOnCanvas(ctx, meta.url, width - 260, 1600, 210);

      // 5. Bottom Footer Bar with *T&C Apply Disclaimer
      const footerY = height - 65;
      ctx.fillStyle = 'rgba(0, 0, 0, 0.55)';
      ctx.fillRect(0, footerY, width, 65);
      ctx.fillStyle = '#cbd5e1';
      ctx.font = '600 16px Montserrat, sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(`Website: ${BASE_CANONICAL_DOMAIN}  •  *T&C Apply. Fees, offers & syllabus subject to updates online.`, 50, footerY + 40);

      return new Promise(resolve => {
        canvas.toBlob(blob => resolve(blob), 'image/png');
      });
    }

    /* ==========================================================================
       STANDARD / LANDSCAPE / SQUARE CANVAS RENDERER (1200x630, 1080x1080, etc.)
       ========================================================================== */
    if (logoLoaded) {
      ctx.drawImage(logoImg, 40, logoY, logoSize, logoSize);
    } else {
      ctx.fillStyle = palette.accentTabBg;
      ctx.beginPath();
      ctx.roundRect(40, logoY, logoSize, logoSize, 14);
      ctx.fill();
      ctx.fillStyle = palette.accentTabTextColor;
      ctx.font = `bold ${logoSize * 0.48}px Montserrat, sans-serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('C', 40 + logoSize / 2, logoY + logoSize / 2);
    }

    // Institutional Header Typography
    ctx.textAlign = 'left';
    ctx.textBaseline = 'alphabetic';
    ctx.fillStyle = '#FFFFFF';

    let headTextX = 40 + logoSize + 18;
    let headTitleSize = 32;
    let headSubSize = 14;
    let headTagSize = 13;
    let headLine1Y = 68;
    let headLine2Y = 91;
    let headLine3Y = 112;
    let headerDividerY = 132;

    if (formatKey === '1080x1080') {
      headTitleSize = 36;
      headSubSize = 15;
      headTagSize = 14;
      headLine1Y = 78;
      headLine2Y = 104;
      headLine3Y = 126;
      headerDividerY = 148;
    }

    ctx.font = `800 ${headTitleSize}px Montserrat, sans-serif`;
    ctx.fillText('CACTS Pune', headTextX, headLine1Y);

    ctx.fillStyle = '#cbd5e1';
    ctx.font = `500 ${headSubSize}px Montserrat, sans-serif`;
    ctx.fillText('Centre of Advanced Computer Training and Studies', headTextX, headLine2Y);

    ctx.fillStyle = palette.subheadColor;
    ctx.font = `600 ${headTagSize}px Montserrat, sans-serif`;
    ctx.fillText('ISO 9001:2015 Compliant IT Institute  •  Call/WA: +91 96655 66357', headTextX, headLine3Y);

    // Header Glow Line
    const headGrad = ctx.createLinearGradient(40, 0, width - 200, 0);
    headGrad.addColorStop(0, 'rgba(255, 255, 255, 0.3)');
    headGrad.addColorStop(1, 'transparent');
    ctx.fillStyle = headGrad;
    ctx.fillRect(40, headerDividerY, width - 240, 2);

    // Top-Right Overhanging Badge Tab (Expanded Schema Text Box)
    let tabWidth = 250;
    let tabHeight = 72;
    if (formatKey === '1080x1080') {
      tabWidth = 270;
      tabHeight = 78;
    }

    const tabX = width - tabWidth - 35;
    const tabY = 0;

    ctx.save();
    ctx.shadowColor = 'rgba(0, 0, 0, 0.6)';
    ctx.shadowBlur = 18;
    ctx.shadowOffsetY = 8;

    ctx.fillStyle = palette.accentTabBg;
    ctx.beginPath();
    ctx.roundRect(tabX, tabY, tabWidth, tabHeight, [0, 0, 16, 16]);
    ctx.fill();
    ctx.restore();

    ctx.fillStyle = palette.accentTabTextColor;
    ctx.textAlign = 'center';
    ctx.font = 'bold 13px Montserrat, sans-serif';
    ctx.fillText(palette.accentTabTextTop, tabX + tabWidth / 2, 28);
    ctx.font = '800 16px Montserrat, sans-serif';
    ctx.fillText(palette.accentTabTextBottom, tabX + tabWidth / 2, 54);

    // Title Typography
    let baseTitleSize = 48;
    let titleY = 205;
    let maxTitleWidth = width - 310;
    let maxTitleLines = 3;

    if (formatKey === '1080x1080') {
      baseTitleSize = 64;
      titleY = 230;
      maxTitleWidth = width - 100;
      maxTitleLines = 4;
    } else if (formatKey === '1920x1080') {
      baseTitleSize = 68;
      titleY = 240;
      maxTitleWidth = width - 380;
      maxTitleLines = 3;
    } else if (formatKey === '1200x900') {
      baseTitleSize = 54;
      titleY = 220;
      maxTitleWidth = width - 320;
      maxTitleLines = 3;
    }

    ctx.font = `800 ${baseTitleSize}px Montserrat, sans-serif`;
    while (ctx.measureText(displayTitle).width > maxTitleWidth * (maxTitleLines - 0.5) && baseTitleSize > 28) {
      baseTitleSize -= 2;
      ctx.font = `800 ${baseTitleSize}px Montserrat, sans-serif`;
    }

    ctx.save();
    ctx.shadowColor = 'rgba(0, 0, 0, 0.85)';
    ctx.shadowBlur = 12;
    ctx.shadowOffsetY = 4;

    ctx.textAlign = 'left';
    ctx.textBaseline = 'alphabetic';
    ctx.fillStyle = '#FFFFFF';
    const linesDrawn = wrapText(ctx, displayTitle, 40, titleY, maxTitleWidth, baseTitleSize * 1.28, maxTitleLines);
    ctx.restore();

    // Title Divider Bar
    const titleDividerY = titleY + (linesDrawn * baseTitleSize * 1.28) + 12;
    const divGrad = ctx.createLinearGradient(40, 0, maxTitleWidth, 0);
    divGrad.addColorStop(0, palette.accentTabBg);
    divGrad.addColorStop(1, 'transparent');
    ctx.fillStyle = divGrad;
    ctx.fillRect(40, titleDividerY, maxTitleWidth, 4);

    // Description Body Text
    let descFontSize = 23;
    let descLineHeight = 35;
    let maxDescLines = 4;

    if (formatKey === '1080x1080') {
      descFontSize = 32;
      descLineHeight = 52;
      maxDescLines = 8;
    } else if (formatKey === '1920x1080') {
      descFontSize = 30;
      descLineHeight = 46;
      maxDescLines = 5;
    } else if (formatKey === '1200x900') {
      descFontSize = 26;
      descLineHeight = 39;
      maxDescLines = 5;
    }

    const descY = titleDividerY + 44;
    ctx.fillStyle = '#f1f5f9';
    ctx.font = `400 ${descFontSize}px Montserrat, sans-serif`;
    wrapText(ctx, displayDesc, 40, descY, maxTitleWidth, descLineHeight, maxDescLines);

    // Explicit "SCAN QR CODE TO..." CTA Pill Button
    let btnWidth = 520;
    let btnHeight = 58;
    let btnFontSize = 17;
    let btnY = height - 135;

    if (formatKey === '1080x1080') {
      btnWidth = 560;
      btnHeight = 72;
      btnFontSize = 20;
      btnY = height - 160;
    } else if (formatKey === '1920x1080') {
      btnWidth = 580;
      btnHeight = 68;
      btnFontSize = 20;
      btnY = height - 160;
    } else if (formatKey === '1200x900') {
      btnWidth = 520;
      btnHeight = 62;
      btnFontSize = 18;
      btnY = height - 140;
    }

    ctx.save();
    ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
    ctx.shadowBlur = 12;
    ctx.shadowOffsetY = 5;

    ctx.fillStyle = palette.accentTabBg;
    ctx.beginPath();
    ctx.roundRect(40, btnY, btnWidth, btnHeight, btnHeight / 2);
    ctx.fill();
    ctx.restore();

    ctx.fillStyle = palette.accentTabTextColor;
    ctx.font = `bold ${btnFontSize}px Montserrat, sans-serif`;
    ctx.textAlign = 'center';
    ctx.fillText(palette.ctaLabel, 40 + btnWidth / 2, btnY + (btnHeight / 2) + (btnFontSize / 3.2));

    // Vector QR Code (Clean & Uncluttered Display)
    let qrX = width - 185;
    let qrY = 150;
    let qrSize = 145;

    if (formatKey === '1080x1080') {
      qrX = width - 210;
      qrY = height - 260;
      qrSize = 165;
    } else if (formatKey === '1920x1080') {
      qrX = width - 240;
      qrY = 160;
      qrSize = 180;
    }

    await renderRealQrCodeOnCanvas(ctx, meta.url, qrX, qrY, qrSize);

    // Bottom Footer Bar with *T&C Apply Disclaimer
    const footerY = height - 55;
    ctx.fillStyle = 'rgba(0, 0, 0, 0.55)';
    ctx.fillRect(0, footerY, width, 55);

    ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, footerY);
    ctx.lineTo(width, footerY);
    ctx.stroke();

    ctx.fillStyle = '#cbd5e1';
    ctx.font = '600 14px Montserrat, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(`Website: ${BASE_CANONICAL_DOMAIN}  •  *T&C Apply. Fees, offers & syllabus subject to updates online.`, 40, footerY + 34);

    return new Promise(resolve => {
      canvas.toBlob(blob => resolve(blob), 'image/png');
    });
  }

  // Multi-Paragraph Word Wrapper with Explicit Left Alignment & Padding Preservation
  function wrapText(ctx, text, x, y, maxWidth, lineHeight, maxLines = 2) {
    if (!text) return 0;
    
    ctx.textAlign = 'left';
    ctx.textBaseline = 'alphabetic';

    const paragraphs = text.split(/\r?\n/).map(p => p.trim()).filter(p => p.length > 0);
    let totalLines = 0;
    let currentY = y;

    for (let pIdx = 0; pIdx < paragraphs.length; pIdx++) {
      if (totalLines >= maxLines) break;

      const words = paragraphs[pIdx].split(' ');
      let line = '';

      for (let n = 0; n < words.length; n++) {
        const testLine = line + words[n] + ' ';
        const metrics = ctx.measureText(testLine);
        if (metrics.width > maxWidth && n > 0) {
          ctx.fillText(line.trim(), x, currentY);
          line = words[n] + ' ';
          currentY += lineHeight;
          totalLines++;

          if (totalLines >= maxLines) {
            ctx.fillText(line.trim() + '...', x, currentY);
            return totalLines;
          }
        } else {
          line = testLine;
        }
      }

      if (line.trim().length > 0 && totalLines < maxLines) {
        ctx.fillText(line.trim(), x, currentY);
        currentY += lineHeight;
        totalLines++;
      }
    }

    return totalLines;
  }

  /* ==========================================================================
     Real QR Code Generator Mechanism (qrcode.js CDN with Reed-Solomon Fallback)
     ========================================================================== */
  async function renderRealQrCodeOnCanvas(ctx, textUrl, x, y, size) {
    ctx.save();
    ctx.fillStyle = '#FFFFFF';
    ctx.beginPath();
    ctx.roundRect(x, y, size, size, 12);
    ctx.fill();

    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 2;
    ctx.stroke();

    const quietPadding = Math.round(size * 0.06);
    const qrBoxX = x + quietPadding;
    const qrBoxY = y + quietPadding;
    const qrBoxSize = size - (quietPadding * 2);

    // Primary Mechanism: QRCode library from qrcode.min.js CDN
    if (window.QRCode) {
      try {
        const tempContainer = document.createElement('div');
        tempContainer.style.position = 'absolute';
        tempContainer.style.left = '-9999px';
        tempContainer.style.top = '-9999px';
        document.body.appendChild(tempContainer);

        new window.QRCode(tempContainer, {
          text: textUrl,
          width: 256,
          height: 256,
          colorDark: '#0F172A',
          colorLight: '#FFFFFF',
          correctLevel: window.QRCode.CorrectLevel.H
        });

        await new Promise(r => setTimeout(r, 60));

        const qrCanvas = tempContainer.querySelector('canvas');
        const qrImg = tempContainer.querySelector('img');

        let drawn = false;
        if (qrCanvas) {
          ctx.drawImage(qrCanvas, qrBoxX, qrBoxY, qrBoxSize, qrBoxSize);
          drawn = true;
        } else if (qrImg && qrImg.src) {
          await new Promise((resolve) => {
            if (qrImg.complete && qrImg.naturalWidth > 0) {
              ctx.drawImage(qrImg, qrBoxX, qrBoxY, qrBoxSize, qrBoxSize);
              drawn = true;
              resolve();
            } else {
              qrImg.onload = () => {
                ctx.drawImage(qrImg, qrBoxX, qrBoxY, qrBoxSize, qrBoxSize);
                drawn = true;
                resolve();
              };
              qrImg.onerror = () => resolve();
            }
          });
        }

        if (document.body.contains(tempContainer)) {
          document.body.removeChild(tempContainer);
        }

        if (drawn) {
          ctx.restore();
          return;
        }
      } catch (e) {
        console.warn('QRCode JS library render error, using Reed-Solomon GF(256) matrix fallback', e);
      }
    }

    // Standards-Compliant Fallback: ISO/IEC 18004 Reed-Solomon GF(256) Matrix Encoder
    try {
      const qrData = QRCodeGen.generateMatrix(textUrl);
      const matrix = qrData.matrix;
      const count = qrData.count;

      const modSize = qrBoxSize / count;
      ctx.fillStyle = '#0F172A';
      for (let r = 0; r < count; r++) {
        for (let c = 0; c < count; c++) {
          if (matrix[r][c]) {
            const mx = qrBoxX + c * modSize;
            const my = qrBoxY + r * modSize;
            ctx.fillRect(mx, my, modSize + 0.35, modSize + 0.35);
          }
        }
      }
    } catch (e) {}

    ctx.restore();
  }

  /* ==========================================================================
     MODULE D: Modal UI Controller & Flow Execution
     ========================================================================== */
  function mountModalUI() {
    if (document.getElementById('cactsSocialModal')) return;

    const modalHtml = `
      <div class="social-modal-overlay" id="cactsSocialModal">
        <div class="social-modal-container">
          <!-- Modal Header -->
          <div class="social-modal-header">
            <div class="social-modal-header-left">
              <h3 class="social-modal-title">CACTS Social Syndication &amp; Media Generator</h3>
              <span class="social-recognition-badge" id="socialRecBadge">[Recognized: Web Page]</span>
            </div>
            <button class="social-modal-close" id="socialModalClose">&times;</button>
          </div>

          <!-- Modal Body -->
          <div class="social-modal-body">
            
            <!-- STEP 1: Platform & Placement Selection Bar -->
            <div class="social-step-section">
              <div class="social-step-header">
                <h4 class="social-step-title">STEP 1: Select Target Platform &amp; Placement Format</h4>
              </div>
              <div class="social-platforms-bar" id="socialPlatformsBar"></div>
            </div>

            <!-- STEP 2 & 3: Two Column Main Grid -->
            <div class="social-main-grid">
              
              <!-- Left Column: Live Canvas Media Panel -->
              <div class="social-canvas-panel">
                <div class="social-step-header">
                  <h4 class="social-step-title">STEP 2: Media Graphic Preview</h4>
                  <div class="social-format-tabs" id="socialFormatTabs">
                    <button class="social-format-tab active" data-format="1200x630">1200x630</button>
                    <button class="social-format-tab" data-format="1080x1080">1080x1080</button>
                    <button class="social-format-tab" data-format="1080x1920">1080x1920</button>
                    <button class="social-format-tab" data-format="1200x900">1200x900</button>
                  </div>
                </div>

                <div class="social-preview-container" id="socialPreviewBox">
                  <img id="socialCanvasImg" class="social-preview-canvas" alt="Generated CACTS Banner Graphic" />
                </div>

                <div class="social-media-controls">
                  <button class="social-toggle-btn" id="socialFeedToggle">Dark Feed Preview</button>
                  <div class="social-download-group">
                    <button class="social-btn-small social-btn-copy-img" id="socialCopyImgBtn">Copy Image</button>
                    <button class="social-btn-small social-btn-download" id="socialDownloadImgBtn">Download PNG</button>
                  </div>
                </div>
              </div>

              <!-- Right Column: Caption, Tailored Hashtags & Action Execution -->
              <div class="social-execution-panel">
                <div class="social-step-header">
                  <h4 class="social-step-title">STEP 3: Caption, Hashtags &amp; Action</h4>
                </div>

                <div class="social-caption-box">
                  <div class="social-caption-header">
                    <span class="social-caption-label">Auto-Generated Social Caption &amp; Full URL</span>
                    <div class="social-caption-tools">
                      <span class="social-char-counter" id="socialCharCounter">0 / 280</span>
                    </div>
                  </div>

                  <textarea class="social-caption-textarea" id="socialCaptionText"></textarea>

                  <!-- Dedicated Text & Hashtag Copy Controls Bar -->
                  <div class="social-caption-actions-bar">
                    <button class="social-btn-small social-btn-copy-text" id="socialCopyTextOnlyBtn">
                      Copy Text Only
                    </button>
                    <button class="social-btn-small social-btn-copy-full" id="socialCopyTextBtn">
                      Copy Full Caption
                    </button>
                    <button class="social-btn-small social-btn-copy-tags" id="socialCopyTagsBtn">
                      Copy Hashtags Only
                    </button>
                  </div>

                  <!-- Dynamic Tailored Hashtags -->
                  <div class="social-hashtag-box" id="socialHashtagBox">
                    <span class="social-hashtag-title" id="socialHashtagTitle">Tailored Platform Hashtags (Click to insert):</span>
                    <div class="social-hashtag-pills" id="socialHashtagPills"></div>
                  </div>
                </div>

                <!-- Primary Execution Button -->
                <button class="social-primary-action-btn" id="socialPrimaryActionBtn">
                  Share to Selected Platform
                </button>
              </div>

            </div>
          </div>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHtml);
    attachModalEvents();
  }

  function attachModalEvents() {
    const modal = document.getElementById('cactsSocialModal');
    const closeBtn = document.getElementById('socialModalClose');
    const feedToggle = document.getElementById('socialFeedToggle');
    const formatTabs = document.getElementById('socialFormatTabs');
    const downloadBtn = document.getElementById('socialDownloadImgBtn');
    const copyImgBtn = document.getElementById('socialCopyImgBtn');
    const copyTextOnlyBtn = document.getElementById('socialCopyTextOnlyBtn');
    const copyTextBtn = document.getElementById('socialCopyTextBtn');
    const copyTagsBtn = document.getElementById('socialCopyTagsBtn');
    const captionArea = document.getElementById('socialCaptionText');
    const primaryBtn = document.getElementById('socialPrimaryActionBtn');

    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', e => { if (e.target === modal) closeModal(); });

    feedToggle.addEventListener('click', () => {
      isLightFeed = !isLightFeed;
      const box = document.getElementById('socialPreviewBox');
      if (isLightFeed) {
        box.classList.add('light-feed');
        feedToggle.innerText = 'Light Feed Preview';
      } else {
        box.classList.remove('light-feed');
        feedToggle.innerText = 'Dark Feed Preview';
      }
    });

    formatTabs.addEventListener('click', async e => {
      const tab = e.target.closest('.social-format-tab');
      if (!tab) return;

      formatTabs.querySelectorAll('.social-format-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      activeFormat = tab.dataset.format;
      await refreshCanvasPreview();
    });

    downloadBtn.addEventListener('click', () => {
      if (!currentBlob) return;
      const link = document.createElement('a');
      link.download = `cacts-share-${activeFormat}-${Date.now()}.png`;
      link.href = currentObjectUrl;
      link.click();
      showToast('Downloaded PNG canvas graphic!');
    });

    copyImgBtn.addEventListener('click', async () => {
      if (!currentBlob) return;
      try {
        await navigator.clipboard.write([new ClipboardItem({ 'image/png': currentBlob })]);
        showToast('Image binary copied to clipboard!');
      } catch (e) {
        showToast('Clipboard image binary copy not supported in this browser. Use the Download PNG button.');
      }
    });

    copyTextOnlyBtn.addEventListener('click', async () => {
      const fullVal = captionArea.value;
      // Strip words starting with # to copy text body & full URL only
      const cleanText = fullVal.split(/\s+/).filter(w => !w.startsWith('#')).join(' ').trim();
      try {
        await navigator.clipboard.writeText(cleanText);
        showToast('Text body & URL only copied to clipboard (hashtags excluded)!');
      } catch (e) {
        showToast('Failed to copy text.');
      }
    });

    copyTextBtn.addEventListener('click', async () => {
      let fullVal = captionArea.value.trim();
      
      // Only append hashtags if the active platform supports hashtags
      if (!NO_HASHTAG_PLATFORMS.includes(activePlatformId)) {
        const pillsContainer = document.getElementById('socialHashtagPills');
        const tags = Array.from(pillsContainer.querySelectorAll('.social-hashtag-pill')).map(p => p.innerText.trim()).filter(t => t.length > 0);

        tags.forEach(tag => {
          if (!fullVal.includes(tag)) {
            fullVal += ' ' + tag;
          }
        });
      }

      try {
        await navigator.clipboard.writeText(fullVal.trim());
        showToast(NO_HASHTAG_PLATFORMS.includes(activePlatformId) ? 'Caption text copied (Hashtags excluded for this platform)!' : 'Full caption (Text + Hashtags) copied to clipboard!');
      } catch (e) {
        showToast('Failed to copy full caption.');
      }
    });

    copyTagsBtn.addEventListener('click', async () => {
      if (NO_HASHTAG_PLATFORMS.includes(activePlatformId)) {
        showToast('Hashtags are not recommended for this platform.');
        return;
      }
      const pillsContainer = document.getElementById('socialHashtagPills');
      const tags = Array.from(pillsContainer.querySelectorAll('.social-hashtag-pill')).map(p => p.innerText.trim()).join(' ');
      try {
        await navigator.clipboard.writeText(tags);
        showToast('Tailored hashtags copied to clipboard!');
      } catch (e) {
        showToast('Failed to copy hashtags.');
      }
    });

    captionArea.addEventListener('input', () => {
      updateCharCounter();
      
      const lines = captionArea.value.split('\n').map(l => l.trim()).filter(l => l.length > 0);
      if (lines.length > 0) {
        currentMetadata.customTitle = lines[0];
        currentMetadata.customDescription = lines.slice(1).join(' ');
      }

      clearTimeout(captionDebounceTimer);
      captionDebounceTimer = setTimeout(async () => {
        await refreshCanvasPreview();
      }, 300);
    });

    primaryBtn.addEventListener('click', async () => {
      const platforms = getPlatformSuitability(currentMetadata);
      const selected = platforms.find(p => p.id === activePlatformId) || platforms[0];
      if (selected) {
        await handlePlatformAction(selected);
      }
    });
  }

  function updateCharCounter() {
    const area = document.getElementById('socialCaptionText');
    const counter = document.getElementById('socialCharCounter');
    const len = area.value.length;
    const maxLen = activePlatformId === 'twitter-tweet' ? 280 : (activePlatformId === 'bluesky-post' ? 300 : 500);

    counter.innerText = `${len} / ${maxLen}`;
    counter.className = 'social-char-counter';
    if (len > maxLen) counter.classList.add('danger');
    else if (len > maxLen - 40) counter.classList.add('warning');
  }

  async function openModalForUrl(targetUrl = window.location.href, pageItemData = null) {
    mountModalUI();

    currentMetadata = extractPageMetadata(document, targetUrl, pageItemData);

    const badge = document.getElementById('socialRecBadge');
    badge.innerText = currentMetadata.badgeTitle;

    const captionArea = document.getElementById('socialCaptionText');
    captionArea.value = currentMetadata.ldCaption;

    renderPlatformSelectorBar(currentMetadata);

    const platforms = getPlatformSuitability(currentMetadata);
    const defaultPlatform = platforms[0];
    if (defaultPlatform) {
      await selectPlatform(defaultPlatform.id);
    }

    const modal = document.getElementById('cactsSocialModal');
    modal.classList.add('active');
  }

  function renderPlatformSelectorBar(meta) {
    const bar = document.getElementById('socialPlatformsBar');
    const platforms = getPlatformSuitability(meta);

    bar.innerHTML = platforms.map(p => `
      <div class="social-platform-pill ${p.id === activePlatformId ? 'selected' : ''}" data-id="${p.id}">
        <div class="social-pill-icon" style="background: ${p.color}; color: #ffffff;">${p.icon}</div>
        <div class="social-pill-details">
          <div class="social-pill-name">
            ${p.name}
            ${p.recommended ? '<span class="social-rec-dot" title="Recommended for this page"></span>' : ''}
          </div>
          <div class="social-pill-format">${p.formatTag}</div>
        </div>
      </div>
    `).join('');

    bar.querySelectorAll('.social-platform-pill').forEach(pill => {
      pill.addEventListener('click', async e => {
        const platformId = e.currentTarget.dataset.id;
        await selectPlatform(platformId);
      });
    });
  }

  async function selectPlatform(platformId) {
    const platforms = getPlatformSuitability(currentMetadata);
    const platform = platforms.find(p => p.id === platformId) || platforms[0];
    if (!platform) return;

    activePlatformId = platform.id;

    document.querySelectorAll('.social-platform-pill').forEach(pill => {
      if (pill.dataset.id === activePlatformId) pill.classList.add('selected');
      else pill.classList.remove('selected');
    });

    const targetFormat = PLATFORM_FORMATS[activePlatformId] || '1200x630';
    activeFormat = targetFormat;

    document.querySelectorAll('.social-format-tab').forEach(tab => {
      if (tab.dataset.format === activeFormat) tab.classList.add('active');
      else tab.classList.remove('active');
    });

    renderTailoredHashtags(activePlatformId, currentMetadata ? currentMetadata.presetKey : 'guide');

    const primaryBtn = document.getElementById('socialPrimaryActionBtn');
    if (primaryBtn && platform) {
      primaryBtn.innerText = platform.actionLabel;
    }

    updateCharCounter();
    await refreshCanvasPreview();
  }

  function getDynamicContentHashtags(meta) {
    if (!meta) return [];
    const text = ((meta.title || '') + ' ' + (meta.customTitle || '') + ' ' + (meta.description || '') + ' ' + (meta.url || '')).toLowerCase();
    const dynamicTags = [];

    if (text.includes('full stack') || text.includes('fullstack')) dynamicTags.push('#FullStackDeveloper');
    if (text.includes('java')) dynamicTags.push('#JavaDeveloper');
    if (text.includes('python')) dynamicTags.push('#PythonDeveloper');
    if (text.includes('ai') || text.includes('machine learning') || text.includes('artificial intelligence')) dynamicTags.push('#ArtificialIntelligence');
    if (text.includes('data science') || text.includes('analytics')) dynamicTags.push('#DataScience');
    if (text.includes('devops') || text.includes('ci/cd') || text.includes('cloud') || text.includes('aws')) dynamicTags.push('#DevOps');
    if (text.includes('testing') || text.includes('selenium') || text.includes('qa')) dynamicTags.push('#SoftwareTesting');
    if (text.includes('react')) dynamicTags.push('#ReactJS');
    if (text.includes('cybersecurity') || text.includes('security') || text.includes('soc')) dynamicTags.push('#Cybersecurity');
    if (text.includes('power bi') || text.includes('visualization')) dynamicTags.push('#PowerBI');
    if (text.includes('architect')) dynamicTags.push('#SoftwareArchitecture');

    return dynamicTags;
  }

  function renderTailoredHashtags(platformId, presetKey) {
    const pillsContainer = document.getElementById('socialHashtagPills');
    const titleElem = document.getElementById('socialHashtagTitle');
    const copyTagsBtn = document.getElementById('socialCopyTagsBtn');

    // If platform does NOT support hashtags, display explicit notice and disable hashtag pills
    if (NO_HASHTAG_PLATFORMS.includes(platformId)) {
      if (titleElem) titleElem.innerText = 'Platform Hashtag Status:';
      if (pillsContainer) {
        pillsContainer.innerHTML = '<span style="font-size: 0.82rem; color: #94a3b8; font-style: italic;">Hashtags are excluded for this platform (Not supported or clutter-inducing on WhatsApp, Google Business &amp; Reddit).</span>';
      }
      if (copyTagsBtn) copyTagsBtn.style.opacity = '0.4';
      return;
    }

    if (titleElem) titleElem.innerText = 'Content & Target-Audience Hashtags (Click to insert):';
    if (copyTagsBtn) copyTagsBtn.style.opacity = '1';

    const topicTags = TOPIC_HASHTAGS[presetKey] || TOPIC_HASHTAGS['guide'];
    const dynamicTags = getDynamicContentHashtags(currentMetadata);
    
    const combined = Array.from(new Set([...topicTags, ...dynamicTags]));
    const captionArea = document.getElementById('socialCaptionText');

    pillsContainer.innerHTML = combined.map(h => `<button class="social-hashtag-pill">${h}</button>`).join('');

    pillsContainer.querySelectorAll('.social-hashtag-pill').forEach(pill => {
      pill.addEventListener('click', () => {
        if (!captionArea.value.includes(pill.innerText)) {
          captionArea.value = captionArea.value.trim() + ' ' + pill.innerText;
          updateCharCounter();
        }
      });
    });
  }

  async function refreshCanvasPreview() {
    if (currentObjectUrl) {
      URL.revokeObjectURL(currentObjectUrl);
    }
    currentBlob = await renderBrandedCanvas(currentMetadata, activeFormat);
    currentObjectUrl = URL.createObjectURL(currentBlob);

    const imgElem = document.getElementById('socialCanvasImg');
    if (imgElem) {
      imgElem.src = currentObjectUrl;
    }
  }

  async function handlePlatformAction(platform) {
    const action = platform.actionType;

    // Get guaranteed full caption (append hashtags ONLY if supported by platform)
    let captionText = document.getElementById('socialCaptionText').value.trim();
    if (!NO_HASHTAG_PLATFORMS.includes(platform.id)) {
      const pillsContainer = document.getElementById('socialHashtagPills');
      if (pillsContainer) {
        const tags = Array.from(pillsContainer.querySelectorAll('.social-hashtag-pill')).map(p => p.innerText.trim()).filter(t => t.length > 0);
        tags.forEach(tag => {
          if (!captionText.includes(tag)) {
            captionText += ' ' + tag;
          }
        });
      }
    }

    // Step 1: Copy Caption Text to Device Clipboard
    let textCopied = false;
    try {
      await navigator.clipboard.writeText(captionText);
      textCopied = true;
    } catch (e) {}

    // Step 2: Copy Image Binary to Clipboard (if supported by browser)
    let imgCopied = false;
    if (currentBlob && navigator.clipboard && navigator.clipboard.write) {
      try {
        await navigator.clipboard.write([new ClipboardItem({ 'image/png': currentBlob })]);
        imgCopied = true;
      } catch (e) {}
    }

    // Step 3: Platform Execution (NO automatic file downloads!)
    if (action === 'native-share') {
      if (navigator.share && currentBlob) {
        try {
          const file = new File([currentBlob], 'cacts-share.png', { type: 'image/png' });
          if (navigator.canShare && navigator.canShare({ files: [file] })) {
            showToast('Caption copied to clipboard! Long-press -> Paste in your target app.', 5000);
            await navigator.share({
              title: currentMetadata.title,
              text: captionText,
              files: [file]
            });
            recordShareHistory(currentMetadata.url);
          } else {
            await navigator.share({
              title: currentMetadata.title,
              text: captionText,
              url: currentMetadata.url
            });
            recordShareHistory(currentMetadata.url);
          }
        } catch (e) {
          showToast('Share sheet cancelled or unsupported.');
        }
      }
    } else {
      // Standard Intent / Social Composer Window Execution
      if (platform.intentUrl) {
        window.open(platform.intentUrl, '_blank');
      }
      recordShareHistory(currentMetadata.url);

      if (textCopied && imgCopied) {
        showToast(`Caption & Image copied to clipboard! Ready to paste (Ctrl+V) on ${platform.name}.`);
      } else if (textCopied) {
        showToast(`Caption copied to clipboard! Opening ${platform.name}...`);
      } else {
        showToast(`Opened ${platform.name} share composer!`);
      }
    }
  }

  function copyCaptionToClipboard() {
    const text = document.getElementById('socialCaptionText').value;
    navigator.clipboard.writeText(text).then(() => {
      showToast('Caption text copied to clipboard!');
    }).catch(() => {
      showToast('Failed to copy text.');
    });
  }

  function recordShareHistory(url) {
    try {
      const history = JSON.parse(localStorage.getItem('cacts_share_history') || '[]');
      if (!history.includes(url)) {
        history.push(url);
        localStorage.setItem('cacts_share_history', JSON.stringify(history));
      }
    } catch (e) {}
  }

  function closeModal() {
    const modal = document.getElementById('cactsSocialModal');
    if (modal) modal.classList.remove('active');
    if (currentObjectUrl) {
      URL.revokeObjectURL(currentObjectUrl);
      currentObjectUrl = null;
    }
  }

  function showToast(msg, duration = 4000) {
    let toast = document.getElementById('cactsSocialToast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'cactsSocialToast';
      toast.className = 'social-toast';
      document.body.appendChild(toast);
    }
    toast.innerText = msg;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), duration);
  }

  return {
    openModalForUrl: openModalForUrl,
    extractPageMetadata: extractPageMetadata,
    renderBrandedCanvas: renderBrandedCanvas,
    ensureFullAbsoluteUrl: ensureFullAbsoluteUrl
  };

})();
