from db.models import Movie, Genre, Actor
from django.db import transaction
from typing import List


def get_movies() -> List[Movie]:
    """
    Retorna todos os filmes cadastrados.

    Returns:
        List[Movie]: Lista de filmes.
    """
    return list(Movie.objects.all())


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: List[int],
    actors_ids: List[int]
) -> Movie:
    """
    Cria um filme e associa gêneros e atores.

    Args:
        movie_title (str): Título do filme.
        movie_description (str): Descrição do filme.
        genres_ids (List[int]): IDs dos gêneros.
        actors_ids (List[int]): IDs dos atores.

    Raises:
        ValueError: Se algum ID não for inteiro.

    Returns:
        Movie: Filme criado.
    """
    if not all(isinstance(i, int) for i in genres_ids):
        raise ValueError("Genres IDs devem ser inteiros")
    if not all(isinstance(i, int) for i in actors_ids):
        raise ValueError("Actors IDs devem ser inteiros")

    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description
    )

    movie.genres.set(Genre.objects.filter(id__in=genres_ids))
    movie.actors.set(Actor.objects.filter(id__in=actors_ids))
    return movie
