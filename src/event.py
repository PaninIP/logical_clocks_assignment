class Event:
    def __init__(self, number, process_id, event_type, lamport, vector, message="", peer=None, send_number=None):
        self.number = number
        self.process_id = process_id
        self.event_type = event_type
        self.lamport = lamport
        self.vector = vector
        self.message = message
        self.peer = peer #с каким процессом общаемся
        self.send_number = send_number #номер отправки для построения стрелки
