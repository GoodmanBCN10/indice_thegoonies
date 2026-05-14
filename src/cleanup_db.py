import os
import json

def audit_and_clean():
    db_path = os.path.join('data', 'database.json')
    if not os.path.exists(db_path):
        print("❌ No se encontró database.json")
        return

    with open(db_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"❌ Error crítico leyendo el JSON: {e}")
            return

    total_raw = len(data)
    unique_games = {}
    corrupted_count = 0

    print(f"🔍 Auditando {total_raw} registros...")

    for entry in data:
        # 1. Validar campos mínimos
        game_id = entry.get('id')
        title = entry.get('title')
        image = entry.get('image')

        if not game_id or not title or not image:
            corrupted_count += 1
            continue

        # 2. Manejar duplicados (quedarse con la versión que tenga más info o la más reciente)
        if game_id not in unique_games:
            unique_games[game_id] = entry
        else:
            # Si el duplicado tiene marca de 'steam' o 'ultra_optimized', preferimos ese
            if entry.get('ultra_optimized') and not unique_games[game_id].get('ultra_optimized'):
                unique_games[game_id] = entry

    clean_data = list(unique_games.values())
    duplicates_removed = total_raw - len(clean_data) - corrupted_count

    # 3. Guardar base de datos limpia
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(clean_data, f, ensure_ascii=False, indent=4)

    print("\n✅ AUDITORÍA COMPLETADA")
    print(f"-------------------------------")
    print(f"📊 Registros totales iniciales: {total_raw}")
    print(f"🗑️  Entradas corruptas borradas: {corrupted_count}")
    print(f"👯 Duplicados eliminados:        {duplicates_removed}")
    print(f"🎮 JUEGOS REALES RECONOCIDOS:    {len(clean_data)}")
    print(f"-------------------------------")
    print("👉 Base de datos saneada. Ahora puedes correr la MIGRACIÓN o el SCRAPER.")

if __name__ == "__main__":
    audit_and_clean()
