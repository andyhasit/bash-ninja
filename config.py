import json
from collections import OrderedDict
from commands import Menu, Command, ClipboardCommand

class JsonConfig():
    """
    Handles loading of config data and bulding the menu.
    """

    def build_menu(self, top_menu_entry, config_file_path):
        data = self._load_config(config_file_path)
        self._attach_menu_items(top_menu_entry, data)

    def _attach_menu_items(self, parent, items_dict):
        for key in items_dict:
            element = items_dict[key]
            text = key
            item_type = element['type']
            if item_type == "menu":
                menu_item = Menu(text, element['info'])
                self._attach_menu_items(menu_item, element['items'])
            elif item_type == "command":
                menu_item = Command(text, element['value'].split(' '))
            elif item_type == "clipboard":
                menu_item = ClipboardCommand(text, element['value'])
            parent.add(menu_item)

    def _load_config(self, config_file_path):
        with open(config_file_path) as f:
            data = json.load(f, object_pairs_hook=OrderedDict)
        return data
        
