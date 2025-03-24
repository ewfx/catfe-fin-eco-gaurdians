Feature: login.txt

  Scenario: 1
    Given I open the application
    Then Login using adminEmail admin@example.com and Password 12345 invalid credentials
