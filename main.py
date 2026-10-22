import csv
from pathlib import Path
from itertools import combinations

from examples.example_scenario import run_scenario
from src.vector_clock import happens_before, concurrent
from src.visualizer import draw_diagram


#папка, в которой будут лежать график и csv таблицы
GRAPHS = Path("graphs")
GRAPHS.mkdir(exist_ok=True)


def save_csv(file_name, columns, rows):
    with open(GRAPHS / file_name, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)


def main():
    events, results = run_scenario()

    #выводим все события с часами Лэмпорта и векторными часами
    print("\nСобытия процессов:")
    print("№ | Процесс | Событие | Lamport | Vector")

    rows = []
    for event in events:
        name = f"P{event.process_id + 1}"
        print(f"{event.number:2} | {name:7} | {event.event_type:8} | {event.lamport:7} | {event.vector}")
        rows.append([event.number, name, event.event_type, event.message,
                     event.lamport, str(event.vector),
                     f"P{event.peer + 1}" if event.peer is not None else "-",
                     event.send_number if event.send_number is not None else "-"])

    save_csv("events.csv", ["№", "Процесс", "Событие", "Сообщение", "Lamport",
                            "Vector [P1,P2,P3]", "С кем", "Отправка №"], rows)

    #ищем причинно-связанные и конкурентные пары через векторные часы
    related = []
    unrelated = []

    for first, second in combinations(events, 2):
        if happens_before(first.vector, second.vector):
            related.append([first.number, second.number])
        elif happens_before(second.vector, first.vector):
            related.append([second.number, first.number])
        elif concurrent(first.vector, second.vector):
            unrelated.append([first.number, second.number])

    save_csv("causal_pairs.csv", ["Событие раньше", "Событие позже"], related)
    save_csv("concurrent_pairs.csv", ["Первое событие", "Второе событие"], unrelated)

    draw_diagram(events, GRAPHS / "time_space.png")

    all_pairs = len(events) * (len(events) - 1) // 2
    print("\nСтатистика:")
    print(f"Всего событий: {len(events)}")
    print(f"Всего пар: {all_pairs}")
    print(f"Причинно-связанных пар: {len(related)}")
    print(f"Конкурентных пар: {len(unrelated)}")

    print("\nЧто получилось с x:")
    for strategy in ("lww", "merge"):
        state = results[strategy]["x"]
        print(f"{strategy.upper()}: x = {state['value']}, версия {state['vector']}")
    print(f"Merge для строк: {results['text']['value']}")
    print("\nГрафик и таблицы сохранены в graphs")


if __name__ == "__main__":
    main()
