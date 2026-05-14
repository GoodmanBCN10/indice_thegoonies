import os
import json
import base64

DB_PATH = os.path.join('data', 'database.json')
AVATAR_PATH = os.path.join('template', 'avatar.jpg')

def get_avatar_b64():
    if os.path.exists(AVATAR_PATH):
        with open(AVATAR_PATH, 'rb') as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

def refresh():
    if not os.path.exists(DB_PATH):
        print("❌ No se encontró database.json")
        return

    print("🚀 Generando HTML optimizado...")
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        games = json.load(f)

    # Importamos la función de generación del scraper original para mantener el diseño
    from scraper import generate_portable_html
    
    avatar_b64 = get_avatar_b64()
    generate_portable_html(games, avatar_b64)
    
    size_mb = os.path.getsize('index.html') / (1024 * 1024)
    print(f"✨ ¡LISTO! Tu nuevo index.html pesa solo {size_mb:.2f} MB.")
    print("👉 Ya puedes abrirlo en tu navegador.")

if __name__ == "__main__":
    refresh()
