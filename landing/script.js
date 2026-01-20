// VERSÃO: v0.2.15
console.log('🎨 Landing Page v0.2.15 carregada! Ícones monocromáticos ativos.');

// Mobile Menu Logic
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const navMenu = document.getElementById('nav-menu');
const menuOverlay = document.createElement('div');
menuOverlay.className = 'menu-overlay';
menuOverlay.id = 'menu-overlay';
document.body.appendChild(menuOverlay);
const navLinks = document.querySelectorAll('.nav-link');

function toggleMenu() {
    navMenu.classList.toggle('active');
    menuOverlay.classList.toggle('active');
    
    // Alterna ícone
    const icon = mobileMenuBtn.querySelector('i');
    if (navMenu.classList.contains('active')) {
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
    } else {
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    }
}

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', toggleMenu);
    menuOverlay.addEventListener('click', toggleMenu);

    // Fecha menu ao clicar em um link
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navMenu.classList.contains('active')) {
                toggleMenu();
            }
        });
    });
}

// FAQ Toggle
function toggleFAQ(button) {
    const faqItem = button.parentElement;
    const isActive = faqItem.classList.contains('active');
    
    // Fecha todos os outros itens
    document.querySelectorAll('.faq-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Toggle do item clicado
    if (!isActive) {
        faqItem.classList.add('active');
    }
}

// Efeito spotlight seguindo o mouse nos cards
document.addEventListener('DOMContentLoaded', () => {
    // Spotlight nos cards
    const cards = document.querySelectorAll('.feature-card');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100 + '%';
            const y = ((e.clientY - rect.top) / rect.height) * 100 + '%';
            
            card.style.setProperty('--x', x);
            card.style.setProperty('--y', y);
        });
    });

    // Spotlight nas seções dark
    const darkSections = document.querySelectorAll('.section-dark');
    darkSections.forEach(section => {
        section.addEventListener('mousemove', (e) => {
            const rect = section.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100 + '%';
            const y = ((e.clientY - rect.top) / rect.height) * 100 + '%';
            
            section.style.setProperty('--mx', x);
            section.style.setProperty('--my', y);
        });
    });
});
