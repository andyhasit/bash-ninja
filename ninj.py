#!/usr/bin/env python3
'''
Tool for running or copying shell commands to clipboard.


Example JSON config file:
{
    "Django" : {
        "type": "menu",
        "info": "select command",
        "items": {
            "create-project": {
                "type": "clipboard",
                "value": "django-admin startproject ..."
            },
            "create-app": {
                "type": "clipboard",
                "value": "python manage.py startapp"
            },
            "migrations": {
                "type": "menu",
                "info": "select command",
                "items": {
                    "create migrations": {
                        "type": "clipboard",
                        "value": "python manage.py makemigrations"
                    },
                    "apply migrations": {
                        "type": "clipboard",
                        "value": "python manage.py migrate"
                    }
                }
            }
        }
    },
    "Misc" : {
        "type": "menu",
        "info": "select command",
        "items": {
            "facebook": {
                "type": "command",
                "value": "xdg-open http://www.facebook.com"
            }
        }
    }
}
'''

import os, sys
from config import JsonConfig
from commands import Menu

if __name__ == "__main__":
    if len(sys.argv) == 1:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        config_file_path = os.path.join(script_dir, 'ninj_conf.json')
    else:
        config_file_path = sys.argv[1]
    
    top_menu = Menu("Ninj", "A bash helper for people with bad memory.", 
        exclude_back_option=True)
    json_config = JsonConfig()
    json_config.build_menu(top_menu, config_file_path)
    top_menu.enter()