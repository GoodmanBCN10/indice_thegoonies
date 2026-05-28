import json
import os
import sys

# Fix for Windows CMD encoding
sys.stdout.reconfigure(encoding='utf-8')

CHANNELS_PATH = os.path.join('data', 'channels.json')
TEMPLATE_DIR = 'template'

def load_channels():
    if not os.path.exists(CHANNELS_PATH): return []
    try:
        with open(CHANNELS_PATH, 'rb') as f:
            raw_data = f.read()
            if not raw_data: return []
            content = raw_data.decode('utf-8-sig').strip()
            if not content or content == "[]": return []
            return json.loads(content)
    except Exception as e:
        print(f"⚠️ Nota al leer canales: {e}")
        return []

def save_channels(channels):
    try:
        if not os.path.exists('data'): os.makedirs('data')
        with open(CHANNELS_PATH, 'w', encoding='utf-8') as f:
            json.dump(channels, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"❌ Error al guardar canales: {e}")
        return False

def get_available_avatars():
    try:
        valid_ext = ('.jpg', '.jpeg', '.png', '.webp')
        if not os.path.exists(TEMPLATE_DIR):
            os.makedirs(TEMPLATE_DIR)
            return []
        return [f for f in os.listdir(TEMPLATE_DIR) if f.lower().endswith(valid_ext)]
    except:
        return []

def add_new_channel():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("======================================================")
        print("           AÑADIR NUEVA BIBLIOTECA / SUBGRUPO")
        print("======================================================")
        
        name = input("  Nombre de la biblioteca: ").strip()
        if not name: return

        c_id = input("  ID de Telegram (-100...): ").strip()
        if not c_id: return

        t_id = input("  ID Topic (Enter si no hay): ").strip()
        if not t_id: t_id = "0"
        
        html = input("  Archivo HTML (ej: Biblioteca_PC): ").strip()
        if not html: return
        if not html.lower().endswith(".html"): html += ".html"
        
        db = html.lower().replace(".html", ".json")
        if not db.startswith("database_") and db != "database.json":
            db = f"database_{db}"

        t_m = input("  Titulo Web Principal: ").strip()
        t_s = input("  Subtitulo Web: ").strip()

        # Selección de Avatar Protegida
        selected_avatar = "avatar.jpg"
        try:
            avatars = get_available_avatars()
            if len(avatars) > 1:
                print("\n  Avatares disponibles:")
                for i, av in enumerate(avatars):
                    print(f"    {i+1}. {av}")
                av_choice = input(f"\n  Elija numero [1-{len(avatars)}]: ")
                if av_choice.isdigit():
                    idx = int(av_choice) - 1
                    if 0 <= idx < len(avatars):
                        selected_avatar = avatars[idx]
            elif len(avatars) == 1:
                selected_avatar = avatars[0]
        except:
            pass # Si falla la busqueda de avatares, seguimos con el default

        channels = load_channels()
        new_entry = {
            "id": name.upper().replace(" ", "_"),
            "channel_id": c_id,
            "topic_id": t_id,
            "name": name,
            "html": html,
            "db": db,
            "avatar": selected_avatar,
            "title_main": t_m,
            "title_sub": t_s
        }
        
        channels.append(new_entry)
        if save_channels(channels):
            print(f"\n  ✅ EXITO: Guardado como '{html}'")
        else:
            print("\n  ❌ FALLO: No se pudo guardar el archivo JSON.")
            
        print("\n======================================================")
        input("  Presione una tecla para volver...")

    except Exception as e:
        print(f"\n  ❌ ERROR INESPERADO: {e}")
        input("  Presione una tecla para ver el error antes de salir...")

if __name__ == "__main__":
    add_new_channel()
