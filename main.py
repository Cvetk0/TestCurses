#!/usr/bin/env python
# coding=utf-8
from curses import *
from curses.panel import *
from objects import Mainwin, Dropdown
from functions import make_color
import locale


def main():
    # Set locale
    locale.setlocale(locale.LC_ALL, '')

    # Initialize object stack, all objects on screen should be stacked in it
    object_stack = []

    stdscr = initscr()

    if not has_colors():
        print "Your terminal needs to have colors to run this program"
        return 1
    else:
        start_color()

    noecho()
    curs_set(False)
    stdscr.keypad(True)

    stdscr.move(0, 50)
    stdscr.addstr("Status:")
    status = newwin(3, 15, 1, 50)
    status.box()
    status_panel = new_panel(status)
    stdscr.move(0, 67)
    stdscr.addstr("Key:")
    keywin = newwin(3, 15, 1, 67)
    keywin.box()
    keywin_panel = new_panel(keywin)
    stdscr.move(0, 84)
    stdscr.addstr("Stack size:")
    stackwin = newwin(3, 15, 1, 84)
    stackwin.box()
    stackwin_panel = new_panel(stackwin)

    # Initial panel display
    update_screen()

    Mainwin(stdscr, title="Menu application", debug_lines=False)
    # object_stack.append(Mainwin(stdscr, title="Test title", debug_lines=False))
    #
    # running = True
    # while running:
    #     display_stack_size(stackwin, object_stack)
    #     key = stdscr.getch()
    #     display_keypress(keywin, key)
    #
    #     if object_stack:
    #         object_stack[-1].keypress(key)
    #         display_status(status, object_stack[-1])
    #
    #     if key == 27:
    #         running = False
    #         break
    #
    #     if key == ord("d"):
    #         object_stack.append(Dropdown(["Item1", "Item2", "Item  čćščćšč", "Jenko", "Ninjas rule"], position=(1, 1),
    #                                      scrollable=True))
    #
    #     if key == ord("f"):
    #         object_stack.append(Dropdown(["Menu 2", "Whatisthis", "Shit", "Mastah", "We rule"], position=(2, 2)))
    #
    #     if key == ord("g"):
    #         object_stack.append(Mainwin(stdscr, title="Test title", debug_lines=False))
    #
    #     if key == ord("c") and object_stack:
    #         i = object_stack.pop(-1)
    #         i.clear()
    #         del i
    #         update_screen()

    endwin()

def display_stack_size(window, stack):
    stack_len = str(len(stack))
    window.addstr(1, 1,  stack_len + " " * (8 - len(stack_len)))
    update_screen()

def display_status(window, object):
    item = str(object.get_status())
    window.addstr(1, 1, item + " " * (8 - len(item)))
    update_screen()

def display_keypress(window, key):
    window.addstr(1, 1, str(key) + " " * (8 - len(str(key))))
    update_screen()

def update_screen():
    update_panels()
    doupdate()

if __name__ == "__main__":
    main()
