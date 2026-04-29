import requests
from config import Config

BASE_URL = "https://www.googleapis.com/youtube/v3/search"

def search_youtube(query, max_results=20):
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": Config.YOUTUBE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return []

    items = response.json().get("items", [])
    if not items:
        return []

    video_ids = [v["id"]["videoId"] for v in items]
    stats = _get_stats(video_ids)

    for v in items:
        vid = v["id"]["videoId"]
        v["statistics"] = stats.get(vid, {})

    return items


def _get_stats(video_ids):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "statistics",
        "id": ",".join(video_ids),
        "key": Config.YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return {}
    return {
        item["id"]: item.get("statistics", {})
        for item in response.json().get("items", [])
    }


def get_video_details(video_id):
    # Détails + stats
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics",
        "id": video_id,
        "key": Config.YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None, []

    items = response.json().get("items", [])
    if not items:
        return None, []

    video = items[0]

    # 5 meilleurs commentaires (triés par likes)
    comments = _get_top_comments(video_id, max_results=5)

    return video, comments


from html import unescape

def _get_top_comments(video_id, max_results=5):
    """Récupère les 5 commentaires les plus likés."""
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": 20,
        "order": "relevance",
        "key": Config.YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    items = response.json().get("items", [])

    comments = []
    for item in items:
        top = item["snippet"]["topLevelComment"]["snippet"]
        comments.append({
            "author": unescape(top.get("authorDisplayName", "Anonyme")),
            "text": unescape(top.get("textDisplay", "")),
            "likes": top.get("likeCount", 0),
            "date": top.get("publishedAt", "")[:10]
        })

    comments.sort(key=lambda c: c["likes"], reverse=True)
    return comments[:max_results]