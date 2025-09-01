from db.models import Order, Ticket, User, MovieSession
from django.db import transaction, models
from datetime import datetime


@transaction.atomic
def create_order(
    tickets: list[dict], username: str, date: str | None = None
) -> Order:
    user = User.objects.get(username=username)
    order_data = {}

    if date:
        order_data["created_at"] = datetime.strptime(
            date,
            "%Y-%m-%d %H:%M"
        )

    order = Order.objects.create(user=user, **order_data)

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket_data["movie_session"]
        )
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )

    return order


def get_orders(username: str | None = None) -> models.QuerySet:
    qs = Order.objects.all()

    if username:
        qs = qs.filter(user__username=username)

    return qs
