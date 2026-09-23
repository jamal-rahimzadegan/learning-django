import pytest
from utils.to_upper_case import to_upper_case


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("hello", "HELLO"),
        ("Python 123", "PYTHON 123"),
        ("", ""),
        (None, None),
    ],
)
def test_to_upper_case(input_str, expected):
    assert to_upper_case(input_str) == expected