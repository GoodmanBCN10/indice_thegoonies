import json
import os
import sys
import asyncio

CHANNELS_PATH = os.path.join('data', 'channels.json')
TEMP_PATH = os.path.join('data', '.selection.tmp')
ENV_PATH = '.env'
SESSION_NAME = "my_session"

def check_credentials_and_login():
    """Verifica credenciales y lanza asistente si es necesario."""
    needs_config = True
    if os.path.exists(ENV_PATH):
        try:
            with open(ENV_PATH, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if "API_ID=" in content and "API_HASH=" in content:
                    if "XXXXXX" not in content:
                        needs_config = False
        except: pass
    
    session_exists = os.path.exists(f"{SESSION_NAME}.session")
    
    if needs_config or not session_exists:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("======================================================")
        print("       ASISTENTE DE CONFIGURACION DE TELEGRAM")
        print("======================================================")
        
        if needs_config:
            print("\n 1. CONFIGURACION DE API (Consiguela en my.telegram.org)")
            api_id = input("    Introduce tu API_ID: ").strip()
            api_hash = input("    Introduce tu API_HASH: ").strip()
            
            if not api_id or not api_hash:
                print("\n❌ Error: Datos invalidos."); sys.exit(1)
                
            with open(ENV_PATH, 'w') as f:
                f.write(f"API_ID={api_id}\nAPI_HASH={api_hash}\n")
            print(" ✅ Credenciales guardadas.")
        
        if not session_exists:
            print("\n 2. INICIO DE SESIÓN OFICIAL EN TELEGRAM")
            print("    Se te pedira tu numero de telefono y el codigo que")
            print("    recibiras en tu app de Telegram.\n")
            
            try:
                from hydrogram import Client
                from dotenv import load_dotenv
                load_dotenv()
                
                a_id = os.getenv('API_ID')
                a_hash = os.getenv('API_HASH')

                async def run_login_process():
                    # IMPORTANTE: Crear el cliente DENTRO de la funcion asincrona
                    # para evitar el error 'different loop' en Windows.
                    app = Client(SESSION_NAME, api_id=int(a_id), api_hash=a_hash)
                    async with app:
                        me = await app.get_me()
                        print(f"\n ✅ SESION INICIADA: @{me.username or me.first_name}")

                # Ejecutar de forma segura
                asyncio.run(run_login_process())
                
                print("\n --- Configuracion inicial completada con éxito ---")
                input(" Presione una tecla para continuar al menú principal...")
            except Exception as e:
                print(f"\n❌ ERROR CRITICO DE CONEXION: {e}")
                print("\n Intente borrar el archivo 'my_session.session' si existe.")
                input(" Presione una tecla para salir...")
                sys.exit(1)

def load_channels():
    if not os.path.exists(CHANNELS_PATH): return []
    try:
        with open(CHANNELS_PATH, 'rb') as f:
            raw_data = f.read()
            if not raw_data: return []
            content = raw_data.decode('utf-8-sig').strip()
            if not content or content == "[]": return []
            return json.loads(content)
    except:
        return []

def show_menu():
    check_credentials_and_login()
    
    channels = load_channels()
    if os.path.exists(TEMP_PATH): os.remove(TEMP_PATH)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("======================================================")
    print("           SDCS GRUPO STEAM DECK - GESTOR")
    print("======================================================")
    print("\n SELECCIONE UNA BIBLIOTECA:\n")
    
    if not channels:
        print("  (No hay bibliotecas configuradas todavia)")
    else:
        for i, c in enumerate(channels):
            topic_info = f" [Topic: {c.get('topic_id')}]" if c.get('topic_id') and c.get('topic_id') != "0" else ""
            print(f"  {i+1}. {c['name']}{topic_info} ({c['html']})")
    
    add_opt = len(channels) + 1
    exit_opt = len(channels) + 2
    
    print(f"  {add_opt}. [+] AÑADIR NUEVA SECCION / SUBGRUPO")
    print(f"  {exit_opt}. SALIR")
    print("\n======================================================")
    
    try:
        choice = input(f"Seleccione una opcion [1-{exit_opt}]: ")
        if not choice: show_menu(); return
        idx = int(choice) - 1
        
        if idx == exit_opt - 1: sys.exit(0)
        elif idx == add_opt - 1:
            import subprocess
            subprocess.run([sys.executable, "src/manager.py", "--add"])
            show_menu()
        elif 0 <= idx < len(channels):
            c = channels[idx]
            data = f"{c['channel_id']}|{c.get('topic_id','0')}|{c['db']}|{c['html']}|{c['title_main']}|{c['title_sub']}|{c.get('avatar','avatar.jpg')}|{c['name']}"
            with open(TEMP_PATH, 'w', encoding='utf-8') as f: f.write(data)
        else: show_menu()
    except (ValueError, EOFError, KeyboardInterrupt):
        sys.exit(0)

if __name__ == "__main__":
    show_menu()
