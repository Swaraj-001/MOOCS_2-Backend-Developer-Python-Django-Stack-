import json
from pymongo import MongoClient

def import_karad_attractions(json_file_path):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['localTourist']
    collection = db['tourist_attractions']

    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Insert data into MongoDB collection
    for item in data:
        collection.update_one(
            {'name': item['name']},
            {'$set': item},
            upsert=True
        )

if __name__ == "__main__":
    import_karad_attractions('api/sample_karad_attractions.json')
    print("Karad attractions imported successfully.")
