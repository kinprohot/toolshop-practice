import re
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.contact_page import ContactPage


@pytest.mark.smoke
@pytest.mark.ui
def test_smoke_search_keyword_shows_matching_products(page):
    """Goal: search filters the grid.
    Precondition: none.
    Expected: caption shows the keyword and every product name contains it."""
    home = HomePage(page).open().search("pliers")
    expect(home.search_completed).to_be_visible()
    expect(home.search_caption).to_contain_text("pliers")
    names = home.product_names.all_inner_texts()
    assert names, "search returned no products"
    assert all("pliers" in n.lower() for n in names), names


@pytest.mark.smoke
@pytest.mark.ui
def test_smoke_product_add_quantity_three_updates_cart_badge(page):
    """Goal: add-to-cart uses the chosen quantity.
    Precondition: product 'Claw Hammer' exists.
    Expected: toast 'Product added to shopping cart' and the cart badge shows 3."""
    product = HomePage(page).open().open_product("Claw Hammer")
    expect(product.name).to_have_text("Claw Hammer")
    product.add_to_cart(quantity=3)
    expect(product.toast).to_contain_text("Product added to shopping cart")
    expect(product.cart_quantity).to_have_text("3")


@pytest.mark.smoke
@pytest.mark.ui
def test_smoke_login_wrong_password_shows_error(page):
    """Goal: invalid credentials are rejected.
    Precondition: an e-mail with no account. NEVER a shared account.
    Expected: 'Invalid email or password' and the URL still ends with /auth/login."""
    login = LoginPage(page).open().login("nobody-exists-sprint1@example.com", "WrongPassword123!")
    expect(login.error).to_contain_text("Invalid email or password")
    expect(page).to_have_url(re.compile(r"/auth/login$"))


@pytest.mark.smoke
@pytest.mark.ui
def test_smoke_contact_empty_form_shows_required_errors(page):
    """Goal: client-side validation on empty contact form submission.
    Precondition: none.
    Expected: 'Subject is required' and 'Message is required' error messages appear."""
    contact = ContactPage(page).open()
    contact.submit()
    expect(contact.subject_error).to_contain_text("Subject is required")
    expect(contact.message_error).to_contain_text("Message is required")
