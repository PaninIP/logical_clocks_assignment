from src.vector_clock import happens_before, concurrent


class VersionedKV:
    def __init__(self, strategy="lww"):
        self.strategy = strategy #lww или merge
        self.data = {}
        self.conflicts = 0

    def get(self, key):
        if key not in self.data:
            return None

        item = self.data[key]
        return {"value": item["value"], "vector": item["vector"].copy()}

    def put(self, key, value, vector_clock):
        #для простоты каждая запись это значение и его векторная версия
        new_vector = vector_clock.copy()

        if key not in self.data:
            self.data[key] = {"value": value, "vector": new_vector}
            return "created"

        old = self.data[key]
        old_vector = old["vector"]

        if new_vector == old_vector:
            return "duplicate" #такую версию уже получали

        if happens_before(new_vector, old_vector):
            return "old" #старую версию записывать не будем

        if happens_before(old_vector, new_vector):
            self.data[key] = {"value": value, "vector": new_vector}
            return "updated"

        if concurrent(old_vector, new_vector):
            self.conflicts += 1

            if self.strategy == "lww":
                result = value #последнее пришедшее обновление победило
            else:
                #по условию числа складываем, строки соединяем через |
                if isinstance(value, (int, float)) and isinstance(old["value"], (int, float)):
                    result = old["value"] + value
                elif isinstance(value, str) and isinstance(old["value"], str):
                    result = old["value"] + "|" + value
                else:
                    raise ValueError("Не получилось объединить значения")

            merged_vector = [max(a, b) for a, b in zip(old_vector, new_vector)]
            self.data[key] = {"value": result, "vector": merged_vector}
            return "conflict"
