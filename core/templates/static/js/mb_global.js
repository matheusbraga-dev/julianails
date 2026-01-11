// ==========================================
// 1. FUNÇÕES GLOBAIS (Lightbox)
// Precisam ficar FORA do DOMContentLoaded para o onclick funcionar
// ==========================================

function openLightbox(imageUrl, title) {
    const lightbox = document.getElementById('portfolio-lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxCaption = document.getElementById('lightbox-caption');

    if (!lightbox || !lightboxImg) return;

    // Define conteúdo
    lightboxImg.src = imageUrl;
    if (lightboxCaption) lightboxCaption.textContent = title;

    // Mostra o modal
    lightbox.classList.remove('hidden');
    
    // Animação de entrada (delay pequeno para o CSS processar a remoção do hidden)
    setTimeout(() => {
        lightbox.classList.remove('opacity-0');
        lightboxImg.classList.remove('scale-95');
        lightboxImg.classList.add('scale-100');
    }, 10);

    // Trava o scroll da página
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    const lightbox = document.getElementById('portfolio-lightbox');
    const lightboxImg = document.getElementById('lightbox-img');

    if (!lightbox || !lightboxImg) return;

    // Animação de saída
    lightbox.classList.add('opacity-0');
    lightboxImg.classList.remove('scale-100');
    lightboxImg.classList.add('scale-95');

    // Espera animação terminar para esconder
    setTimeout(() => {
        lightbox.classList.add('hidden');
        lightboxImg.src = ''; 
        document.body.style.overflow = 'auto'; // Destrava scroll
    }, 300);
}

// Fechar com tecla ESC
document.addEventListener('keydown', function(e) {
    const lightbox = document.getElementById('portfolio-lightbox');
    if (e.key === 'Escape' && lightbox && !lightbox.classList.contains('hidden')) {
        closeLightbox();
    }
});
document.addEventListener('DOMContentLoaded', () => {
    
    // ==========================================
    // 1. LÓGICA DO MENU MOBILE & UI GERAL
    // ==========================================
    const menuBtn = document.getElementById('mobile-menu-btn');
    const closeMenuBtn = document.getElementById('close-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const navbar = document.getElementById('navbar');

    // Função para abrir/fechar menu
    function toggleMenu() {
        if (mobileMenu) {
            mobileMenu.classList.toggle('hidden');
            // Bloqueia rolagem do fundo quando menu está aberto
            if (!mobileMenu.classList.contains('hidden')) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = 'auto';
            }
        }
    }

    // Event Listeners do Menu (com verificação se o elemento existe)
    if (menuBtn) menuBtn.addEventListener('click', toggleMenu);
    if (closeMenuBtn) closeMenuBtn.addEventListener('click', toggleMenu);

    // Fechar menu ao clicar nos links
    document.querySelectorAll('#mobile-menu a').forEach(link => {
        link.addEventListener('click', toggleMenu);
    });

    // Sombra no Navbar ao rolar
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('shadow-sm');
            } else {
                navbar.classList.remove('shadow-sm');
            }
        });
    }

    // Minimizar janelas (Cards estilo Y2K)
    document.querySelectorAll('.window-toggle').forEach(btn => {
        btn.addEventListener('click', () => {
            const win = btn.closest('.y2k-window');
            if (win) win.classList.toggle('window-collapsed');
        });
    });

    // ==========================================
    // 2. LÓGICA DO FORMULÁRIO & WHATSAPP
    // ==========================================
    const formState = document.getElementById('form-state');
    const successState = document.getElementById('success-state');
    const bookingForm = document.getElementById('booking-form');
    const resetBtn = document.getElementById('reset-btn');
    const inputDate = document.getElementById('input-date');

    // Configuração de Data Mínima (Hoje)
    if (inputDate) {
        const today = new Date().toISOString().split('T')[0];
        inputDate.setAttribute('min', today);
    }

    // Função auxiliar para alternar telas
    function showSuccessScreen() {
        if (formState && successState) {
            formState.classList.add('hidden');
            successState.classList.remove('hidden');
            
            // Rola suavemente até a mensagem de sucesso
            successState.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    // A. Verifica sessão ao carregar (se o usuário já enviou e deu refresh)
    if (sessionStorage.getItem('bookingSubmitted') === 'true') {
        showSuccessScreen();
    }

    // B. Envio do Formulário
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Captura valores
            const name = document.getElementById('input-name').value;
            const service = document.getElementById('input-service').value;
            const rawDate = inputDate.value; // Vem como AAAA-MM-DD
            const time = document.getElementById('input-time').value;
            
            // Pega número do HTML
            const whatsappNumber = this.getAttribute('data-whatsapp');

            if (!whatsappNumber) {
                alert('Erro de configuração: Número do WhatsApp não encontrado.');
                return;
            }

            // Feedback visual no botão
            const btnSubmit = bookingForm.querySelector('button[type="submit"]');
            const originalText = btnSubmit.innerHTML;
            btnSubmit.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Abrindo WhatsApp...';
            btnSubmit.disabled = true;

            // Formata a data para dia/mês/ano
            let formattedDate = rawDate;
            if (rawDate) {
                const dateParts = rawDate.split('-');
                formattedDate = `${dateParts[2]}/${dateParts[1]}/${dateParts[0]}`;
            }

            // Monta a mensagem
            const message = `Olá! Me chamo *${name}*.\nGostaria de agendar o serviço: *${service}*.\n\n📅 Data: *${formattedDate}*\n⏰ Horário: *${time}*`;

            // Abre WhatsApp após pequeno delay para UI atualizar
            setTimeout(() => {
                const url = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;
                window.open(url, '_blank');

                // Atualiza tela para sucesso
                sessionStorage.setItem('bookingSubmitted', 'true');
                showSuccessScreen();

                // Restaura botão (caso ele volte na página depois)
                btnSubmit.innerHTML = originalText;
                btnSubmit.disabled = false;
            }, 800);
        });
    }

    // C. Botão "Agendar Outro" (Refazer)
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            sessionStorage.removeItem('bookingSubmitted');
            
            // Limpa campos
            document.getElementById('input-name').value = '';
            const serviceSelect = document.getElementById('input-service');
            if (serviceSelect) serviceSelect.selectedIndex = 0;
            
            if (inputDate) inputDate.value = '';
            document.getElementById('input-time').value = '';

            // Troca telas de volta
            if (successState && formState) {
                successState.classList.add('hidden');
                formState.classList.remove('hidden');
            }
        });
    }
    
});
