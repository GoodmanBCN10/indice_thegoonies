import os

target = r'c:\Users\josel\Downloads\Antigravity\INDICE Switch ES - The Goonies OS\src\ui.py'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

old_css = '''        .card { background: var(--card); border-radius: 8px; overflow: hidden; cursor: pointer; position: relative; border: 1px solid rgba(255,255,255,0.05); min-height: 300px; }
        .card:hover { transform: scale(1.08) translateY(-10px); border-color: var(--accent); z-index: 10; box-shadow: 0 20px 50px rgba(0,0,0,0.8); }
        .img-c { width: 100%; aspect-ratio: 2/3; background: #000; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; }
        .backdrop { position: absolute; width:120%; height:120%; background-size: cover; filter: blur(12px) brightness(0.3); }
        .card img { width: 100%; height: 100%; object-fit: contain; position: relative; z-index: 1; opacity: 0; transition: opacity 0.6s; }
        .card-info { padding: 15px; background: linear-gradient(transparent, rgba(0,0,0,0.95)); position: absolute; bottom: 0; width: 100%; }
        .title { font-size: 0.9rem; font-weight: 800; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin: 0; color: #fff; }'''

# We have to substitute '{' and '}' with '{{' and '}}' to match the actual file contents (since it's an f-string)
old_css_escaped = old_css.replace('{', '{{').replace('}', '}}')

new_css = '''        .card { background: var(--card); border-radius: 8px; overflow: hidden; cursor: pointer; position: relative; border: 1px solid rgba(255,255,255,0.05); min-height: 300px; display: flex; flex-direction: column; }
        .card:hover { transform: scale(1.08) translateY(-10px); border-color: var(--accent); z-index: 10; box-shadow: 0 20px 50px rgba(0,0,0,0.8); }
        .img-c { width: 100%; aspect-ratio: 2/3; background: #000; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; flex-shrink: 0; border-bottom: 1px solid rgba(0,0,0,0.5); }
        .backdrop { position: absolute; width:120%; height:120%; background-size: cover; filter: blur(12px) brightness(0.3); }
        .card img { width: 100%; height: 100%; object-fit: contain; position: relative; z-index: 1; opacity: 0; transition: opacity 0.6s; }
        .card-info { padding: 15px; background: rgba(0,0,0,0.2); flex-grow: 1; display: flex; flex-direction: column; justify-content: center; }
        .title { font-size: 0.9rem; font-weight: 700; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; text-overflow: ellipsis; margin: 0; color: #e1e8ed; }'''

new_css_escaped = new_css.replace('{', '{{').replace('}', '}}')

if old_css_escaped in content:
    content = content.replace(old_css_escaped, new_css_escaped)
    with open(target, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated card layout successfully.')
else:
    print('Target CSS block not found.')
