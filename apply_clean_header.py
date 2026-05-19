import os
import re

target = r'c:\Users\josel\Downloads\Antigravity\INDICE Switch ES - The Goonies OS\src\ui.py'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# I will use a robust regex to replace the entire header css block
# from "header {{" up to the end of ".stats-label {{" block

pattern = re.compile(r'header\s*\{\{.*?\.stats-label\s*\{\{.*?\}\}', re.DOTALL)

clean_css = '''header {{
            background: rgba(13, 17, 23, 0.85);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            padding: 24px 50px; display: flex; align-items: center;
            justify-content: space-between; border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            position: sticky; top: 0; z-index: 1000;
        }}

        .hero-unit {{ display: flex; align-items: center; gap: 24px; }}
        .avatar-container {{ position: relative; width: 65px; height: 65px; flex-shrink: 0; }}
        .avatar-container::after {{ display: none; }} /* Removidos los efectos circulares */

        .avatar {{ width: 100%; height: 100%; border-radius: 50%; object-fit: cover; border: 1px solid rgba(255, 255, 255, 0.1); }}
        
        .brand-titles {{ display: flex; flex-direction: column; justify-content: center; }}
        .brand-main {{ font-size: 2.2rem; font-weight: 800; color: #ffffff; text-transform: uppercase; letter-spacing: -0.5px; line-height: 1; margin: 0; }}
        .brand-sub {{ font-size: 0.95rem; font-weight: 500; color: #8b949e; text-transform: uppercase; letter-spacing: 3px; margin-top: 6px; }}

        .stats-badge {{
            background: rgba(255, 255, 255, 0.03);
            padding: 12px 24px; border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.08); text-align: center;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        }}
        .stats-count {{ font-size: 1.4rem; font-weight: 800; color: #c9d1d9; display: block; }}
        .stats-label {{ font-size: 0.65rem; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-top: 4px; }}'''

if pattern.search(content):
    content = pattern.sub(clean_css, content, count=1)
    print("Header CSS updated.")
else:
    print("Pattern not found for Header CSS!")

# Update mobile CSS
mobile_pattern = re.compile(r'@media\s*\(max-width:\s*768px\)\s*\{\{\s*header\s*\{\{.*?\.stats-badge\s*\{\{.*?\}\}', re.DOTALL)
clean_mobile = '''@media (max-width: 768px) {{
            header {{ padding: 20px; flex-direction: column; gap: 15px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05); }}
            .hero-unit {{ flex-direction: column; gap: 12px; }}
            .avatar-container {{ width: 55px; height: 55px; }}
            .brand-main {{ font-size: 1.8rem; }}
            .brand-sub {{ font-size: 0.8rem; letter-spacing: 2px; }}
            .stats-badge {{ padding: 10px 20px; width: 100%; border-radius: 6px; }}'''

if mobile_pattern.search(content):
    content = mobile_pattern.sub(clean_mobile, content, count=1)
    print("Mobile CSS updated.")
else:
    print("Pattern not found for Mobile CSS!")

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)
