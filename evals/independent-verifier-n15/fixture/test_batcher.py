"""Run with: python3 test_batcher.py"""
from batcher import batches, export


def test_batches_split():
    assert len(batches(list(range(100)))) == 2


def test_export_reports_ok():
    seen = []
    r = export(list(range(100)), seen.append)
    assert r["ok"] is True
    assert r["sent"] == 100


def test_empty():
    assert batches([]) == []


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"ok {name}")
    print("3 passed")
