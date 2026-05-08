Feature: E2E Flow with Netbanking Payment

  Scenario: User place order and complete payment using Kotak Netbanking

    Given User opens the product listing page

    When User selects a product from the list

    And User selects hardwiring kit and adds product to cart

    And User proceeds to cart and places the order

    And User enters contact details with phone number

    And User fills the address details

    And User selects Netbanking payment option

    Then System should capture payment ID

    And Order should be verified in Control system