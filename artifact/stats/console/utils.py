# -*- coding: utf-8 -*-

"""A module with utils for rendering stats in the console."""

from datetime import datetime
import curses


def is_update_needed():
    """Decide if a widget needs its data updated."""
    return not datetime.now().second % 10


def heading(widget):
    """Paint the heading."""
    pad = widget["pad"]
    heading = "   " + widget["name"]
    cols = widget["cols"]
    padding = cols - (len(heading) + 2)
    for i in range(padding):
        heading += " "
    pad.addstr(1, 1, heading, curses.A_REVERSE)


def body(widget):
    """Paint the curses data."""
    pad = widget["pad"]
    data = widget["data"]
    line = 2
    for fieldset in data:
        for i, field in enumerate(fieldset):
            line += 1
            if i == 0:
                pad.addstr(line, 1, " - " + field, curses.A_BOLD)
            else:
                pad.addstr(line, 1, "   " + field)
        pad.addstr(line, 1, "")
        line += 1
