import pytest


@pytest.fixture
def new_cart(api):
    response = api.post("/carts")
    assert response.status == 201, response.text()
    return response.json()["id"]


@pytest.mark.api
def test_cart_add_product_quantity_two_is_stored(api, new_cart):
    """Goal: cart API stores the product with chosen quantity.
    Precondition: a new cart created by fixture and first product from GET /products.
    Expected: GET /carts/{id} contains 1 item with quantity 2 and matching product_id."""
    product = api.get("/products", params={"page": 1}).json()["data"][0]
    added = api.post(f"/carts/{new_cart}", data={"product_id": product["id"], "quantity": 2})
    assert added.ok, added.text()
    items = api.get(f"/carts/{new_cart}").json()["cart_items"]
    assert len(items) == 1
    assert items[0]["quantity"] == 2
    assert str(items[0]["product_id"]) == str(product["id"])
