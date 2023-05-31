from lidi import Lidi

from tests.shared import SimpleDataclassA, SimpleDataclassB, SimpleDataclassC


def test_should_resolve_simple_dataclass() -> None:
    # Given
    lidi = Lidi()
    lidi.bind(SimpleDataclassA, SimpleDataclassB)

    # When
    resolved_class = lidi.resolve(SimpleDataclassA)

    # Then
    assert isinstance(resolved_class, SimpleDataclassB)
    assert not isinstance(resolved_class, SimpleDataclassA)


def test_should_resolve_simple_dataclass_as_instance() -> None:
    # Given
    lidi = Lidi()
    initiated_class = SimpleDataclassB()
    lidi.bind(SimpleDataclassA, initiated_class)

    # When
    resolved_class = lidi.resolve(SimpleDataclassA)

    # Then
    assert isinstance(resolved_class, SimpleDataclassB)
    assert initiated_class is resolved_class
    assert not isinstance(resolved_class, SimpleDataclassA)


def test_should_resolve_simple_dataclass_as_singleton() -> None:
    # Given
    lidi = Lidi()
    lidi.bind(SimpleDataclassA, SimpleDataclassB, singleton=True)

    # When
    resolved_class_first = lidi.resolve(SimpleDataclassA)
    resolved_class_second = lidi.resolve(SimpleDataclassA)

    # Then
    assert isinstance(resolved_class_first, SimpleDataclassB)
    assert isinstance(resolved_class_second, SimpleDataclassB)
    assert not isinstance(resolved_class_first, SimpleDataclassA)
    assert not isinstance(resolved_class_second, SimpleDataclassC)
    assert resolved_class_first is resolved_class_second


def test_should_dynamically_resolve_simple_dataclass() -> None:
    # Given
    lidi = Lidi()

    lidi.bind(SimpleDataclassA, SimpleDataclassB)
    resolved_class = lidi.resolve(SimpleDataclassA)
    assert isinstance(resolved_class, SimpleDataclassB)

    # When
    lidi.bind(SimpleDataclassA, SimpleDataclassC)
    resolved_class = lidi.resolve(SimpleDataclassA)

    # Then
    assert isinstance(resolved_class, SimpleDataclassC)
    assert not isinstance(resolved_class, SimpleDataclassA)
    assert not isinstance(resolved_class, SimpleDataclassB)


def test_should_dynamically_resolve_simple_dataclass_as_instance() -> None:
    # Given
    lidi = Lidi()

    initiated_class = SimpleDataclassB()
    lidi.bind(SimpleDataclassA, initiated_class)
    resolved_class = lidi.resolve(SimpleDataclassA)
    assert resolved_class is initiated_class
    assert isinstance(resolved_class, type(initiated_class))

    # When
    lidi.bind(SimpleDataclassA, SimpleDataclassC)
    resolved_class = lidi.resolve(SimpleDataclassA)

    # Then
    assert isinstance(resolved_class, SimpleDataclassC)
    assert not isinstance(resolved_class, SimpleDataclassA)
    assert not isinstance(resolved_class, SimpleDataclassB)


def test_should_dynamically_resolve_simple_dataclass_as_singleton() -> None:
    # Given
    lidi = Lidi()
    lidi.bind(SimpleDataclassA, SimpleDataclassB, singleton=True)
    resolved_class_first = lidi.resolve(SimpleDataclassA)
    resolved_class_second = lidi.resolve(SimpleDataclassA)
    assert isinstance(resolved_class_first, SimpleDataclassB)
    assert isinstance(resolved_class_second, SimpleDataclassB)
    assert resolved_class_first is resolved_class_second

    # When
    lidi.bind(SimpleDataclassA, SimpleDataclassC, singleton=True)
    resolved_class_first = lidi.resolve(SimpleDataclassA)
    resolved_class_second = lidi.resolve(SimpleDataclassA)

    # Then
    assert isinstance(resolved_class_first, SimpleDataclassC)
    assert isinstance(resolved_class_second, SimpleDataclassC)
    assert not isinstance(resolved_class_first, SimpleDataclassA)
    assert not isinstance(resolved_class_second, SimpleDataclassB)
    assert resolved_class_first is resolved_class_second
