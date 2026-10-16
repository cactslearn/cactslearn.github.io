/* ==========================================================================
   QUIZ & READINESS DIAGNOSTIC ENGINE (js/quiz-engine.js)
   Multi-step assessment logic for course readiness and developer evaluation
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
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
          if (qScoreTitle) qScoreTitle.textContent = `${pct}% High Developer Readiness`;
          if (qScoreDesc) qScoreDesc.textContent = 'You possess a solid analytical mindset and strong debugging commitment. You are well-positioned for 1-to-1 intensive developer lab mentorship.';
          if (qRecTime) qRecTime.textContent = '12 to 16 Weeks';
          if (qRecRisk) qRecRisk.textContent = 'Low Risk (Future-Proof)';
        } else if (pct >= 55) {
          if (qScoreTitle) qScoreTitle.textContent = `${pct}% Moderate Readiness`;
          if (qScoreDesc) qScoreDesc.textContent = 'You have good potential, but need consistent daily hands-on keyboard time (10+ hrs/wk) to build line-by-line debugging confidence.';
          if (qRecTime) qRecTime.textContent = '16 to 20 Weeks';
          if (qRecRisk) qRecRisk.textContent = 'Moderate Risk';
        } else {
          if (qScoreTitle) qScoreTitle.textContent = `${pct}% Foundation Building Phase`;
          if (qScoreDesc) qScoreDesc.textContent = 'We recommend starting with logic foundations and dedicated 1-to-1 mentorship to avoid getting overwhelmed by batch fast-pacing.';
          if (qRecTime) qRecTime.textContent = '20+ Weeks';
          if (qRecRisk) qRecRisk.textContent = 'High Batch Risk';
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
});
