(() => {
  const nav = document.querySelector('.app-nav');
  const updateHeader = () => nav?.classList.toggle('nav-scrolled', window.scrollY > 12);
  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });

  const revealItems = document.querySelectorAll('.feature-card, .metric, .space-card, .content-panel, .cta-panel');
  revealItems.forEach(item => item.classList.add('reveal'));
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    }), { threshold: 0.12 });
    revealItems.forEach(item => observer.observe(item));
  } else {
    revealItems.forEach(item => item.classList.add('is-visible'));
  }

  const onboarding = document.getElementById('vehicleOnboarding');
  if (onboarding && !sessionStorage.getItem('smartpark-vehicle-prompt-dismissed')) {
    window.setTimeout(() => bootstrap.Modal.getOrCreateInstance(onboarding).show(), 5000);
    onboarding.addEventListener('hidden.bs.modal', () => sessionStorage.setItem('smartpark-vehicle-prompt-dismissed', '1'));
  }
})();
