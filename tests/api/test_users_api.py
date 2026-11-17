import pytest


@pytest.mark.api
def test_users_register_empty_body_returns_422_with_field_errors(api):
    """Goal: server-side validation on user registration.
    Precondition: none.
    Expected: 422 status and error lists for 'email' and 'password' fields."""
    response = api.post("/users/register", data={})
    assert response.status == 422, response.text()
    errors = response.json()
    assert "email" in errors and "password" in errors, errors


@pytest.mark.api
def test_users_me_with_token_returns_own_profile(api, auth_headers, test_user):
    """Goal: authenticated profile access via bearer token.
    Precondition: user registered by the fixture.
    Expected: 200 status and returned email matches the registered user email."""
    response = api.get("/users/me", headers=auth_headers)
    assert response.status == 200, response.text()
    assert response.json()["email"] == test_user["email"]
