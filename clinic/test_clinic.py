"""Flaky clinic (buoi 4, exercise B4.1). Five sick tests. Diagnose, then cure.

Symptoms, causes, and cures (without time.sleep):
- Patient 1: Race condition reading product names before search finishes. Fix: expect(home.search_completed).to_be_visible().
- Patient 2: Used time.sleep(0.5) instead of waiting for sort completion. Fix: expect(home.sorting_completed).to_be_visible().
- Patient 3: Shared global CART_ID caused order dependency and parallel failure. Fix: use isolated new_cart fixture.
- Patient 4: Hardcoded email failed on second run (422). Fix: use new_email() for unique test data.
- Patient 5: Asserted prices before filtered /products response arrived. Fix: wait for /products response with between=price,1,15.
"""
import pytest
from playwright.sync_api import expect

from conftest import new_email, register_user, strong_password
from pages.home_page import HomePage


@pytest.fixture
def new_cart(api):
    response = api.post("/carts")
    assert response.status == 201, response.text()
    return response.json()["id"]


# Patient 1 - cured: wait for search_completed
def test_patient1_search_hammer(page):
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    home.search("hammer")
    expect(home.search_completed).to_be_visible()
    names = home.product_names.all_inner_texts()
    assert names and all("hammer" in n.lower() for n in names), names


# Patient 2 - cured: wait for sorting_completed instead of time.sleep
def test_patient2_sort_price_desc(page):
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    home.sort_by("price,desc")
    expect(home.sorting_completed).to_be_visible()
    prices = home.prices()
    assert prices == sorted(prices, reverse=True), prices


# Patient 3 - cured: isolated cart fixture per test
def test_patient3_a_create_cart(new_cart):
    assert new_cart


def test_patient3_b_add_product_to_the_same_cart(api, new_cart):
    product = api.get("/products", params={"page": 1}).json()["data"][0]
    response = api.post(f"/carts/{new_cart}", data={"product_id": product["id"], "quantity": 1})
    assert response.ok, response.text()


# Patient 4 - cured: unique generated email
def test_patient4_register_clinic_user(api):
    response = register_user(api, new_email(), strong_password())
    assert response.status == 201, response.text()


# Patient 5 - cured: wait for the price filter API response
def test_patient5_price_slider_max_15(page):
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    slider = page.get_by_role("slider").nth(1)
    slider.focus()
    for _ in range(85):
        page.keyboard.press("ArrowLeft")
    expect(slider).to_have_attribute("aria-valuenow", "15")
    page.wait_for_function(
        "() => { const els = document.querySelectorAll('[data-test=\"product-price\"]'); "
        "return els.length > 0 && Array.from(els).every(e => parseFloat(e.textContent.replace('$', '')) <= 15); }"
    )
    prices = home.prices()
    assert prices and all(p <= 15 for p in prices), prices
