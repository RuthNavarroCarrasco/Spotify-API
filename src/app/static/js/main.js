document.addEventListener('DOMContentLoaded', function () {
    const artistSections = document.querySelectorAll('.artist-section');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            } else {
                entry.target.classList.remove('visible');
            }
        });
    }, { threshold: 0.5 });

    artistSections.forEach(section => {
        observer.observe(section);
    });

    document.addEventListener('scroll', function () {
        artistSections.forEach(section => {
            const media = section.querySelector('.artist-media img');
            const stats = section.querySelector('.artist-stats');
            const rect = section.getBoundingClientRect();

            // Efecto para escalar la imagen cuando la sección esté visible
            if (rect.top >= 0 && rect.top <= window.innerHeight) {
                const progress = (window.innerHeight - rect.top) / window.innerHeight;
                if (progress <= 0.6) {
                    media.style.transform = `scale(${1 + progress * 0.5})`;
                } else {
                    section.classList.add('small-view'); // Se mantiene el tamaño pequeño y aparecen las estadísticas
                }
            } else {
                section.classList.remove('small-view'); // Restablece el tamaño
            }
        });
    });
});
