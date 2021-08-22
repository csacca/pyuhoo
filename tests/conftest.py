import os

import pytest


@pytest.fixture(scope="module")
def username():
    return os.getenv("UHOO_USERNAME")


@pytest.fixture(scope="module")
def password():
    return os.getenv("UHOO_PASSWORD")
