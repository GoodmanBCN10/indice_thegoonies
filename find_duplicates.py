import json
from collections import Counter

try:
    with open('data/database_the_goonies.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    titles = [g['title'] for g in db]
    counts = Counter(titles)
    
    dupes = [t for t, c in counts.items() if c > 1]
    if dupes:
        print("Duplicates found:")
        for t in dupes:
            print(f"- {t}")
    else:
        print("No exact duplicate titles found.")
except Exception as e:
    print(e)
