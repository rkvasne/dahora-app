// Animações e interações para seções escuras e cards
// Mantém separado do script principal por responsabilidade única

document.addEventListener('DOMContentLoaded', () => {
  setupDarkObservers();
  setupHoverBloom();
  setupSectionFocus();
});

function setupDarkObservers() {
  const options = { threshold: 0.12, rootMargin: '0px 0px -40px 0px' };
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate');
        if (entry.target.classList.contains('dark-card')) {
          entry.target.style.transform = 'translateY(0)';
          entry.target.style.opacity = '1';
        }
      }
    });
  }, options);

  document.querySelectorAll('.section--dark .section-header, .dark-card, .mock-window').forEach((el) => {
    el.classList.add('animate-on-scroll');
    observer.observe(el);
  });
}

function setupHoverBloom() {
  const items = document.querySelectorAll('.hover-bloom');
  items.forEach((item) => {
    item.addEventListener('mousemove', (e) => {
      const rect = item.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100 + '%';
      const y = ((e.clientY - rect.top) / rect.height) * 100 + '%';
      item.style.setProperty('--x', x);
      item.style.setProperty('--y', y);
    });
  });
}

function setupSectionFocus() {
  const darkSections = document.querySelectorAll('.section--dark');
  darkSections.forEach((section) => {
    section.addEventListener('mousemove', (e) => {
      const rect = section.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100 + '%';
      const y = ((e.clientY - rect.top) / rect.height) * 100 + '%';
      section.style.setProperty('--mx', x);
      section.style.setProperty('--my', y);
    });
  });
}