from dataclasses import dataclass, field

from lidi import Lidi

from tests.shared import SimpleBaseClass, SimpleInheritClassA, SimpleInheritClassB


def test_should_resolve_binding_in_dataclass_field_using_resolve_defer() -> None:
    # Given
    lidi = Lidi()

    @dataclass
    class SimpleDataClassA:
        base_class: SimpleBaseClass = field(default_factory=lidi.resolve_defer(SimpleBaseClass))

    # When
    lidi.bind(SimpleBaseClass, SimpleInheritClassA)
    class_instance = SimpleDataClassA()

    # Then
    assert isinstance(class_instance.base_class, SimpleBaseClass)
    assert type(class_instance.base_class) == SimpleInheritClassA


def test_should_resolve_binding_in_dataclass_field_using_lambda_resolve() -> None:
    # Given
    lidi = Lidi()

    @dataclass
    class SimpleDataClass:
        base_class: SimpleBaseClass = field(
            default_factory=lambda: lidi.resolve(SimpleBaseClass)  # type: ignore
        )

    # When
    lidi.bind(SimpleBaseClass, SimpleInheritClassA)
    class_instance = SimpleDataClass()

    # Then
    assert isinstance(class_instance.base_class, SimpleBaseClass)
    assert type(class_instance.base_class) == SimpleInheritClassA


def test_should_dynamically_resolve_binding_in_dataclass_field_using_resolve_defer() -> None:
    # Given
    lidi = Lidi()

    @dataclass
    class SimpleDataClass:
        base_class: SimpleBaseClass = field(default_factory=lidi.resolve_defer(SimpleBaseClass))

    # When
    lidi.bind(SimpleBaseClass, SimpleInheritClassA)
    class_instance_first = SimpleDataClass()
    lidi.bind(SimpleBaseClass, SimpleInheritClassB)
    class_instance_second = SimpleDataClass()

    # Then
    assert isinstance(class_instance_first.base_class, SimpleBaseClass)
    assert isinstance(class_instance_second.base_class, SimpleBaseClass)
    assert type(class_instance_first.base_class) == SimpleInheritClassA
    assert type(class_instance_second.base_class) == SimpleInheritClassB
    assert not isinstance(class_instance_first, SimpleInheritClassB)
    assert not isinstance(class_instance_second, SimpleInheritClassA)


def test_should_dynamically_resolve_binding_in_dataclass_field_using_lambda_resolve() -> None:
    # Given
    lidi = Lidi()

    @dataclass
    class SimpleDataClass:
        base_class: SimpleBaseClass = field(
            default_factory=lambda: lidi.resolve(SimpleBaseClass)  # type: ignore
        )

    # When
    lidi.bind(SimpleBaseClass, SimpleInheritClassA)
    class_instance_first = SimpleDataClass()
    lidi.bind(SimpleBaseClass, SimpleInheritClassB)
    class_instance_second = SimpleDataClass()

    # Then
    assert isinstance(class_instance_first.base_class, SimpleBaseClass)
    assert isinstance(class_instance_second.base_class, SimpleBaseClass)
    assert type(class_instance_first.base_class) == SimpleInheritClassA
    assert type(class_instance_second.base_class) == SimpleInheritClassB
    assert not isinstance(class_instance_first, SimpleInheritClassB)
    assert not isinstance(class_instance_second, SimpleInheritClassA)
