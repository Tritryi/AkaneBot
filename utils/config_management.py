import json
from pathlib import Path

CONFIG_PATH= Path(__file__).parent.parent / "config.json"


def get_config():
    """
    Charge la config depuis le fichier json
    """
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)
    
def update_config(key,value):
    """
    Change la config en fonction des valeurs entrées en paramètres. Changement notamment des id de message.
    """
    data = get_config()
    data[key] = value
    with open(CONFIG_PATH, 'w') as f:
        json.dump(data, f, indent=4)