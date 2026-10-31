import os
import psutil
from src.parser import stream_csv, ParserError

def print_resources():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / (1024 * 1024)
    print(f"[Мониторинг] Использование памяти: {mem:.2f} MB")

def scenario_huge_file_stream():
    print("\n--- Сценарий 3: Огромный файл (Стриминг) ---")
    print_resources()
    with open("huge_file.csv", "w", encoding="utf-8") as f:
        f.write("date,category,amount\n")
        for i in range(2_000_000):
            f.write(f"2024-01-01,food,{i}\n")
    
    print("Файл создан. Начинаем стриминговый парсинг...")
    print_resources()
    
    total_sum = 0
    count = 0
    try:
        # Читаем по одной строке через yield
        for row in stream_csv("huge_file.csv"):
            total_sum += row["amount"]
            count += 1
        print(f"Строк обработано: {count}, Сумма: {total_sum}")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        print_resources()
        if os.path.exists("huge_file.csv"):
            os.remove("huge_file.csv")

if __name__ == "__main__":
    scenario_huge_file_stream()
