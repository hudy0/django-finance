from datetime import datetime, timedelta
import pytest
from django.urls import reverse

from tracker.models import Category


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
