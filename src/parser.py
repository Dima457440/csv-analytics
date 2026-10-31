import csv
import os


class ParserError(Exception):
    """Ошибка парсинга CSV."""


REQUIRED_COLUMNS = {"date", "category", "amount"}


def parse_csv(file_path: str) -> list[dict]:
    if not os.path.exists(file_path):
        raise ParserError(f"Файл не найден: {file_path}")

    # utf-8-sig автоматически отбрасывает BOM, если он есть
    with open(file_path, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        if not reader.fieldnames:
            raise ParserError("Файл пуст или отсутствует заголовок")

        # нормализация имён колонок: убираем пробелы и возможные BOM-символы
        reader.fieldnames = [
            name.strip().lstrip("\ufeff") for name in reader.fieldnames
        ]

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ParserError(f"Отсутствуют колонки: {', '.join(sorted(missing))}")

        rows = []
        for i, row in enumerate(reader, start=2):
            try:
                row["amount"] = float(row["amount"])
            except (TypeError, ValueError) as exc:
                raise ParserError(f"Строка {i}: amount не является числом") from exc
            rows.append(row)

    return rows
