// SOLECRAFT AI STYLE ASSISTANT WIZARD

document.addEventListener('DOMContentLoaded', function () {
  let currentStep = 1;
  const totalSteps = 5;

  const answers = {
    vibe: 'minimalist',
    occasion: 'daily',
    colors: 'monochrome',
    footwear_type: 'all',
    budget: '150_220'
  };

  // Option select handler for choice cards
  document.querySelectorAll('.ai-choice-card').forEach(card => {
    card.addEventListener('click', function () {
      const stepEl = this.closest('.ai-wizard-step');
      stepEl.querySelectorAll('.ai-choice-card').forEach(c => c.classList.remove('active'));
      this.classList.add('active');

      const field = this.getAttribute('data-field');
      const value = this.getAttribute('data-value');
      answers[field] = value;
    });
  });

  // Next Step button
  document.querySelectorAll('.btn-ai-next').forEach(btn => {
    btn.addEventListener('click', function () {
      if (currentStep < totalSteps) {
        goToStep(currentStep + 1);
      } else {
        runAiAnalysis();
      }
    });
  });

  // Back button
  document.querySelectorAll('.btn-ai-back').forEach(btn => {
    btn.addEventListener('click', function () {
      if (currentStep > 1) {
        goToStep(currentStep - 1);
      }
    });
  });

  function goToStep(step) {
    document.querySelectorAll('.ai-wizard-step').forEach(s => s.classList.add('d-none'));
    const target = document.getElementById(`step-${step}`);
    if (target) target.classList.remove('d-none');

    currentStep = step;

    // Progress bar
    const progressEl = document.getElementById('ai-progress-bar');
    if (progressEl) {
      const pct = (currentStep / totalSteps) * 100;
      progressEl.style.width = `${pct}%`;
    }
  }

  function runAiAnalysis() {
    // Hide questions, show analyzing animation
    document.querySelectorAll('.ai-wizard-step').forEach(s => s.classList.add('d-none'));
    const loadingScreen = document.getElementById('ai-loading-screen');
    if (loadingScreen) loadingScreen.classList.remove('d-none');

    const loaderText = document.getElementById('ai-loader-text');
    const messages = [
      'Scanning style parameters and lifestyle ergonomics...',
      'Matching anatomical silhouettes with luxury materials...',
      'Synthesizing bespoke colorways and curated recommendations...'
    ];

    let msgIdx = 0;
    const interval = setInterval(() => {
      msgIdx++;
      if (msgIdx < messages.length && loaderText) {
        loaderText.innerText = messages[msgIdx];
      }
    }, 600);

    // Call backend API
    fetch('/ai-stylist/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify(answers)
    })
    .then(res => res.json())
    .then(data => {
      clearInterval(interval);
      setTimeout(() => {
        if (loadingScreen) loadingScreen.classList.add('d-none');
        renderAiResults(data);
      }, 1400);
    })
    .catch(err => {
      clearInterval(interval);
      console.error('AI Stylist error:', err);
    });
  }

  function renderAiResults(data) {
    const resultsContainer = document.getElementById('ai-results-container');
    if (!resultsContainer) return;

    resultsContainer.classList.remove('d-none');

    // 1. Archetype Banner
    const arch = data.archetype;
    document.getElementById('ai-arch-title').innerText = arch.title;
    document.getElementById('ai-arch-quote').innerText = `"${arch.quote}"`;
    document.getElementById('ai-summary-text').innerText = data.summary;

    // 2. Recommendations Grid
    const recGrid = document.getElementById('ai-recommendations-grid');
    recGrid.innerHTML = '';

    data.recommendations.forEach(item => {
      const col = document.createElement('div');
      col.className = 'col-lg-6 mb-4';
      col.innerHTML = `
        <div class="product-card h-100 shadow-sm border">
          <div class="product-image-wrap position-relative">
            <span class="product-card-badge badge-discount" style="background: var(--accent);">
              ✦ ${item.match_percent}% VIBE MATCH
            </span>
            <img src="${item.image}" alt="${item.name}">
          </div>
          <div class="product-info-wrap p-3">
            <div class="product-category-tag">${item.category}</div>
            <h5 class="fw-bold mb-1"><a href="${item.url}" class="text-decoration-none text-dark">${item.name}</a></h5>
            <div class="small text-muted mb-2 fst-italic">"${item.reason}"</div>
            <div class="product-price-row mt-auto pt-2 border-top d-flex justify-content-between align-items-center">
              <span class="product-price fs-5 fw-bold">$${item.effective_price.toFixed(2)}</span>
              <a href="${item.url}" class="btn btn-sm btn-solecraft-dark">View Product</a>
            </div>
          </div>
        </div>
      `;
      recGrid.appendChild(col);
    });

    // 3. Custom Studio Preset Action
    const presetBtn = document.getElementById('btn-ai-launch-customizer');
    if (presetBtn && data.custom_preset) {
      presetBtn.href = `/customizer?preset=${data.custom_preset.shoe_type}`;
    }

    // Scroll smoothly to results
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
  }

  // Retake Questionnaire
  const retakeBtn = document.getElementById('btn-ai-retake');
  if (retakeBtn) {
    retakeBtn.addEventListener('click', function () {
      document.getElementById('ai-results-container').classList.add('d-none');
      goToStep(1);
    });
  }
});
