import asyncio
import os
from hydrogram import Client
from dotenv import load_dotenv

async def main():
    print("======================================================")
    print("       PREPARACION DE SECRETS PARA GITHUB ACTIONS")
    print("======================================================\n")
    print("Extrayendo clave segura de sesion...")

    load_dotenv()
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    
    session_name = "my_session"
    if not os.path.exists("my_session.session") and os.path.exists("src/my_session.session"):
        session_name = "src/my_session"
        
    try:
        app = Client(session_name, api_id=api_id, api_hash=api_hash)
        await app.start()
        string_session = await app.export_session_string()
        await app.stop()
        
        with open("SECRETO_A_COPIAR.txt", "w") as f:
            f.write(string_session)
            
        print("\n¡EXITO! He creado un archivo llamado SECRETO_A_COPIAR.txt en esta carpeta.")
        print("Abre ese archivo, selecciona TODO el texto (es solo una linea larga) y pegalo en GitHub como TELEGRAM_SESSION.")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    asyncio.run(main())