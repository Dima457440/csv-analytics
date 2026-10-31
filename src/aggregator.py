from statistics import mean

NUMERIC_TYPES = (int, float)

DEFAULT_COLUMNS = ("amount",)


def _is_number(value) -> bool:

    return isinstance(value, NUMERIC_TYPES) and not isinstance(value, bool)


def aggregate(rows: list[dict], numeric_cols=DEFAULT_COLUMNS) -> dict:
    """Сводная статистика: sum, mean, min, max по числовым колонкам."""

    if not rows:

        return {col: None for col in numeric_cols}

    result = {}

    for col in numeric_cols:

        values = [r[col] for r in rows if _is_number(r.get(col))]

        if not values:

            result[col] = None

            continue

        result[col] = {
            "sum": sum(values),
            "mean": mean(values),
            "min": min(values),
            "max": max(values),
            "count": len(values),
        }

    return result
