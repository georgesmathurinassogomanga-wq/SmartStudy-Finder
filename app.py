from flask import Flask, render_template, request, jsonify, redirect, session
import json
from datetime import datetime
import random
import os
from services.youtube_api import search_youtube, get_video_details
from services.score import compute_score
from services.filter import filter_videos
from services.analyzer import analyze_history

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "smartstudy-secret-2026")

SUGGESTIONS = [
    "Python débutant",
    "Intelligence artificielle",
    "Développement web",
    "Structures de données",
    "Algorithmes faciles",
    "Cybersécurité basics",
    "Machine Learning introduction",
    "Linux commandes",
    "SQL pour débutants",
    "JavaScript projets"
]

# ------------------ UTIL ------------------
def get_history():
    return session.get("history", [])

def get_favorites():
    return session.get("favorites", [])

# ------------------ ACCUEIL ------------------
@app.route("/")
def index():
    return render_template(
        "index.html",
        suggestions=random.sample(SUGGESTIONS, 5),
        history=get_history(),
        results=None
    )

# ------------------ SEARCH ------------------
@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return redirect("/")

    # 1. Recherche YouTube
    results = search_youtube(query) or []

    # 2. Filtrage éducatif
    results = filter_videos(results)

    # 3. Score
    for v in results:
        v["score"] = compute_score(v)
        if v["score"] > 50:
            v["relevant"] = True

    # 4. Tri
    results.sort(key=lambda v: (v["relevant"], v["score"]), reverse=True)

    # 5. Historique en session
    history = get_history()
    history.append({
        "query": query,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    session["history"] = history[-50:]  # garde les 50 dernières
    session.modified = True

    return render_template(
        "index.html",
        results=results,
        query=query,
        suggestions=random.sample(SUGGESTIONS, 5),
        history=get_history()
    )

# ------------------ HISTORY ------------------
@app.route("/history")
def history():
    return render_template(
        "history.html",
        history=get_history(),
        active="history"
    )

@app.route("/clear_history", methods=["POST"])
def clear_history():
    session["history"] = []
    session.modified = True
    return redirect("/history")

# ------------------ FAVORITES ------------------
@app.route("/favorites")
def favorites():
    return render_template(
        "favorites.html",
        favorites=get_favorites(),
        active="favorites"
    )

@app.route("/toggle_favorite", methods=["POST"])
def toggle_favorite():
    video_id = request.json.get("id")
    title = request.json.get("title")
    favorites = get_favorites()
    exists = any(v["id"] == video_id for v in favorites)
    if exists:
        favorites = [v for v in favorites if v["id"] != video_id]
        action = "removed"
    else:
        favorites.append({"id": video_id, "title": title})
        action = "added"
    session["favorites"] = favorites
    session.modified = True
    return jsonify({"status": action})

# ------------------ ANALYTICS ------------------
@app.route("/analytics")
def analytics():
    stats = analyze_history(get_history())
    return render_template(
        "analytics.html",
        stats=stats,
        active="analytics"
    )

# ------------------ ABOUT ------------------
@app.route("/about")
def about():
    return render_template("about.html", active="about")

# ------------------ VIDEO ------------------
@app.route("/video/<video_id>")
def video_detail(video_id):
    video, comments = get_video_details(video_id)
    if not video:
        return "Erreur récupération vidéo 😅"
    score = compute_score(video)

    # Vérifie si déjà en favori
    is_favorite = any(v["id"] == video_id for v in get_favorites())

    return render_template(
        "video.html",
        video=video,
        comments=comments,
        score=score,
        is_favorite=is_favorite
    )

# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(debug=True)