import json
from pathlib import Path

# Get the directory where database.py actually lives
BASE_DIR = Path(__file__).resolve().parent.parent 
# Join the directory with the filename
json_path = BASE_DIR / "shipments.json"
shipments ={}
try:
    with open(json_path) as json_file:
        data = json.load(json_file)
        for value in data:
            shipments[value['id']] = value
except FileNotFoundError:
    print(f"Warning: {json_path} not found. Starting with empty shipments.")

print(shipments)

def save():
    with open(json_path ,'w')  as json_file:
        json.dump(
           list( shipments.values()),
           json_file
        )