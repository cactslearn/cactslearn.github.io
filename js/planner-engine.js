/**
 * CACTS Pune - Social Content Planner Dashboard Engine
 * Filename: js/planner-engine.js
 * Description: Client-side content planner engine indexing 240 structured pages, providing filtering,
 *              search, urgent/evergreen queue rotation, gridIndex palette dispersion, and social share modal trigger.
 */

window.CactsPlannerEngine = (function() {
  'use strict';

  let rawContentIndex = [];
  let urgentQueue = [];
  let evergreenQueue = [];

  let currentFilter = 'ALL';
  let searchQuery = '';

  document.addEventListener('DOMContentLoaded', () => {
    initPlannerEngine();
  });

  async function initPlannerEngine() {
    try {
      const resp = await fetch('js/content-index.json');
      if (!resp.ok) throw new Error('Failed to load content index');
      rawContentIndex = await resp.json();

      processQueues();
      bindFilterEvents();
      setupKeyboardShortcuts();
      renderDashboard();
    } catch (e) {
      console.error('Planner initialization error:', e);
      const container = document.getElementById('urgentCardsGrid');
      if (container) {
        container.innerHTML = '<div class="planner-error-msg">Failed to load indexed pages. Ensure js/content-index.json exists.</div>';
      }
    }
  }

  function processQueues() {
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

    urgentQueue = [];
    evergreenQueue = [];

    rawContentIndex.forEach((item, idx) => {
      item.gridIndex = idx;
      const itemDate = new Date(item.date);
      if (itemDate >= thirtyDaysAgo || item.is_new) {
        urgentQueue.push(item);
      } else {
        evergreenQueue.push(item);
      }
    });

    if (urgentQueue.length === 0 && rawContentIndex.length > 0) {
      urgentQueue = rawContentIndex.slice(0, 30);
      evergreenQueue = rawContentIndex.slice(30);
    }
  }

  function bindFilterEvents() {
    const searchInput = document.getElementById('plannerSearchInput');
    const filterPills = document.querySelectorAll('.planner-filter-pill');
    const exportCsvBtn = document.getElementById('exportCsvBtn');
    const exportJsonBtn = document.getElementById('exportJsonBtn');
    const exportHistoryBtn = document.getElementById('exportHistoryBtn');

    if (searchInput) {
      searchInput.addEventListener('input', e => {
        searchQuery = e.target.value.toLowerCase().trim();
        renderDashboard();
      });
    }

    filterPills.forEach(pill => {
      pill.addEventListener('click', e => {
        filterPills.forEach(p => p.classList.remove('active'));
        e.target.classList.add('active');
        currentFilter = e.target.dataset.filter || 'ALL';
        renderDashboard();
      });
    });

    if (exportCsvBtn) exportCsvBtn.addEventListener('click', exportQueueCsv);
    if (exportJsonBtn) exportJsonBtn.addEventListener('click', exportQueueJson);
    if (exportHistoryBtn) exportHistoryBtn.addEventListener('click', exportShareHistoryCsv);

    const shareAllUrlBtn = document.getElementById('shareCurrentUrlBtn');
    if (shareAllUrlBtn) {
      shareAllUrlBtn.addEventListener('click', () => {
        if (window.CactsSocialShareEngine) {
          window.CactsSocialShareEngine.openModalForUrl(window.location.href);
        }
      });
    }
  }

  function setupKeyboardShortcuts() {
    document.addEventListener('keydown', e => {
      if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
        e.preventDefault();
        const searchInput = document.getElementById('plannerSearchInput');
        if (searchInput) searchInput.focus();
      }
      if (e.key === 'Escape') {
        const modal = document.getElementById('cactsSocialModal');
        if (modal && modal.classList.contains('active')) {
          modal.classList.remove('active');
        }
      }
    });
  }

  function renderDashboard() {
    const urgentContainer = document.getElementById('urgentCardsGrid');
    const evergreenContainer = document.getElementById('evergreenCardsGrid');
    const totalCountElem = document.getElementById('totalIndexedCount');

    if (totalCountElem) {
      totalCountElem.innerText = rawContentIndex.length;
    }

    const shareHistory = JSON.parse(localStorage.getItem('cacts_share_history') || '[]');

    const filteredUrgent = filterItems(urgentQueue);
    const filteredEvergreen = filterItems(evergreenQueue);

    if (urgentContainer) {
      if (filteredUrgent.length === 0) {
        urgentContainer.innerHTML = '<div class="planner-empty-msg">No newly updated content items match your current filter.</div>';
      } else {
        urgentContainer.innerHTML = filteredUrgent.map((item, idx) => renderContentCard(item, 'URGENT', shareHistory, idx)).join('');
      }
    }

    if (evergreenContainer) {
      if (filteredEvergreen.length === 0) {
        evergreenContainer.innerHTML = '<div class="planner-empty-msg">No evergreen rotation content items match your current filter.</div>';
      } else {
        evergreenContainer.innerHTML = filteredEvergreen.map((item, idx) => renderContentCard(item, 'EVERGREEN', shareHistory, idx + filteredUrgent.length)).join('');
      }
    }

    attachCardShareEvents();
  }

  function filterItems(items) {
    return items.filter(item => {
      if (currentFilter !== 'ALL') {
        const itemSchema = (item.schema_type || '').toUpperCase();
        const urlLower = (item.url || '').toLowerCase();

        if (currentFilter === 'JOB' && !itemSchema.includes('JOB') && !urlLower.includes('/jobs/')) return false;
        if (currentFilter === 'COURSE' && !itemSchema.includes('COURSE') && !urlLower.includes('/courses/')) return false;
        if (currentFilter === 'CREDENTIAL' && !itemSchema.includes('CREDENTIAL') && !urlLower.includes('verify.html')) return false;
        if (currentFilter === 'TOOL' && (!itemSchema.includes('WEBAPPLICATION') && !itemSchema.includes('TOOL')) && !urlLower.includes('/tools/')) return false;
        if (currentFilter === 'REPORT' && !itemSchema.includes('REPORT') && !urlLower.includes('report')) return false;
        if (currentFilter === 'LOCATION' && !itemSchema.includes('LOCALBUSINESS') && !urlLower.includes('/locations/')) return false;
        if (currentFilter === 'REVIEW' && !itemSchema.includes('STUDENTREVIEWS') && !urlLower.includes('reviews.html')) return false;
        if (currentFilter === 'GUIDE' && !itemSchema.includes('ARTICLE') && !urlLower.includes('/guides/') && !urlLower.includes('/comparisons/')) return false;
        if (currentFilter === 'POLICY' && !urlLower.includes('privacy') && !urlLower.includes('terms') && !urlLower.includes('about') && !urlLower.includes('contact') && !urlLower.includes('faq') && !urlLower.includes('sitemap')) return false;
      }

      if (searchQuery) {
        const matchTitle = (item.title || '').toLowerCase().includes(searchQuery);
        const matchUrl = (item.url || '').toLowerCase().includes(searchQuery);
        const matchDesc = (item.description || '').toLowerCase().includes(searchQuery);
        if (!matchTitle && !matchUrl && !matchDesc) return false;
      }

      return true;
    });
  }

  function renderContentCard(item, queueType, shareHistory, gridIndex = 0) {
    const isRecentlyShared = shareHistory.includes(item.url);
    const badgeLabel = queueType === 'URGENT' ? 'Urgent Priority' : 'Evergreen Rotation';
    const badgeClass = queueType === 'URGENT' ? 'urgent-badge' : 'evergreen-badge';

    return `
      <div class="planner-card" data-url="${item.url}">
        <div class="planner-card-header">
          <span class="planner-badge ${badgeClass}">${badgeLabel}</span>
          ${isRecentlyShared ? '<span class="planner-badge shared-badge">Recently Shared</span>' : ''}
          <span class="planner-read-time">${item.reading_time || '2 min read'}</span>
        </div>

        <h4 class="planner-card-title">${item.title}</h4>
        <p class="planner-card-desc">${truncateText(item.description, 130)}</p>

        <div class="planner-card-meta">
          <span class="planner-schema-tag">[${item.schema_type || 'WebPage'}]</span>
          <span class="planner-card-date">Updated: ${item.date || 'Recently'}</span>
        </div>

        <div class="planner-card-footer">
          <a href="${item.url}" target="_blank" class="planner-view-link">View Page ➔</a>
          <button class="planner-share-btn" data-url="${item.url}" data-index="${gridIndex}">
            Share Now
          </button>
        </div>
      </div>
    `;
  }

  function attachCardShareEvents() {
    document.querySelectorAll('.planner-share-btn').forEach(btn => {
      btn.addEventListener('click', e => {
        const targetUrl = e.target.dataset.url;
        const gridIdx = parseInt(e.target.dataset.index || '0', 10);
        const matchedItem = rawContentIndex.find(i => i.url === targetUrl);
        const pageItemData = matchedItem ? { ...matchedItem, gridIndex: gridIdx } : { gridIndex: gridIdx };
        if (window.CactsSocialShareEngine) {
          window.CactsSocialShareEngine.openModalForUrl(targetUrl, pageItemData);
        }
      });
    });
  }

  function truncateText(str, maxLen) {
    if (!str || str.length <= maxLen) return str;
    return str.substring(0, maxLen - 3) + '...';
  }

  function exportQueueCsv() {
    const allFiltered = [...filterItems(urgentQueue), ...filterItems(evergreenQueue)];
    let csvStr = 'Title,URL,Schema,ReadingTime,LastModifiedDate\n';
    allFiltered.forEach(item => {
      const cleanTitle = `"${(item.title || '').replace(/"/g, '""')}"`;
      csvStr += `${cleanTitle},"${item.url}","${item.schema_type}","${item.reading_time}","${item.date}"\n`;
    });

    downloadBlob(new Blob([csvStr], { type: 'text/csv' }), `cacts-social-planner-${Date.now()}.csv`);
  }

  function exportQueueJson() {
    const allFiltered = [...filterItems(urgentQueue), ...filterItems(evergreenQueue)];
    const jsonStr = JSON.stringify(allFiltered, null, 2);
    downloadBlob(new Blob([jsonStr], { type: 'application/json' }), `cacts-social-planner-${Date.now()}.json`);
  }

  function exportShareHistoryCsv() {
    const history = JSON.parse(localStorage.getItem('cacts_share_history') || '[]');
    let csvStr = 'URL,SharedDate\n';
    history.forEach(url => {
      csvStr += `"${url}","Recorded"\n`;
    });
    downloadBlob(new Blob([csvStr], { type: 'text/csv' }), `cacts-share-history-${Date.now()}.csv`);
  }

  function downloadBlob(blob, filename) {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href);
  }

})();
