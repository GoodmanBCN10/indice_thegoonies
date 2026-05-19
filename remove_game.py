import json
import os
import base64
from src.ui import generate_html

DB_PATH = os.path.join('data', 'database_the_goonies.json')
HTML_NAME = 'The_Goonies.html'
AVATAR_PATH = os.path.join('template', 'goonies_avatar.jpg')

def get_avatar_b64():
    fallback = os.path.join('template', 'avatar.jpg')
    path = AVATAR_PATH if os.path.exists(AVATAR_PATH) else fallback
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

def remove_and_refresh():
    if not os.path.exists(DB_PATH):
        print(f"❌ No se encontró {DB_PATH}")
        return

    with open(DB_PATH, 'r', encoding='utf-8') as f:
        games = json.load(f)

    # Buscar y eliminar el juego problemático
    original_count = len(games)
    
    search_term = input("Introduce el nombre (o parte del nombre) del juego a eliminar: ").strip().lower()
    
    if not search_term:
        print("No se introdujo ningún nombre. Cancelando.")
        return
        
    def is_match(g):
        t = g.get('title', '').lower()
        return search_term in t

    games = [g for g in games if not is_match(g)]
    removed_count = original_count - len(games)

    if removed_count == 0:
        print(f"No se encontró ningún juego que contenga '{search_term}'.")
        return
        
    print(f"Éxito: Se han eliminado {removed_count} entrada(s) que coinciden con '{search_term}'.")

    # Guardar la base de datos
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(games, f, ensure_ascii=False, indent=4)

    # Regenerar el HTML
    try:
        avatar_b64 = get_avatar_b64()
        generate_html(games, avatar_b64, HTML_NAME, "The Goonies OS", "Switch Backup Library")
        print(f"HTML regenerado correctamente!")
    except Exception as e:
        print(f"Error al regenerar HTML: {e}")

if __name__ == "__main__":
    remove_and_refresh()
