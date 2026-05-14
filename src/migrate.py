import os
import json
import re
import base64
import asyncio
import aiohttp
import io
import sys
from PIL import Image
from urllib.parse import quote

# Asegurar que se encuentre el modulo ui.py en la misma carpeta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ui import generate_html

AVATAR_PATH = os.path.join('template', 'avatar.jpg')

def get_avatar_b64():
    if os.path.exists(AVATAR_PATH):
        with open(AVATAR_PATH, 'rb') as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

def clean_text_strictly(text):
    if not text: return ""
    text = re.sub(r'[^\w\s\d\.,:;\-\(\)\?¿!¡/\\\'"áéíóúÁÉÍÓÚñÑ]', '', text)
    text = re.sub(r'Portable\s*\(desde\s*Steam\)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Link\s*Steam', '', text, flags=re.IGNORECASE)
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    return text.strip()

def get_clean_search_term(title):
    term = re.sub(r'v?\d+\.\d+.*|GOLD|EDITION|REPACK|FULL|DLC|JUEGO|REMAKE|DELUXE|EARLY ACCESS|BETA', '', title, flags=re.IGNORECASE)
    return term.strip()

def optimize_image_b64(b64_string):
    try:
        if "," in b64_string: header, b64_string = b64_string.split(",")
        img_data = base64.b64decode(b64_string)
        img = Image.open(io.BytesIO(img_data))
        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        img.thumbnail((240, 360), Image.Resampling.LANCZOS)
        output = io.BytesIO()
        img.save(output, format="JPEG", quality=55, optimize=True)
        return f"data:image/jpeg;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}"
    except: return None

async def search_steam_appid(title, session):
    term = get_clean_search_term(title)
    try:
        url = f"https://store.steampowered.com/api/storesearch/?term={quote(term)}&l=spanish&cc=ES"
        async with session.get(url, timeout=5) as response:
            if response.status == 200:
                data = await response.json()
                if data.get('items'): return str(data['items'][0]['id'])
    except: pass
    return None

async def download_and_optimize_steam(appid, session):
    url = f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/library_600x900_2x.jpg"
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                data = await response.read()
                return optimize_image_b64(base64.b64encode(data).decode('utf-8'))
    except: pass
    return None

async def migrate():
    db_path = os.path.join('data', 'database.json')
    if not os.path.exists(db_path): return

    with open(db_path, 'r', encoding='utf-8') as f:
        games = json.load(f)

    print(f"🚀 Migrando y actualizando interfaz para {len(games)} juegos...")
    async with aiohttp.ClientSession() as session:
        for i, game in enumerate(games):
            # Limpieza y optimizacion si es necesario
            game['title'] = clean_text_strictly(game['title'])
            if not game.get('ultra_optimized'):
                opt = optimize_image_b64(game['image'])
                if opt:
                    game['image'] = opt
                    game['ultra_optimized'] = True
            
            if i % 100 == 0: print(f"Procesado: {i}/{len(games)}")

    # Guardar y REGENERAR UI
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(games, f, ensure_ascii=False, indent=4)
    
    print("🎨 Generando nueva interfaz...")
    generate_html(games, get_avatar_b64())
    print("✨ Sincronizacion de UI completada.")

if __name__ == "__main__":
    asyncio.run(migrate())
