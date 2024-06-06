import pytest
from app.calculations import add

@pytest.mark.parametrize("num1, num2, expected",[
    (2,3,5),
    (10,10,20),
    (9,1,10),
    (3,1,4)
])
def test_add(num1,num2,expected):
    assert add(num1,num2) == expected