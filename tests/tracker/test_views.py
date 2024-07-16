from datetime import datetime, timedelta

import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from tracker.models import Category, Transaction


@pytest.mark.django_db
def test_total_value_transactions(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    income_total = sum(t.amount for t in user_transactions if t.type == "income")
    expense_total = sum(t.amount for t in user_transactions if t.type == "expense")
    # net_income
    balance = income_total - expense_total
    response = client.get(reverse("transactions_list"))

    assert response.context["total_income"] == income_total
    assert response.context["total_expenses"] == expense_total
    assert response.context["balance"] == balance


@pytest.mark.django_db
def test_transactions_type_filter(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    # check income filter
    _get_params_ = {"transaction_type": "income"}
    response = client.get(reverse("transactions_list"), _get_params_)
    qs = response.context["filter"].qs
    for transaction in qs:
        assert transaction.type == "income"

    # check expense filter
    _get_params_ = {"transaction_type": "expense"}
    response = client.get(reverse("transactions_list"), _get_params_)
    qs = response.context["filter"].qs
    for transaction in qs:
        assert transaction.type == "expense"


@pytest.mark.django_db
def test_start_end_date_filter(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    # check start date filter
    _start_date_ = datetime.now().date() - timedelta(days=120)
    _get_params_ = {"start_date": _start_date_}
    response = client.get(reverse("transactions_list"), _get_params_)
    qs = response.context["filter"].qs
    for transaction in qs:
        assert transaction.date >= _start_date_

    # check end date filter
    _end_date_ = datetime.now().date() - timedelta(days=10)
    _get_params_ = {"end_date": _end_date_}
    response = client.get(reverse("transactions_list"), _get_params_)
    qs = response.context["filter"].qs
    for transaction in qs:
        assert transaction.date <= _end_date_


@pytest.mark.django_db
def test_category_filter(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    # check category filter
    _category_pk_ = Category.objects.all()[:2].values_list("pk", flat=True)
    _get_params_ = {"category": _category_pk_}
    response = client.get(reverse("transactions_list"), _get_params_)
    qs = response.context["filter"].qs
    for transaction in qs:
        assert transaction.category.pk in _category_pk_


@pytest.mark.django_db
def test_add_transactions_requested(user_transactions, transactions_dictionary_parameter, client):
    user = user_transactions[0].user
    client.force_login(user)
    user_transactions_count = Transaction.objects.filter(user=user).count()

    headers = {"HTTP_HX-Request": "true"}
    response = client.post(reverse("transactions_create"), transactions_dictionary_parameter, **headers)
    assert Transaction.objects.filter(user=user).count() == user_transactions_count + 1
    assertTemplateUsed(response, "tracker/transactions_create_success.html")


@pytest.mark.django_db
def test_cannot_add_transactions_with_negative_amount(user_transactions, transactions_dictionary_parameter, client):
    user = user_transactions[0].user
    client.force_login(user)
    user_transactions_count = Transaction.objects.filter(user=user).count()

    transactions_dictionary_parameter["amount"] = -30
    response = client.post(reverse("transactions_create"), transactions_dictionary_parameter)
    assert Transaction.objects.filter(user=user).count() == user_transactions_count
    assertTemplateUsed(response, "tracker/transactions_create.html")
    assert "HX-Retarget" in response.headers


@pytest.mark.django_db
def test_update_transactions_requested(user_transactions, transactions_dictionary_parameter, client, transactions):
    user = user_transactions[0].user
    assert Transaction.objects.filter(user=user).count() == 20
    transaction = Transaction.objects.first()

    transactions_dictionary_parameter["amount"] = 40
    client.post(reverse("transactions_update", kwargs={"pk": transaction.pk}), transactions_dictionary_parameter)

    # check the request has UPDATED, not created a new transaction
    assert Transaction.objects.filter(user=user).count() == 20
    transaction = Transaction.objects.first()
    assert transaction.amount == 5


@pytest.mark.django_db
def test_delete_transactions_requested(user_transactions, transactions_dictionary_parameter, client, transactions):
    user = user_transactions[0].user
    client.force_login(user)
    assert Transaction.objects.filter(user=user).count() == 20
    transaction = Transaction.objects.first()
    client.delete(reverse("transactions_delete", kwargs={"pk": transaction.pk}))
    assert Transaction.objects.filter(user=user).count() == 19
