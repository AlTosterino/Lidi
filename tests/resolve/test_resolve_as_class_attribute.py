from lidipy import Lidi

from tests.shared import SimpleClassA, SimpleClassB

_lidi = Lidi()


class ClassWithAttr:
    to_resolve: SimpleClassA = _lidi.resolve_attr(SimpleClassA)

    def get_resolved(self) -> SimpleClassA:
        return self.to_resolve


def test_should_resolve_attr_on_simple_class() -> None:
    # Given
    _lidi.bind(SimpleClassA, SimpleClassB)

    # When
    resolved = ClassWithAttr().get_resolved()

    # Then
    assert isinstance(resolved, SimpleClassB)
    assert not isinstance(resolved, SimpleClassA)
