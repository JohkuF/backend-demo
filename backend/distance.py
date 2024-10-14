import math
import logging
from fastapi import APIRouter
from backend import schemas
from backend.constants import CartValue, NumberOfItems, RushHour, Delivery


router = APIRouter()


@router.post("/fee")
async def get_distance(order: schemas.Request):
    fee = round(await calculate_delivery_fee(order))
    response = schemas.Response(delivery_fee=fee)
    logging.info(f"Response sent", extra={"data": response.model_dump_json()})
    return response


async def calculate_delivery_fee(order: schemas.Request) -> int:
    assert isinstance(order, schemas.Request)

    fee = 0

    if order.cart_value >= CartValue.NO_DELIVERY_FEE_LIMIT:
        fee = 0
        return fee

    # <---------- Cart value under 10€ ---------->
    if order.cart_value < CartValue.SMALL_CART_LIMIT:
        fee += CartValue.SMALL_CART_LIMIT - order.cart_value

    # <---------- Delivery fee ---------->
    fee += Delivery.FIRST_KM_COST
    # Check if delivery is more than 1000 meters
    if order.delivery_distance >= 1000:
        fee += euros_to_cents(math.ceil((order.delivery_distance - 1000) / 500))

    # <---------- Bulk fee ---------->
    # Check if more that the limit for the cart limit for no extra bulk fee
    if order.number_of_items > NumberOfItems.CART_LIMIT:
        if order.number_of_items > NumberOfItems.EXTRA_BULK_LIMIT:
            fee += NumberOfItems.EXTRA_BULK_FEE
        fee += (order.number_of_items - 4) * NumberOfItems.SURCHARGE

    # <---------- rush hour ---------->
    _order_time = order.time.hour
    if (
        order.time.weekday() == RushHour.DAY.value
        and RushHour.START <= _order_time
        and _order_time <= RushHour.END
    ):
        fee *= RushHour.FEE

    # <---------- Too big fee ---------->
    if fee > CartValue.FEE_LIMIT:
        fee = CartValue.FEE_LIMIT

    return fee


def euros_to_cents(n: int | float) -> int:
    return n * 100
