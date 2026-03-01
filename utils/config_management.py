import json
from pathlib import Path
import datetime

CONFIG_PATH= Path(__file__).parent.parent / "config.json"
LOG_PATH = Path(__file__).parent.parent / "logs" / "bot.log"


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


def logger(message, filename):
    now = datetime.datetime.now()
    date = now.strftime("%d-%m-%Y %X")

    with open(LOG_PATH, 'r') as f:
        line_count = sum(1 for line in f)

    mode = 'w' if line_count >= 50 else 'a'
    with open (LOG_PATH, mode) as f:
        log = date + " in " + filename + " : " + str(message)
        f.write(log+"\n")