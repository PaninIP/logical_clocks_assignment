import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def draw_diagram(events, file_name):
    #три горизонтальные линии для P1, P2 и P3
    fig, ax = plt.subplots(figsize=(16, 6))
    levels = {0: 3, 1: 2, 2: 1}
    colors = {"INTERNAL": "steelblue", "SEND": "seagreen", "RECEIVE": "orange", "WRITE": "red"}
    max_number = len(events)

    for process_id in range(3):
        ax.hlines(levels[process_id], 0, max_number + 1, color="lightgray")

    for event in events:
        x = event.number #по горизонтали порядок событий, не реальные секунды
        y = levels[event.process_id]
        color = colors[event.event_type]

        ax.scatter(x, y, color=color, s=85, zorder=3)
        label = f"{event.number}\nL={event.lamport}"
        if event.event_type == "RECEIVE":
            ax.text(x, y - 0.14, label, ha="center", va="top", fontsize=8)
        else:
            ax.text(x, y + 0.11, label, ha="center", va="bottom", fontsize=8)

        if event.event_type == "RECEIVE":
            #находим отправку сообщения и рисуем стрелку к получению
            sent = events[event.send_number - 1]
            ax.annotate("", xy=(x, y), xytext=(sent.number, levels[sent.process_id]),
                        arrowprops={"arrowstyle": "->", "color": "gray", "lw": 1.3})

    legend = [Line2D([0], [0], marker="o", color="w", markerfacecolor=color, markersize=8, label=kind)
              for kind, color in colors.items()]
    ax.legend(handles=legend, loc="upper right", ncol=4)
    ax.set_yticks([3, 2, 1], ["P1", "P2", "P3"])
    ax.set_xticks(range(1, max_number + 1))
    ax.set_xlim(0, max_number + 1)
    ax.set_ylim(0.3, 3.8)
    ax.set_xlabel("Номер события")
    ax.set_title("События трёх процессов (красным выделен конфликт)")
    ax.grid(axis="x", alpha=0.15)

    plt.tight_layout()
    plt.savefig(file_name, dpi=150)
    plt.close()
