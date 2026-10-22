class LamportClock:
    def __init__(self):
        self.timestamp = 0 #начинаем отсчёт с нуля

    def increment(self):
        #увеличиваем часы при своём событии или отправке сообщения
        self.timestamp += 1
        return self.timestamp

    def update(self, received_timestamp):
        #при получении берём большее время и прибавляем единицу
        self.timestamp = max(self.timestamp, received_timestamp) + 1
        return self.timestamp
