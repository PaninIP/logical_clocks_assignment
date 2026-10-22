class VectorClock:
    def __init__(self, cnt_processes=3):
        self.vector = [0] * cnt_processes #для каждого процесса свой счётчик

    def increment(self, process_id):
        self.vector[process_id] += 1
        return self.copy()

    def update(self, received_vector):
        #сравниваем элементы двух векторов и оставляем наибольшие
        for i in range(len(self.vector)):
            self.vector[i] = max(self.vector[i], received_vector[i])
        return self.copy()

    def copy(self):
        return self.vector.copy() #копия нужна, чтобы старые события не изменялись


def happens_before(v1, v2):
    #v1 раньше v2, если он не больше по всем компонентам и где-то меньше
    return all(a <= b for a, b in zip(v1, v2)) and any(a < b for a, b in zip(v1, v2))


def concurrent(v1, v2):
    #если ни одно событие не было раньше другого, значит они конкурентны
    return v1 != v2 and not happens_before(v1, v2) and not happens_before(v2, v1)
