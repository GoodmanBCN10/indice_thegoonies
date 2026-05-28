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
        
    print("\n[+] Proceso automatico completado.")

if __name__ == "__main__":
    main()
