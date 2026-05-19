import os
import re

target = r'c:\Users\josel\Downloads\Antigravity\INDICE Switch ES - The Goonies OS\src\ui.py'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# I need to restore the {{ }} for the CSS I injected!
old_css = '''        header { 
            background: rgba(16, 25, 33, 0.75);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            padding: 20px 40px; display: flex; align-items: center; 
            justify-content: space-between; border-bottom: 1px solid rgba(102, 192, 244, 0.2); 
            box-shadow: 0 10px 40px rgba(0,0,0,0.4); position: sticky; top: 0; z-index: 1000;
        }

        .hero-unit { display: flex; align-items: center; gap: 25px; }
        .avatar-container { position: relative; width: 80px; height: 80px; flex-shrink: 0; }
        .avatar-container::after {
            content: ""; position: absolute; inset: -4px; border: 2px solid transparent;
            border-radius: 50%; 
            background: linear-gradient(45deg, #66c0f4, #b966f4, #f466b9) border-box;
            -webkit-mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: destination-out;
            mask-composite: exclude;
            animation: spin 4s linear infinite;
        }

        @keyframes spin { 100% { transform: rotate(360deg); } }
        .avatar { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; position: relative; z-index: 2; border: 3px solid #101921; }
        .brand-titles { display: flex; flex-direction: column; }
        .brand-main { font-size: 2.8rem; font-weight: 900; color: transparent; background: linear-gradient(90deg, #ffffff, #66c0f4); -webkit-background-clip: text; background-clip: text; text-transform: uppercase; letter-spacing: -1px; line-height: 1; margin: 0; text-shadow: 0 0 30px rgba(102, 192, 244, 0.3); }
        .brand-sub { font-size: 1rem; font-weight: 600; color: #a3c2d1; text-transform: uppercase; letter-spacing: 5px; margin-top: 4px; }

        .stats-badge {
            background: linear-gradient(135deg, rgba(42, 71, 94, 0.6), rgba(27, 40, 56, 0.8));
            padding: 12px 25px; border-radius: 20px;
            border: 1px solid rgba(102, 192, 244, 0.4); text-align: center;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5), 0 5px 15px rgba(0,0,0,0.3);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        }
        .stats-count { font-size: 1.6rem; font-weight: 900; color: #66c0f4; text-shadow: 0 0 10px rgba(102, 192, 244, 0.5); display: block; }
        .stats-label { font-size: 0.65rem; color: #fff; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; opacity: 0.8; }'''

new_css = old_css.replace('{', '{{').replace('}', '}}')
content = content.replace(old_css, new_css)

old_mobile = '''.avatar-container { width: 70px; height: 70px; }
            .brand-main { font-size: 2.2rem; }
            .brand-sub { font-size: 0.8rem; letter-spacing: 4px; }
            .stats-badge { padding: 10px 20px; width: 100%; border-radius: 12px; }'''
new_mobile = old_mobile.replace('{', '{{').replace('}', '}}')
content = content.replace(old_mobile, new_mobile)

# The JS functions also have { and }, but since they are in an f-string, wait!
# JS in an f-string also needs {{ and }}!
# The JS I replaced had single braces!
# Let's fix the JS replacement too!

old_setCat = '''function setCategory(cat) {
            currentCategory = cat;
            document.getElementById('search').value = '';
            document.querySelectorAll('.letter-btn').forEach(b => b.classList.remove('active'));
            if(cat !== 'HOME' && cat !== 'NUM' && cat !== 'SYM') {
                const activeBtn = Array.from(document.querySelectorAll('.letter-btn')).find(b => b.innerText === cat);
                if(activeBtn) activeBtn.classList.add('active');
            }
            window.scrollTo({ top: 0, behavior: 'smooth' });
            renderInitial();
        }'''

new_setCat = old_setCat.replace('{', '{{').replace('}', '}}')
content = content.replace(old_setCat, new_setCat)

old_render = '''function renderInitial() {
            const term = document.getElementById('search').value.toLowerCase();
            const sortBy = document.getElementById('sort').value;
            if (term) {
                backBtn.style.display = 'block';
                viewTitle.innerText = RESULTADOS DE BÚSQUEDA: "";
                filteredGames = allGames.filter(g => {
                    return g.title.toLowerCase().includes(term) || g.description.toLowerCase().includes(term);
                });
                filteredGames.sort((a, b) => {
                    if (sortBy === 'name-asc') return a.title.localeCompare(b.title);
                    return new Date(b.date) - new Date(a.date);
                });
                document.querySelectorAll('.letter-btn').forEach(b => b.classList.remove('active'));
            } else if (currentCategory === 'HOME') {
                viewTitle.innerText = "PUBLICACIONES RECIENTES";
                backBtn.style.display = 'none';
                filteredGames = getRecentDatesGames();
                filteredGames.sort((a, b) => new Date(b.date) - new Date(a.date));
            } else {
                backBtn.style.display = 'block';
                viewTitle.innerText = "EXPLORANDO: " + currentCategory;
                filteredGames = allGames.filter(g => {
                    const title = g.title.toUpperCase();
                    const firstChar = title.charAt(0);
                    if (currentCategory === 'NUM') return /[0-9]/.test(firstChar);
                    if (currentCategory === 'SYM') return /[^A-Z0-9]/.test(firstChar);
                    return firstChar === currentCategory;
                });
                filteredGames.sort((a, b) => {
                    if (sortBy === 'name-asc') return a.title.localeCompare(b.title);
                    return new Date(b.date) - new Date(a.date);
                });
            }
            document.getElementById('counter').innerText = filteredGames.length;
            document.getElementById('total-counter').innerText = de  JUEGOS;
            grid.innerHTML = ''; currentIndex = 0; loadMore();
        }'''

new_render = old_render.replace('{', '{{').replace('}', '}}')
# Except inside the JS template string ${term.toUpperCase()} which needs to evaluate as JS but inside an f-string it shouldn't evaluate as python.
# Wait, in the JS I used RESULTADOS DE BÚSQUEDA: "". No python interpolation, but python f-string would try to evaluate it if I use {}!
# If I change it to {{term.toUpperCase()}}, python ignores it, and it outputs {term.toUpperCase()}, which then JS template string interprets correctly because JS uses ${...}! So ${{term.toUpperCase()}} is outputted as ${term.toUpperCase()}. Wait!
# Python replacing { with {{ for ${...} results in ${{...}}. So the f-string outputs ${...}. Perfect!

content = content.replace(old_render, new_render)

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed f-string braces in ui.py!')
