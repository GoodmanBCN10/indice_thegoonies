import json
import os
import subprocess
import sys

# Fix for Windows CMD encoding
sys.stdout.reconfigure(encoding='utf-8')

def main():
    # Asegurarnos de que estamos en la carpeta raíz
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root_dir)

    channels_path = os.path.join('data', 'channels.json')
    if not os.path.exists(channels_path):
        print("❌ No hay canales configurados en data/channels.json")
        return

    try:
        with open(channels_path, 'rb') as f:
            content = f.read().decode('utf-8-sig').strip()
            channels = json.loads(content) if content else []
    except Exception as e:
        print(f"❌ Error leyendo channels.json: {e}")
        return

    print(f"======================================================")
    print(f"       INICIANDO ACTUALIZACION AUTOMATICA ({len(channels)} canales)")
    print(f"======================================================")

    scraper_path = os.path.join('src', 'scraper.py')
    py_engine = sys.executable

    for idx, c in enumerate(channels):
        print(f"\n[{idx+1}/{len(channels)}] ACTUALIZANDO: {c.get('name', 'Desconocido')}")
        args = [
            py_engine,
            scraper_path,
            str(c.get('channel_id', '')),
            str(c.get('topic_id', '0')),
            str(c.get('db', '')),
            str(c.get('html', '')),
            str(c.get('title_main', '')),
            str(c.get('title_sub', '')),
            str(c.get('avatar', 'avatar.jpg'))
        ]
        
        # Ejecutar el scraper original
        subprocess.run(args)
        
        # Sincronizar automáticamente con index.html
        html_name = c.get('html', '')
        if html_name and os.path.exists(html_name):
            import shutil
            shutil.copyfile(html_name, "index.html")
            print(f"📢 Sincronizado {html_name} con index.html")
        
    print("\n[+] Proceso automatico completado.")


if __name__ == "__main__":
    main()
