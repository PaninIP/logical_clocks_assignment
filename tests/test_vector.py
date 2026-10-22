from src.vector_clock import VectorClock, happens_before, concurrent
from examples.example_scenario import run_scenario


def test_vector():
    clock = VectorClock(3)
    assert clock.increment(0) == [1, 0, 0]
    old_vector = clock.copy()
    clock.update([0, 2, 1])
    assert clock.vector == [1, 2, 1]
    assert old_vector == [1, 0, 0]


def test_comparison():
    assert happens_before([1, 0, 0], [1, 1, 0])
    assert not happens_before([1, 1, 0], [1, 0, 0])
    assert concurrent([1, 0, 0], [0, 1, 0])
    assert not concurrent([1, 0, 0], [1, 0, 0])


def test_messages():
    events, _ = run_scenario()
    received = [event for event in events if event.event_type == "RECEIVE"]
    assert len(received) == 8
    for event in received:
        sent = events[event.send_number - 1]
        assert happens_before(sent.vector, event.vector)
