import pytest
from lidi import Lidi
from lidi.exceptions import BindingMissing


def test_should_resolve_simple_function() -> None:
    # Given
    lidi = Lidi()

    def function_a() -> None:
        ...

    def function_b() -> None:
        ...

    lidi.bind(function_a, function_b)

    # When
    resolved_function = lidi.resolve(function_a)

    # Then
    assert resolved_function is function_b
    assert resolved_function is not function_a


def test_should_dynamically_resolve_simple_function() -> None:
    # Given
    lidi = Lidi()

    def function_a() -> None:
        ...

    def function_b() -> None:
        ...

    def function_c() -> None:
        ...

    lidi.bind(function_a, function_b)
    resolved_function = lidi.resolve(function_a)
    assert resolved_function is function_b

    # When
    lidi.bind(function_a, function_c)
    resolved_function = lidi.resolve(function_a)

    # Then
    assert resolved_function is function_c
    assert resolved_function is not function_a
    assert resolved_function is not function_b


def test_should_resolve_simple_class() -> None:
    # Given
    lidi = Lidi()

    class A:
        ...

    class B:
        ...

    lidi.bind(A, B)

    # When
    resolved_class = lidi.resolve(A)

    # Then
    assert resolved_class is B
    assert resolved_class is not A


def test_should_dynamically_resolve_simple_class() -> None:
    # Given
    lidi = Lidi()

    class A:
        ...

    class B:
        ...

    class C:
        ...

    lidi.bind(A, B)
    resolved_class = lidi.resolve(A)
    assert resolved_class is B

    # When
    lidi.bind(A, C)
    resolved_class = lidi.resolve(A)

    # Then
    assert resolved_class is C
    assert resolved_class is not A
    assert resolved_class is not B


def test_should_raise_if_binding_no_binding_found() -> None:
    # Given
    lidi = Lidi()

    class A:
        ...

    # Then
    with pytest.raises(BindingMissing) as err:
        lidi.resolve(A)

    assert str(err.value) == "Binding missing for type: A"
