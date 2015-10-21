# -*- coding: utf-8 -*-

"""A module for displaying stats in the console."""

from datetime import datetime
import sys

import curses
from curses import wrapper

from artifact.stats.console import autoscalinggroups
from artifact.stats.console import ec2
from artifact.stats.console import ecsclusters
from artifact.stats.console import ecscontainerinstances
from artifact.stats.console import ecsservices
from artifact.stats.console import ecstasks
from artifact.stats.console import ecstaskdefinitions
from artifact.stats.console import elasticloadbalancers
from artifact.stats.console import securitygroups
from artifact.stats.console import launchconfigurations
from artifact.stats.console import subnets
from artifact.stats.console import utils
from artifact.stats.console import vpcs


def get_tty_rows():
    """Get how many rows are in the terminal."""
    return curses.LINES - 1


def get_tty_cols():
    """Get how many columns are in the terminal."""
    return curses.COLS - 1


def get_widgets():
    """Get a dict of widget definitions."""
    tty_rows = get_tty_rows()
    row_1_rows = tty_rows - 20
    row_2_rows = 30
    return [
        {
            "name": "VPCs",
            "top_row": 0,
            "left_col": 0,
            "rows": row_1_rows,
            "cols": 25,
            "pad": None,
            "data": [["No data"]],
            "data_func": vpcs.data,
            "heading_func": utils.heading,
            "body_func": utils.body,
        },
        {
            "name": "Subnets",
            "top_row": 0,
            "left_col": 25,
            "rows": row_1_rows,
            "cols": 25,
            "pad": None,
            "data": [["No data"]],
            "data_func": subnets.data,
            "heading_func": utils.heading,
            "body_func": utils.body,
        },
        {
            "name": "Auto Scaling Groups",
            "top_row": 0,
            "left_col": 50,
            "rows": row_1_rows,
            "cols": 30,
            "pad": None,
            "data": [["No data"]],
            "data_func": autoscalinggroups.data,
            "heading_func": utils.heading,
            "body_func": utils.body,
        },
        {
            "name": "Instances",
            "top_row": 0,
            "left_col": 80,
            "rows": row_1_rows,
            "cols": 30,
            "pad": None,
            "data": [["No data"]],
            "data_func": ec2.data,
            "heading_func": utils.heading,
            "body_func": utils.body,
        },
        {
            "name": "ELBs",
            "top_row": 0,
            "left_col": 110,
            "rows": row_1_rows,
            "cols": 30,
            "pad": None,
            "data": [["No data"]],
            "data_func": elasticloadbalancers.data,
            "heading_func": utils.heading,
            "body_func": utils.body,
        },
        {
            "name": "Security Groups",
            "top_row": row_1_rows,
            "left_col": 0,
            "rows": row_2_rows,
            "cols": 25,
            "pad": None,
            "data": [["No data"]],
            "data_func": securitygroups.data,
            "heading_func": utils.heading,
            "body_func": utils.body,
        },
        {
            "name": "Launch Configs",
            "top_row": row_1_rows,
            "left_col": 25,
            "rows": row_2_rows,
            "cols": 25,
            "pad": None,
            "data": [["No data"]],
            "data_func": launchconfigurations.data,
            "heading_func": utils.heading,
            "body_func": utils.body,
        },
        {
            "name": "ECS Clusters",
            "top_row": row_1_rows,
            "left_col": 50,
            "rows": row_2_rows,
            "cols": 25,
            "pad": None,
            "data": [["No data"]],
            "data_func": ecsclusters.data,
            "heading_func": utils.heading,
            "body_func": utils.body,
        },
        {
            "name": "ECS Instances",
            "top_row": row_1_rows,
            "left_col": 75,
            "rows": row_2_rows,
            "cols": 25,
            "pad": None,
            "data": [["No data"]],
            "data_func": ecscontainerinstances.data,
            "heading_func": utils.heading,
            "body_func": utils.body,
        },
        {
            "name": "ECS Services",
            "top_row": row_1_rows,
            "left_col": 100,
            "rows": row_2_rows,
            "cols": 25,
            "pad": None,
            "data": [["No data"]],
            "data_func": ecsservices.data,
            "heading_func": utils.heading,
            "body_func": utils.body,
        },
        {
            "name": "ECS Tasks",
            "top_row": row_1_rows,
            "left_col": 125,
            "rows": row_2_rows,
            "cols": 25,
            "pad": None,
            "data": [["No data"]],
            "data_func": ecstasks.data,
            "heading_func": utils.heading,
            "body_func": utils.body,
        },
        {
            "name": "ECS Task Defs",
            "top_row": row_1_rows,
            "left_col": 150,
            "rows": row_2_rows,
            "cols": 25,
            "pad": None,
            "data": [["No data"]],
            "data_func": ecstaskdefinitions.data,
            "heading_func": utils.heading,
            "body_func": utils.body,
        },
    ]


def get_total_widget_rows(widgets):
    """Calculate how many total rows the widgets take up."""
    result = 0
    for widget in widgets:
        bottom_row = widget["top_row"] + widget["rows"]
        if bottom_row > result:
            result = bottom_row
    return result


def get_total_widget_cols(widgets):
    """Calculate how many total columns the widgets take up."""
    result = 0
    for widget in widgets:
        right_col = widget["left_col"] + widget["cols"]
        if right_col > result:
            result = right_col
    return result


def repaint(widget, row_offset, col_offset, top_row, left_col, bottom_row, right_col):
    """Repaint a widget."""
    pad = widget["pad"]
    pad.border(0, 0, 0, 0, 0, 0)

    # Paint the heading for the widget.
    widget["heading_func"](widget)

    # Get the data to paint (update it if needed).
    original_data = widget["data"]
    updated_data = widget["data_func"](widget)
    if updated_data != original_data:
        widget["data"] = updated_data

    # Paint the body of the widget.
    widget["body_func"](widget)

    # Refresh the viewing pane.
    pad.noutrefresh(row_offset, col_offset, top_row, left_col, bottom_row, right_col)


def event_loop(screen):
    """The main event loop."""
    # Hide the cursor.
    curses.curs_set(False)

    # When we run getch() below, don't block and wait for the user
    # to type a character. Just check and move on.
    screen.nodelay(True)

    # Get the widget definitions.
    widgets = get_widgets()

    # Build the widgets.
    for widget in widgets:
        widget["pad"] = curses.newpad(widget["rows"], widget["cols"])

    # When we begin, the screen hasn't been scrolled yet.
    scroll_row_offset = 0
    scroll_col_offset = 0

    # Start a loop that, on each iteration, redraws the screen.
    while True:

        # How big is the TTY?
        tty_rows = get_tty_rows()
        tty_cols = get_tty_cols()

        # How many rows and cols in total are taken up by the widgets?
        # This is irrespective of screen size.
        total_widget_rows = get_total_widget_rows(widgets)
        total_widget_cols = get_total_widget_cols(widgets)
        
        # Do we need to update the screen? Assume no to start.
        do_update = False

        # Is the state an invalid state (like if the user has tried
        # to scroll too far off screen or something?)
        is_invalid = False

        # Has the user pressed a key? Capture the character they pressed.
        captured_char = screen.getch()

        # Is it "q"? Quit.
        if captured_char == ord("q"):
            sys.exit(1)

        # Did the user press DOWN?
        elif captured_char == curses.KEY_DOWN:
            if total_widget_rows < tty_rows:
                is_invalid = True
            elif (scroll_row_offset + 1) > 0:
                is_invalid = True
            else:
                scroll_row_offset += 1
                do_update = True

        # Did the user press UP?
        elif captured_char == curses.KEY_UP:
            if total_widget_rows < tty_rows:
                is_invalid = True
            elif (scroll_row_offset - 1) < (0 - (total_widget_rows - tty_rows)):
                is_invalid = True
            else:
                scroll_row_offset += -1
                do_update = True
            
        # Did the user press RIGHT?
        elif captured_char == curses.KEY_RIGHT:
            if total_widget_cols < tty_cols:
                is_invalid = True
            elif (scroll_col_offset + 1) > 0:
                is_invalid = True
            else:
                scroll_col_offset += 1
                do_update = True

        # Did the user press LEFT?
        elif captured_char == curses.KEY_LEFT:
            if total_widget_cols < tty_cols:
                is_invalid = True
            elif (scroll_col_offset - 1) < (0 - (total_widget_cols - tty_cols)):
                is_invalid = True
            else:
                scroll_col_offset -= 1
                do_update = True

        # Show a screen flash and beep if the user is trying to enter
        # an invalid state.
        if is_invalid:
            curses.flash()
            curses.beep()

        else:

            # Erase the screen if we need to update the screen.
            # This is an expensive operation, so we only do it if we need to.
            if do_update:
                screen.erase()

            # Paint each widget on the screen.
            for i, widget in enumerate(widgets):

                # Is the widget visible (on the screen)? Assume yes to start.
                is_visible = True

                # Calculate row positions (irrespective of the screen).
                row_offset = 0
                top_row = widget["top_row"] + scroll_row_offset
                rows = widget["rows"]
                bottom_row = top_row + rows

                # Adjust row positions to fit on screen.
                if top_row >= tty_rows:
                    is_visible = False
                elif bottom_row <= 0:
                    is_visible = False
                elif top_row <= 0:
                    row_offset = abs(top_row)
                    top_row = 0
                if bottom_row >= tty_rows:
                    bottom_row = tty_rows

                # Calculate col positions (irrespective of the screen).
                col_offset = 0
                left_col = widget["left_col"] + scroll_col_offset
                cols = widget["cols"]
                right_col = left_col + cols 

                # Adjust the col positions to fit on the screen.
                if left_col >= tty_cols:
                    is_visible = False
                elif right_col <= 0:
                    is_visible = False
                elif left_col <= 0:
                    col_offset = abs(left_col)
                    left_col = 0
                if right_col >= tty_cols:
                    right_col = tty_cols

                # If the widget is visible, paint it.
                if is_visible:
                    repaint(widget, row_offset, col_offset, top_row, left_col, bottom_row, right_col)

            # Tell curses to redraw the screen for real.
            curses.doupdate()


def start():
    """Start the event loop."""
    try:
        wrapper(event_loop)
    except KeyboardInterrupt:
        sys.exit(1)
