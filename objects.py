from curses import endwin, newwin, doupdate, color_pair,A_REVERSE, A_BOLD, A_UNDERLINE, KEY_UP, KEY_DOWN, COLOR_CYAN, \
    COLOR_BLACK, COLOR_YELLOW, COLOR_BLUE, COLOR_GREEN, COLOR_MAGENTA, COLOR_RED, COLOR_WHITE
from curses.panel import new_panel, update_panels
from functions import make_color


class Mainwin():
    def __init__(self, screen, height=24, width=80, title=None, menu=None, debug_lines=False):
        self.height = height
        self.width = width
        self.y = screen.getmaxyx()[0] / 2 - self.height / 2
        self.x = screen.getmaxyx()[1] / 2 - self.width / 2
        self.title = title
        self.menu = menu
        self.menu_shortcuts = None
        self.debug = debug_lines

        del screen

        # CREATE MAIN WINDOW
        self.window = newwin(self.height, self.width, self.y, self.x)
        #self.window.box()
        self.panel = new_panel(self.window)

        # DEBUG
        if self.debug:
            self.debugwin = self.window.subwin(self.height, self.width, self.y, self.x)
            self.debugpan = new_panel(self.debugwin)
            self.debugwin.vline(0, 0, ".", self.height)
            self.debugwin.vline(0, self.width - 1, ".", self.height)
        #if self.debug == False:
        #    self.debugpan.hide()

        # CREATE TITLE
        # TODO title color is a mock or maybe not... but has to be reversed for proper coloring of title
        cyan = make_color(COLOR_CYAN, COLOR_BLACK)
        self.titlewin = self.window.subwin(1, self.width, self.y, self.x)
        self.titlewin.bkgd(" ", color_pair(cyan) + A_REVERSE)
        self.titlewin.addstr(0, (self.width / 2 - len(self.title) / 2), self.title)

        # CREATE STATUS LINE
        self.statuswin = self.window.subwin(1, self.width, (self.y + self.height - 1), self.x)
        self.statuswin.bkgd(" ", A_REVERSE)

        # CREATE MOCK MENU
        # TODO actual menu with actions will need implementation of menu class + maybe menu item class
        self.add_menu(
            [
                ("Ff", "File", ["New", "Open", "Exit"]),
                ("Hh", "Help", ["About"]),
                ("Cc", "Curses", ["About curses"])
            ])

        # UPDATE SELF
        self.update()

        # ENTER MAIN LOOP
        self.main()

    def debug_toggle(self):
        self.statuswin.addstr(0, 0, str(self.debugpan.hidden()))
        if self.debugpan.hidden():
            self.debugpan.hide()
        else:
            self.debugpan.hide()

        self.update()

    def add_menu(self, menu_tuples):
        # TODO this is just a mock, should probably place it in separate subwindow
        yellow = make_color(COLOR_YELLOW, COLOR_BLACK)
        self.window.move(1, 0)
        menu_index = 0

        for mt in menu_tuples:
            # Add menu shortcuts
            if self.menu is None:
                self.menu = mt[0]
            else:
                self.menu += mt[0]

            # Place menu items on screen
            self.window.addch(mt[1][0], color_pair(yellow) + A_BOLD)
            self.window.addstr(mt[1][1:], A_BOLD)

            # If it's not the last menu item, add some blank spaces to it for separation
            if menu_index != len(menu_tuples) - 1:
                self.window.addstr("  ")

            menu_index += 1

    def main(self):
        running = True
        while running:
            key = self.window.getch()
            action = self.keypress(key)

            if action == True:
                running = False
                self.clear()
                break

            if action is not None:
                pass

    def keypress(self, key):
        if key == 27:
            return True

    def get_status(self):
        return str(None)

    def clear(self):
        self.window.clear()

    @staticmethod
    def update():
        update_panels()
        doupdate()

class Menu():
    pass


class Dropdown():
    def __init__(self, menu_items, foreground=None, background=None, position=(0, 0), scrollable=False):
        self.scrollable = scrollable
        self.menu_items = menu_items
        self.width = self.longest_item(self.menu_items) + 2
        self.height = len(menu_items) + 2
        self.x = position[1]
        self.y = position[0]
        self.cx = 0
        self.cy = 0
        self.current_item = 0
        self.num_items = 0

        ### CREATE DROP DOWN WINDOW
        self.window = newwin(self.height, self.width, self.y, self.x)
        self.window.box()
        self.panel = new_panel(self.window)
        #self.window.addstr("Y", A_BOLD)


        ### POPULATE INITIAL ITEMS
        self.display_items()

        self.update()


    def display_items(self):
        self.move_cursor(0, 0)
        #self.window.addstr("X", A_BOLD)
        idx = 0
        for item in self.menu_items:
            # Move cursor to initial position before starting
            self.move_cursor(self.cy + 1, 1)
            # Check if item index matches current item, reverse colors if it does
            if idx == self.current_item:
                self.window.addstr(item + (" " * (self.width - len(item) - 2)), A_REVERSE)
            else:
                self.window.addstr(item + (" " * (self.width - len(item) - 2)))
            self.num_items += 1
            idx += 1

    def move_cursor(self, y, x):
        self.window.move(y, x)
        self.cx = x
        self.cy = y

    def keypress(self, key):
        moved = False

        if key == KEY_UP and self.current_item > 0 and not moved:
            moved = True
            self.current_item -= 1

        if key == KEY_DOWN and self.current_item < (len(self.menu_items) - 1) and not moved:
            moved = True
            self.current_item += 1

        if self.scrollable == True and not moved:
            if key == KEY_UP and self.current_item == 0 and not moved:
                moved = True
                self.current_item = len(self.menu_items) - 1

            if key == KEY_DOWN and self.current_item == (len(self.menu_items) - 1) and not moved:
                moved = True
                self.current_item = 0

        if moved:
            self.display_items()

        self.update()

    def get_status(self):
        return "idx: " + str(self.current_item)

    def clear(self):
        self.window.clear()

    @staticmethod
    def longest_item(items):
        length = 0
        for item in items:
            l = len(item.decode('utf-8'))
            if l > length:
                length = l

        return length

    @staticmethod
    def update():
        update_panels()
        doupdate()