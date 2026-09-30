// Disney Family Trip 2026 - Interactive Scripts

document.addEventListener('DOMContentLoaded', () => {
  // Highlight active nav link
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  const navLinks = document.querySelectorAll('nav.main-nav a');
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });

  // Interactive TODO Checklists with LocalStorage
  const todoItems = document.querySelectorAll('.todo-item');
  if (todoItems.length > 0) {
    const STORAGE_KEY = 'disney_trip_2026_todos';
    let savedState = {};

    try {
      savedState = JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
    } catch (e) {
      console.warn('LocalStorage not available');
    }

    todoItems.forEach((item, index) => {
      const itemId = item.getAttribute('data-id') || `todo_${index}`;
      item.setAttribute('data-id', itemId);

      // Restore state
      if (savedState[itemId]) {
        item.classList.add('checked');
      }

      // Toggle click
      item.addEventListener('click', () => {
        item.classList.toggle('checked');
        savedState[itemId] = item.classList.contains('checked');
        try {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(savedState));
        } catch (e) {}
      });
    });
  }

  // View Switchers (Timeline / Table, Table / Card)
  const viewSwitchers = document.querySelectorAll('.view-switcher');
  viewSwitchers.forEach(switcher => {
    const buttons = switcher.querySelectorAll('.view-btn');
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetId = btn.getAttribute('data-target');
        const container = switcher.closest('.section-card') || document;
        
        // Update active button in this switcher
        buttons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Toggle target view panes
        const panes = container.querySelectorAll('.view-pane');
        panes.forEach(pane => {
          if (pane.id === targetId) {
            pane.classList.remove('hidden');
          } else {
            pane.classList.add('hidden');
          }
        });
      });
    });
  });

  // Automatically ensure scroll hints on all table wrappers
  const tableWrappers = document.querySelectorAll('.table-wrapper, .table-responsive');
  tableWrappers.forEach(wrapper => {
    const prev = wrapper.previousElementSibling;
    if (!prev || !prev.classList.contains('table-scroll-hint')) {
      const hint = document.createElement('div');
      hint.className = 'table-scroll-hint';
      hint.innerHTML = '<span class="hint-icon">👈</span><span>横にスワイプして全体を確認できます</span><span class="hint-icon">👉</span>';
      wrapper.parentNode.insertBefore(hint, wrapper);
    }
  });
});
