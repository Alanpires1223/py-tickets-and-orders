from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


# ---------------------------
# Custom User
# ---------------------------
class User(AbstractUser):
    pass  # Herda tudo de AbstractUser


# ---------------------------
# Movie
# ---------------------------
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duração em minutos")

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
        ]

    def __str__(self) -> str:
        return self.title


# ---------------------------
# Order
# ---------------------------
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"<Order: {self.created_at}>"


# ---------------------------
# Ticket
# ---------------------------
class Ticket(models.Model):
    movie_session = models.ForeignKey("MovieSession", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_session", "row", "seat"], name="unique_ticket"
            )
        ]

    def clean(self) -> None:
        errors = {}
        if self.row < 1 or self.row > self.movie_session.cinema_hall.rows:
            errors["row"] = [
                f"row number must be in available range: (1, rows): "
                f"(1, {self.movie_session.cinema_hall.rows})"
            ]
        if (
            self.seat < 1
            or self.seat > self.movie_session.cinema_hall.seats_in_row
        ):
            errors["seat"] = [
                f"seat number must be in available range: (1, seats_in_row): "
                f"(1, {self.movie_session.cinema_hall.seats_in_row})"
            ]

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs) -> None:
        self.full_clean()  # chama clean() antes de salvar
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (
            f"<Ticket: {self.movie_session.movie.title} "
            f"{self.movie_session.show_time} (row: {self.row}, "
            f"seat: {self.seat})>"
        )
