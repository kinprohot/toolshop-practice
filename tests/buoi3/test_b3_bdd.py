"""Buoi 3 - BDD with pytest-bdd. Step definitions only call page objects (no new locators here).

Run:  pytest tests/buoi3 -v
Each Examples row becomes its own pytest test - read the test names in the output.
"""
import pytest
from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from pages.home_page import HomePage

pytestmark = [pytest.mark.bdd, pytest.mark.ui]

scenarios("../../buoi3/features/search.feature", "../../buoi3/features/cart.feature")


# ---------------------------------------------------------------- given (B3.1: read and run)
@given("I am on the home page", target_fixture="home")
def home(page):
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    return home


@when(parsers.parse('I search for "{keyword}"'))
def search(home, keyword):
    home.search(keyword)


@then(parsers.parse('every product name contains "{keyword}"'))
def names_contain(home, keyword):
    expect(home.search_completed).to_be_visible()
    names = home.product_names.all_inner_texts()
    assert names and all(keyword.lower() in n.lower() for n in names), names


# ---------------------------------------------------------------- B3.2: the two missing steps
@then(parsers.parse('the search caption mentions "{keyword}"'))
def caption_mentions(home, keyword):
    expect(home.search_caption).to_contain_text(keyword)


@then(parsers.parse('I see the message "{message}"'))
def see_message(home, message):
    expect(home.no_results).to_have_text(message)
    expect(home.product_names).to_have_count(0)


# ---------------------------------------------------------------- B3.4: steps for cart.feature
@when(parsers.parse('I open the product "{product}"'), target_fixture="product_page")
def open_product(home, product):
    return home.open_product(product)


@when(parsers.parse("I add it to the cart with quantity {quantity:d}"), target_fixture="unit_price")
def add_to_cart(product_page, quantity):
    unit = product_page.price()
    product_page.add_to_cart(quantity=quantity)
    return unit


@when("I go to the cart", target_fixture="cart_page")
def go_to_cart(product_page):
    return product_page.go_to_cart()


@then(parsers.parse("the line total equals the unit price times {quantity:d}"))
def line_total(cart_page, unit_price, quantity):
    expect(cart_page.product_titles.first).to_be_visible()
    assert cart_page.line_totals() == [pytest.approx(unit_price * quantity)]
