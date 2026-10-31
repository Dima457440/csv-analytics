import csv

import os

import logging

log = logging.getLogger(__name__)


class ParserError(Exception):
    """Ошибка парсинга CSV."""


REQUIRED_COLUMNS = {"date", "category", "amount"}


def parse_csv(file_path: str) -> list[dict]:
    """Читает CSV файл и возвращает список словарей."""

    log.info("Начат парсинг файла: %s", file_path)

    if not os.path.exists(file_path):

        log.error("Файл не найден: %s", file_path)

        raise ParserError(f"Файл не найден: {file_path}")

    with open(file_path, mode="r", encoding="utf-8-sig", newline="") as f:

        reader = csv.DictReader(f)

        if not reader.fieldnames:

            raise ParserError("Файл пуст или отсутствует заголовок")

        # Нормализация заголовков

        reader.fieldnames = [
            name.strip().lstrip("\ufeff") for name in reader.fieldnames
        ]

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)

        if missing:

            msg = f"Отсутствуют колонки: {', '.join(sorted(missing))}"

            raise ParserError(msg)

        rows = []

        for i, row in enumerate(reader, start=2):

            try:

                row["amount"] = float(row["amount"])

            except (TypeError, ValueError) as exc:

                log.error("Ошибка в строке %s: %s", i, exc)

                raise ParserError(f"Строка {i}: amount не является числом") from exc

            rows.append(row)

    log.info("Парсинг завершен. Строк: %s", len(rows))

    return rows
def stream_csv(file_path: str):
    """Генератор: читает CSV построчно, не загружая всё в память (для больших файлов)."""
    import os
    import csv
    import logging
    log = logging.getLogger(__name__)
    
    if not os.path.exists(file_path):
        log.error("Файл не найден: %s", file_path)
        raise ParserError(f"Файл не найден: {file_path}")

    with open(file_path, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ParserError("Файл пуст или отсутствует заголовок")
            
        reader.fieldnames = [name.strip().lstrip("\ufeff") for name in reader.fieldnames]
        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ParserError(f"Отсутствуют колонки: {', '.join(sorted(missing))}")

        for i, row in enumerate(reader, start=2):
            try:
                row["amount"] = float(row["amount"])
            except (TypeError, ValueError) as exc:
                raise ParserError(f"Строка {i}: amount не является числом") from exc
            yield row
