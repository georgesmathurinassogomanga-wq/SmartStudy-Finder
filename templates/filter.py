import re

EDUCATIONAL_KEYWORDS = [
    "apprendre", "learn", "tutoriel", "tutorial",
    "cours", "lesson", "débutant", "beginner",
    "introduction", "guide", "formation",
    "exercice", "practice", "basics", "base",
    "explication", "détaillé", "comprendre",
    "comment", "how to", "étape", "step",
    "commande", "command", "master", "démarrer",
    "start", "fondamental", "essentiel", "formation",
    "comprendre", "apprend", "enseign", "éducati"
]

def normalize(text: str) -> str:
    text = text.lower()
    return re.sub(r"[^a-z0-9àâçéèêëîïôûùüÿñæœ\s]", " ", text)

def is_educational(text: str) -> bool:
    text = normalize(text)
    for keyword in EDUCATIONAL_KEYWORDS:
        if keyword.lower() in text:
            return True
    return False

def filter_videos(videos):
    """Retourne UNIQUEMENT les vidéos éducatives."""
    filtered = []
    for v in videos:
        snippet = v.get("snippet", {})
        title = snippet.get("title", "")
        desc = snippet.get("description", "")
        text = normalize(title + " " + desc)

        if is_educational(text):
            v["relevant"] = True
            filtered.append(v)  # ← on n'ajoute QUE les éducatives
        else:
            print(f"[FILTER] ❌ Exclu: '{title[:60]}'")

    print(f"[FILTER] ✅ {len(filtered)}/{len(videos)} vidéos éducatives gardées")
    return filtered