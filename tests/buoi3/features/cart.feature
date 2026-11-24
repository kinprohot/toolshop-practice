Feature: Cart line price calculation
  As a shopper
  I want the cart to calculate line totals accurately
  So that I know how much I am paying for each product

  Background:
    Given I am on the home page

  Scenario Outline: Adding a product calculates line price from unit price and quantity
    When I open the product "<product>"
    And I add it to the cart with quantity <quantity>
    And I go to the cart
    Then the line total equals the unit price times <quantity>

    Examples:
      | product            | quantity |
      | Combination Pliers | 1        |
      | Claw Hammer        | 3        |
