import os
import json
import base64

DB_PATH = os.path.join('data', 'database.json')
AVATAR_PATH = os.path.join('template', 'avatar.jpg')

def get_avatar():
    if os.path.exists(AVATAR_PATH):
        with open(AVATAR_PATH, 'rb') as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

def build():
    if not os.path.exists(DB_PATH):
        print("❌ No hay base de datos.")
        return

    with open(DB_PATH, 'r', encoding='utf-8') as f:
        games = json.load(f)

    avatar_b64 = get_avatar()
    json_data = json.dumps(games)
    
    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>SDCS Backups</title>
    <style>
        :root {{ --bg: #0b0e14; --accent: #66c0f4; --card: #202932; }}
        body {{ background: var(--bg); color: #c7d5e0; font-family: sans-serif; margin: 0; overflow-x: hidden; }}
        header {{ background: #171d25; padding: 15px 40px; display: flex; align-items: center; justify-content: space-between; border-bottom: 3px solid var(--accent); }}
        .avatar {{ width: 70px; height: 70px; border-radius: 12px; border: 2px solid var(--accent); object-fit: cover; }}
        .brand {{ font-size: 2rem; font-weight: 900; color: #fff; text-transform: uppercase; }}
        .controls {{ margin: 20px auto; max-width: 1000px; display: flex; gap: 10px; padding: 0 20px; }}
        input, select {{ background: #2a3f5a; color: #fff; border: none; padding: 12px; border-radius: 4px; outline: none; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px; padding: 20px 30px; }}
        .card {{ background: var(--card); border-radius: 4px; overflow: hidden; cursor: pointer; border: 1px solid rgba(255,255,255,0.02); }}
        .card:hover {{ transform: scale(1.05); border-color: var(--accent); }}
        .img-c {{ width: 100%; aspect-ratio: 2/3; background: #000; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; }}
        .backdrop {{ position: absolute; width:115%; height:115%; background-size: cover; filter: blur(8px) brightness(0.3); }}
        .card img {{ width: 100%; height: 100%; object-fit: contain; position: relative; z-index: 1; }}
        .modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.95); z-index: 2000; justify-content: center; align-items: center; }}
        .m-content {{ background: #1b2838; padding: 40px; border-radius: 8px; max-width: 700px; width: 90%; max-height: 85vh; overflow-y: auto; border: 1px solid var(--accent); }}
        .btn {{ padding: 12px 25px; border-radius: 2px; text-decoration: none; font-weight: bold; color: white; display: inline-block; margin-right: 10px; }}
    </style>
</head>
<body>
    <header>
        <div style="display:flex; align-items:center; gap:20px;">
            <img src="{avatar_b64}" class="avatar">
            <div class="brand">SDCS Backups</div>
        </div>
        <div id="counter" style="color:var(--accent); font-weight:bold;"></div>
    </header>
    <div class="controls">
        <input type="text" id="search" placeholder="Buscar...">
        <select id="sort">
            <option value="date-desc">RECIENTES</option>
            <option value="name-asc">A-Z</option>
        </select>
    </div>
    <div class="grid" id="grid"></div>
    <div id="modal" class="modal"><div class="m-content" id="m-body"></div></div>

    <script>
        const games = {json_data};
        function render() {{
            const t = document.getElementById('search').value.toLowerCase();
            const s = document.getElementById('sort').value;
            let f = games.filter(g => g.title.toLowerCase().includes(t));
            if(s==='name-asc') f.sort((a,b)=>a.title.localeCompare(b.title));
            else f.sort((a,b)=>new Date(b.date)-new Date(a.date));
            
            document.getElementById('counter').innerText = f.length + ' TITULOS';
            document.getElementById('grid').innerHTML = f.map(g => `
                <div class="card" onclick="openM('${{g.id}}')">
                    <div class="img-c">
                        <div class="backdrop" style="background-image:url('${{g.image}}')"></div>
                        <img src="${{g.image}}" loading="lazy">
                    </div>
                    <div style="padding:8px; font-size:0.7rem; font-weight:bold; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${{g.title}}</div>
                </div>
            `).join('');
        }}

        function openM(id) {{
            const g = games.find(item => String(item.id) === String(id));
            if(!g) return;
            const steam = g.steam_url ? '<a href="'+g.steam_url+'" target="_blank" class="btn" style="background:#5c7e10">STEAM</a>' : '';
            document.getElementById('m-body').innerHTML = `
                <h1 style="color:#fff;margin-top:0;">${{g.title}}</h1>
                <div style="background:rgba(0,0,0,0.3);padding:20px;border-radius:4px;margin:20px 0;line-height:1.7;">${{g.description}}</div>
                <a href="${{g.telegram_url}}" target="_blank" class="btn" style="background:#0088cc">TELEGRAM</a>
                ${{steam}}
                <button onclick="document.getElementById('modal').style.display='none';document.body.style.overflow='auto'" style="float:right;background:none;border:none;color:var(--accent);cursor:pointer;font-weight:bold;padding:10px;">CERRAR</button>
            `;
            document.getElementById('modal').style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }}

        document.getElementById('search').oninput = render;
        document.getElementById('sort').onchange = render;
        render();
    </script>
</body>
</html>
    """
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✨ index.html regenerado correctamente.")

if __name__ == "__main__":
    build()
