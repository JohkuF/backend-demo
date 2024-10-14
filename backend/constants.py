from enum import Enum


# VALUES IN CENTS!!!
class CartValue:
    SMALL_CART_LIMIT = 1000
    NO_DELIVERY_FEE_LIMIT = 20000
    FEE_LIMIT = 1500


class Delivery:
    FIRST_KM_COST = 200
    AFTER_FIRST_KM = 100


class NumberOfItems:
    CART_LIMIT = 4
    SURCHARGE = 50
    EXTRA_BULK_LIMIT = 12
    EXTRA_BULK_FEE = 120


# Datetime days format
class Day(Enum):
    FRIDAY = 4


class RushHour:
    DAY = Day.FRIDAY
    START = 15
    END = 19
    FEE = 1.2
