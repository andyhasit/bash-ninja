from subprocess import call
import os
import pyperclip

HR = "----------------------------------------"


class MenuItem(object):
    """
    Represents a menu item, which can be another menu, or a command.
    It has one method: select() which dictates what happens when it is selected.
    """

    def enter(self, parent_menu=None):
        raise NotImplemented("Menu Item did not implement method enter(). \
                Check your code!")
    def __repr__(self):
        return self.text


class Back(MenuItem):
    """
    The back menu item.
    """
    def __init__(self, parent_menu=None):
        self.text = "Go back"
        self.parent_menu = parent_menu

    def enter(self, parent_menu=None):
        if self.parent_menu:
            self.parent_menu.enter()
        else:
            exit(0)


class Menu(MenuItem):
    """
    A menu item that contains sub items.
    """
    def __init__(self, text, info, exclude_back_option=False):
        self.text = text
        self.info = info
        self.items = []
        self.exclude_back_option = exclude_back_option

    def enter(self, parent_menu=None):
        print("{0}\n{0}".format(HR))
        print(self.text)
        print("\n{0}\n".format(self.info))
        choices = self.items[:]
        start = 1
        if not self.exclude_back_option:
            back = Back(parent_menu)
            choices.insert(0, back)
            start = 0
        while True:
            choice = self.get_choice(choices, start)
            choice.enter(parent_menu=self)

    def add(self, item):
        self.items.append(item)

    def get_choice(self, items, start=0):
        choices = {}
        def print_choices():
            for i, item in enumerate(items):
                key = str(i + start)
                print("{0}: {1}".format(key, item))
                choices[key] = item
        while True:
            try:
                print_choices()
                choice = raw_input("\nEnter selection>>>")
                assert choice in choices
                return choices[choice]
            except AssertionError as e:
                print("That is not a valid selection. Try again.\n") 

class Command(MenuItem):
    """
    A menu item which executes a command.
    """
    def __init__(self, text, callargs):
        self.text = text
        self.callargs = callargs

    def enter(self, parent_menu=None):
        """parent_menu is not used"""
        print(self.callargs)
        call(self.callargs)#, shell=True, cwd=os.getcwd())


class ClipboardCommand(MenuItem):
    """
    A menu item which places text in the clipboard then exits. The idea being 
    that you paste and enter. 
    Reason being that you might need to do stuff in current context (like cd).
    """
    def __init__(self, text, value):
        self.text = text
        self.value = value

    def enter(self, parent_menu=None):
        """parent_menu is not used"""
        pyperclip.copy(self.value)
        print("Command copied to clipboard, press ctrl+V")
        exit(0)