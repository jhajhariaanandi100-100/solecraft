// SOLECRAFT MAIN SCRIPTS

document.addEventListener('DOMContentLoaded', function () {
  // Toast container setup
  let toastContainer = document.querySelector('.solecraft-toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.className = 'solecraft-toast-container';
    document.body.appendChild(toastContainer);
  }

  window.showToast = function (message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = 'solecraft-toast';
    
    let icon = '✦';
    if (type === 'success') icon = '✓';
    if (type === 'danger') icon = '✕';
    if (type === 'warning') icon = '⚠';

    toast.innerHTML = `<span>${icon}</span> <div>${message}</div>`;
    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => toast.remove(), 400);
    }, 3800);
  };

  // Wishlist AJAX Toggle
  document.querySelectorAll('.wishlist-btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

      const productId = this.getAttribute('data-product-id');
      if (!productId) return;

      fetch(`/auth/wishlist/toggle/${productId}`, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'Content-Type': 'application/json'
        }
      })
      .then(res => {
        if (res.status === 401) {
          window.location.href = '/auth/login?next=' + encodeURIComponent(window.location.pathname);
          return;
        }
        return res.json();
      })
      .then(data => {
        if (!data) return;
        if (data.success) {
          if (data.added) {
            this.classList.add('active');
            window.showToast(data.message, 'success');
          } else {
            this.classList.remove('active');
            window.showToast(data.message, 'info');
          }
        }
      })
      .catch(err => console.error('Wishlist error:', err));
    });
  });

  // Quick View Modal
  const quickViewModalEl = document.getElementById('quickViewModal');
  if (quickViewModalEl) {
    const modal = new bootstrap.Modal(quickViewModalEl);

    document.querySelectorAll('.btn-card-quick').forEach(btn => {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        const productId = this.getAttribute('data-product-id');
        if (!productId) return;

        fetch(`/products/quick-view/${productId}`)
          .then(res => res.json())
          .then(data => {
            document.getElementById('qv-title').innerText = data.name;
            document.getElementById('qv-category').innerText = data.shoe_type;
            document.getElementById('qv-tagline').innerText = data.tagline || '';
            document.getElementById('qv-desc').innerText = data.description;
            document.getElementById('qv-material').innerText = data.material;
            document.getElementById('qv-img').src = data.main_image;
            document.getElementById('qv-link').href = data.detail_url;
            document.getElementById('qv-product-id').value = data.id;

            const priceEl = document.getElementById('qv-price');
            if (data.has_discount) {
              priceEl.innerHTML = `$${data.discount_price.toFixed(2)} <span class="original-price">$${data.price.toFixed(2)}</span>`;
            } else {
              priceEl.innerHTML = `$${data.price.toFixed(2)}`;
            }

            // Sizes select
            const sizeSelect = document.getElementById('qv-sizes');
            sizeSelect.innerHTML = '';
            data.sizes.forEach(s => {
              const opt = document.createElement('option');
              opt.value = s;
              opt.innerText = s;
              sizeSelect.appendChild(opt);
            });

            modal.show();
          })
          .catch(err => console.error('Quick view error:', err));
      });
    });

    // Quick View Add to Cart form AJAX
    const qvForm = document.getElementById('qv-cart-form');
    if (qvForm) {
      qvForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(qvForm);

        fetch('/cart/add', {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: formData
        })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            modal.hide();
            window.showToast(data.message, 'success');
            updateCartBadges(data.cart_count);
          }
        })
        .catch(err => console.error('Cart add error:', err));
      });
    }
  }

  // Update Cart badge counter
  window.updateCartBadges = function (count) {
    document.querySelectorAll('.cart-badge-pill').forEach(badge => {
      badge.innerText = count;
      badge.style.display = count > 0 ? 'flex' : 'none';
    });
  };

  // Newsletter AJAX subscription
  const newsletterForms = document.querySelectorAll('.newsletter-form');
  newsletterForms.forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const input = this.querySelector('input[type="email"]');
      const formData = new FormData();
      formData.append('email', input.value);

      fetch('/newsletter', {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        body: formData
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          window.showToast(data.message, 'success');
          input.value = '';
        } else {
          window.showToast(data.message, 'warning');
        }
      })
      .catch(err => {
        window.showToast('Subscribed! Welcome to the SoleCraft Inner Circle.', 'success');
        input.value = '';
      });
    });
  });
});
