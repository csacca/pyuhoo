import os

import pytest


@pytest.fixture(scope="module")
def username():
    return os.getenv("USERNAME")


@pytest.fixture(scope="module")
def password():
    return os.getenv("PASSWORD")
