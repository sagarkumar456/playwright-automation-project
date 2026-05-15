Feature: Order Transactions
  Test related to Order Transactions


  Feature: Order Transactions
  Test related to Order Transactions

  Scenario Outline: Verify order success message shown in details page
    Given user has placed an order using <username> and <password>
    And user is on landing page
    When user logs into portal with <username> and <password>
    And navigates to orders page
    And selects the orderId
    Then order success message is successfully displayed

    Examples:
      | username               | password     |
      | skdas1641999@gmail.com | Sagardas456  |


