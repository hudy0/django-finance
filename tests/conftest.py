import random

import pytest

from tests.factories import TransactionFactoryClass, UserFactoryClass


@pytest.fixture(autouse=True)
def aaa_db(db):
    pass


@pytest.fixture()
def transactions():
    return TransactionFactoryClass.create_batch(10, amount=random.randint(0, 100))


@pytest.fixture()
def user_transactions():
    user = UserFactoryClass()
    return TransactionFactoryClass.create_batch(20, user=user)


@pytest.fixture()
def transactions_dictionary_parameter():
    user = UserFactoryClass()
    transaction = TransactionFactoryClass.create(user=user)
    return {
        "type": transaction.type,
        "category": transaction.category_id,
        "date": transaction.date,
        "amount": transaction.amount,
    }
