from src.versioned_kv import VersionedKV


def test_conflict():
    store = VersionedKV("lww")
    store.put("x", 0, [0, 0, 0])
    store.put("x", 1, [1, 0, 0])
    assert store.put("x", 0, [0, 1, 0]) == "conflict"
    assert store.get("x") == {"value": 0, "vector": [1, 1, 0]}

    merge = VersionedKV("merge")
    merge.put("x", 0, [0, 0, 0])
    merge.put("x", 1, [1, 0, 0])
    merge.put("x", 0, [0, 1, 0])
    assert merge.get("x")["value"] == 1
    assert merge.conflicts == 1


def test_old_version():
    store = VersionedKV()
    store.put("x", 2, [2, 0, 0])
    assert store.put("x", 9, [1, 0, 0]) == "old"
    assert store.get("x")["value"] == 2


def test_text_merge():
    store = VersionedKV("merge")
    store.put("text", "Hello", [1, 0, 0])
    store.put("text", "World", [0, 1, 0])
    assert store.get("text")["value"] == "Hello|World"
