import random

import pytest

from tests.factories import TransactionFactoryClass


@pytest.fixture(autouse=True)
def aaa_db(db):
    pass


@pytest.fixture()
def transactions():
    return TransactionFactoryClass.create_batch(10, amount=random.randint(0, 100))
