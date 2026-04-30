// =====================
// THEME
// =====================
function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
    const btn = document.getElementById("theme-toggle");
    if (btn) btn.textContent = theme === "dark" ? "☀️ Clair" : "🌙 Sombre";
}

function toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme");
    applyTheme(current === "dark" ? "light" : "dark");
}

// Applique le thème sauvegardé au chargement
(function () {
    const saved = localStorage.getItem("theme");
    if (saved) {
        applyTheme(saved);
    } else {
        // Détecte la préférence système
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        applyTheme(prefersDark ? "dark" : "light");
    }
})();

// =====================
// BURGER MENU
// =====================
function toggleMenu() {
    const links = document.getElementById("nav-links");
    const overlay = document.getElementById("nav-overlay");
    const burger = document.getElementById("burger-btn");
    links.classList.toggle("open");
    overlay.classList.toggle("open");
    burger.textContent = links.classList.contains("open") ? "✕" : "☰";
}

function closeMenu() {
    const links = document.getElementById("nav-links");
    const overlay = document.getElementById("nav-overlay");
    const burger = document.getElementById("burger-btn");
    links.classList.remove("open");
    overlay.classList.remove("open");
    burger.textContent = "☰";
}

// =====================
// INIT
// =====================
console.log("SmartStudy Finder loaded");

function showMessage(text) {
    const msg = document.getElementById("fav-msg");
    if (!msg) return;
    msg.textContent = text;
    msg.style.opacity = "1";
    setTimeout(() => { msg.style.opacity = "0"; }, 2000);
}

function searchAgain(query) {
    window.location.href = "/search?q=" + encodeURIComponent(query);
}

// =====================
// VOIX
// =====================
function startVoice() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        alert("Utilise Chrome pour la reconnaissance vocale.");
        return;
    }
    const recognition = new SpeechRecognition();
    const mic = document.getElementById("mic-btn");
    recognition.lang = "fr-FR";
    recognition.continuous = false;
    recognition.interimResults = false;
    if (mic) mic.classList.add("listening");
    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        const input = document.getElementById("search-input");
        if (input) {
            input.value = transcript;
            input.closest("form").submit();
        }
    };
    recognition.onerror = function (event) {
        if (event.error === "not-allowed") alert("Autorise le microphone dans les paramètres.");
        else alert("Erreur microphone : " + event.error);
        if (mic) mic.classList.remove("listening");
    };
    recognition.onend = function () {
        if (mic) mic.classList.remove("listening");
    };
    recognition.start();
}

// =====================
// HISTORIQUE & FAVORIS
// =====================
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("search-input");
    const historyBox = document.getElementById("history-box");
    if (input && historyBox) {
        input.addEventListener("focus", () => { historyBox.style.display = "block"; });
        document.addEventListener("click", (e) => {
            if (!e.target.closest(".search-box")) historyBox.style.display = "none";
        });
    }

    const btn = document.getElementById("fav-btn");
    if (btn) {
        btn.addEventListener("click", async () => {
            const id = btn.dataset.id;
            const title = btn.dataset.title;
            const res = await fetch("/toggle_favorite", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id, title })
            });
            const data = await res.json();
            if (data.status === "added") {
                btn.classList.add("active");
                btn.textContent = "✔ Retirer des favoris";
                showMessage("Ajouté aux favoris ⭐");
            } else if (data.status === "removed") {
                btn.classList.remove("active");
                btn.textContent = "⭐ Ajouter aux favoris";
                showMessage("Retiré des favoris ❌");
            } else {
                showMessage("Erreur ⚠️");
            }
        });
    }
});