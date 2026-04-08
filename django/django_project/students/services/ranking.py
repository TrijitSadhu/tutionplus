import logging

from django.core.cache import cache
from django.db.models import F, Window
from django.db.models.functions import Rank

from students.models import MockTestAttempt

logger = logging.getLogger(__name__)


def rank_mocktest_attempts(mock_test_id: int):
    """Return queryset annotated with rank using PostgreSQL window function.

    Only submitted (inactive) attempts are ranked; active attempts are excluded.
    """

    return (
        MockTestAttempt.objects.filter(mock_test_id=mock_test_id, is_active=False, submitted_at__isnull=False)
        .annotate(rank=Window(expression=Rank(), order_by=F("total_score").desc(nulls_last=True)))
        .order_by("rank", "-total_score")
    )


def invalidate_leaderboard_cache(mock_test_id: int):
    cache.delete(f"leaderboard:{mock_test_id}")
    logger.debug("Invalidated leaderboard cache for mock_test_id=%s", mock_test_id)
