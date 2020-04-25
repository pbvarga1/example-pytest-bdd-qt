[![Build Status](https://travis-ci.com/pbvarga1/example-pytest-bdd-qt.svg?branch=master)](https://travis-ci.com/pbvarga1/example-pytest-bdd-qt)

# Example pytest-qt + pytest-bdd

This is a very simple and short example of using pytest-qt in conjuction with
pytest-bdd. I tried to write up an explanation on the steps I took as some help
but I don't intend it to be a complete or even good guide. Just as a reference
if you get a bit confused with the code.

## Setup

```bash
$ pip install -e .
$ pip install PyQt5 or PySide2
$ pip install -r requirements.txt
```

## Run Tests

```bash
$ pytest tests -v
```

## Guide

### Pre-Reading

* You are expected to know how to write a qt application. See
  [ZetCode](http://zetcode.com/gui/qt5/) for a good introduction
* https://docs.pytest.org
* https://pytest-qt.readthedocs.io
* https://pytest-bdd.readthedocs.io/

### The App

The app will consist of one line edit and one button. When the button is
pressed, it will set the text of the line edit to ``foo``, ``bar``, and ``baz``
in a cycle. The line edit can be changed and will be overwritten by the button.
These are the only features because it allows for simple ``qtbot`` mouse and
keyboard interaction as well as simple signal-slot interaction. Most apps will
just be more larger and more complex versions of this project so this should be
enough for people to use as a complete example.

### Testing

In TDD fashion, let's write our feature file first
``tests/feature/example.feature``:

```Gherkin
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
```

Note: You may notice it's not exactly the same as the file which is on purpose.

Now we know what features we want to implement and the behaviors we expect to
see. Let's generate our test file using ``pytest-bdd generate``

```bash
$ pytest-bdd generate tests/feature/example.feature > tests/test_example.py
```

Which will create the following output:

```python
# coding=utf-8
"""Example feature tests."""

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)


@scenario('features/example.feature', 'Edit Text')
def test_edit_text():
    """Edit Text."""


@scenario('features/example.feature', 'Edit Text then press button')
def test_edit_text_then_press_button():
    """Edit Text then press button."""


@scenario('features/example.feature', 'Pushing the button first')
def test_pushing_the_button_first():
    """Pushing the button first."""


@scenario('features/example.feature', 'Pushing the button twice')
def test_pushing_the_button_twice():
    """Pushing the button twice."""


@given('The window')
def the_window():
    """The window."""
    raise NotImplementedError


@when('I press the button')
def i_press_the_button():
    """I press the button."""
    raise NotImplementedError


@when('I type "42"')
def i_type_42():
    """I type "42"."""
    raise NotImplementedError


@when('I type "life"')
def i_type_life():
    """I type "life"."""
    raise NotImplementedError


@then('The text is "42"')
def the_text_is_42():
    """The text is "42"."""
    raise NotImplementedError


@then('The text is "bar"')
def the_text_is_bar():
    """The text is "bar"."""
    raise NotImplementedError


@then('The text is "foo"')
def the_text_is_foo():
    """The text is "foo"."""
    raise NotImplementedError


@then('The text is "life"')
def the_text_is_life():
    """The text is "life"."""
    raise NotImplementedError
```

Let's simplify our test file by making use of several pytest-bdd features:

1. Let's be able to remove the need for writing the ``features`` path in every
   scenario. This would be especially helpful if we wrote more than one feature
   file. We will use [Feature File Paths](https://pytest-bdd.readthedocs.io/en/latest/index.html?highlight=string#feature-file-paths).
   In the ``setup.cfg`` write the following:
   ```INI
   [tool:pytest]
   bdd_features_base_dir = tests/features/
   ```
   Then every scenario should change the path to the feature file from
   ``features/example.feature`` to ``example.feature``.

2. Next we will remove all the scenarios with the [scenarios shortcut](https://pytest-bdd.readthedocs.io/en/latest/index.html?highlight=string#scenarios-shortcut).
   Replace all the scenarios with ``scenarios('example.feature')``

3. Since our steps follow a simple pattern, we can make use of pytest-bdd's
   [step-arguments](https://pytest-bdd.readthedocs.io/en/latest/index.html?highlight=string#step-arguments)
   feature. For example, we can combine the ``@when('I type "42"')`` and
   ``@when('I type "life"')`` decorators into
   ``@when(parsers.parse('I type "{line}"'))`` decorator. Do the same for the
   ``The text is`` decorators.

Finally, our test should now be:

```python
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers,
    scenarios,
)

scenarios('example.feature')


@given('The window')
def the_window_is_open(qtbot, window):
    """The window is open."""
    raise NotImplementedError


@when('I press the button')
def i_press_the_button(qtbot, window):
    """I press the button."""
    raise NotImplementedError


@when(parsers.parse('I type "{line}"'))
def type_in_line(line, window, qtbot):
    """I type "life"."""
    raise NotImplementedError


@then(parsers.parse('The text is "{line}"'))
def the_text_is(window, line):
    """The text is "bar"."""
    raise NotImplementedError
```

Create ``example.py``. It's beyond the scope to go through how the app works
in detail. Now we can now import the widget and test the application. Lets make
a fixture to create the example widget:

```python
@pytest.fixture
def window():
    return example.ExampleWindow()
```

Then lets fill in the given:

```python
@given('The window')
def the_window_is_open(qtbot, window):
    """The window is open."""
    qtbot.addWidget(window)
```

We add the widget in the given function so that the widget is properly handled
when the test finishes. The rest of the functions will be:

```python
@when('I press the button')
def i_press_the_button(qtbot, window):
    """I press the button."""
    qtbot.mouseClick(window.btn, QtCore.Qt.LeftButton)


@when(parsers.parse('I type "{line}"'))
def type_in_line(line, window, qtbot):
    """I type "line"."""
    window.line_edit.clear()
    qtbot.keyClicks(window.line_edit, line)


@then(parsers.parse('The text is "{line}"'))
def the_text_is(window, line):
    """The text is "line"."""
    assert window.line_edit.text() == line
```

Now when we run the tests they should all pass! Let's say we forgot a scenario,
since we use the ``scenarios`` shortcut, all we have to do is add the extra
scenario to the the feature file:

```Gherkin
Scenario: Edit Text then press button then edit again
    Given The window
    When I type "life"
    And I press the button
    And I type "42"
    Then The text is "42"
```

Then we rerun the tests and the new scenario will run.
