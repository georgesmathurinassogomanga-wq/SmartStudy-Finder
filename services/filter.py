import re

EDUCATIONAL_KEYWORDS = [
    "apprendre", "learn", "tutoriel", "tutorial",
    "cours", "lesson", "débutant", "beginner",
    "introduction", "guide", "formation",
    "exercice", "practice", "basics", "base",
    "explication", "détaillé", "comprendre",
    "comment", "how to", "étape", "step",
    "commande", "command", "master", "démarrer",
    "start", "fondamental", "essentiel",
    "apprend", "enseign", "éducati"
]

def normalize(text: str) -> str:
    text = text.lower()
    return re.sub(r"[^a-z0-9àâçéèêëîïôûùüÿñæœ\s]", " ", text)

def is_educational(text: str) -> bool:
    text = normalize(text)
    return any(keyword.lower() in text for keyword in EDUCATIONAL_KEYWORDS)

def filter_videos(videos):
    """Retourne UNIQUEMENT les vidéos éducatives."""
    return [
        {**v, "relevant": True}
        for v in videos
        if is_educational(
            normalize(
                v.get("snippet", {}).get("title", "") + " " +
                v.get("snippet", {}).get("description", "")
            )
        )
    ]
