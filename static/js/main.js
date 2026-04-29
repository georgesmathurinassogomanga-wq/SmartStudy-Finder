// =====================
// INIT
// =====================
console.log("SmartStudy Finder loaded");

// =====================
// MESSAGE UTILITAIRE
// =====================
function showMessage(text) {
    const msg = document.getElementById("fav-msg");
    if (!msg) return;
    msg.textContent = text;
    msg.style.opacity = "1";
    setTimeout(() => {
        msg.style.opacity = "0";
    }, 2000);
}

// =====================
// RECHERCHE RAPIDE
// =====================
function searchAgain(query) {
    window.location.href = "/search?q=" + encodeURIComponent(query);
}

// =====================
// VOIX (MICRO)
// =====================
function startVoice() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Ton navigateur ne supporte pas la reconnaissance vocale. Utilise Chrome.");
        return;
    }

    const recognition = new SpeechRecognition();
    const mic = document.getElementById("mic-btn");

    recognition.lang = "fr-FR";
    recognition.continuous = false;
    recognition.interimResults = false;

    if (mic) mic.classList.add("listening");

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        const input = document.getElementById("search-input");
        if (input) {
            input.value = transcript;
            // Lance la recherche automatiquement après la voix
            input.closest("form").submit();
        }
    };

    recognition.onerror = function(event) {
        console.error("Erreur micro:", event.error);
        if (event.error === "not-allowed") {
            alert("Accès au microphone refusé. Autorise-le dans les paramètres du navigateur.");
        } else {
            alert("Erreur microphone : " + event.error);
        }
        if (mic) mic.classList.remove("listening");
    };

    recognition.onend = function() {
        if (mic) mic.classList.remove("listening");
    };

    recognition.start();
}

// =====================
// HISTORIQUE
// =====================
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("search-input");
    const historyBox = document.getElementById("history-box");

    if (input && historyBox) {
        input.addEventListener("focus", () => {
            historyBox.style.display = "block";
        });
        document.addEventListener("click", (e) => {
            if (!e.target.closest(".search-box")) {
                historyBox.style.display = "none";
            }
        });
    }

    // =====================
    // FAVORIS
    // =====================
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

// =====================
// THEME
// =====================
function toggleTheme() {
    document.body.classList.toggle("dark-mode");
}