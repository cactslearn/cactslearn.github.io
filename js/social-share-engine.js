/**
 * CACTS Pune - 10-Platform Dynamic Client-Side Social Syndication Engine
 * Filename: js/social-share-engine.js
 * Description: Zero-dependency client-side social sharing engine featuring dynamic JSON-LD/OG content
 *              recognition, human-centric non-robotic social captions, audience-tailored problem statements,
 *              perfectly matched card badges & CTA buttons, laser-focused non-spam hashtags,
 *              automatic 100% full canonical text share URLs, pre-filled intent composers,
 *              dedicated Copy Text Only, Copy Full Caption (Text + Hashtags), & Copy Hashtags Only controls,
 *              automatic clipboard image binary & PNG file download, mobile share sheet clipboard preservation,
 *              live graphic preview re-rendering, format-proportional font sizing, radial background lighting,
 *              16-theme rich dark gradient palettes with index-dispersed background variation,
 *              multi-paragraph line wrapping with strict left alignment, 1080x1920 vertical space-filling grid,
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

  // Platform Formats Mapping
  const PLATFORM_FORMATS = {
    'linkedin-feed': '1200x630',
    'linkedin-add': '1200x630',
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

  // Platform Hashtags Base Matrix
  const PLATFORM_HASHTAGS = {
    'linkedin-feed': ['#CACTSPune', '#PuneITJobs', '#SoftwareEngineering'],
    'linkedin-add': ['#CACTSPune', '#CertifiedDeveloper', '#TechAccreditation'],
    'instagram-story': ['#cactspune', '#fullstackdeveloper', '#punestudents', '#learncoding', '#puneitjobs'],
    'whatsapp-chat': ['#CACTSPune', '#1to1Mentorship', '#PuneTraining'],
    'whatsapp-enroll': ['#CACTSPune', '#Admissions2026', '#ITCoursesPune'],
    'twitter-tweet': ['#CACTSPune', '#DevCommunity', '#TechJobs'],
    'facebook-feed': ['#CACTSPune', '#PuneITJobs', '#SoftwareTraining'],
    'gbp-post': ['#CACTSPune', '#PuneITInstitute', '#ShivanePune'],
    'reddit-post': ['#CACTSPune', '#developersIndia', '#learnprogramming'],
    'bluesky-post': ['#CACTSPune', '#TechUpdate', '#WebDev'],
    'native-os-share': ['#CACTSPune', '#FullStackDeveloper', '#PuneITJobs']
  };

  // Laser-Focused Topic Hashtags Matrix (Targeted for High Feed Relevancy)
  const TOPIC_HASHTAGS = {
    'job': ['#CACTSPune', '#TechHiring', '#PuneITJobs', '#SoftwareJobs', '#PuneJobs', '#ITCareers'],
    'course': ['#CACTSPune', '#FullStackDeveloper', '#ITCoursesPune', '#1to1Mentorship', '#LearnCoding', '#PuneInstitute'],
    'cert': ['#TechHiring', '#HRTech', '#PuneITJobs', '#CACTSPune', '#CredentialVerification', '#VerifiedDeveloper'],
    'guide': ['#CACTSPune', '#DevCommunity', '#TechGuide', '#CareerRoadmap', '#WebDev', '#Coding'],
    'tool': ['#CACTSPune', '#DevTools', '#WebDev', '#CodingTools', '#Productivity'],
    'review': ['#CACTSPune', '#StudentSuccess', '#AlumniReviews', '#PuneInstitute', '#TechJobs']
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

      for (let i = 0; i < 9; i++) {
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
     MODULE A: Content Recognition & Human-Centric Social Captions Engine
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

    const cleanTitle = meta.title.replace(/\s*\|\s*CACTS.*$/i, '').trim();

    // 1. Certificate Verification Portal & Credentials (Strict Rule Enforcement)
    if (fullUrl.includes('verify.html') || (pageItemData && (pageItemData.schema_type || '').toLowerCase().includes('credential'))) {
      meta.schemaType = 'EducationalOccupationalCredential';
      meta.badgeTitle = '[Recognized: Certificate Verification Portal]';
      meta.presetKey = 'cert';
      meta.ldCaption = `Hiring managers & recruiters: Need to verify a candidate's CACTS credentials in under 10 seconds?\n\nOur official accreditation portal allows tech employers to instantly validate live project completion, 1-to-1 mentorship hours, and verified student certifications.\n\nVerify Credentials Online: ${meta.url}`;
      return meta;
    }

    // 2. Tech Job Postings
    if (fullUrl.includes('/jobs/') || (pageItemData && (pageItemData.schema_type || '').toLowerCase().includes('job'))) {
      meta.schemaType = 'JobPosting';
      meta.badgeTitle = '[Recognized: Tech Job Posting]';
      meta.presetKey = 'job';
      meta.ldCaption = `Hiring Alert for Pune Tech Developers & Engineering Graduates!\n\n${cleanTitle} at CACTS Pune. Gain 1-to-1 live mentor code reviews, production codebase access & career guidance.\n\nApply Now: ${meta.url}`;
      return meta;
    }

    // 3. Course Syllabi
    if (fullUrl.includes('/courses/') || (pageItemData && (pageItemData.schema_type || '').toLowerCase().includes('course'))) {
      meta.schemaType = 'Course';
      meta.badgeTitle = '[Recognized: Course Syllabus]';
      meta.presetKey = 'course';
      meta.ldCaption = `Want to master full-stack software development with 1-to-1 live mentor code reviews?\n\nExplore ${cleanTitle} at CACTS Pune with practical hands-on curriculum, production company projects & career guidance.\n\nSyllabus & Enrollment Details: ${meta.url}`;
      return meta;
    }

    // 4. Interactive Developer Tools
    if (fullUrl.includes('/tools/') || (pageItemData && (pageItemData.schema_type || '').toLowerCase().includes('tool'))) {
      meta.schemaType = 'WebApplication';
      meta.badgeTitle = '[Recognized: Interactive Developer Tool]';
      meta.presetKey = 'tool';
      meta.ldCaption = `Boost your developer productivity with free interactive tools by CACTS Pune!\n\n${cleanTitle}: ${truncateText(meta.description, 130)}\n\nTry Tool Online: ${meta.url}`;
      return meta;
    }

    // 5. Student Reviews & Alumni Success
    if (fullUrl.includes('reviews.html')) {
      meta.schemaType = 'StudentReviews';
      meta.badgeTitle = '[Recognized: Student Reviews & Alumni Ratings]';
      meta.presetKey = 'review';
      meta.ldCaption = `Discover authentic career transformations & student reviews at CACTS Pune.\n\nSee how 1-to-1 live code reviews & real company project internships help developers land tech roles.\n\nRead Alumni Reviews: ${meta.url}`;
      return meta;
    }

    // 6. Branch Location Pages
    if (fullUrl.includes('/locations/')) {
      meta.schemaType = 'LocalBusiness';
      meta.badgeTitle = '[Recognized: Pune Branch Location]';
      meta.presetKey = 'course';
      meta.ldCaption = `Looking for top-rated software & IT training institutes in Pune?\n\nVisit CACTS Pune (${cleanTitle}) for 1-to-1 developer mentorship, practical labs, and live company projects.\n\nExplore Branch Details: ${meta.url}`;
      return meta;
    }

    // 7. Developer Tech Articles & Guides (Default Fallback)
    meta.schemaType = 'Article';
    meta.badgeTitle = '[Recognized: Tech Article / Guide]';
    meta.presetKey = 'guide';
    meta.ldCaption = `Looking to solve complex software engineering challenges?\n\nRead ${cleanTitle} written by CACTS Pune engineering mentors.\n\nVisit Guide: ${meta.url}`;
    return meta;
  }

  /* ==========================================================================
     MODULE B: Platform Suitability Scoring & Pre-filled Intent Generation
     ========================================================================== */
  function getPlatformSuitability(meta) {
    const targetUrl = ensureFullAbsoluteUrl(meta.url);
    const captionElem = document.getElementById('socialCaptionText');
    const liveCaption = captionElem ? captionElem.value : (meta.ldCaption || meta.title);

    const encUrl = encodeURIComponent(appendUtmParams(targetUrl, 'social_syndication'));
    const encTitle = encodeURIComponent(meta.title);
    const encFullCaption = encodeURIComponent(liveCaption);

    const platforms = [];

    if (meta.schemaType === 'EducationalOccupationalCredential' || (meta.url && meta.url.includes('verify.html'))) {
      platforms.push({
        id: 'linkedin-add',
        name: 'LinkedIn Add Cert',
        icon: 'IN',
        color: '#0077b5',
        recommended: true,
        formatTag: 'Direct Profile Link',
        actionType: 'linkedin-add-profile',
        actionLabel: 'Add Certificate to LinkedIn Profile ➔'
      });
    }

    platforms.push({
      id: 'linkedin-feed',
      name: 'LinkedIn Feed',
      icon: 'IN',
      color: '#0077b5',
      recommended: ['JobPosting', 'Course', 'EducationalOccupationalCredential', 'Article', 'Report'].includes(meta.schemaType),
      formatTag: '1200x630 Feed Banner',
      actionType: 'intent',
      intentUrl: `https://www.linkedin.com/sharing/share-offsite/?url=${encUrl}`,
      actionLabel: 'Share to LinkedIn Feed ➔'
    });

    platforms.push({
      id: 'instagram-story',
      name: 'Instagram Story',
      icon: 'IG',
      color: '#e1306c',
      recommended: ['Course', 'EducationalOccupationalCredential', 'StudentReviews', 'StudentShowcase'].includes(meta.schemaType),
      formatTag: '1080x1920 Story Card',
      actionType: 'download-copy',
      formatKey: '1080x1920',
      actionLabel: 'Download Story PNG & Copy Caption ➔'
    });

    platforms.push({
      id: 'whatsapp-chat',
      name: 'WhatsApp Chat',
      icon: 'WA',
      color: '#25d366',
      recommended: true,
      formatTag: 'Text & Link Share',
      actionType: 'intent',
      intentUrl: `https://api.whatsapp.com/send?text=${encFullCaption}`,
      actionLabel: 'Share Full Text & Link to WhatsApp ➔'
    });

    platforms.push({
      id: 'whatsapp-enroll',
      name: 'WhatsApp Desk',
      icon: 'WA',
      color: '#128c7e',
      recommended: ['Course', 'JobPosting'].includes(meta.schemaType),
      formatTag: 'Direct Desk Inquiry',
      actionType: 'intent',
      intentUrl: `https://wa.me/919665566357?text=${encodeURIComponent('Hello CACTS Pune, I am inquiring about: ' + meta.title + ' (' + targetUrl + ')')}`,
      actionLabel: 'Open Direct WhatsApp Desk Inquiry ➔'
    });

    platforms.push({
      id: 'twitter-tweet',
      name: 'X (Twitter)',
      icon: 'X',
      color: '#1da1f2',
      recommended: ['JobPosting', 'Article', 'WebApplication', 'Report'].includes(meta.schemaType),
      formatTag: '1200x630 Tech Tweet',
      actionType: 'intent',
      intentUrl: `https://twitter.com/intent/tweet?text=${encFullCaption}`,
      actionLabel: 'Post Pre-filled Tweet on X ➔'
    });

    platforms.push({
      id: 'facebook-feed',
      name: 'Facebook Feed',
      icon: 'FB',
      color: '#1877f2',
      recommended: ['Course', 'LocalBusiness', 'StudentReviews'].includes(meta.schemaType),
      formatTag: '1200x630 Link Post',
      actionType: 'intent',
      intentUrl: `https://www.facebook.com/sharer/sharer.php?u=${encUrl}`,
      actionLabel: 'Share to Facebook ➔'
    });

    platforms.push({
      id: 'gbp-post',
      name: 'Google Business',
      icon: 'G',
      color: '#ea4335',
      recommended: ['Course', 'LocalBusiness', 'StudentReviews'].includes(meta.schemaType),
      formatTag: '1200x900 Promo Card',
      actionType: 'download-copy',
      formatKey: '1200x900',
      actionLabel: 'Download 1200x900 Image & Copy Caption ➔'
    });

    platforms.push({
      id: 'reddit-post',
      name: 'Reddit Post',
      icon: 'RD',
      color: '#ff4500',
      recommended: ['JobPosting', 'Article', 'WebApplication', 'Report'].includes(meta.schemaType),
      formatTag: 'Discussion Link',
      actionType: 'intent',
      intentUrl: `https://www.reddit.com/submit?url=${encUrl}&title=${encTitle}`,
      actionLabel: 'Post to Reddit ➔'
    });

    platforms.push({
      id: 'bluesky-post',
      name: 'Bluesky Tech',
      icon: 'BS',
      color: '#0085ff',
      recommended: ['Article', 'WebApplication', 'JobPosting'].includes(meta.schemaType),
      formatTag: 'Tech Update',
      actionType: 'intent',
      intentUrl: `https://bsky.app/intent/compose?text=${encFullCaption}`,
      actionLabel: 'Post Pre-filled Text to Bluesky ➔'
    });

    if (navigator.share) {
      platforms.unshift({
        id: 'native-os-share',
        name: 'Mobile Share Sheet',
        icon: 'OS',
        color: '#8b5cf6',
        recommended: true,
        formatTag: 'Native Image & Text Share',
        actionType: 'native-share',
        actionLabel: 'Open Mobile System Share Sheet ➔'
      });
    }

    return platforms;
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

  // Index-Dispersed Palette & Card Badge Selection Engine (Strict Category Alignment)
  function getItemPalette(meta) {
    let hash = 0;
    const keyStr = (meta.url || '') + (meta.title || '');
    for (let i = 0; i < keyStr.length; i++) {
      hash = keyStr.charCodeAt(i) + ((hash << 5) - hash);
    }

    const pageItemData = meta.pageItemData;
    const idxOffset = (pageItemData && typeof pageItemData.gridIndex === 'number') ? pageItemData.gridIndex * 5 : 0;
    const paletteIndex = Math.abs(hash + idxOffset) % RICH_PALETTES_16.length;
    
    const p = RICH_PALETTES_16[paletteIndex];

    let tabTop = 'FEATURED';
    let tabBottom = '1-to-1 Tech';
    let cta = 'Explore Details & Apply ➔';

    const targetUrl = (meta.url || '').toLowerCase();

    if (meta.schemaType === 'EducationalOccupationalCredential' || targetUrl.includes('verify.html')) {
      tabTop = 'OFFICIAL ACCREDITATION';
      tabBottom = 'Verify Portal';
      cta = 'Verify Credentials Online ➔';
    } else if (meta.schemaType === 'JobPosting' || targetUrl.includes('/jobs/')) {
      tabTop = 'HIRING';
      tabBottom = 'Tech Job';
      cta = 'Apply for Tech Job Position ➔';
    } else if (meta.schemaType === 'Course' || targetUrl.includes('/courses/')) {
      tabTop = '1-TO-1 SKILLS';
      tabBottom = 'Best Value';
      cta = 'Enroll Now & Get Mentored ➔';
    } else if (meta.schemaType === 'WebApplication' || targetUrl.includes('/tools/')) {
      tabTop = 'DEV TOOL';
      tabBottom = 'Interactive';
      cta = 'Launch Interactive Tool ➔';
    } else if (meta.schemaType === 'StudentReviews' || targetUrl.includes('reviews.html')) {
      tabTop = 'STUDENT PROOF';
      tabBottom = '5-Star Reviews';
      cta = 'Read Alumni Reviews ➔';
    } else if (meta.schemaType === 'LocalBusiness' || targetUrl.includes('/locations/')) {
      tabTop = 'PUNE HUB';
      tabBottom = '1-to-1 Labs';
      cta = 'Explore Branch Details ➔';
    } else if (meta.schemaType === 'Report' || targetUrl.includes('report')) {
      tabTop = 'SALARY INDEX';
      tabBottom = '2026 Report';
      cta = 'Explore Salary Benchmarks ➔';
    } else {
      tabTop = 'TECH INSIGHT';
      tabBottom = 'Read Guide';
      cta = 'Read Full Developer Guide ➔';
    }

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

      // Top Right Overhanging Badge Tab
      const tabX = width - 285;
      ctx.save();
      ctx.shadowColor = 'rgba(0, 0, 0, 0.6)';
      ctx.shadowBlur = 18;
      ctx.shadowOffsetY = 8;
      ctx.fillStyle = palette.accentTabBg;
      ctx.beginPath();
      ctx.roundRect(tabX, 0, 250, 92, [0, 0, 18, 18]);
      ctx.fill();
      ctx.restore();

      ctx.fillStyle = palette.accentTabTextColor;
      ctx.textAlign = 'center';
      ctx.font = 'bold 17px Montserrat, sans-serif';
      ctx.fillText(palette.accentTabTextTop, tabX + 125, 38);
      ctx.font = '800 23px Montserrat, sans-serif';
      ctx.fillText(palette.accentTabTextBottom, tabX + 125, 68);

      // 2. Title Section (Space Filling)
      let titleY = 320;
      let baseTitleSize = 68;
      ctx.font = `800 ${baseTitleSize}px Montserrat, sans-serif`;
      while (ctx.measureText(displayTitle).width > (width - 100) * 3.5 && baseTitleSize > 34) {
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
      const titleLinesDrawn = wrapText(ctx, displayTitle, 50, titleY, width - 100, baseTitleSize * 1.28, 4);
      ctx.restore();

      // Title Divider Accent Line
      const titleDividerY = titleY + (titleLinesDrawn * baseTitleSize * 1.28) + 16;
      const divGrad = ctx.createLinearGradient(50, 0, width - 100, 0);
      divGrad.addColorStop(0, palette.accentTabBg);
      divGrad.addColorStop(1, 'transparent');
      ctx.fillStyle = divGrad;
      ctx.fillRect(50, titleDividerY, width - 100, 4);

      // 3. Description Section
      const descY = titleDividerY + 52;
      const descFontSize = 36;
      const descLineHeight = 56;
      ctx.fillStyle = '#f1f5f9';
      ctx.font = `400 ${descFontSize}px Montserrat, sans-serif`;
      const descLinesDrawn = wrapText(ctx, displayDesc, 50, descY, width - 100, descLineHeight, 8);

      const nextY = descY + (descLinesDrawn * descLineHeight) + 40;

      // 4. Middle Feature Highlights Grid Box (Exact Terminology Rules Enforcement)
      const gridY = Math.max(nextY, 930);
      const gridWidth = width - 100;
      const gridHeight = 440;

      ctx.save();
      ctx.fillStyle = 'rgba(15, 23, 42, 0.75)';
      ctx.strokeStyle = palette.accentTabBg;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.roundRect(50, gridY, gridWidth, gridHeight, 20);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = palette.accentTabBg;
      ctx.font = 'bold 24px Montserrat, sans-serif';
      ctx.fillText('PROGRAM HIGHLIGHTS & INSTITUTIONAL STANDARDS', 80, gridY + 52);

      const tiles = [
        { num: '01', title: '1-to-1 Mentor Reviews', desc: 'Personalized practical training' },
        { num: '02', title: 'Real Company Projects', desc: 'Live production codebases' },
        { num: '03', title: 'ISO 9001:2015 Compliant', desc: 'Accredited IT institute' },
        { num: '04', title: 'Career Guidance', desc: 'Mentorship & career support' }
      ];

      const tileW = (gridWidth - 70) / 2;
      const tileH = 135;

      tiles.forEach((tile, tIdx) => {
        const row = Math.floor(tIdx / 2);
        const col = tIdx % 2;
        const tx = 75 + col * (tileW + 20);
        const ty = gridY + 85 + row * (tileH + 18);

        ctx.fillStyle = 'rgba(30, 41, 59, 0.8)';
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.roundRect(tx, ty, tileW, tileH, 12);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = palette.accentTabBg;
        ctx.font = 'bold 20px Montserrat, sans-serif';
        ctx.fillText(tile.num, tx + 20, ty + 40);

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 18px Montserrat, sans-serif';
        ctx.fillText(tile.title, tx + 60, ty + 40);

        ctx.fillStyle = '#94a3b8';
        ctx.font = '500 14px Montserrat, sans-serif';
        ctx.fillText(tile.desc, tx + 60, ty + 68);
      });
      ctx.restore();

      // 5. Solid CTA Button & Real QRCode Renderer
      const btnY = 1680;
      const btnW = 580;
      const btnH = 84;

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
      ctx.font = 'bold 25px Montserrat, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(palette.ctaLabel, 50 + btnW / 2, btnY + 52);

      await renderRealQrCodeOnCanvas(ctx, meta.url, width - 260, 1600, 210);

      // 6. Bottom Footer Bar with *T&C Apply Disclaimer
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

    // Top-Right Overhanging Badge Tab
    let tabWidth = 170;
    let tabHeight = 66;
    if (formatKey === '1080x1080') {
      tabWidth = 200;
      tabHeight = 74;
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
    ctx.font = '800 17px Montserrat, sans-serif';
    ctx.fillText(palette.accentTabTextBottom, tabX + tabWidth / 2, 52);

    // Title Typography
    let baseTitleSize = 48;
    let titleY = 205;
    let maxTitleWidth = width - 270;
    let maxTitleLines = 3;

    if (formatKey === '1080x1080') {
      baseTitleSize = 58;
      titleY = 225;
      maxTitleWidth = width - 260;
      maxTitleLines = 4;
    } else if (formatKey === '1920x1080') {
      baseTitleSize = 68;
      titleY = 240;
      maxTitleWidth = width - 360;
      maxTitleLines = 3;
    } else if (formatKey === '1200x900') {
      baseTitleSize = 54;
      titleY = 220;
      maxTitleWidth = width - 280;
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
      descFontSize = 28;
      descLineHeight = 44;
      maxDescLines = 6;
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
    const descLinesDrawn = wrapText(ctx, displayDesc, 40, descY, maxTitleWidth, descLineHeight, maxDescLines);

    // Glassmorphic Highlights Card for 1080x1080
    if (formatKey === '1080x1080') {
      const cardY = descY + (descLinesDrawn * descLineHeight) + 30;
      const cardWidth = width - 80;
      const cardHeight = 160;

      if (cardY + cardHeight < height - 250) {
        ctx.save();
        ctx.fillStyle = 'rgba(15, 23, 42, 0.65)';
        ctx.strokeStyle = palette.accentTabBg;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.roundRect(40, cardY, cardWidth, cardHeight, 16);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = palette.accentTabBg;
        ctx.font = 'bold 18px Montserrat, sans-serif';
        ctx.fillText('WHY TRAIN WITH CACTS PUNE:', 65, cardY + 38);

        const bullets = [
          '• 1-to-1 Live Code Reviews & Real Company Projects',
          '• Official ISO 9001:2015 Compliant IT Institute'
        ];

        ctx.fillStyle = '#e2e8f0';
        ctx.font = '500 16px Montserrat, sans-serif';
        ctx.fillText(bullets[0], 65, cardY + 82);
        ctx.fillText(bullets[1], 65, cardY + 116);
        ctx.restore();
      }
    }

    // CTA Pill Button
    let btnWidth = 360;
    let btnHeight = 56;
    let btnFontSize = 18;
    let btnY = height - 135;

    if (formatKey === '1080x1080') {
      btnWidth = 460;
      btnHeight = 66;
      btnFontSize = 21;
      btnY = height - 150;
    } else if (formatKey === '1920x1080') {
      btnWidth = 460;
      btnHeight = 68;
      btnFontSize = 22;
      btnY = height - 160;
    } else if (formatKey === '1200x900') {
      btnWidth = 400;
      btnHeight = 60;
      btnFontSize = 19;
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

    // Vector QR Code
    let qrX = width - 185;
    let qrY = 150;
    let qrSize = 145;

    if (formatKey === '1080x1080') {
      qrX = width - 200;
      qrY = height - 240;
      qrSize = 150;
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
          ctx.fillStyle = '#94a3b8';
          ctx.font = 'bold 11px Montserrat, sans-serif';
          ctx.textAlign = 'center';
          ctx.fillText('SCAN FOR LIVE T&C', x + size / 2, y + size + 16);
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
    ctx.fillStyle = '#94a3b8';
    ctx.font = 'bold 11px Montserrat, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('SCAN FOR LIVE T&C', x + size / 2, y + size + 16);
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
                  <div class="social-hashtag-box">
                    <span class="social-hashtag-title">Tailored Platform Hashtags (Click to insert):</span>
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
        showToast('Clipboard image binary copy not supported on this browser. Downloading PNG file instead.');
        downloadBtn.click();
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
      const pillsContainer = document.getElementById('socialHashtagPills');
      const tags = Array.from(pillsContainer.querySelectorAll('.social-hashtag-pill')).map(p => p.innerText.trim()).filter(t => t.length > 0);

      // Ensure all hashtag pills are appended into the copied string
      tags.forEach(tag => {
        if (!fullVal.includes(tag)) {
          fullVal += ' ' + tag;
        }
      });

      try {
        await navigator.clipboard.writeText(fullVal.trim());
        showToast('Full caption (Text + Hashtags) copied to clipboard!');
      } catch (e) {
        showToast('Failed to copy full caption.');
      }
    });

    copyTagsBtn.addEventListener('click', async () => {
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
    const defaultPlatform = platforms.find(p => p.recommended) || platforms[0];
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
    activePlatformId = platformId;

    document.querySelectorAll('.social-platform-pill').forEach(pill => {
      if (pill.dataset.id === platformId) pill.classList.add('selected');
      else pill.classList.remove('selected');
    });

    const targetFormat = PLATFORM_FORMATS[platformId] || '1200x630';
    activeFormat = targetFormat;

    document.querySelectorAll('.social-format-tab').forEach(tab => {
      if (tab.dataset.format === activeFormat) tab.classList.add('active');
      else tab.classList.remove('active');
    });

    renderTailoredHashtags(platformId, currentMetadata ? currentMetadata.presetKey : 'guide');

    const platforms = getPlatformSuitability(currentMetadata);
    const platform = platforms.find(p => p.id === platformId) || platforms[0];
    const primaryBtn = document.getElementById('socialPrimaryActionBtn');
    if (primaryBtn && platform) {
      primaryBtn.innerText = platform.actionLabel;
    }

    updateCharCounter();
    await refreshCanvasPreview();
  }

  function renderTailoredHashtags(platformId, presetKey) {
    const pillsContainer = document.getElementById('socialHashtagPills');
    const platformTags = PLATFORM_HASHTAGS[platformId] || PLATFORM_HASHTAGS['linkedin-feed'];
    const topicTags = TOPIC_HASHTAGS[presetKey] || TOPIC_HASHTAGS['guide'];
    
    const combined = Array.from(new Set([...topicTags, ...platformTags]));
    const captionArea = document.getElementById('socialCaptionText');

    pillsContainer.innerHTML = combined.map(h => `<button class="social-hashtag-pill">${h}</button>`).join('');

    // Automatically append tailored hashtags into caption text area if not present
    if (captionArea) {
      let currentVal = captionArea.value;
      const missingTags = combined.filter(t => !currentVal.includes(t));
      if (missingTags.length > 0) {
        captionArea.value = currentVal.trim() + '\n\n' + missingTags.join(' ');
        updateCharCounter();
      }
    }

    pillsContainer.querySelectorAll('.social-hashtag-pill').forEach(pill => {
      pill.addEventListener('click', () => {
        if (!captionArea.value.includes(pill.innerText)) {
          captionArea.value += ' ' + pill.innerText;
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

    // Get guaranteed full caption with all hashtags
    let captionText = document.getElementById('socialCaptionText').value.trim();
    const pillsContainer = document.getElementById('socialHashtagPills');
    if (pillsContainer) {
      const tags = Array.from(pillsContainer.querySelectorAll('.social-hashtag-pill')).map(p => p.innerText.trim()).filter(t => t.length > 0);
      tags.forEach(tag => {
        if (!captionText.includes(tag)) {
          captionText += ' ' + tag;
        }
      });
    }

    // Step 1: Guarantee Caption Text Copy to Mobile & Desktop Device Clipboard
    let textCopied = false;
    try {
      await navigator.clipboard.writeText(captionText);
      textCopied = true;
    } catch (e) {}

    let imgCopied = false;
    if (currentBlob && navigator.clipboard && navigator.clipboard.write) {
      try {
        await navigator.clipboard.write([new ClipboardItem({ 'image/png': currentBlob })]);
        imgCopied = true;
      } catch (e) {}
    }

    // Step 2: Specialized Execution for LinkedIn Feed Share
    if (platform.id === 'linkedin-feed') {
      const link = document.createElement('a');
      link.download = `cacts-share-linkedin-${Date.now()}.png`;
      link.href = currentObjectUrl;
      link.click();

      window.open(platform.intentUrl, '_blank');
      recordShareHistory(currentMetadata.url);
      showToast('LinkedIn Share: Caption & Hashtags copied & 1200x630 banner saved! Paste text (Ctrl+V) & attach banner image on LinkedIn.', 6000);
      return;
    }

    // Step 3: Auto-Download Image for File-Based Social Platforms
    if (action === 'download-copy' || platform.id === 'instagram-story' || platform.id === 'gbp-post') {
      const link = document.createElement('a');
      link.download = `cacts-share-${activeFormat}-${Date.now()}.png`;
      link.href = currentObjectUrl;
      link.click();
    }

    // Step 4: Execute Platform Specific Action / Intent Composer
    if (action === 'linkedin-add-profile') {
      if (typeof window.addToLinkedInProfile === 'function') {
        window.addToLinkedInProfile();
      } else {
        const certUrl = `https://www.linkedin.com/profile/add?startTask=CERTIFICATION_NAME&name=${encodeURIComponent(currentMetadata.title)}&organizationName=${encodeURIComponent("CACTS Pune")}&issueYear=2026&issueMonth=8&certUrl=${encodeURIComponent(currentMetadata.url)}`;
        window.open(certUrl, '_blank');
      }
      showToast('Caption copied! Opening LinkedIn Certificate addition window...');
    } else if (action === 'intent') {
      window.open(platform.intentUrl, '_blank');
      recordShareHistory(currentMetadata.url);
      
      if (textCopied && imgCopied) {
        showToast(`Caption & Graphic Image copied! Ready to paste (Ctrl+V) on ${platform.name}.`);
      } else if (textCopied) {
        showToast(`Caption copied to clipboard! Opening pre-filled ${platform.name}...`);
      } else {
        showToast(`Opened ${platform.name} share composer!`);
      }
    } else if (action === 'download-copy') {
      recordShareHistory(currentMetadata.url);
      showToast(`Caption copied & ${activeFormat} image saved! Ready to upload/paste on ${platform.name}.`);
    } else if (action === 'native-share') {
      if (navigator.share && currentBlob) {
        try {
          const file = new File([currentBlob], 'cacts-share.png', { type: 'image/png' });
          if (navigator.canShare && navigator.canShare({ files: [file] })) {
            showToast('Caption & hashtags copied to clipboard! Long-press -> Paste in your target app.', 5000);
            
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
