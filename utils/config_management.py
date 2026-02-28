import json
from pathlib import Path

CONFIG_PATH= Path(__file__).parent.parent / "config.json"

def get_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)
    
def update_config(key,value):
    data = get_config()
    data[key] = value
    with open(CONFIG_PATH, 'w') as f:
        json.dump(data, f, indent=4)