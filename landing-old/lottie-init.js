// Lottie microinterações inspiradas em Fluent
// Carrega animações leves em ícones dos cards. Fallback silencioso se lottie não estiver disponível.

(function initLottie() {
  try {
    if (!window.lottie) {
      return; // Sem lottie-web, mantém ícones estáticos
    }

    const map = {
      'fa-mouse-pointer': 'https://assets10.lottiefiles.com/packages/lf20_nioqglkb.json',
      'fa-keyboard': 'https://assets8.lottiefiles.com/packages/lf20_5q2glscc.json',
      'fa-clock': 'https://assets10.lottiefiles.com/packages/lf20_6e1q3qql.json',
      'fa-history': 'https://assets4.lottiefiles.com/packages/lf20_1yyb1x1p.json',
      'fa-bell': 'https://assets2.lottiefiles.com/packages/lf20_io7xry9a.json',
      'fa-shield-alt': 'https://assets6.lottiefiles.com/packages/lf20_0yfsb3a9.json'
    };

    const icons = document.querySelectorAll('.feature-card .feature-icon');
    icons.forEach((holder) => {
      // identifica a classe do ícone FontAwesome dentro do holder
      const i = holder.querySelector('i');
      if (!i) return;
      const faClass = Array.from(i.classList).find(c => c.startsWith('fa-'));
      const src = faClass ? map[faClass] : null;
      if (!src) return;

      // cria container lottie e injeta antes do <i>
      const div = document.createElement('div');
      div.style.width = '60px';
      div.style.height = '60px';
      div.style.position = 'absolute';
      div.style.inset = '0';
      div.style.margin = 'auto';
      div.style.pointerEvents = 'none';
      holder.style.position = 'relative';
      holder.insertBefore(div, i);
      i.style.opacity = '0'; // mantém fallback escondido quando lottie carrega

      const anim = lottie.loadAnimation({
        container: div,
        path: src,
        renderer: 'svg',
        loop: true,
        autoplay: true
      });

      // acelera um pouco e pausa ao sair do viewport
      anim.setSpeed(1.15);
      const observer = new IntersectionObserver((entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) anim.play(); else anim.pause();
        });
      }, { threshold: 0.2 });
      observer.observe(holder);
    });
  } catch (e) {
    // Fallback silencioso
    console.warn('[Lottie] Falha ao inicializar:', e);
  }
})();