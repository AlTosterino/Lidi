from dataclasses import dataclass

import pytest
from lidi import Lidi
from lidi.exceptions import BindingMissing

from tests.shared import SimpleBaseClass, SimpleInheritClassA, SimpleInheritClassB


def test_should_resolve_binding_in_dataclass_field() -> None:
    # Given
    lidi = Lidi()
    lidi.bind(SimpleBaseClass, SimpleInheritClassA)

    @dataclass
    class SimpleDataClassA:
        base_class: SimpleBaseClass = lidi.resolve(SimpleBaseClass)

    # When
    class_instance = SimpleDataClassA()

    # Then
    assert isinstance(class_instance.base_class, SimpleBaseClass)
    assert type(class_instance.base_class) == SimpleInheritClassA


def test_should_not_dynamically_resolve_binding_in_dataclass_field() -> None:
    # Given
    lidi = Lidi()
    lidi.bind(SimpleBaseClass, SimpleInheritClassA)

    @dataclass
    class SimpleDataClass:
        base_class: SimpleBaseClass = lidi.resolve(SimpleBaseClass)

    # When
    class_instance_first = SimpleDataClass()
    lidi.bind(SimpleBaseClass, SimpleInheritClassB)
    class_instance_second = SimpleDataClass()

    # Then
    assert isinstance(class_instance_first.base_class, SimpleBaseClass)
    assert isinstance(class_instance_second.base_class, SimpleBaseClass)
    assert type(class_instance_first.base_class) == SimpleInheritClassA
    assert type(class_instance_second.base_class) == SimpleInheritClassA
    assert not isinstance(class_instance_first, SimpleInheritClassB)
    assert not isinstance(class_instance_second, SimpleInheritClassA)


def test_should_raise_when_no_binding_available_before_creating_dataclass() -> None:
    # Given
    lidi = Lidi()

    # Then
    with pytest.raises(BindingMissing) as err:
        # When
        @dataclass
        class SimpleDataClass:
            base_class: SimpleBaseClass = lidi.resolve(SimpleBaseClass)

    assert str(err.value) == "Binding missing for type: SimpleBaseClass"
