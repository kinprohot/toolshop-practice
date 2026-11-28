import pytest
from playwright.sync_api import expect

from pages.account_page import AccountPage
from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.login_page import LoginPage


# ---------------------------------------------------------------- Group 1: Danh sách và tìm kiếm
@pytest.mark.ui
def test_search_unknown_keyword_shows_no_results(page):
    """Goal: verify empty search result state.
    Precondition: none.
    Expected: 'There are no products found.' message and zero product cards."""
    home = HomePage(page).open().search("zzz-no-such-tool")
    expect(home.no_results).to_have_text("There are no products found.")
    expect(home.product_names).to_have_count(0)


@pytest.mark.ui
@pytest.mark.parametrize("order", ["price,asc", "price,desc"])
def test_sort_by_price_orders_products(page, order):
    """Goal: sorting products by price in ascending and descending directions.
    Precondition: none.
    Expected: prices on the first page are ordered according to the chosen sort direction."""
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    home.sort_by(order)
    expect(home.sorting_completed).to_be_visible()
    prices = home.prices()
    assert prices == sorted(prices, reverse=order.endswith("desc")), prices


# ---------------------------------------------------------------- Group 2: Bộ lọc
@pytest.mark.ui
def test_filter_by_category_hammer_shows_matching_products(page):
    """Goal: category filter shows only products belonging to the selected category.
    Precondition: none.
    Expected: every product name in the filtered results contains 'Hammer'."""
    home = HomePage(page).open().filter_by_category("Hammer")
    expect(home.product_names.first).to_contain_text("Hammer")
    names = home.product_names.all_inner_texts()
    assert names, "No products displayed for category Hammer"
    assert all("hammer" in n.lower() for n in names), names


# ---------------------------------------------------------------- Group 3: Chi tiết sản phẩm
@pytest.mark.ui
def test_product_detail_shows_correct_name_and_price(page):
    """Goal: product details page displays correct product information.
    Precondition: product 'Combination Pliers' exists in the catalog.
    Expected: product title is 'Combination Pliers' and unit price is a valid positive value."""
    product = HomePage(page).open().open_product("Combination Pliers")
    expect(product.name).to_have_text("Combination Pliers")
    assert product.price() > 0


# ---------------------------------------------------------------- Group 4: Giỏ hàng
@pytest.mark.ui
def test_cart_line_price_equals_unit_price_times_quantity(page):
    """Goal: cart calculates line totals correctly based on quantity.
    Precondition: fresh browser context with an empty cart.
    Expected: line price equals unit price times 2 and total matches the line sum."""
    product = HomePage(page).open().open_product("Combination Pliers")
    unit = product.price()
    product.add_to_cart(quantity=2)
    expect(product.cart_quantity).to_have_text("2")
    cart = product.go_to_cart()
    expect(cart.product_titles).to_have_count(1)
    assert cart.line_totals() == [pytest.approx(unit * 2)]
    assert cart.total_value() == pytest.approx(sum(cart.line_totals()))


@pytest.mark.ui
def test_cart_continue_shopping_returns_to_home(page):
    """Goal: continue shopping button returns user to home product grid.
    Precondition: one product added to cart.
    Expected: product grid on the home page is visible after clicking continue shopping."""
    cart = HomePage(page).open().open_product("Hammer").add_to_cart().go_to_cart()
    expect(cart.product_titles.first).to_have_text("Hammer")
    cart.continue_shopping.click()
    expect(HomePage(page).product_names.first).to_be_visible()


# ---------------------------------------------------------------- Group 5: Xác thực
@pytest.mark.ui
def test_login_empty_form_shows_required_errors(page):
    """Goal: client-side required field validation on empty login submission.
    Precondition: none.
    Expected: 'Email is required' and 'Password is required' error messages appear."""
    login = LoginPage(page).open()
    login.submit_button.click()
    expect(login.email_error).to_contain_text("Email is required")
    expect(login.password_error).to_contain_text("Password is required")


# ---------------------------------------------------------------- Group 6: Liên hệ, tài khoản
@pytest.mark.ui
def test_account_page_logged_in_shows_user_menu(logged_in_page):
    """Goal: reuse saved authentication state via logged_in_page fixture.
    Precondition: user authenticated once using storage_state.
    Expected: Account page title is 'My account' and user navigation menu shows account name."""
    account = AccountPage(logged_in_page).open()
    expect(account.title).to_have_text("My account")
    expect(account.nav_menu).to_contain_text("QA Bot")


@pytest.mark.ui
def test_contact_without_subject_shows_error(page):
    contact = ContactPage(page).open()
    contact.first_name.fill("Linh")
    contact.last_name.fill("Nguyen")
    contact.email.fill("linh@example.com")
    contact.message.fill("Hello, I need help with my order number 12345678901234567890.")
    contact.submit()
    expect(contact.subject_error).to_be_visible()
