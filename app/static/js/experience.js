(() => {
  const nav = document.querySelector('.app-nav');
  const updateHeader = () => nav?.classList.toggle('nav-scrolled', window.scrollY > 12);
  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });

  const revealItems = document.querySelectorAll('.feature-card, .feature-bento-card, .metric, .space-card, .content-panel, .cta-panel, .showcase-main, .showcase-card, .showcase-pills, .reveal-up');
  revealItems.forEach((item, index) => {
    item.classList.add('reveal');
    item.style.transitionDelay = `${Math.min(index * 45, 240)}ms`;
  });
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

  const navMenu = document.getElementById('nav');
  const navToggle = document.querySelector('[data-bs-target="#nav"]');
  const closeNav = () => {
    if (navMenu?.classList.contains('show')) {
      bootstrap.Collapse.getOrCreateInstance(navMenu).hide();
    }
  };
  navMenu?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeNav));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') closeNav();
  });
  navToggle?.setAttribute('aria-controls', 'nav');

  const onboarding = document.getElementById('vehicleOnboarding');
  if (onboarding && !sessionStorage.getItem('smartpark-vehicle-prompt-dismissed')) {
    window.setTimeout(() => bootstrap.Modal.getOrCreateInstance(onboarding).show(), 5000);
    onboarding.addEventListener('hidden.bs.modal', () => sessionStorage.setItem('smartpark-vehicle-prompt-dismissed', '1'));
  }
})();
