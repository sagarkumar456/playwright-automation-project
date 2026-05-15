Feature: Order Transaction
    Test related to Order  Transaction



Scenario Outline: Verify Order success message shown in details page
  Given place the item order with <username> and <password>
  And the user is on landing page
  When I login to portal with <username> and <password>
  And navigate to orders page
  And select the orderId
  Then order message is successfully displayed
  Examples:
     |        username      |   password  |
     | skdas1641999@gmail.com | sagardas456 |