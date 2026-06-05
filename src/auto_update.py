import os
import subprocess
import sys

# Fix for Windows CMD encoding
sys.stdout.reconfigure(encoding='utf-8')

def main():
    # Asegurarnos de que estamos en la carpeta raíz
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root_dir)

    print("======================================================")
    print("       INICIANDO ACTUALIZACION AUTOMATICA (NUEVO INDICE)")
    print("======================================================")

    # 1. Ejecutar el script generador
    print("\nEjecutando generar_indice.py...")
    subprocess.run([sys.executable, "generar_indice.py"])

    # 2. Guardar cambios y subir a GitHub de forma automática
    if os.path.exists('.git'):
        print("\n📤 Subiendo cambios a GitHub desde el VPS...")
        try:
            # Añadir archivos al commit
            subprocess.run(["git", "add", "indice_juegos.json", "index.html"], check=True)
            
            # Crear commit con un autor personalizado
            commit_process = subprocess.run([
                "git", "commit", 
                "-m", "Actualizacion automatica del catalogo desde VPS",
                "--author=VPS Auto Updater <vps@goodmanbcn10.com>"
            ], capture_output=True, text=True)
            
            if "nothing to commit" in commit_process.stdout or "no changes added to commit" in commit_process.stdout:
                print("✅ No había cambios nuevos que subir.")
            else:
                # Hacer push a GitHub
                push_process = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
                if push_process.returncode == 0:
                    print("🚀 ¡Cambios subidos a GitHub y publicados en la web con éxito!")
                else:
                    print(f"❌ Error en git push:\n{push_process.stderr}")
        except Exception as e:
            print(f"❌ Error al sincronizar con GitHub: {e}")

    print("\n[+] Proceso automatico completado.")

if __name__ == "__main__":
    main()
