import os

target = r'c:\Users\josel\Downloads\Antigravity\INDICE Switch ES - The Goonies OS\src\ui.py'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

old_filter = '''                filteredGames = allGames.filter(g => {{
                    return g.title.toLowerCase().includes(term) || g.description.toLowerCase().includes(term);
                }});'''

new_filter = '''                filteredGames = allGames.filter(g => {{
                    // Si solo hay 1 o 2 letras, busca SOLO en el título para que los resultados sean precisos desde la primera letra
                    if (term.length < 3) {{
                        return g.title.toLowerCase().includes(term);
                    }}
                    // A partir de 3 letras, busca en título y descripción
                    return g.title.toLowerCase().includes(term) || g.description.toLowerCase().includes(term);
                }});'''

content = content.replace(old_filter, new_filter)

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated ui.py with smart length-based search')
