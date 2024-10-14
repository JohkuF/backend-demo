import json
import logging
from fastapi import Response
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_1():
    request = json.dumps(
        {
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": "2024-01-15T13:00:00Z",
        }
    )

    """
    Delivery_fee:
    small cost => 1000 - 790 = 210
    distance   => 2235 - 1000 => 200 & ceil(1235 / 500) = 3 => 3 * 100 == 5000
    items      => 4 <= 5 => No extra cost
    total: 210 + 500 = 710 c
    """

    response: Response = client.post("/fee", data=request)
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 710}


def test_rush_hour():
    request = json.dumps(
        {
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 4,
            "time": "2024-01-12T16:00:00Z",
        }
    )

    """
    Delivery_fee:
    small cost => 0
    distance   => 200
    items      => 4 <= 5 => No extra cost
    rush hour  => *1.2
    
    total: 240
    """

    response: Response = client.post("/fee", data=request)
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 240}


def test_over_free_delivery():
    request = json.dumps(
        {
            "cart_value": 20000,
            "delivery_distance": 1000,
            "number_of_items": 4,
            "time": "2024-01-12T16:00:00Z",
        }
    )

    response: Response = client.post("/fee", data=request)
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 0}


def test_over_bulk_fee():
    request = json.dumps(
        {
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 6,
            "time": "2024-01-16T16:00:00Z",
        }
    )

    """
    Delivery_fee:
    small cost => 0
    distance   => 200
    items      => 6 <= 5 => + 100
    rush hour  => 0
    
    total: 300
    """

    response: Response = client.post("/fee", data=request)
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 300}


def test_over_big_bulk_fee():
    request = json.dumps(
        {
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 13,
            "time": "2024-01-13T16:00:00Z",
        }
    )

    """
    Delivery_fee:
    small cost => 0
    distance   => 200
    items      => 13 <= 5 => 13-4=9 => 9*0.5=450 + 120 = 570
    rush hour  => 0
    
    total: 770
    """

    response: Response = client.post("/fee", data=request)
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 770}


def test_delivery_fee_small_order_surcharge():
    response = client.post(
        "/fee",
        data=json.dumps(
            {
                "cart_value": 890,
                "delivery_distance": 1000,
                "number_of_items": 3,
                "time": "2024-01-13T16:00:00Z",
            }
        ),
    )

    assert response.status_code == 200
    assert response.json()["delivery_fee"] == 310


def test_delivery_fee_additional_distance_surcharge():
    response = client.post(
        "/fee",
        data=json.dumps(
            {
                "cart_value": 1500,
                "delivery_distance": 1501,
                "number_of_items": 2,
                "time": "2024-01-13T16:00:00Z",
            }
        ),
    )
    assert response.status_code == 200

    assert response.json()["delivery_fee"] == 400


def test_delivery_fee_item_surcharge_and_extra_items():
    response = client.post(
        "/fee",
        data=json.dumps(
            {
                "cart_value": 1000,
                "delivery_distance": 1200,
                "number_of_items": 7,
                "time": "2024-01-13T16:00:00Z",
            }
        ),
    )
    assert response.status_code == 200
    assert response.json()["delivery_fee"] == 450


def test_delivery_fee_bulk_item_surcharge():
    response = client.post(
        "/fee",
        data=json.dumps(
            {
                "cart_value": 1000,
                "delivery_distance": 800,
                "number_of_items": 15,
                "time": "2024-01-13T16:00:00Z",
            }
        ),
    )
    assert response.status_code == 200
    assert response.json()["delivery_fee"] == 870


def test_delivery_fee_bulk_item_surcharge_with_black_friday():
    response = client.post(
        "/fee",
        data=json.dumps(
            {
                "cart_value": 1000,
                "delivery_distance": 800,
                "number_of_items": 15,
                "time": "2024-01-12T16:00:00Z",
            }
        ),
    )
    assert response.status_code == 200
    assert response.json()["delivery_fee"] == 1044


def test_delivery_fee_free_delivery():
    response = client.post(
        "/fee",
        data=json.dumps(
            {
                "cart_value": 20040,
                "delivery_distance": 500,
                "number_of_items": 200,
                "time": "2024-01-13T16:00:00Z",
            }
        ),
    )
    assert response.status_code == 200
    assert response.json()["delivery_fee"] == 0


def test_delivery_fee_friday_rush():
    response = client.post(
        "/fee",
        data=json.dumps(
            {
                "cart_value": 200,
                "delivery_distance": 1000,
                "number_of_items": 2,
                "time": "2024-01-12T16:00:00Z",
            }
        ),
    )
    assert response.status_code == 200
    assert response.json()["delivery_fee"] == 1200


def test_negative_value():
    response = client.post(
        "fee",
        data=json.dumps(
            {
                "cart_value": 200,
                "delivery_distance": 1000,
                "number_of_items": 2,
                "time": "2024-01-12T16:00:00Z",
            }
        ),
    )
    assert response.status_code == 422
