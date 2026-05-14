import os
import json
import re
import asyncio
import aiohttp
import sys
import io
from datetime import datetime
from PIL import Image
from hydrogram import Client
from dotenv import load_dotenv

# Asegurar que se encuentre el modulo ui.py en la misma carpeta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ui import generate_html

load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

app = Client("my_session", api_id=API_ID, api_hash=API_HASH)

def format_channel_id(cid):
    if not cid: return None
    cid_str = str(cid).strip()
    if cid_str.replace('-', '').isdigit(): return int(cid_str)
    return cid_str

def clean_text_strictly(text):
    if not text: return ""
    text = re.sub(r'[^\w\s\d\.,:;\-\(\)\?¿!¡/\\\'"áéíóúÁÉÍÓÚñÑ]', '', text)
    text = re.sub(r'Portable\s*\(desde\s*Steam\)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Link\s*Steam', '', text, flags=re.IGNORECASE)
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    return text.strip()

def clean_title(text):
    if not text: return "Sin Título"
    text = clean_text_strictly(text)
    first_line = text.split('\n')[0]
    title = re.sub(r'^SDCS Backups\s*', '', first_line, flags=re.IGNORECASE)
    return title.strip()

def optimize_image_b64(raw_data):
    try:
        img = Image.open(io.BytesIO(raw_data))
        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        img.thumbnail((240, 360), Image.Resampling.LANCZOS)
        output = io.BytesIO()
        img.save(output, format="JPEG", quality=55, optimize=True)
        import base64
        return f"data:image/jpeg;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}"
    except: return None

async def download_and_optimize(url, session):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                data = await response.read()
                return optimize_image_b64(data)
    except: pass
    return None

def get_steam_appid(text):
    if not text: return None
    match = re.search(r'store\.steampowered\.com/app/(\d+)', text)
    return match.group(1) if match else None

def get_avatar_b64(avatar_name):
    av_path = os.path.join('template', avatar_name)
    if os.path.exists(av_path):
        with open(av_path, 'rb') as f:
            return optimize_image_b64(f.read())
    fallback = os.path.join('template', 'avatar.jpg')
    if os.path.exists(fallback):
        with open(fallback, 'rb') as f:
            return optimize_image_b64(f.read())
    return ""

def load_existing_data(db_path):
    if os.path.exists(db_path):
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    if 'id' in item: item['id'] = str(item['id'])
                return data
        except: pass
    return []

async def main():
    if len(sys.argv) < 8:
        print("❌ Error: Faltan argumentos.")
        return

    target_channel = format_channel_id(sys.argv[1])
    topic_id = int(sys.argv[2]) if sys.argv[2].isdigit() and sys.argv[2] != "0" else None
    db_name = sys.argv[3]
    html_name = sys.argv[4]
    
    if not html_name.lower().endswith(".html"): html_name += ".html"
    if not db_name.lower().endswith(".json"): db_name += ".json"

    title_m = sys.argv[5]
    title_s = sys.argv[6]
    avatar_name = sys.argv[7]
    
    start_date = None
    if len(sys.argv) > 8:
        try: start_date = datetime.strptime(sys.argv[8], "%d/%m/%Y")
        except: pass

    db_path = os.path.join('data', db_name)
    
    # El bloque 'async with' gestiona el inicio y cierre automático de la base de datos
    async with app:
        print(f"📡 Resolviendo canal: {target_channel}...")
        try:
            chat = await app.get_chat(target_channel)
            print(f"✅ Conectado a: {chat.title}")

            existing_games = load_existing_data(db_path)
            indexed_ids = {str(g['id']) for g in existing_games if 'id' in g}
            
            async with aiohttp.ClientSession() as session:
                async for message in app.get_chat_history(target_channel):
                    if start_date and message.date < start_date: break
                    if topic_id:
                        msg_topic = getattr(message, "message_thread_id", None)
                        if msg_topic != topic_id: continue

                    msg_id = str(message.id)
                    has_media = message.photo or (message.web_page and message.web_page.photo)
                    text_content = message.caption or message.text
                    
                    if has_media and text_content:
                        if msg_id in indexed_ids:
                            if not start_date: break
                            continue
                        
                        title = clean_title(text_content)
                        print(f"🆕 [{message.date.strftime('%d/%m/%Y')}] {title}")
                        appid = get_steam_appid(text_content)
                        img_b64 = None
                        if appid:
                            url = f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/library_600x900_2x.jpg"
                            img_b64 = await download_and_optimize(url, session)
                        
                        if not img_b64:
                            try:
                                await asyncio.sleep(1.8) 
                                img_data = await message.download(in_memory=True)
                                if img_data: img_b64 = optimize_image_b64(img_data.getbuffer())
                            except: continue

                        if not img_b64: continue

                        existing_games.append({
                            "id": msg_id, "title": title, "description": clean_text_strictly(text_content).replace('\n', '<br>'),
                            "image": img_b64, "image_source": 'steam' if appid else 'telegram',
                            "steam_url": f"https://store.steampowered.com/app/{appid}" if appid else "",
                            "telegram_url": f"https://t.me/c/{str(chat.id)[4:]}/{msg_id}" if str(chat.id).startswith("-100") else f"https://t.me/{chat.id}/{msg_id}",
                            "date": message.date.isoformat()
                        })

            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump(existing_games, f, ensure_ascii=False, indent=4)
            
            generate_html(existing_games, get_avatar_b64(avatar_name), html_name, title_m, title_s)
            print(f"✨ ¡Hecho! Biblioteca '{html_name}' con avatar '{avatar_name}'")

        except Exception as e:
            print(f"❌ Error durante la ejecución: {e}")

if __name__ == "__main__":
    app.run(main())