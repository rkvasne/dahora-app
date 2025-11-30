// VERSÃO: v0.2.1
console.log('🎨 Landing Page v0.2.1 carregada! Ícones monocromáticos ativos.');

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
