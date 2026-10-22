from src.lamport_clock import LamportClock


def test_lamport():
    clock = LamportClock()
    assert clock.increment() == 1
    assert clock.update(5) == 6 #принимаем сообщение от процесса с часами 5
    assert clock.update(2) == 7
