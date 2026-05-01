document.addEventListener("DOMContentLoaded", function () {

    /* ================= COUNTDOWN ================= */
    const countdown = document.getElementById("countdown");

    if (countdown) {

        const fechaTexto = countdown.dataset.fecha;
        const fechaEvento = new Date(fechaTexto).getTime();

        const diasEl = document.getElementById("dias");
        const horasEl = document.getElementById("horas");
        const minutosEl = document.getElementById("minutos");
        const segundosEl = document.getElementById("segundos");

        let finalizado = false;

        const intervalo = setInterval(function () {

            const ahora = new Date().getTime();
            const diferencia = fechaEvento - ahora;

            if (diferencia <= 0) {

                if (!finalizado) {
                    finalizado = true;
                    clearInterval(intervalo);

                    countdown.innerHTML = "";
                    countdown.style.display = "block";

                    const finalMsg = document.createElement("div");
                    finalMsg.className = "evento-finalizado";

                    const color = countdown.style.color || countdown.dataset.color;
                    if (color) finalMsg.style.color = color;

                    finalMsg.textContent = "¡EL EVENTO YA EMPEZÓ!";

                    countdown.appendChild(finalMsg);
                }

                return;
            }

            if (diasEl && horasEl && minutosEl && segundosEl) {

                diasEl.textContent = Math.floor(diferencia / (1000 * 60 * 60 * 24));

                horasEl.textContent = String(
                    Math.floor((diferencia % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
                ).padStart(2, '0');

                minutosEl.textContent = String(
                    Math.floor((diferencia % (1000 * 60 * 60)) / (1000 * 60))
                ).padStart(2, '0');

                segundosEl.textContent = String(
                    Math.floor((diferencia % (1000 * 60)) / 1000)
                ).padStart(2, '0');
            }

        }, 1000);
    }


    /* ================= DROPDOWN ================= */
    document.querySelectorAll('.dropdown > a').forEach(menu => {
        menu.addEventListener('click', function (e) {

            if (window.innerWidth <= 768) {
                e.preventDefault();

                document.querySelectorAll('.dropdown').forEach(d => {
                    if (d !== this.parentElement) {
                        d.classList.remove('active');
                    }
                });

                this.parentElement.classList.toggle('active');
            }

        });
    });

    document.addEventListener('click', function (e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown').forEach(d => {
                d.classList.remove('active');
            });
        }
    });


    /* ================= AVISO ================= */
    const aviso = document.getElementById('aviso-modal');
    const btnAviso = document.getElementById('btn-aviso');

    if (aviso && btnAviso) {
        btnAviso.addEventListener('click', function () {
            aviso.style.display = 'none';
        });
    }


    /* ================= MENU ================= */
    const toggle = document.getElementById('menu-toggle');
    const navLinks = document.getElementById('nav-links');

    if (toggle && navLinks) {
        toggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            toggle.textContent = navLinks.classList.contains('active') ? '✕' : '☰';
        });
    }


    /* ================= MODAL ================= */
    const modal = document.getElementById("modal-img");

    if (modal) {

        const img = document.getElementById("ev-img-grande");
        const titulo = document.getElementById("ev-modal-titulo");
        const desc = document.getElementById("ev-modal-desc");
        const fecha = document.getElementById("ev-modal-fecha");
        const hora = document.getElementById("ev-modal-hora");
        const categoria = document.getElementById("ev-modal-cat");
        const btnWa = document.getElementById("ev-btn-wa");
        const cerrarBtn = document.getElementById("ev-cerrar");

        let galeriaImgs = [];
        let currentIndex = 0;
        let modoGaleria = false; // 🔥 clave para no romper eventos

        function abrirModalEvento(data) {

            if (!img) return;

            modoGaleria = false;

            img.src = data.img;
            img.alt = data.titulo || "evento";

            if (titulo) titulo.textContent = data.titulo || "";
            if (desc) desc.innerHTML = data.desc || "";
            if (fecha) fecha.textContent = data.fecha || "";
            if (hora) hora.textContent = data.hora || "";

            if (categoria) {
                categoria.textContent = data.cat || "";
                categoria.style.background = data.bg || "#eee";
                categoria.style.color = data.color || "#333";
            }

            if (btnWa) {
                const msg = encodeURIComponent(
                    `Hola, estoy interesado en el evento: ${data.titulo}`
                );
                btnWa.href = `https://wa.me/573001234567?text=${msg}`;
            }

            modal.classList.remove("solo-img");
            modal.classList.add("active");
            document.body.style.overflow = "hidden";
        }

        function abrirModalGaleria(src) {

            if (!img) return;

            modoGaleria = true;

            img.src = src;

            modal.classList.add("solo-img");
            modal.classList.add("active");
            document.body.style.overflow = "hidden";
        }

        function cerrarModal() {
            modal.classList.remove("active");
            document.body.style.overflow = "auto";
        }

        /* EVENTOS */
        document.querySelectorAll(".evento-card").forEach(card => {
            card.addEventListener("click", () => {
                abrirModalEvento({
                    img: card.dataset.img,
                    titulo: card.dataset.titulo,
                    desc: card.dataset.desc,
                    fecha: card.dataset.fecha,
                    hora: card.dataset.hora,
                    cat: card.dataset.cat,
                    bg: card.dataset.bg,
                    color: card.dataset.color
                });
            });
        });

        /* GALERÍA */
        document.querySelectorAll(".galeria-item").forEach((item, index) => {

            galeriaImgs.push(item.dataset.img);

            item.addEventListener("click", () => {
                currentIndex = index;
                abrirModalGaleria(galeriaImgs[currentIndex]);
            });

        });

        function cambiarImagen(direccion) {

            if (!modal.classList.contains("active") || !modoGaleria) return;

            currentIndex += direccion;

            if (currentIndex < 0) currentIndex = galeriaImgs.length - 1;
            if (currentIndex >= galeriaImgs.length) currentIndex = 0;

            img.src = galeriaImgs[currentIndex];
        }

        /* TECLADO */
        document.addEventListener("keydown", function (e) {

            if (!modal.classList.contains("active")) return;

            if (e.key === "Escape") cerrarModal();

            if (modoGaleria) {
                if (e.key === "ArrowRight") cambiarImagen(1);
                if (e.key === "ArrowLeft") cambiarImagen(-1);
            }

        });

        /* SWIPE */
        let startX = 0;

        modal.addEventListener("touchstart", (e) => {
            startX = e.touches[0].clientX;
        });

        modal.addEventListener("touchend", (e) => {

            if (!modoGaleria) return;

            let endX = e.changedTouches[0].clientX;
            let diff = startX - endX;

            if (Math.abs(diff) > 50) {
                if (diff > 0) cambiarImagen(1);
                else cambiarImagen(-1);
            }

        });

        /* CERRAR */
        if (cerrarBtn) {
            cerrarBtn.addEventListener("click", cerrarModal);
        }

        modal.addEventListener("click", (e) => {
            if (e.target === modal) cerrarModal();
        });

    }

});