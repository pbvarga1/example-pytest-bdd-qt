Feature: Example
   The main window

Scenario: Pushing the button first
    Given The window
    When I press the button
    Then The text is "foo"

Scenario: Pushing the button twice
    Given The window
    When I press the button
    And I press the button
    Then The text is "bar"

Scenario: Edit Text
    Given The window
    When I type "life"
    Then The text is "life"

Scenario: Edit Text then press button
    Given The window
    When I type "life"
    And I press the button
    Then The text is "foo"

Scenario: Edit Text then press button then edit again
    Given The window
    When I type "life"
    And I press the button
    And I type "42"
    Then The text is "42"
