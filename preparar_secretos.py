import os
import base64

def main():
    print("======================================================")
    print("       PREPARACION DE SECRETS PARA GITHUB ACTIONS")
    print("======================================================\n")

    # 1. Sesion de Telegram
    session_file = "my_session.session"
    if not os.path.exists(session_file):
        # A veces se guarda en src/
        session_file = os.path.join("src", "my_session.session")
        if not os.path.exists(session_file):
            print(f"❌ ERROR: No se encuentra el archivo my_session.session.")
            print("Asegúrate de ejecutar run.bat y configurar tu cuenta de Telegram primero.")
            return

    with open(session_file, "rb") as f:
        session_data = f.read()
    
    session_b64 = base64.b64encode(session_data).decode('utf-8')

    print("Copia el siguiente texto y pégalo en GitHub Secrets con el nombre: TELEGRAM_SESSION\n")
    print("-" * 60)
    print(session_b64)
    print("-" * 60)
    print("\n")

    # 2. .env file
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            env_content = f.read()
        print("Copia los valores de tu .env a los siguientes Secrets:")
        print("TELEGRAM_API_ID = (El numero que tienes en API_ID)")
        print("TELEGRAM_API_HASH = (El texto que tienes en API_HASH)")
        print("\nContenido actual de tu .env para referencia:")
        print(env_content)
    else:
        print("❌ No se encontró el archivo .env")

    print("\nProceso terminado. Presiona enter para salir.")
    input()

if __name__ == "__main__":
    main()
