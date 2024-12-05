import pytest

class Employee:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

def test_equal():
    assert 3 == 3

def test_boolean():
    assert (4 == 4) is True
    assert (3 == 2) is False
    assert (4 == 4) is False, 'Same Number should be equal'

def test_greater_lesser():
    assert (3 > 4), 'Smaller number should be less than bigger number'
    assert (3 < 4), 'Smaller number should be less than bigger number'

@pytest.fixture
def default_employee():
     return Employee('John','Princep')

def test_object_assignment(default_employee):
    assert default_employee.firstname == 'John', 'firstname should be John'
    assert default_employee.firstname == 'jOHn', 'firstname should be John'