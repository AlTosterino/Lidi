import pytest
from lidipy import Lidi
from lidipy.exceptions import BindingMissing

from tests.shared import SimpleClassA


def test_should_raise_if_binding_no_binding_found() -> None:
    # Given
    lidi = Lidi()

    # Then
    with pytest.raises(BindingMissing) as err:
        lidi.resolve(SimpleClassA)

    assert str(err.value) == "Binding missing for type: SimpleClassA"
