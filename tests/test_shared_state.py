import threading

from lidipy import Lidi

from tests.shared import SimpleClassA, SimpleClassB, SimpleClassC, ThreadService


def test_should_not_have_shared_state() -> None:
    # Given
    lidi_first = Lidi()
    lidi_second = Lidi()

    lidi_first.bind(SimpleClassA, SimpleClassB)
    lidi_second.bind(SimpleClassA, SimpleClassC)

    # When
    resolved_first = lidi_first.resolve(SimpleClassA)
    resolved_second = lidi_second.resolve(SimpleClassA)

    # Then
    assert isinstance(resolved_first, SimpleClassB)
    assert isinstance(resolved_second, SimpleClassC)
    assert type(resolved_first) != type(resolved_second)


def test_should_be_threadsafe() -> None:
    # Given
    lidi = Lidi()
    lidi.bind(ThreadService, ThreadService)

    def resolve_and_increment() -> None:
        thread_service = lidi.resolve(ThreadService)
        thread_service.increment()

    # When
    num_threads = 10
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=resolve_and_increment)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    # Then
    service = lidi.resolve(ThreadService)
    # Value should be 0, that means no state was shared between threads
    assert not service.value


def test_should_be_threadsafe_for_singletons() -> None:
    # Given
    lidi = Lidi()
    lidi.bind(ThreadService, ThreadService, singleton=True)

    def resolve_and_increment() -> None:
        thread_service = lidi.resolve(ThreadService)
        thread_service.increment()

    # When
    num_threads = 10
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=resolve_and_increment)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    # Then
    # Check if the final value of TestService's attribute is equal to the number of threads
    service = lidi.resolve(ThreadService)
    assert service.value == num_threads
