from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class Request(BaseModel):
    cart_value: int = Field(
        ...,
        # alias="cartValue",
        description="Value of the shopping cart in cents. 790 (790 cents = 7.90€)",
    )
    delivery_distance: int = Field(
        ...,
        # alias="deliveryDistance",
        description="The distance between the store and customer's location in meters. 2235 (2235 meters = 2.235 km)",
    )
    number_of_items: int = Field(
        ...,
        # alias="numberOfItems",
        description="The number of items in the customer's shopping cart. 4 (customer has 4 items in the cart)",
    )
    time: datetime = Field(
        ...,
        # alias="time",
        description="Order time in UTC in ISO format. 2024-01-15T13:00:00Z",
    )

    @field_validator("cart_value", "delivery_distance", "number_of_items")
    def is_positive(cls, v):
        if v < 0:
            raise ValueError("Value can't be negative")
        return v


class Response(BaseModel):
    delivery_fee: int = Field(
        ...,
        # alias="deliveryFee",
        description="Calculated delivery fee in cents. 710 (710 cents = 7.10€)",
    )
