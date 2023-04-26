from lidi import Lidi

from tests.shared import SimpleClassA, SimpleClassB, SimpleClassC


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
