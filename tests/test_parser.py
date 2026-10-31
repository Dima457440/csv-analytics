import pytest
from pathlib import Path
from src.parser import parse_csv, ParserError


def test_parse_ok(tmp_path: Path):
    f = tmp_path / "ok.csv"
    f.write_text("date,category,amount\n2024-01-01,food,10.5\n", encoding="utf-8")
    rows = parse_csv(str(f))
    assert len(rows) == 1
    assert rows[0]["amount"] == 10.5


def test_missing_columns(tmp_path: Path):
    f = tmp_path / "bad.csv"
    f.write_text("date,amount\n2024-01-01,1\n", encoding="utf-8")
    with pytest.raises(ParserError, match="Отсутствуют колонки"):
        parse_csv(str(f))


def test_file_not_found(tmp_path: Path):
    with pytest.raises(ParserError, match="не найден"):
        parse_csv(str(tmp_path / "none.csv"))
