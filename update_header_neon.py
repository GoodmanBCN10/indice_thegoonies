import os

target = r'c:\Users\josel\Downloads\Antigravity\INDICE Switch ES - The Goonies OS\src\ui.py'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

old_css = '''        header {{
            background: rgba(16, 25, 33, 0.75);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            padding: 20px 40px; display: flex; align-items: center;
            justify-content: space-between; border-bottom: 1px solid rgba(102, 192, 244, 0.2);
            box-shadow: 0 10px 40px rgba(0,0,0,0.4); position: sticky; top: 0; z-index: 1000;
        }}

        .hero-unit {{ display: flex; align-items: center; gap: 25px; }}
        .avatar-container {{ position: relative; width: 80px; height: 80px; flex-shrink: 0; }}
        .avatar-container::after {{
            content: ""; position: absolute; inset: -4px; border: 2px solid transparent;
            border-radius: 50%;
            background: linear-gradient(45deg, #66c0f4, #b966f4, #f466b9) border-box;
            -webkit-mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: destination-out;
            mask-composite: exclude;
            animation: spin 4s linear infinite;
        }}

        @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
        .avatar {{ width: 100%; height: 100%; border-radius: 50%; object-fit: cover; position: relative; z-index: 2; border: 3px solid #101921; }}
        .brand-titles {{ display: flex; flex-direction: column; }}
        .brand-main {{ font-size: 2.8rem; font-weight: 900; color: transparent; background: linear-gradient(90deg, #ffffff, #66c0f4); -webkit-background-clip: text; background-clip: text; text-transform: uppercase; letter-spacing: -1px; line-height: 1; margin: 0; text-shadow: 0 0 30px rgba(102, 192, 244, 0.3); }}
        .brand-sub {{ font-size: 1rem; font-weight: 600; color: #a3c2d1; text-transform: uppercase; letter-spacing: 5px; margin-top: 4px; }}

        .stats-badge {{
            background: linear-gradient(135deg, rgba(42, 71, 94, 0.6), rgba(27, 40, 56, 0.8));
            padding: 12px 25px; border-radius: 20px;
            border: 1px solid rgba(102, 192, 244, 0.4); text-align: center;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5), 0 5px 15px rgba(0,0,0,0.3);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        }}
        .stats-count {{ font-size: 1.6rem; font-weight: 900; color: #66c0f4; text-shadow: 0 0 10px rgba(102, 192, 244, 0.5); display: block; }}
        .stats-label {{ font-size: 0.65rem; color: #fff; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; opacity: 0.8; }}'''

new_css = '''        header {{
            background: linear-gradient(135deg, rgba(12, 10, 20, 0.9), rgba(20, 15, 35, 0.95));
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            padding: 20px 30px; display: flex; align-items: center;
            justify-content: space-between; border-radius: 20px;
            border: 1px solid rgba(0, 255, 204, 0.3);
            box-shadow: 0 0 30px rgba(0, 255, 204, 0.1), inset 0 0 20px rgba(255, 0, 128, 0.1);
            position: sticky; top: 15px; z-index: 1000;
            margin: 0 15px; width: calc(100% - 30px);
        }}

        .hero-unit {{ display: flex; align-items: center; gap: 20px; }}
        .avatar-container {{ position: relative; width: 75px; height: 75px; flex-shrink: 0; }}
        .avatar-container::after {{
            content: ""; position: absolute; inset: -3px; border: 2px solid transparent;
            border-radius: 16px;
            background: linear-gradient(45deg, #00ffcc, #ff007f) border-box;
            -webkit-mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: destination-out;
            mask-composite: exclude;
            animation: pulse-neon 2s infinite alternate;
        }}

        @keyframes pulse-neon {{ 0% {{ opacity: 0.7; box-shadow: 0 0 10px rgba(0,255,204,0.5); }} 100% {{ opacity: 1; box-shadow: 0 0 25px rgba(255,0,127,0.8); }} }}
        .avatar {{ width: 100%; height: 100%; border-radius: 14px; object-fit: cover; position: relative; z-index: 2; border: 2px solid #0c0a14; }}
        
        .brand-titles {{ display: flex; flex-direction: column; }}
        .brand-main {{ font-size: 2.6rem; font-weight: 900; color: transparent; background: linear-gradient(90deg, #00ffcc, #ff007f); -webkit-background-clip: text; background-clip: text; text-transform: uppercase; letter-spacing: 0px; line-height: 1; margin: 0; filter: drop-shadow(0 0 8px rgba(0,255,204,0.4)); }}
        .brand-sub {{ font-size: 0.95rem; font-weight: 800; color: #ff007f; text-transform: uppercase; letter-spacing: 6px; margin-top: 6px; text-shadow: 0 0 10px rgba(255,0,127,0.5); }}

        .stats-badge {{
            background: rgba(0, 0, 0, 0.6);
            padding: 10px 25px; border-radius: 12px;
            border: 1px solid rgba(0, 255, 204, 0.5); text-align: center;
            box-shadow: 0 0 15px rgba(0, 255, 204, 0.2), inset 0 0 10px rgba(0, 255, 204, 0.1);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            position: relative; overflow: hidden;
        }}
        .stats-badge::before {{ content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%; background: linear-gradient(90deg, transparent, rgba(0,255,204,0.2), transparent); animation: sweep 3s infinite; }}
        @keyframes sweep {{ 0% {{ left: -100%; }} 50%, 100% {{ left: 200%; }} }}
        .stats-count {{ font-size: 1.7rem; font-weight: 900; color: #00ffcc; text-shadow: 0 0 15px rgba(0, 255, 204, 0.8); display: block; letter-spacing: 1px; }}
        .stats-label {{ font-size: 0.65rem; color: #fff; text-transform: uppercase; letter-spacing: 2px; font-weight: 800; opacity: 0.9; margin-top: 2px; }}'''

content = content.replace(old_css, new_css)

old_mobile = '''        @media (max-width: 768px) {{
            header {{ padding: 20px; flex-direction: column; gap: 20px; text-align: center; }}
            .hero-unit {{ flex-direction: column; gap: 15px; }}
            .avatar-container {{ width: 70px; height: 70px; }}
            .brand-main {{ font-size: 2.2rem; }}
            .brand-sub {{ font-size: 0.8rem; letter-spacing: 4px; }}
            .stats-badge {{ padding: 10px 20px; width: 100%; border-radius: 12px; }}'''

new_mobile = '''        @media (max-width: 768px) {{
            header {{ padding: 15px; flex-direction: column; gap: 15px; text-align: center; top: 10px; margin: 0 10px; width: calc(100% - 20px); border-radius: 15px; }}
            .hero-unit {{ flex-direction: column; gap: 15px; }}
            .avatar-container {{ width: 60px; height: 60px; }}
            .brand-main {{ font-size: 1.9rem; }}
            .brand-sub {{ font-size: 0.75rem; letter-spacing: 3px; }}
            .stats-badge {{ padding: 10px 20px; width: 100%; border-radius: 10px; }}'''

content = content.replace(old_mobile, new_mobile)

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated header successfully')
