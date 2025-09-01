from db.models import Order, Ticket, User, MovieSession
from django.db import transaction, models
from datetime import datetime
from typing import List, Dict, Optional


@transaction.atomic
def create_order(
    tickets: List[Dict],
    username: str,
    date: Optional[str] = None
) -> Order:
    """
    Cria um pedido (Order) e os tickets associados.

    Args:
        tickets (List[Dict]): Lista de tickets com 'movie_session', 'row',
            'seat'.
        username (str): Nome de usuário do comprador.
        date (Optional[str]): Data do pedido em formato "%Y-%m-%d %H:%M".

    Returns:
        Order: Pedido criado com sucesso.
    """
    user = User.objects.get(username=username)

    order_data = {}
    if date:
        date_format = "%Y-%m-%d %H:%M"
        parsed_date = datetime.strptime(
            date,
            date_format
        )
        order_data["created_at"] = parsed_date

    order = Order.objects.create(
        user=user,
        **order_data
    )

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


def get_orders(username: Optional[str] = None) -> models.QuerySet:
    """
    Retorna todos os pedidos ou filtrados por usuário.

    Args:
        username (Optional[str]): Nome do usuário para filtrar pedidos.

    Returns:
        QuerySet: QuerySet de Orders.
    """
    qs = Order.objects.all()
    if username:
        qs = qs.filter(
            user__username=username
        )
    return qs
