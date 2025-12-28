document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.createElement('div');
  overlay.className = 'sidebar-overlay';
  document.body.appendChild(overlay);

  // Define SVG Icons (Navy Theme)
  const icons = {
    home: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#003366" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>`,
    dashboard: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#003366" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>`,
    income: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#003366" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"/><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"/><path d="M18 12a2 2 0 0 0 0 4h4v-4Z"/></svg>`,
    credit: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#003366" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>`,
    insurance: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#003366" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/></svg>`,
    chatbot: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#003366" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg>`,
    logout: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/></svg>`
  };

  // Define sidebar HTML structure
  const sidebarHTML = `
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="sidebar-logo">FinBridge</div>
      </div>
      <nav class="sidebar-nav">
        <a href="index.html" class="sidebar-link">
          <span class="icon">${icons.home}</span> Home
        </a>
        <a href="dashboard.html" class="sidebar-link">
          <span class="icon">${icons.dashboard}</span> Dashboard
        </a>
        <a href="income.html" class="sidebar-link">
          <span class="icon">${icons.income}</span> Income
        </a>
        <a href="credit-score.html" class="sidebar-link">
          <span class="icon">${icons.credit}</span> Credit Score
        </a>
        <a href="insurance.html" class="sidebar-link">
          <span class="icon">${icons.insurance}</span> Insurance
        </a>
        <a href="chatbot.html" class="sidebar-link">
          <span class="icon">${icons.chatbot}</span> FinBot
        </a>
      </nav>
      <div class="sidebar-footer">
        <button class="sidebar-logout" onclick="window.location.href='index.html'">
          <span class="icon">${icons.logout}</span> Logout
        </button>
      </div>
    </aside>
  `;

  // Inject sidebar before script tags
  document.body.insertAdjacentHTML('afterbegin', sidebarHTML);

  const sidebar = document.querySelector('.sidebar');
  const overlayEl = document.querySelector('.sidebar-overlay');

  // New unified way to find the menu toggle button
  // We will expect the HTML to have a class 'menu-toggle-btn' for reliability

  const toggleMenu = (e) => {
    e.preventDefault();
    sidebar.classList.add('active');
    overlayEl.classList.add('active');
  };

  // Attach execution based on class
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.menu-toggle-btn');
    if (btn) {
      toggleMenu(e);
    }
  });

  // Close sidebar
  const closeMenu = () => {
    sidebar.classList.remove('active');
    overlayEl.classList.remove('active');
  };

  overlayEl.addEventListener('click', closeMenu);

  // Highlight active link
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  const links = document.querySelectorAll('.sidebar-link');
  links.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
});
