import os
import re
import json
import base64
import io
import sys
from PIL import Image

# Asegurar que se encuentre el modulo ui.py en la misma carpeta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ui import generate_html

def get_avatar_b64(avatar_name):
    av_path = os.path.join('template', avatar_name)
    if os.path.exists(av_path):
        with open(av_path, 'rb') as f:
            img = Image.open(io.BytesIO(f.read()))
            img.thumbnail((240, 360))
            output = io.BytesIO()
            img.save(output, format="JPEG", quality=60)
            return f"data:image/jpeg;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}"
    return ""

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

def rescue_data(db_name, html_name, title_m, title_s, avatar_name):
    db_path = os.path.join('data', db_name)
    if not os.path.exists(db_path): 
        print(f"❌ No se encontro {db_path}"); return

    print(f"🚑 Reparando y optimizando {db_name}...")
    with open(db_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        pattern = re.compile(r'\{[^{}]*"id":[^{}]*"title":[^{}]*"image":[^{}]*\}', re.DOTALL)
        matches = pattern.finditer(content)
        
        rescued_games = []
        for match in matches:
            try:
                game_data = json.loads(match.group(0))
                if game_data.get('image') and not game_data.get('ultra_optimized'):
                    game_data['image'] = optimize_image_b64(game_data['image'])
                    game_data['ultra_optimized'] = True
                rescued_games.append(game_data)
            except: continue

    if rescued_games:
        unique_games = list({str(g['id']): g for g in rescued_games}.values())
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(unique_games, f, ensure_ascii=False, indent=4)
        
        print(f"✅ {len(unique_games)} juegos listos. Generando {html_name}...")
        generate_html(unique_games, get_avatar_b64(avatar_name), html_name, title_m, title_s)
        print("✨ ¡Todo listo! Web actualizada.")

if __name__ == "__main__":
    # Parametros: DB_FILE HTML_FILE TITLE_M TITLE_S AVATAR
    if len(sys.argv) < 6:
        print("❌ Error: Parametros de rescate insuficientes.")
    else:
        rescue_data(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
