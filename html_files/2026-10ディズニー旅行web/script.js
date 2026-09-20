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
});
