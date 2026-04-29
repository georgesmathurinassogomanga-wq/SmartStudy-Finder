from flask import Flask, render_template, request, jsonify, redirect
import json
from datetime import datetime
import random
from services.youtube_api import search_youtube, get_video_details
from services.score import compute_score
from services.filter import filter_videos
from services.analyzer import analyze_history

app = Flask(__name__)

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

def get_history():
    try:
        with open("data/history.json", "r") as f:
            return json.load(f)
    except:
        return []

@app.route("/")
def index():
    return render_template(
        "index.html",
        suggestions=random.sample(SUGGESTIONS, 5),
        history=get_history(),
        results=None
    )

@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return redirect("/")

    # 1. Recherche YouTube
    results = search_youtube(query) or []

    # 2. Filtrage — garde uniquement les vidéos éducatives
    results = filter_videos(results)

    # 3. Score
    for v in results:
        v["score"] = compute_score(v)
        if v["score"] > 50:
            v["relevant"] = True

    # 4. Tri : pertinents en premier, puis par score décroissant
    results.sort(key=lambda v: (v["relevant"], v["score"]), reverse=True)

    # 5. Historique
    try:
        with open("data/history.json", "r+") as f:
            data = json.load(f)
            data.append({
                "query": query,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
    except:
        pass

    return render_template(
        "index.html",
        results=results,
        query=query,
        suggestions=random.sample(SUGGESTIONS, 5),
        history=get_history()
    )

@app.route("/history")
def history():
    return render_template("history.html", history=get_history(), active="history")

@app.route("/favorites")
def favorites():
    try:
        with open("data/favorites.json") as f:
            favs = json.load(f)
    except:
        favs = []
    return render_template("favorites.html", favorites=favs, active="favorites")

@app.route("/toggle_favorite", methods=["POST"])
def toggle_favorite():
    video_id = request.json.get("id")
    title = request.json.get("title")
    try:
        with open("data/favorites.json", "r+") as f:
            data = json.load(f)
            exists = any(v["id"] == video_id for v in data)
            if exists:
                data = [v for v in data if v["id"] != video_id]
                action = "removed"
            else:
                data.append({"id": video_id, "title": title})
                action = "added"
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
        return jsonify({"status": action})
    except:
        return jsonify({"status": "error"})

@app.route("/analytics")
def analytics():
    history = get_history()
    stats = analyze_history(history)
    return render_template("analytics.html", stats=stats, active="analytics")

@app.route("/about")
def about():
    return render_template("about.html", active="about")

@app.route("/video/<video_id>")
def video_detail(video_id):
    video, comments = get_video_details(video_id)
    if not video:
        return "Erreur récupération vidéo 😅"
    score = compute_score(video)
    return render_template("video.html", video=video, comments=comments, score=score)

if __name__ == "__main__":
    app.run(debug=True)