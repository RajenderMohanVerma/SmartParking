(() => {
  const header = document.getElementById('siteHeader');
  const collapse = document.getElementById('nav');
  if (!header) return;

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

  collapse?.querySelectorAll('.dropdown-toggle').forEach((toggle) => {
    toggle.addEventListener('click', (event) => {
      if (window.innerWidth >= 992) return;
      event.preventDefault();
      event.stopPropagation();
      const item = toggle.closest('.dropdown');
      const menu = item?.querySelector('.dropdown-menu');
      if (!item || !menu) return;
      const open = menu.classList.toggle('show');
      item.classList.toggle('show', open);
      toggle.setAttribute('aria-expanded', String(open));
    });
  });

  collapse?.querySelectorAll('a:not(.dropdown-toggle)').forEach((link) => {
    link.addEventListener('click', () => {
      if (window.innerWidth < 992 && collapse.classList.contains('show')) {
        collapse.querySelectorAll('.dropdown-menu.show').forEach((menu) => menu.classList.remove('show'));
        collapse.querySelectorAll('.dropdown.show').forEach((item) => item.classList.remove('show'));
        bootstrap.Collapse.getOrCreateInstance(collapse).hide();
      }
    });
  });
})();
