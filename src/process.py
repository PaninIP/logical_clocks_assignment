from src.lamport_clock import LamportClock
from src.vector_clock import VectorClock
from src.event import Event


class Process:
    def __init__(self, process_id, events):
        self.process_id = process_id #0, 1, 2 соответствуют P1, P2, P3
        self.lamport = LamportClock()
        self.vector = VectorClock(3)
        self.events = events

    def add_event(self, event_type, message="", peer=None, send_number=None):
        #сохраняем состояние обоих часов на момент события
        event = Event(
            len(self.events) + 1,
            self.process_id,
            event_type,
            self.lamport.timestamp,
            self.vector.copy(),
            message,
            peer,
            send_number
        )
        self.events.append(event)
        return event

    def internal(self, message="Внутреннее событие"):
        self.lamport.increment()
        self.vector.increment(self.process_id)
        return self.add_event("INTERNAL", message)

    def write(self, message):
        #запись в хранилище тоже считаем локальным событием
        self.lamport.increment()
        self.vector.increment(self.process_id)
        return self.add_event("WRITE", message)

    def send(self, receiver_id, message):
        self.lamport.increment()
        self.vector.increment(self.process_id)
        event = self.add_event("SEND", message, receiver_id)

        #передаём текст сообщения и копии логических часов
        return {
            "sender": self.process_id,
            "receiver": receiver_id,
            "message": message,
            "timestamp": self.lamport.timestamp,
            "vector": self.vector.copy(),
            "send_number": event.number
        }

    def receive(self, message):
        self.lamport.update(message["timestamp"])
        self.vector.update(message["vector"])
        self.vector.increment(self.process_id) #после получения увеличиваем свой счётчик

        return self.add_event(
            "RECEIVE", message["message"], message["sender"], message["send_number"]
        )
