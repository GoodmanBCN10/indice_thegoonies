import json

try:
    with open('data/database_the_goonies.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    print("Last 10 games added:")
    for g in db[-10:]:
        print(f"ID: {g['id']} | Title: {g['title']}")
except Exception as e:
    print(e)
