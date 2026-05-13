/**
 * Avtomatlashtirilgan Kutubxona Tizimi - JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    initNavToggle();
    initFlashMessages();
    initAnimations();
});

/** Mobil navigatsiya */
function initNavToggle() {
    const toggle = document.getElementById('navToggle');
    const links = document.getElementById('navLinks');
    if (toggle && links) {
        toggle.addEventListener('click', () => {
            links.classList.toggle('show');
        });
    }
}

/** Forma ochish/yopish */
function toggleForm(formId) {
    const form = document.getElementById(formId);
    const icon = document.getElementById(formId + 'Icon');
    if (form) {
        form.classList.toggle('collapsed');
        if (icon) {
            icon.style.transform = form.classList.contains('collapsed')
                ? 'rotate(-90deg)' : 'rotate(0deg)';
        }
    }
}

/** Flash xabarlarni avtomatik yopish */
function initFlashMessages() {
    const container = document.getElementById('flashContainer');
    if (container) {
        setTimeout(() => {
            container.querySelectorAll('.flash-message').forEach((msg, i) => {
                setTimeout(() => {
                    msg.style.animation = 'slideIn 0.3s ease reverse forwards';
                    setTimeout(() => msg.remove(), 300);
                }, i * 200);
            });
        }, 4000);
    }
}

/** Elementlar animatsiyasi */
function initAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.stat-card, .action-card, .about-card, .card.glass-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });
}
