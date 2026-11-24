import pytest
from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from pages.home_page import HomePage

pytestmark = [pytest.mark.bdd, pytest.mark.ui]

scenarios("cart.feature")


@given("I am on the home page", target_fixture="home")
def home(page):
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    return home


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
def check_line_total(cart_page, unit_price, quantity):
    expect(cart_page.product_titles.first).to_be_visible()
    assert cart_page.line_totals() == [pytest.approx(unit_price * quantity)]
