from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from apps.prediction.models import PredictionHistory

def get_disaster_breakdown(user):
    """Return list of {disaster_type, count} for the user."""
    counts = (
        PredictionHistory.objects.filter(user=user)
        .values('predicted_disaster')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    return [{'disaster_type': item['predicted_disaster'], 'count': item['count']} for item in counts]


def get_most_common_disaster(user):
    """Return the most frequent disaster type or None."""
    breakdown = get_disaster_breakdown(user)
    return breakdown[0]['disaster_type'] if breakdown else None


def get_monthly_trends(user, months_back=6):
    """
    Return monthly counts per disaster type for the last `months_back` months.
    """
    cutoff = timezone.now() - timedelta(days=30 * months_back)
    history = PredictionHistory.objects.filter(user=user, created_at__gte=cutoff)

    # Group by year-month
    trend_data = defaultdict(lambda: defaultdict(int))
    for record in history:
        month_key = record.created_at.strftime('%Y-%m')
        trend_data[month_key][record.predicted_disaster] += 1

    # Sort months chronologically
    sorted_months = sorted(trend_data.keys())
    result = []
    for month in sorted_months:
        result.append({
            'month': month,
            'counts': dict(trend_data[month]),
            'total': sum(trend_data[month].values())
        })
    return result


def get_recent_predictions(user, limit=10):
    """Return most recent predictions ordered by created_at descending."""
    return PredictionHistory.objects.filter(user=user).order_by('-created_at')[:limit]


def get_total_predictions(user):
    """Return total number of predictions made by user."""
    return PredictionHistory.objects.filter(user=user).count()