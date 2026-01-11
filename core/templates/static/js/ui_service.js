document.addEventListener('DOMContentLoaded', () => {
    // =========================================
    // 1. LÓGICA DO SLIDER / CARROSSEL
    // =========================================
    const slider = document.getElementById('portfolio-scroll');
    const dotsContainer = document.getElementById('portfolio-dots');
    
    if (slider && dotsContainer) {
        let isDown = false;
        let startX;
        let scrollLeft;
        let isDragging = false; 

        // Mouse Down
        slider.addEventListener('mousedown', (e) => {
            isDown = true;
            isDragging = false;
            slider.classList.add('cursor-grabbing');
            startX = e.pageX - slider.offsetLeft;
            scrollLeft = slider.scrollLeft;
            slider.style.scrollSnapType = 'none'; 
        });

        // Mouse Leave
        slider.addEventListener('mouseleave', () => {
            isDown = false;
            slider.classList.remove('cursor-grabbing');
            slider.style.scrollSnapType = 'x mandatory'; 
        });

        // Mouse Up
        slider.addEventListener('mouseup', () => {
            isDown = false;
            slider.classList.remove('cursor-grabbing');
            slider.style.scrollSnapType = 'x mandatory';
            setTimeout(() => { isDragging = false; }, 50);
        });

        // Mouse Move
        slider.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - slider.offsetLeft;
            const walk = (x - startX) * 2; 
            if (Math.abs(x - startX) > 5) isDragging = true;
            slider.scrollLeft = scrollLeft - walk;
        });

        // Previne clique se estiver arrastando
        const links = slider.querySelectorAll('button, a');
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                if (isDragging) {
                    e.preventDefault();
                    e.stopPropagation();
                }
            });
        });

        // Dots Logic
        function initDots() {
            dotsContainer.innerHTML = '';
            const visibleWidth = slider.clientWidth; 
            const totalWidth = slider.scrollWidth;
            if (totalWidth <= visibleWidth) return;
            
            // Cria um dot para cada "página" visual ou item
            // Simplificação: criando baseado no número de filhos para garantir navegação
            const totalItems = slider.children.length;

            for (let i = 0; i < totalItems; i++) {
                const dot = document.createElement('div');
                dot.className = "w-2.5 h-2.5 rounded-full bg-lilac-200 transition-all duration-300 cursor-pointer";
                dot.onclick = () => {
                    slider.children[i]?.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' });
                };
                dotsContainer.appendChild(dot);
            }
        }

        function updateDots() {
            const dots = dotsContainer.children;
            if (dots.length === 0) return;
            
            // Lógica simplificada: pega o item mais próximo do centro ou esquerda
            // Assumindo largura fixa + gap
            const itemWidth = 240; // Ajuste conforme seu CSS (w-52 + gap)
            const index = Math.round(slider.scrollLeft / itemWidth);

            [...dots].forEach((dot, i) => {
                if (i === index) {
                    dot.classList.remove('bg-lilac-200');
                    dot.classList.add('bg-lilac-500', 'scale-125');
                } else {
                    dot.classList.remove('bg-lilac-500', 'scale-125');
                    dot.classList.add('bg-lilac-200');
                }
            });
        }

        initDots();
        updateDots();
        slider.addEventListener('scroll', updateDots);
        window.addEventListener('resize', () => { initDots(); updateDots(); });
    }
});

// =========================================
// 2. LÓGICA DO LIGHTBOX (MODAL)
// =========================================
// Funções globais (window) para serem acessadas pelo onclick="" do HTML

window.openLightbox = function(imageUrl, title) {
    const lightbox = document.getElementById('portfolio-lightbox');
    const img = document.getElementById('lightbox-img');
    const caption = document.getElementById('lightbox-caption');

    if (!lightbox || !img) return;

    // Define conteúdo
    img.src = imageUrl;
    if(caption) caption.textContent = title || '';

    // Mostra o modal (remove hidden)
    lightbox.classList.remove('hidden');

    // Pequeno delay para permitir a transição de opacidade (fade in)
    setTimeout(() => {
        lightbox.classList.remove('opacity-0');
        img.classList.remove('scale-95');
        img.classList.add('scale-100');
    }, 10);
};

window.closeLightbox = function() {
    const lightbox = document.getElementById('portfolio-lightbox');
    const img = document.getElementById('lightbox-img');

    if (!lightbox) return;

    // Inicia animação de saída
    lightbox.classList.add('opacity-0');
    if(img) {
        img.classList.remove('scale-100');
        img.classList.add('scale-95');
    }

    // Espera a animação acabar (300ms) para esconder o elemento
    setTimeout(() => {
        lightbox.classList.add('hidden');
        if(img) img.src = ''; // Limpa src para não piscar na próxima
    }, 300);
};