from src.process import Process
from src.versioned_kv import VersionedKV
from src.vector_clock import concurrent


def run_scenario():
    events = []

    #создаём три процесса, у каждого свои часы
    p1 = Process(0, events)
    p2 = Process(1, events)
    p3 = Process(2, events)
    processes = [p1, p2, p3]

    #P1 и P2 независимо читают x=0 и пытаются его изменить
    write_p1 = p1.write("x = 0 + 1 = 1")
    write_p2 = p2.write("x = 0 * 2 = 0")
    print("Конфликт обновлений:", concurrent(write_p1.vector, write_p2.vector))

    #проверяем обе стратегии, начиная с одной и той же версии x=0
    results = {}
    for strategy in ("lww", "merge"):
        store = VersionedKV(strategy)
        store.put("x", 0, [0, 0, 0])
        store.put("x", 1, write_p1.vector)
        status = store.put("x", 0, write_p2.vector)
        results[strategy] = {"x": store.get("x"), "status": status, "conflicts": store.conflicts}

    #заодно проверяем объединение строк
    text_store = VersionedKV("merge")
    text_store.put("text", "Hello", [1, 0, 0])
    text_store.put("text", "World", [0, 1, 0])
    results["text"] = text_store.get("text")

    p3.internal("Начало работы P3")
    p1.internal("Вычисление P1")

    #теперь процессы обмениваются восемью сообщениями
    messages = [
        (0, 1, "Hello P2"),
        (1, 2, "Hello P3"),
        (2, 0, "Ответ P1"),
        (0, 2, "Данные для P3"),
        (1, 0, "Ping P1"),
        (2, 1, "Ответ P2"),
        (1, 2, "Обновление P3"),
        (0, 1, "Последнее сообщение")
    ]

    for sender, receiver, message in messages:
        packet = processes[sender].send(receiver, message)
        processes[receiver].receive(packet)

    p3.internal("Завершение P3")

    return events, results
