#Fixture
import pytest


@pytest.fixture(scope="module")
def prework():
    print("I setup browser")
    return  "fail"

@pytest.fixture(scope="function")
def secondWork():
    print("I secondWork instance")
    yield
    print(" tear down validation")

@pytest.mark.smoke
def test_initialCheck(prework, secondWork):
    print("This is first test")
    assert prework == "fail"

@pytest.mark.skip(reason="this is a skip test")
def test_SecondCheck(presetupwork, secondWork):
    print("This is Second test")

