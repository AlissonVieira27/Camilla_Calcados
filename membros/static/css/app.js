const menuButton = document.querySelector('.menu-toggle');
const sidebar = document.querySelector('.sidebar');
const overlay = document.querySelector('.sidebar-overlay');

function closeMenu() {
  if (!sidebar || !menuButton) return;
  sidebar.classList.remove('open');
  menuButton.setAttribute('aria-expanded', 'false');
}

if (menuButton && sidebar) {
  menuButton.addEventListener('click', () => {
    const isOpen = sidebar.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(isOpen));
  });
}

if (overlay) overlay.addEventListener('click', closeMenu);
