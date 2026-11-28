"""Buoi 4 - TIGHTENED assertions (Exercise B4.4).

Every test here stays GREEN on PROD and turns RED on BUGGY, catching real defects
with clear failure messages.
"""
import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.ui
def test_b4_a_add_to_cart_shows_a_toast(page):
    """Goal: user gets accurate feedback after add-to-cart.
    Precondition: product 'Combination Pliers' exists.
    Expected: toast confirms 'Product added to shopping cart'."""
    product = HomePage(page).open().open_product("Combination Pliers").add_to_cart()
    expect(product.toast.first).to_contain_text("Product added to shopping cart")


@pytest.mark.regression
@pytest.mark.ui
def test_b4_b_cart_has_a_total(page):
    """Goal: cart displays accurate line price and total.
    Precondition: one product, quantity 2.
    Expected: line total equals unit price x 2 and cart total equals sum of lines."""
    product = HomePage(page).open().open_product("Combination Pliers")
    unit = product.price()
    cart = product.add_to_cart(quantity=2).go_to_cart()
    expect(cart.product_titles.first).to_have_text("Combination Pliers")
    assert cart.line_totals() == [pytest.approx(unit * 2)], f"Expected line total {unit * 2}, got {cart.line_totals()}"
    assert cart.total_value() == pytest.approx(sum(cart.line_totals()))


@pytest.mark.regression
@pytest.mark.ui
def test_b4_c_search_without_results_counts_zero(page):
    """Goal: empty search state informs the user clearly.
    Precondition: none.
    Expected: 'There are no products found.' message and 0 product cards."""
    home = HomePage(page).open().search("zzz-no-such-tool")
    expect(home.no_results).to_have_text("There are no products found.")
    expect(home.product_names).to_have_count(0)


@pytest.mark.regression
@pytest.mark.ui
def test_b4_d_login_empty_form_stays_on_login(page):
    """Goal: validation of empty login form displays required messages.
    Precondition: none.
    Expected: stays on /auth/login and displays 'Email is required' and 'Password is required'."""
    login = LoginPage(page).open()
    login.submit_button.click()
    expect(page).to_have_url(re.compile(r"/auth/login$"))
    expect(login.email_error).to_contain_text("Email is required")
    expect(login.password_error).to_contain_text("Password is required")


@pytest.mark.regression
@pytest.mark.ui
def test_b4_e_header_has_contact_and_search(page):
    """Goal: header controls exist with exact spelled labels.
    Precondition: none.
    Expected: Contact link says 'Contact' and Search button says 'Search'."""
    home = HomePage(page).open()
    expect(home.nav_contact).to_have_text("Contact")
    expect(home.search_button).to_have_text("Search")


@pytest.mark.regression
@pytest.mark.ui
def test_b4_f_home_lists_products(page, api):
    """Goal: catalogue is browsable across all pages when total > per_page.
    Precondition: none.
    Expected: pagination controls are visible when total products exceed per_page."""
    meta = api.get("/products", params={"page": 1}).json()
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    if meta["total"] > meta["per_page"]:
        expect(home.pagination).to_be_visible()


@pytest.mark.regression
@pytest.mark.api
def test_b4_g_search_api_finds_wrench(api):
    """Goal: search endpoint returns only matching products.
    Precondition: none.
    Expected: all returned product names contain 'wrench'."""
    names = [p["name"] for p in api.get("/products/search", params={"q": "wrench"}).json()["data"]]
    assert names and all("wrench" in n.lower() for n in names), names
