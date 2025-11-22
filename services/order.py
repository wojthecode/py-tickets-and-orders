from django.db import transaction
from django.db.models import QuerySet
from datetime import datetime as dt

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: str | None = None
) -> Order:

    order = Order.objects.create(user=User.objects.get(username=username))

    if date:
        order.created_at = dt.strptime(date, "%Y-%m-%d %H:%M")
        order.save()

    occupied = Ticket.objects.values("row", "seat", "movie_session")
    for ticket in tickets:
        if ticket in occupied:
            raise ValueError("Seat is already taken.")
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
            order=order,
        )
    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user=User.objects.get(username=username))
    return orders
