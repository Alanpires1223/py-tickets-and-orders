from db.models import Movie
from django.db import transaction, models


def get_movies(
    title: str | None = None,
    genres_ids: list[int] | None = None,
    actors_ids: list[int] | None = None
) -> models.QuerySet:
    qs = Movie.objects.all()
    if title:
        qs = qs.filter(title__icontains=title)
    if genres_ids:
        qs = qs.filter(genres__id__in=genres_ids).distinct()
    if actors_ids:
        qs = qs.filter(actors__id__in=actors_ids).distinct()
    return qs


@transaction.atomic
def create_movie(title: str, description: str, duration: int) -> Movie:
    movie = Movie.objects.create(
        title=title,
        description=description,
        duration=duration
    )
    return movie
