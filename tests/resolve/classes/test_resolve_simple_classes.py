from lidipy import Lidi

from tests.shared import SimpleClassA, SimpleClassB, SimpleClassC


def test_should_resolve_simple_class() -> None:
    # Given
    lidi = Lidi()
    lidi.bind(SimpleClassA, SimpleClassB)

    # When
    resolved_class = lidi.resolve(SimpleClassA)

    # Then
    assert isinstance(resolved_class, SimpleClassB)
    assert not isinstance(resolved_class, SimpleClassA)


def test_should_resolve_simple_class_as_instance() -> None:
    # Given
    lidi = Lidi()
    initiated_class = SimpleClassB()
    lidi.bind(SimpleClassA, initiated_class)

    # When
    resolved_class = lidi.resolve(SimpleClassA)

    # Then
    assert isinstance(resolved_class, SimpleClassB)
    assert initiated_class is resolved_class
    assert not isinstance(resolved_class, SimpleClassA)


def test_should_resolve_simple_class_as_singleton() -> None:
    # Given
    lidi = Lidi()
    lidi.bind(SimpleClassA, SimpleClassB, singleton=True)

    # When
    resolved_class_first = lidi.resolve(SimpleClassA)
    resolved_class_second = lidi.resolve(SimpleClassA)

    # Then
    assert isinstance(resolved_class_first, SimpleClassB)
    assert isinstance(resolved_class_second, SimpleClassB)
    assert not isinstance(resolved_class_first, SimpleClassA)
    assert not isinstance(resolved_class_second, SimpleClassC)
    assert resolved_class_first is resolved_class_second


def test_should_dynamically_resolve_simple_class() -> None:
    # Given
    lidi = Lidi()

    lidi.bind(SimpleClassA, SimpleClassB)
    resolved_class = lidi.resolve(SimpleClassA)
    assert isinstance(resolved_class, SimpleClassB)

    # When
    lidi.bind(SimpleClassA, SimpleClassC)
    resolved_class = lidi.resolve(SimpleClassA)

    # Then
    assert isinstance(resolved_class, SimpleClassC)
    assert not isinstance(resolved_class, SimpleClassA)
    assert not isinstance(resolved_class, SimpleClassB)


def test_should_dynamically_resolve_simple_class_as_instance() -> None:
    # Given
    lidi = Lidi()

    initiated_class = SimpleClassB()
    lidi.bind(SimpleClassA, initiated_class)
    resolved_class = lidi.resolve(SimpleClassA)
    assert resolved_class is initiated_class
    assert isinstance(resolved_class, type(initiated_class))

    # When
    lidi.bind(SimpleClassA, SimpleClassC)
    resolved_class = lidi.resolve(SimpleClassA)

    # Then
    assert isinstance(resolved_class, SimpleClassC)
    assert not isinstance(resolved_class, SimpleClassA)
    assert not isinstance(resolved_class, SimpleClassB)


def test_should_dynamically_resolve_simple_class_as_singleton() -> None:
    # Given
    lidi = Lidi()
    lidi.bind(SimpleClassA, SimpleClassB, singleton=True)
    resolved_class_first = lidi.resolve(SimpleClassA)
    resolved_class_second = lidi.resolve(SimpleClassA)
    assert isinstance(resolved_class_first, SimpleClassB)
    assert isinstance(resolved_class_second, SimpleClassB)
    assert resolved_class_first is resolved_class_second

    # When
    lidi.bind(SimpleClassA, SimpleClassC, singleton=True)
    resolved_class_first = lidi.resolve(SimpleClassA)
    resolved_class_second = lidi.resolve(SimpleClassA)

    # Then
    assert isinstance(resolved_class_first, SimpleClassC)
    assert isinstance(resolved_class_second, SimpleClassC)
    assert not isinstance(resolved_class_first, SimpleClassA)
    assert not isinstance(resolved_class_second, SimpleClassB)
    assert resolved_class_first is resolved_class_second
