from django.shortcuts import render
from .mongo import collection   # now points at amazon.reviews
from datetime import datetime, timedelta
from bson.json_util import dumps


from django.shortcuts import render
from .mongo import collection
from datetime import datetime, timedelta

def dashboard(request):
    # 1) Sentiment pie (unchanged)…
    sentiment_counts = collection.aggregate([
        {"$group": {"_id": "$sentiment", "count": {"$sum": 1}}}
    ])
    sentiment_data = {d["_id"]: d["count"] for d in sentiment_counts}
    for cat in ("positive", "neutral", "negative"):
        sentiment_data.setdefault(cat, 0)

    total_reviews = sum(sentiment_data.values())
    positive_rate = (sentiment_data["positive"] / total_reviews * 100) if total_reviews else 0

    # 2) Reviews per day over the last N days
    N = 7
    today = datetime.utcnow().date()
    start_date = today - timedelta(days=N - 1)

    # Build the list of date strings YYYY-MM-DD
    dates = [(start_date + timedelta(days=i)).isoformat() for i in range(N)]

    # Aggregate counts by date string
    pipeline = [
        {"$match": {"timestamp": {"$gte": datetime.combine(start_date, datetime.min.time())}}},
        {
            "$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
                "count": {"$sum": 1}
            }
        }
    ]
    cursor = collection.aggregate(pipeline)
    counts_by_date = {doc["_id"]: doc["count"] for doc in cursor}

    # Zero-fill into the exact same order as `dates`
    counts = [counts_by_date.get(d, 0) for d in dates]

    return render(request, "reviews/dashboard.html", {
        "sentiment_data": sentiment_data,
        "total_reviews": total_reviews,
        "positive_rate": round(positive_rate, 1),
        "dates": dates,
        "counts": counts,
    })
