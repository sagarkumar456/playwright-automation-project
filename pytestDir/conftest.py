import pytest


@pytest.fixture(scope="session")
def presetupwork():
    print("I Conftsetup browser")