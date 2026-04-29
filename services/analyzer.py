def analyze_history(history):
    total = len(history)

    last_search = history[-1]["date"] if total > 0 else None

    queries = [h["query"] for h in history]

    top_query = max(set(queries), key=queries.count) if queries else None

    return {
        "total_searches": total,
        "last_search": last_search,
        "top_query": top_query
    }