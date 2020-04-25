from example import example

from qtpy import QtCore
import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers,
    scenarios,
)


@pytest.fixture
def window():
    return example.ExampleWindow()

scenarios('example.feature')


@given('The window')
def the_window_is_open(qtbot, window):
    """The window is open."""
    qtbot.addWidget(window)


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
