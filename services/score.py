def compute_score(video):
    stats = video.get("statistics", {})
    try:
        likes = int(stats.get("likeCount", 0))
        views = int(stats.get("viewCount", 1))
    except:
        return 0
    if views == 0:
        return 0
    score = (likes / views) * 1000
    return min(int(score), 100)