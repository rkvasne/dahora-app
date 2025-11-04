// Dahora App - Landing Page JavaScript
// Funcionalidades interativas e animações

document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    const header = document.querySelector('.header');
    const modals = document.querySelectorAll('.modal');
    const closeButtons = document.querySelectorAll('.close');
    
    // Inicialização
    init();
    
    function init() {
        setupNavigation();
        setupScrollEffects();
        setupAnimations();
        setupModals();
        setupScrollToTop();
        updateDateTime();
        setupDownloadTracking();
    }
    
    // ===== NAVEGAÇÃO RESPONSIVA =====
    function setupNavigation() {
        // Toggle do menu mobile
        navToggle.addEventListener('click', function() {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
            document.body.classList.toggle('nav-open');
        });
        
        // Fechar menu ao clicar em um link
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.classList.remove('nav-open');
            });
        });
        
        // Fechar menu ao clicar fora
        document.addEventListener('click', function(e) {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.classList.remove('nav-open');
            }
        });
        
        // Smooth scroll para links internos
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href.startsWith('#')) {
                    e.preventDefault();
                    const target = document.querySelector(href);
                    if (target) {
                        const headerHeight = header.offsetHeight;
                        const targetPosition = target.offsetTop - headerHeight;
                        
                        window.scrollTo({
                            top: targetPosition,
                            behavior: 'smooth'
                        });
                    }
                }
            });
        });
    }
    
    // ===== EFEITOS DE SCROLL =====
    function setupScrollEffects() {
        let lastScrollTop = 0;
        
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            // Header background no scroll
            if (scrollTop > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
            
            // Atualizar indicador de progresso
            updateScrollProgress();
            
            // Mostrar/ocultar botão scroll to top
            toggleScrollToTop();
            
            lastScrollTop = scrollTop;
        });
    }
    
    function updateScrollProgress() {
        const scrollTop = window.pageYOffset;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        
        // Criar barra de progresso se não existir
        let progressBar = document.querySelector('.scroll-progress');
        if (!progressBar) {
            progressBar = document.createElement('div');
            progressBar.className = 'scroll-progress';
            progressBar.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: ${scrollPercent}%;
                height: 3px;
                background: linear-gradient(90deg, #6366f1, #8b5cf6);
                z-index: 9999;
                transition: width 0.1s ease;
            `;
            document.body.appendChild(progressBar);
        } else {
            progressBar.style.width = scrollPercent + '%';
        }
    }
    
    // ===== ANIMAÇÕES ON SCROLL =====
    function setupAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                    
                    // Animação especial para cards
                    if (entry.target.classList.contains('feature-card') || 
                        entry.target.classList.contains('step-card')) {
                        animateCard(entry.target);
                    }
                }
            });
        }, observerOptions);
        
        // Observar elementos para animação
        const animateElements = document.querySelectorAll(`
            .feature-card,
            .step-card,
            .download-option,
            .section-header,
            .hero-content,
            .hero-image,
            .benefit-item,
            .faq-item,
            .privacy-card
        `);
        
        animateElements.forEach(el => {
            el.classList.add('animate-on-scroll');
            observer.observe(el);
        });
    }
    
    function animateCard(card) {
        const delay = Array.from(card.parentNode.children).indexOf(card) * 100;
        setTimeout(() => {
            card.style.transform = 'translateY(0)';
            card.style.opacity = '1';
        }, delay);
    }
    
    // ===== MODAIS =====
    function setupModals() {
        // Abrir modais
        window.showIssueModal = function() {
            document.getElementById('issueModal').style.display = 'block';
            document.body.style.overflow = 'hidden';
        };
        
        window.showFeatureModal = function() {
            document.getElementById('featureModal').style.display = 'block';
            document.body.style.overflow = 'hidden';
        };
        
        // Fechar modais
        closeButtons.forEach(button => {
            button.addEventListener('click', function() {
                const modal = this.closest('.modal');
                closeModal(modal);
            });
        });
        
        // Fechar modal clicando fora
        modals.forEach(modal => {
            modal.addEventListener('click', function(e) {
                if (e.target === this) {
                    closeModal(this);
                }
            });
        });
        
        // Fechar modal com ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                modals.forEach(modal => {
                    if (modal.style.display === 'block') {
                        closeModal(modal);
                    }
                });
            }
        });
    }
    
    function closeModal(modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
    
    // ===== SCROLL TO TOP =====
    function setupScrollToTop() {
        // Criar botão se não existir
        let scrollBtn = document.querySelector('.scroll-to-top');
        if (!scrollBtn) {
            scrollBtn = document.createElement('button');
            scrollBtn.className = 'scroll-to-top';
            scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
            scrollBtn.setAttribute('aria-label', 'Voltar ao topo');
            document.body.appendChild(scrollBtn);
        }
        
        scrollBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    function toggleScrollToTop() {
        const scrollBtn = document.querySelector('.scroll-to-top');
        if (window.pageYOffset > 300) {
            scrollBtn.classList.add('visible');
        } else {
            scrollBtn.classList.remove('visible');
        }
    }
    
    // ===== ATUALIZAÇÃO DE DATA/HORA =====
    function updateDateTime() {
        const datetimeElements = document.querySelectorAll('.output-text');
        
        function formatDateTime() {
            const now = new Date();
            const day = String(now.getDate()).padStart(2, '0');
            const month = String(now.getMonth() + 1).padStart(2, '0');
            const year = now.getFullYear();
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            
            return `[${day}.${month}.${year}-${hours}:${minutes}]`;
        }
        
        // Atualizar imediatamente
        datetimeElements.forEach(el => {
            el.textContent = formatDateTime();
        });
        
        // Atualizar a cada minuto
        setInterval(() => {
            datetimeElements.forEach(el => {
                el.textContent = formatDateTime();
            });
        }, 60000);
    }
    
    // ===== TRACKING DE DOWNLOADS =====
    function setupDownloadTracking() {
        const downloadButtons = document.querySelectorAll('a[href*="download"], a[download]');
        
        downloadButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                const fileName = this.getAttribute('href') || this.getAttribute('download');
                
                // Animação de loading
                const originalText = this.innerHTML;
                this.innerHTML = '<div class="loading"></div> Baixando...';
                this.style.pointerEvents = 'none';
                
                // Simular delay de download
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-check"></i> Baixado!';
                    
                    setTimeout(() => {
                        this.innerHTML = originalText;
                        this.style.pointerEvents = '';
                    }, 2000);
                }, 1000);
                
                // Analytics (se implementado)
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'download', {
                        'file_name': fileName,
                        'event_category': 'engagement'
                    });
                }
            });
        });
    }
    
    // ===== EFEITOS ESPECIAIS =====
    
    // Efeito de digitação no hero
    function typewriterEffect(element, text, speed = 100) {
        let i = 0;
        element.innerHTML = '';
        
        function type() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        
        type();
    }
    
    // Contador animado
    function animateCounter(element, target, duration = 2000) {
        let start = 0;
        const increment = target / (duration / 16);
        
        function updateCounter() {
            start += increment;
            if (start < target) {
                element.textContent = Math.floor(start);
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target;
            }
        }
        
        updateCounter();
    }
    
    // ===== UTILITÁRIOS =====
    
    // Debounce function
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Throttle function
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
    
    // ===== EASTER EGGS =====
    
    // Konami Code
    let konamiCode = [];
    const konamiSequence = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]; // ↑↑↓↓←→←→BA
    
    document.addEventListener('keydown', function(e) {
        konamiCode.push(e.keyCode);
        
        if (konamiCode.length > konamiSequence.length) {
            konamiCode.shift();
        }
        
        if (konamiCode.join(',') === konamiSequence.join(',')) {
            activateEasterEgg();
            konamiCode = [];
        }
    });
    
    function activateEasterEgg() {
        // Efeito especial quando o Konami Code é ativado
        document.body.style.animation = 'rainbow 2s infinite';
        
        // Criar confetti
        createConfetti();
        
        // Mostrar mensagem especial
        showSpecialMessage();
        
        setTimeout(() => {
            document.body.style.animation = '';
        }, 5000);
    }
    
    function createConfetti() {
        for (let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.style.cssText = `
                position: fixed;
                width: 10px;
                height: 10px;
                background: hsl(${Math.random() * 360}, 100%, 50%);
                left: ${Math.random() * 100}vw;
                top: -10px;
                z-index: 10000;
                animation: confetti-fall 3s linear forwards;
            `;
            document.body.appendChild(confetti);
            
            setTimeout(() => confetti.remove(), 3000);
        }
    }
    
    function showSpecialMessage() {
        const message = document.createElement('div');
        message.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 2rem;
            border-radius: 16px;
            font-size: 1.5rem;
            text-align: center;
            z-index: 10001;
            animation: fadeInUp 0.5s ease;
        `;
        message.innerHTML = `
            <h2>🎉 Easter Egg Encontrado! 🎉</h2>
            <p>Você descobriu o segredo do Dahora App!</p>
            <p>Parabéns pela curiosidade! 🚀</p>
        `;
        
        document.body.appendChild(message);
        
        setTimeout(() => {
            message.style.animation = 'fadeOut 0.5s ease forwards';
            setTimeout(() => message.remove(), 500);
        }, 3000);
    }
    
    // ===== CSS DINÂMICO =====
    
    // Adicionar estilos para animações especiais
    const style = document.createElement('style');
    style.textContent = `
        @keyframes rainbow {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(360deg); }
        }
        
        @keyframes confetti-fall {
            to {
                transform: translateY(100vh) rotate(360deg);
                opacity: 0;
            }
        }
        
        @keyframes fadeOut {
            to {
                opacity: 0;
                transform: translate(-50%, -50%) scale(0.8);
            }
        }
        
        .nav-open {
            overflow: hidden;
        }
        
        .animate-on-scroll {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.8s ease;
        }
        
        .animate-on-scroll.animate {
            opacity: 1;
            transform: translateY(0);
        }
    `;
    document.head.appendChild(style);
    
    // ===== PERFORMANCE MONITORING =====
    
    // Monitorar performance da página
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log('Dahora App - Performance Stats:');
                console.log(`Load Time: ${Math.round(perfData.loadEventEnd - perfData.loadEventStart)}ms`);
                console.log(`DOM Ready: ${Math.round(perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart)}ms`);
            }, 0);
        });
    }
    
    // ===== ACESSIBILIDADE =====
    
    // Melhorar navegação por teclado
    document.addEventListener('keydown', function(e) {
        // Tab navigation highlight
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });
    
    document.addEventListener('mousedown', function() {
        document.body.classList.remove('keyboard-navigation');
    });
    
    // Adicionar estilos para navegação por teclado
    const a11yStyle = document.createElement('style');
    a11yStyle.textContent = `
        .keyboard-navigation *:focus {
            outline: 2px solid #6366f1 !important;
            outline-offset: 2px !important;
        }
        
        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
    `;
    document.head.appendChild(a11yStyle);
});

// ===== FUNÇÕES GLOBAIS =====

// Função para copiar texto (simulação)
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copiado para área de transferência!', 'success');
        });
    } else {
        // Fallback para navegadores mais antigos
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification('Copiado para área de transferência!', 'success');
    }
}

// Sistema de notificações
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#6366f1'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        max-width: 300px;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease forwards';
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

// Adicionar estilos para notificações
const notificationStyle = document.createElement('style');
notificationStyle.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(notificationStyle);

// ===== FAQ ACCORDION =====

// Função global para toggle FAQ
function toggleFAQ(element) {
    const faqItem = element.closest('.faq-item');
    const wasActive = faqItem.classList.contains('active');

    // Fechar todos os itens
    document.querySelectorAll('.faq-item').forEach(item => {
        item.classList.remove('active');
    });

    // Abrir o item clicado se não estava ativo
    if (!wasActive) {
        faqItem.classList.add('active');

        // Scroll suave para o item
        setTimeout(() => {
            faqItem.scrollIntoView({
                behavior: 'smooth',
                block: 'nearest'
            });
        }, 100);
    }
}

// Inicializar FAQ accordion
document.addEventListener('DOMContentLoaded', function() {
    // Adicionar interatividade aos itens FAQ
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const header = item.querySelector('.faq-header');

        if (header) {
            header.addEventListener('click', function() {
                toggleFAQ(header);
            });
        }

        // Adicionar suporte a teclado
        header.setAttribute('tabindex', '0');
        header.setAttribute('role', 'button');
        header.setAttribute('aria-expanded', 'false');

        header.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleFAQ(header);
            }
        });
    });

    // Atualizar ARIA quando mudar estado
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(mutation => {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                const item = mutation.target;
                const header = item.querySelector('.faq-header');
                const isActive = item.classList.contains('active');

                if (header) {
                    header.setAttribute('aria-expanded', isActive);
                }
            }
        });
    });

    faqItems.forEach(item => {
        observer.observe(item, {
            attributes: true,
            attributeFilter: ['class']
        });
    });

    // Abrir primeiro FAQ por padrão (opcional)
    const firstFaq = document.querySelector('.faq-item');
    if (firstFaq && window.innerWidth > 768) {
        setTimeout(() => {
            firstFaq.classList.add('active');
            const firstHeader = firstFaq.querySelector('.faq-header');
            if (firstHeader) {
                firstHeader.setAttribute('aria-expanded', 'true');
            }
        }, 500);
    }
});