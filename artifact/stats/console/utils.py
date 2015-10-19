# -*- coding: utf-8 -*-

"""A module with utils for rendering stats in the console."""

from datetime import datetime
import curses


def break_into_lines(string, num):
    """Break a string into a list of lines."""
    return [string[x:x + num] for x in range(0, len(string), num)]


def is_update_needed():
    """Decide if a widget needs its data updated."""
    return not datetime.now().second % 5


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
    max_chars_per_line = widget["cols"] - 8
    line = 2
    for fieldset in data:
        for i, field in enumerate(fieldset):
            lines = break_into_lines(field, max_chars_per_line)
            line += 1
            if i == 0:
                for j, string in enumerate(lines):
                    if j == 0:
                        pad.addstr(line + j, 1, " - " + string, curses.A_BOLD)
                    else:
                        pad.addstr(line + j, 1, "   " + string, curses.A_BOLD)
            else:
                for j, string in enumerate(lines):
                    if j == 0:
                        pad.addstr(line + j, 1, "   " + string)
                    else:
                        pad.addstr(line + j, 1, "     " + string)
            line += (len(lines) - 1)
        pad.addstr(line, 1, "")
        line += 1

