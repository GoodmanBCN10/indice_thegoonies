import os
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import json
import re
import asyncio
import io
import base64
from datetime import datetime
from PIL import Image
from hydrogram import Client
from dotenv import load_dotenv

# Configuración inicial
load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
SESSION_STRING = os.getenv('TELEGRAM_SESSION')
CHANNEL_ID = -1002861009856
TOPIC_ID = 36
HTML_OUTPUT = "index.html"
DB_FILE = "indice_juegos.json"

try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

if SESSION_STRING:
    app = Client("my_session", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)
else:
    app = Client("my_session", api_id=API_ID, api_hash=API_HASH)

DEFAULT_IMAGE_B64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAADIAQMAAAAwS4omAAAAA1BMVEWAgICQdD0xAAAANUlEQVR42u3BAQ0AAADCoPdPbQ8HFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB8GzXDAAHTSjU2AAAAAElFTkSuQmCC"

def optimize_image_b64(raw_data):
    try:
        img = Image.open(io.BytesIO(raw_data))
        if img.mode in ("RGBA", "P"): 
            img = img.convert("RGB")
        img.thumbnail((240, 360), Image.Resampling.LANCZOS)
        output = io.BytesIO()
        img.save(output, format="JPEG", quality=65, optimize=True)
        return f"data:image/jpeg;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}"
    except Exception as e:
        print(f"Error optimizando imagen: {e}")
        return None

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

def generate_html(items):
    # Generador de HTML con diseño "Premium"
    json_data = json.dumps(items)
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo de Juegos</title>

    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JW7GSTB35V"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      gtag('config', 'G-JW7GSTB35V');
    </script>

    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;500;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --surface-color: rgba(30, 41, 59, 0.7);
            --surface-hover: rgba(51, 65, 85, 0.9);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
            --accent-glow: rgba(56, 189, 248, 0.5);
            --border: rgba(255, 255, 255, 0.08);
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; transition: all 0.25s ease; }}
        
        body {{
            background: radial-gradient(circle at top right, #1e293b, var(--bg-color));
            color: var(--text-main);
            min-height: 100vh;
            padding-bottom: 50px;
        }}

        header {{
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            padding: 20px 40px;
            display: flex;
            flex-direction: column;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        
        .header-content {{
            display: flex;
            align-items: center;
            gap: 25px;
            margin-bottom: 15px;
        }}

        .header-logo {{
            width: 80px;
            height: 80px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid var(--accent);
            box-shadow: 0 0 15px var(--accent-glow);
        }}

        .header-text {{
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        h1 {{ font-size: 2.5rem; font-weight: 800; letter-spacing: -1px; margin-bottom: 5px; color: #fff; }}
        .subtitle {{ color: var(--accent); font-weight: 500; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 3px; }}
        
        .search-container {{
            margin-top: 25px;
            width: 100%;
            max-width: 600px;
            position: relative;
        }}

        #search {{
            width: 100%;
            padding: 16px 24px;
            border-radius: 50px;
            background: var(--surface-color);
            border: 1px solid var(--border);
            color: white;
            font-size: 1.1rem;
            outline: none;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }}

        #search:focus {{
            border-color: var(--accent);
            box-shadow: 0 0 20px var(--accent-glow);
            background: rgba(30, 41, 59, 0.9);
        }}

        .alphabet {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 8px;
            padding: 20px 40px;
            max-width: 1000px;
            margin: 0 auto;
        }}

        .letter-btn {{
            background: var(--surface-color);
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 10px 15px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 800;
            font-size: 1rem;
        }}

        .letter-btn:hover, .letter-btn.active {{
            background: var(--accent);
            color: #000;
            transform: translateY(-3px);
            box-shadow: 0 5px 15px var(--accent-glow);
        }}

        .info-bar {{
            text-align: center;
            padding: 10px;
            color: var(--text-muted);
            font-size: 0.9rem;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 25px;
            padding: 20px 40px;
            max-width: 1400px;
            margin: 0 auto;
        }}

        .card {{
            background: var(--surface-color);
            border: 1px solid var(--border);
            border-radius: 16px;
            overflow: hidden;
            position: relative;
            cursor: pointer;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            display: flex;
            flex-direction: column;
            text-decoration: none;
        }}

        .card:hover {{
            transform: translateY(-10px);
            border-color: var(--accent);
            box-shadow: 0 20px 40px rgba(0,0,0,0.5), 0 0 15px var(--accent-glow);
        }}

        .card-img {{
            width: 100%;
            aspect-ratio: 2/3;
            background-color: #000;
            background-size: cover;
            background-position: center;
            position: relative;
        }}

        .card-content {{
            padding: 15px;
            background: linear-gradient(to top, rgba(15,23,42,1) 0%, rgba(15,23,42,0.8) 100%);
            flex-grow: 1;
            display: flex;
            align-items: center;
        }}

        .card-title {{
            font-size: 0.95rem;
            font-weight: 500;
            color: white;
            line-height: 1.3;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        /* MODAL CSS */
        .modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.90); z-index: 2000; justify-content: center; align-items: center; padding: 20px; backdrop-filter: blur(8px); }}
        .m-content {{ background: var(--bg-color); padding: 50px; border-radius: 15px; max-width: 800px; width: 100%; max-height: 85vh; overflow-y: auto; border: 1px solid var(--accent); position: relative; }}
        .close-modal {{ position: absolute; top: 20px; right: 30px; font-size: 40px; color: var(--accent); cursor: pointer; line-height: 1; }}
        .desc {{ background: rgba(0,0,0,0.4); padding: 30px; border-radius: 10px; line-height: 1.8; margin: 25px 0; color: #d2d2d2; font-size: 1.05rem; border-left: 4px solid var(--accent); }}
        .btn {{ padding: 15px 35px; border-radius: 8px; text-decoration: none; font-weight: 900; font-size: 0.9rem; display: inline-block; margin-right: 15px; text-transform: uppercase; cursor: pointer; }}
        .btn-t {{ background: var(--accent); color: #000; }}

        @media (max-width: 600px) {{
            .grid {{ grid-template-columns: repeat(2, 1fr); padding: 15px; gap: 15px; }}
            header {{ padding: 20px; }}
            h1 {{ font-size: 1.8rem; }}
            .m-content {{ padding: 30px 20px; }}
            .desc {{ padding: 15px; font-size: 0.9rem; }}
        }}
    </style>
</head>
<body>

    <header>
        <div class="header-content">
            <img src="template/avatar.jpg" alt="Logo" class="header-logo" onerror="this.src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAADIAQMAAAAwS4omAAAAA1BMVEWAgICQdD0xAAAANUlEQVR42u3BAQ0AAADCoPdPbQ8HFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB8GzXDAAHTSjU2AAAAAElFTkSuQmCC'">
            <div class="header-text">
                <h1>Biblioteca de juegos Switch ES - The Goonies OS</h1>
                <div class="subtitle">Últimas novedades en juegos para tu Switch</div>
            </div>
        </div>
        <div style="margin-top: 15px; font-size: 0.95rem; text-align: center;">
            Únete a nuestro grupo de Telegram: <a href="https://t.me/+4xc56RbThMg2YjVk" target="_blank" style="color: var(--accent); text-decoration: none; font-weight: 500;" onclick="if(typeof gtag === 'function') gtag('event', 'click_grupo_telegram');">https://t.me/+4xc56RbThMg2YjVk</a>
        </div>
        <div class="search-container">
            <input type="text" id="search" placeholder="Buscar por título o palabra clave...">
        </div>
    </header>

    <div class="alphabet" id="alphabet"></div>
    <div class="info-bar" id="counter-info">Cargando...</div>

    <div class="grid" id="grid"></div>

    <div id="modal" class="modal">
        <div class="m-content">
            <span class="close-modal" onclick="closeM()">&times;</span>
            <div id="m-body"></div>
        </div>
    </div>

    <script>
        const allItems = {json_data};
        let filteredItems = allItems;
        let currentFilter = 'NOVEDADES';

        const alphabetContainer = document.getElementById('alphabet');
        const searchInput = document.getElementById('search');
        const grid = document.getElementById('grid');
        const counterInfo = document.getElementById('counter-info');

        // Generar botones A-Z
        const letters = ['NOVEDADES', 'TODO', '#', ...'ABCDEFGHIJKLMNOPQRSTUVWXYZ'];
        letters.forEach(l => {{
            const btn = document.createElement('button');
            btn.className = 'letter-btn';
            if (l === 'NOVEDADES') btn.classList.add('active');
            btn.innerText = l;
            btn.onclick = () => filterByLetter(l, btn);
            alphabetContainer.appendChild(btn);
        }});

        function filterByLetter(letter, btnElement) {{
            document.querySelectorAll('.letter-btn').forEach(b => b.classList.remove('active'));
            btnElement.classList.add('active');
            currentFilter = letter;
            searchInput.value = ''; // Limpiar buscador
            applyFilters();
        }}

        searchInput.addEventListener('input', () => {{
            document.querySelectorAll('.letter-btn').forEach(b => b.classList.remove('active'));
            if (!searchInput.value.trim()) {{
                document.querySelector('.letter-btn').classList.add('active');
                currentFilter = 'NOVEDADES';
            }} else {{
                currentFilter = 'SEARCH';
            }}
            applyFilters();
        }});

        function applyFilters() {{
            const term = searchInput.value.toLowerCase().trim();
            let isHome = false;
            
            filteredItems = allItems.filter(item => {{
                // Filtro de búsqueda
                if (currentFilter === 'SEARCH' || term) {{
                    return item.title.toLowerCase().includes(term) || item.description.toLowerCase().includes(term);
                }}
                
                // Filtro por letras
                if (currentFilter === 'NOVEDADES') {{
                    isHome = true;
                    return true;
                }}
                if (currentFilter === 'TODO') return true;
                
                const firstChar = item.title.charAt(0).toUpperCase();
                if (currentFilter === '#') {{
                    return /^[0-9\\W]/.test(firstChar); // Número o símbolo
                }}
                return firstChar === currentFilter;
            }});

            if (isHome && !term) {{
                // Ordenar por fecha y sacar los últimos
                filteredItems.sort((a, b) => new Date(b.date) - new Date(a.date));
                filteredItems = filteredItems.slice(0, 15);
                counterInfo.innerText = "Últimas novedades: 15 juegos añadidos recientemente";
            }} else {{
                // Ordenar alfabéticamente
                filteredItems.sort((a, b) => a.title.localeCompare(b.title));
                counterInfo.innerText = `Mostrando ${{filteredItems.length}} publicaciones`;
            }}
            
            renderGrid();
        }}

        function renderGrid() {{
            grid.innerHTML = '';
            const fragment = document.createDocumentFragment();
            
            filteredItems.forEach(item => {{
                const card = document.createElement('div');
                card.className = 'card';
                card.onclick = () => openM(item.id);
                
                card.innerHTML = `
                    <div class="card-img" style="background-image: url('${{item.image}}')"></div>
                    <div class="card-content">
                        <div class="card-title">${{item.title}}</div>
                    </div>
                `;
                fragment.appendChild(card);
            }});
            
            grid.appendChild(fragment);
        }}

        function trackTelegramClick(title) {{
            if (typeof gtag === 'function') {{
                gtag('event', 'click_telegram', {{
                    'juego_titulo': title
                }});
            }}
        }}

        function openM(id) {{
            const g = allItems.find(item => String(item.id) === String(id));
            if (!g) return;
            
            if (typeof gtag === 'function') {{
                gtag('event', 'click_imagen', {{
                    'juego_titulo': g.title
                }});
            }}
            
            document.getElementById('m-body').innerHTML = `
                <h1 style="color:#fff; margin-top:0; font-size: 2.5rem; letter-spacing: -1px;">${{g.title}}</h1>
                <div style="font-size: 0.9rem; color: var(--accent); font-weight: 800; text-transform: uppercase; letter-spacing: 2px;">🗓️ DESDE: ${{new Date(g.date).toLocaleDateString()}}</div>
                <div class="desc">${{g.description}}</div>
                <div style="margin-top: 40px;">
                    <a href="${{g.telegram_url}}" target="_blank" class="btn btn-t" id="btn-telegram">ABRIR EN TELEGRAM</a>
                </div>
            `;
            document.getElementById('btn-telegram').onclick = function() {{ trackTelegramClick(g.title); }};
            document.getElementById('modal').style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }}

        function closeM() {{ document.getElementById('modal').style.display = 'none'; document.body.style.overflow = 'auto'; }}
        window.onclick = (e) => {{ if(e.target == document.getElementById('modal')) closeM(); }};

        // Inicializar
        applyFilters();
    </script>
</body>
</html>"""
    with open(HTML_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ HTML generado exitosamente en: {HTML_OUTPUT}")

async def main():
    print("🚀 Iniciando Gestor de Colecciones Telegram...")
    
    existing_data = []
    indexed_ids = set()
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                for item in existing_data:
                    indexed_ids.add(str(item['id']))
            print(f"📦 Base de datos cargada con {len(existing_data)} elementos.")
        except:
            print("⚠️ Base de datos corrupta o vacía. Se creará una nueva.")

    new_items_count = 0
    
    async with app:
        print("📡 Conectando a Telegram...")
        try:
            chat = await app.get_chat(CHANNEL_ID)
            print(f"✅ Conectado al canal: {chat.title}")
            
            async for message in app.get_chat_history(CHANNEL_ID):
                msg_id = str(message.id)
                
                # Filtrar por topic de juegos
                msg_topic = getattr(message, "message_thread_id", None)
                if msg_topic != TOPIC_ID:
                    continue
                
                if msg_id in indexed_ids:
                    break
                    
                has_media = message.photo or (message.web_page and message.web_page.photo)
                text_content = message.caption or message.text
                
                if has_media and text_content and "#" in text_content:
                    title = clean_title(text_content)
                    
                    img_b64 = None
                    try:
                        await asyncio.sleep(0.5)
                        img_data = await message.download(in_memory=True)
                        if img_data:
                            img_b64 = optimize_image_b64(img_data.getbuffer())
                    except Exception as e:
                        print(f"⚠️ Error al descargar imagen del msg {msg_id}: {e}")
                        
                    if not img_b64:
                        img_b64 = DEFAULT_IMAGE_B64
                        
                    telegram_url = f"https://t.me/c/{str(chat.id)[4:]}/{msg_id}" if str(chat.id).startswith("-100") else f"https://t.me/{chat.id}/{msg_id}"
                    
                    doc = {
                        "id": msg_id,
                        "title": title,
                        "description": clean_text_strictly(text_content).replace('\n', '<br>'),
                        "image": img_b64,
                        "telegram_url": telegram_url,
                        "date": message.date.isoformat()
                    }
                    
                    existing_data.append(doc)
                    print(f"➕ Añadido: {title}")
                    new_items_count += 1
                
        except Exception as e:
            print(f"❌ Error fatal: {e}")
            
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
        
    print(f"💾 Se han guardado {new_items_count} elementos nuevos.")
    
    generate_html(existing_data)
    
if __name__ == "__main__":
    app.run(main())
