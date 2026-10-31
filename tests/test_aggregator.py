from src.aggregator import aggregate


def test_aggregate_ok():
    rows = [{"amount": 10}, {"amount": 20}, {"amount": 30}]
    r = aggregate(rows)["amount"]
    assert r["sum"] == 60
    assert r["mean"] == 20
    assert r["min"] == 10
    assert r["max"] == 30


def test_aggregate_empty():
    assert aggregate([])["amount"] is None


def test_aggregate_ignores_bool():
    rows = [{"amount": 10}, {"amount": True}]
    assert aggregate(rows)["amount"]["count"] == 1
