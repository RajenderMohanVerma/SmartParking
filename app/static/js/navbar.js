(() => {
  const header = document.getElementById('siteHeader');
  const collapse = document.getElementById('nav');
  const mobileToggle = document.getElementById('mobileMenuToggle');
  const mobileMenu = document.getElementById('mobileMenu');
  if (!header) return;

  mobileToggle?.addEventListener('click', () => {
    const open = mobileMenu.hidden;
    mobileMenu.hidden = !open;
    mobileToggle.setAttribute('aria-expanded', String(open));
    mobileToggle.classList.toggle('is-open', open);
  });

  mobileMenu?.querySelectorAll('a, button:not(#mobileThemeToggle)').forEach((link) => {
    link.addEventListener('click', () => {
      mobileMenu.hidden = true;
      mobileToggle?.setAttribute('aria-expanded', 'false');
      mobileToggle?.classList.remove('is-open');
    });
  });

  const mobileTheme = document.getElementById('mobileThemeToggle');
  mobileTheme?.addEventListener('click', () => document.getElementById('themeToggle')?.click());

  const updateHeaderState = () => {
    header.classList.toggle('is-scrolled', window.scrollY > 8);
  };
  updateHeaderState();
  window.addEventListener('scroll', updateHeaderState, { passive: true });

  const toggler = document.querySelector('[data-bs-target="#nav"]');
  collapse?.addEventListener('shown.bs.collapse', () => {
    toggler?.classList.add('is-open');
    toggler?.querySelector('i')?.classList.replace('bi-list', 'bi-x-lg');
  });
  collapse?.addEventListener('hidden.bs.collapse', () => {
    toggler?.classList.remove('is-open');
    toggler?.querySelector('i')?.classList.replace('bi-x-lg', 'bi-list');
  });

  const closeDropdowns = () => {
    collapse?.querySelectorAll('.dropdown.show').forEach((item) => {
      item.classList.remove('show');
      item.querySelector('.dropdown-toggle')?.setAttribute('aria-expanded', 'false');
      item.querySelector('.dropdown-menu')?.classList.remove('show');
    });
  };

  collapse?.querySelectorAll('.dropdown-toggle').forEach((toggle) => {
    toggle.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      const item = toggle.closest('.dropdown');
      const menu = item?.querySelector('.dropdown-menu');
      if (!item || !menu) return;
      const open = !item.classList.contains('show');
      closeDropdowns();
      item.classList.toggle('show', open);
      menu.classList.toggle('show', open);
      toggle.setAttribute('aria-expanded', String(open));
    });
  });

  collapse?.querySelectorAll('a:not(.dropdown-toggle)').forEach((link) => {
    link.addEventListener('click', () => {
      if (window.innerWidth < 992 && collapse.classList.contains('show')) {
        closeDropdowns();
        bootstrap.Collapse.getOrCreateInstance(collapse).hide();
      }
    });
  });

  document.addEventListener('click', (event) => {
    if (!event.target.closest('.site-header')) closeDropdowns();
  });
})();
