import json
import os

def clean_description(text):
    promo_text = "NOS QUEDAN 10 NUMEROS LIBRES PARA EL SORTEO, APROVECHAROS Y ESCRIBIDNOS."
    return text.replace(promo_text, "").strip()

def generate_html(games, avatar_b64, output_name="index.html", title_main="SDCS", title_sub="Grupo Steam Deck"):
    for g in games:
        g['description'] = clean_description(g['description'])
        
    json_data = json.dumps(games)
    
    html_template = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{title_main} {title_sub} - Library</title>
    <style>
        :root {{ 
            --bg-deep: #0b0e14; 
            --bg-header: #101921;
            --accent: #66c0f4; 
            --accent-glow: rgba(102, 192, 244, 0.4); 
            --card: #202932; 
        }}
        
        * {{ box-sizing: border-box; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }}
        
        body {{ 
            background-color: var(--bg-deep); color: #c7d5e0; 
            font-family: 'Motiva Sans', Arial, sans-serif; margin: 0; 
            min-height: 100vh; overflow-x: hidden; 
            -webkit-tap-highlight-color: transparent;
        }}
        
        header {{ 
            background: linear-gradient(90deg, var(--bg-header) 0%, #1b2838 100%);
            padding: 30px 60px; display: flex; align-items: center; 
            justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.1); 
            box-shadow: 0 10px 40px rgba(0,0,0,0.6); position: sticky; top: 0; z-index: 1000;
        }}

        .hero-unit {{ display: flex; align-items: center; gap: 35px; }}
        .avatar-container {{ position: relative; width: 100px; height: 100px; flex-shrink: 0; }}
        .avatar-container::after {{
            content: ""; position: absolute; inset: -8px; border: 2px solid var(--accent);
            border-radius: 18px; box-shadow: 0 0 25px var(--accent-glow);
            animation: pulse-border 4s infinite ease-in-out;
        }}

        @keyframes pulse-border {{ 0%, 100% {{ opacity: 0.4; transform: scale(1); }} 50% {{ opacity: 1; transform: scale(1.05); }} }}
        .avatar {{ width: 100%; height: 100%; border-radius: 12px; object-fit: cover; position: relative; z-index: 2; }}
        .brand-titles {{ display: flex; flex-direction: column; }}
        .brand-main {{ font-size: 3.2rem; font-weight: 900; color: #fff; text-transform: uppercase; letter-spacing: -2px; line-height: 0.9; margin: 0; }}
        .brand-sub {{ font-size: 1.1rem; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 8px; margin-top: 5px; }}

        .stats-badge {{
            background: rgba(0,0,0,0.5); padding: 15px 35px; border-radius: 12px;
            border: 1px solid rgba(102, 192, 244, 0.3); text-align: center;
        }}
        .stats-count {{ font-size: 1.8rem; font-weight: 900; color: #fff; display: block; }}
        .stats-label {{ font-size: 0.7rem; color: var(--accent); text-transform: uppercase; letter-spacing: 2px; font-weight: 800; }}

        .alphabet-container {{ 
            display: flex; justify-content: center; flex-wrap: wrap; 
            gap: 8px; padding: 20px 40px; background: rgba(0,0,0,0.3);
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        .letter-btn {{ 
            padding: 12px 18px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); 
            color: #fff; font-size: 1.3rem; font-weight: 900; cursor: pointer; border-radius: 6px;
        }}
        .letter-btn:hover, .letter-btn.active {{ background: var(--accent); color: #000; transform: translateY(-5px); box-shadow: 0 10px 20px var(--accent-glow); }}

        .controls-container {{ margin: 30px auto; max-width: 1100px; padding: 0 20px; display: flex; gap: 20px; align-items: center; }}
        .back-btn {{ 
            background: var(--accent); border: none; color: #000; padding: 15px 30px; 
            border-radius: 8px; cursor: pointer; font-weight: 900; display: none;
            animation: glow-pulse 2s infinite ease-in-out;
        }}
        @keyframes glow-pulse {{ 0% {{ box-shadow: 0 0 5px var(--accent-glow); }} 50% {{ box-shadow: 0 0 20px var(--accent); }} 100% {{ box-shadow: 0 0 5px var(--accent-glow); }} }}
        
        #search {{ flex-grow: 1; padding: 15px 25px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); background: rgba(42, 71, 94, 0.6); color: #fff; outline: none; font-size: 1.1rem; }}
        #sort {{ background: #2a475e; color: #fff; border: none; padding: 0 20px; height: 54px; border-radius: 8px; cursor: pointer; font-weight: bold; }}

        .section-title {{ padding: 20px 60px; font-size: 2rem; font-weight: 900; letter-spacing: 4px; color: #fff; text-transform: uppercase; }}

        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 30px; padding: 10px 60px 60px 60px; }}
        .card {{ background: var(--card); border-radius: 8px; overflow: hidden; cursor: pointer; position: relative; border: 1px solid rgba(255,255,255,0.05); min-height: 300px; }}
        .card:hover {{ transform: scale(1.08) translateY(-10px); border-color: var(--accent); z-index: 10; box-shadow: 0 20px 50px rgba(0,0,0,0.8); }}
        .img-c {{ width: 100%; aspect-ratio: 2/3; background: #000; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; }}
        .backdrop {{ position: absolute; width:120%; height:120%; background-size: cover; filter: blur(12px) brightness(0.3); }}
        .card img {{ width: 100%; height: 100%; object-fit: contain; position: relative; z-index: 1; opacity: 0; transition: opacity 0.6s; }}
        .card-info {{ padding: 15px; background: linear-gradient(transparent, rgba(0,0,0,0.95)); position: absolute; bottom: 0; width: 100%; }}
        .title {{ font-size: 0.9rem; font-weight: 800; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin: 0; color: #fff; }}

        .modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.96); z-index: 2000; justify-content: center; align-items: center; padding: 20px; backdrop-filter: blur(8px); }}
        .m-content {{ background: linear-gradient(135deg, #1b2838 0%, #0b0e14 100%); padding: 50px; border-radius: 15px; max-width: 800px; width: 100%; max-height: 85vh; overflow-y: auto; border: 1px solid var(--accent); position: relative; }}
        .close-modal {{ position: absolute; top: 20px; right: 30px; font-size: 40px; color: var(--accent); cursor: pointer; line-height: 1; }}
        .desc {{ background: rgba(0,0,0,0.4); padding: 30px; border-radius: 10px; line-height: 1.8; margin: 25px 0; color: #d2d2d2; font-size: 1.05rem; border-left: 4px solid var(--accent); }}
        .btn {{ padding: 15px 35px; border-radius: 4px; text-decoration: none; font-weight: 900; font-size: 0.9rem; display: inline-block; margin-right: 15px; text-transform: uppercase; }}
        .btn-s {{ background: linear-gradient(90deg, #75b022, #588a1b); color: white; }}
        .btn-t {{ background: linear-gradient(90deg, #0088cc, #005580); color: white; }}
        #sentinel {{ height: 80px; width: 100%; }}

        /* --- RESPONSIVE MOBILE RULES --- */
        @media (max-width: 768px) {{
            header {{ padding: 20px; flex-direction: column; gap: 20px; text-align: center; }}
            .hero-unit {{ flex-direction: column; gap: 15px; }}
            .avatar-container {{ width: 80px; height: 80px; }}
            .brand-main {{ font-size: 2.2rem; }}
            .brand-sub {{ font-size: 0.8rem; letter-spacing: 4px; }}
            .stats-badge {{ padding: 10px 20px; width: 100%; }}
            
            .alphabet-container {{ padding: 15px 10px; gap: 5px; }}
            .letter-btn {{ padding: 10px 12px; font-size: 1rem; flex: 1 1 15%; }}
            
            .controls-container {{ flex-direction: column; margin: 20px 15px; }}
            .back-btn {{ width: 100%; order: -1; }}
            #search {{ width: 100%; padding: 12px 15px; font-size: 1rem; }}
            #sort {{ width: 100%; height: 48px; }}
            
            .section-title {{ padding: 20px; font-size: 1.4rem; text-align: center; }}
            
            .grid {{ grid-template-columns: repeat(2, 1fr); gap: 15px; padding: 15px; }}
            .card {{ min-height: 220px; }}
            .card-info {{ padding: 10px; }}
            .title {{ font-size: 0.75rem; }}
            
            .m-content {{ padding: 30px 20px; width: 100%; max-height: 95vh; border-radius: 0; }}
            .m-content h1 {{ font-size: 1.6rem !important; }}
            .desc {{ padding: 15px; font-size: 0.9rem; }}
            .btn {{ width: 100%; margin-bottom: 10px; text-align: center; margin-right: 0; }}
        }}

        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: var(--bg-deep); }}
        ::-webkit-scrollbar-thumb {{ background: #2a475e; border-radius: 5px; }}
    </style>
</head>
<body>
    <header>
        <div class="hero-unit">
            <div class="avatar-container">
                {f'<img src="{avatar_b64}" class="avatar">' if avatar_b64 else ''}
            </div>
            <div class="brand-titles">
                <h1 class="brand-main">{title_main}</h1>
                <span class="brand-sub">{title_sub}</span>
            </div>
        </div>
        <div class="stats-badge">
            <span class="stats-count" id="counter">0</span>
            <span class="stats-label" id="total-counter">de 0 JUEGOS</span>
        </div>
    </header>

    <div class="alphabet-container" id="alphabet">
        <button class="letter-btn" onclick="setCategory('NUM')">#</button>
        <button class="letter-btn" onclick="setCategory('SYM')">@</button>
    </div>

    <div class="controls-container">
        <button class="back-btn" id="back-btn" onclick="setCategory('HOME')">⬅ VOLVER AL INICIO</button>
        <input type="text" id="search" placeholder="Filtrar colección...">
        <select id="sort">
            <option value="date-desc">RECIENTES</option>
            <option value="name-asc">ORDEN A-Z</option>
        </select>
    </div>

    <div id="view-title" class="section-title">PUBLICACIONES RECIENTES</div>
    <div class="grid" id="grid"></div>
    <div id="sentinel"></div>
    
    <div id="modal" class="modal">
        <div class="m-content">
            <span class="close-modal" onclick="closeM()">&times;</span>
            <div id="m-body"></div>
        </div>
    </div>

    <script>
        const allGames = {json_data};
        let filteredGames = [];
        let currentIndex = 0;
        let currentCategory = 'HOME';
        const CHUNK_SIZE = 60;
        const grid = document.getElementById('grid');
        const viewTitle = document.getElementById('view-title');
        const backBtn = document.getElementById('back-btn');
        const alphabet = document.getElementById('alphabet');

        const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
        letters.forEach(l => {{
            const btn = document.createElement('button');
            btn.className = 'letter-btn';
            btn.innerText = l;
            btn.onclick = () => setCategory(l);
            alphabet.appendChild(btn);
        }});

        function setCategory(cat) {{
            currentCategory = cat;
            document.querySelectorAll('.letter-btn').forEach(b => b.classList.remove('active'));
            if(cat !== 'HOME' && cat !== 'NUM' && cat !== 'SYM') {{
                const activeBtn = Array.from(document.querySelectorAll('.letter-btn')).find(b => b.innerText === cat);
                if(activeBtn) activeBtn.classList.add('active');
            }}
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
            renderInitial();
        }}

        function getRecentDatesGames() {{
            const dates = [...new Set(allGames.map(g => g.date.split('T')[0]))];
            dates.sort((a, b) => new Date(b) - new Date(a));
            const lastTwoDates = dates.slice(0, 2);
            return allGames.filter(g => lastTwoDates.includes(g.date.split('T')[0]));
        }}

        function renderInitial() {{
            const term = document.getElementById('search').value.toLowerCase();
            const sortBy = document.getElementById('sort').value;
            if (currentCategory === 'HOME') {{
                viewTitle.innerText = "PUBLICACIONES RECIENTES";
                backBtn.style.display = 'none';
                filteredGames = getRecentDatesGames();
                filteredGames.sort((a, b) => new Date(b.date) - new Date(a.date));
            }} else {{
                backBtn.style.display = 'block';
                viewTitle.innerText = "EXPLORANDO: " + currentCategory;
                filteredGames = allGames.filter(g => {{
                    const title = g.title.toUpperCase();
                    const firstChar = title.charAt(0);
                    const matchSearch = g.title.toLowerCase().includes(term) || g.description.toLowerCase().includes(term);
                    if (!matchSearch) return false;
                    if (currentCategory === 'NUM') return /[0-9]/.test(firstChar);
                    if (currentCategory === 'SYM') return /[^A-Z0-9]/.test(firstChar);
                    return firstChar === currentCategory;
                }});
                filteredGames.sort((a, b) => {{
                    if (sortBy === 'name-asc') return a.title.localeCompare(b.title);
                    return new Date(b.date) - new Date(a.date);
                }});
            }}
            document.getElementById('counter').innerText = filteredGames.length;
            document.getElementById('total-counter').innerText = `de ${{allGames.length}} JUEGOS`;
            grid.innerHTML = ''; currentIndex = 0; loadMore();
        }}

        function loadMore() {{
            const end = Math.min(currentIndex + CHUNK_SIZE, filteredGames.length);
            const chunk = filteredGames.slice(currentIndex, end);
            const fragment = document.createDocumentFragment();
            chunk.forEach((g) => {{
                const card = document.createElement('div');
                card.className = 'card';
                card.onclick = () => openM(g.id);
                card.innerHTML = `<div class="img-c"><div class="backdrop" style="background-image:url('${{g.image}}')"></div><img src="${{g.image}}" onload="this.style.opacity=1" style="opacity:0"></div><div class="card-info"><p class="title">${{g.title}}</p></div>`;
                fragment.appendChild(card);
            }});
            grid.appendChild(fragment);
            currentIndex = end;
        }}

        const observer = new IntersectionObserver((entries) => {{
            if (entries[0].isIntersecting && currentIndex < filteredGames.length) loadMore();
        }}, {{ threshold: 0.1 }});
        observer.observe(document.getElementById('sentinel'));

        function openM(id) {{
            const g = allGames.find(item => String(item.id) === String(id));
            if (!g) return;
            const steamBtn = g.steam_url ? `<a href="${{g.steam_url}}" target="_blank" class="btn btn-s">PÁGINA DE STEAM</a>` : '';
            document.getElementById('m-body').innerHTML = `
                <h1 style="color:#fff; margin-top:0; font-size: 2.5rem; letter-spacing: -1px;">${{g.title}}</h1>
                <div style="font-size: 0.9rem; color: var(--accent); margin-bottom: 20px; font-weight: 800; text-transform: uppercase; letter-spacing: 2px;">DISPONIBLE DESDE: ${{new Date(g.date).toLocaleDateString()}}</div>
                <div class="desc">${{g.description}}</div>
                <div style="margin-top: 40px; display:flex; gap: 15px; align-items:center; flex-wrap: wrap;">
                    <a href="${{g.telegram_url}}" target="_blank" class="btn btn-t">ABRIR EN TELEGRAM</a>
                    ${{steamBtn}}
                </div>
            `;
            document.getElementById('modal').style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }}

        function closeM() {{ document.getElementById('modal').style.display = 'none'; document.body.style.overflow = 'auto'; }}
        window.onclick = (e) => {{ if(e.target == document.getElementById('modal')) closeM(); }};
        document.getElementById('search').oninput = renderInitial;
        document.getElementById('sort').onchange = renderInitial;
        renderInitial();
    </script>
</body>
</html>
    """
    with open(output_name, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"✨ {output_name} actualizado con DISEÑO RESPONSIVO (Móvil + Desktop).")
