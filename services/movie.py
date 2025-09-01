from db.models import Movie
from django.db import transaction, models


def get_movies(title: str | None = None) -> models.QuerySet:
    qs = Movie.objects.all()
    if title:
        qs = qs.filter(title__icontains=title)
    return qs


@transaction.atomic
def create_movie(title: str, description: str, duration: int) -> Movie:
    movie = Movie.objects.create(
        title=title,
        description=description,
        duration=duration
    )
    return movie
