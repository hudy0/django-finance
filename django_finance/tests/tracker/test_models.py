import pytest

from django_finance.tracker.models import Transaction


@pytest.mark.django_db
def test_queryset_get_income(transactions):
    query_set = Transaction.objects.get_income()
    assert query_set.count() > 0
    assert all([transactions.type == "income" for transactions in query_set])


@pytest.mark.django_db
def test_queryset_get_expense(transactions):
    query_set = Transaction.objects.get_expanse()
    assert query_set.count() > 0
    assert all([transactions.type == "expense" for transactions in query_set])


@pytest.mark.django_db
def test_queryset_get_total_income(transactions):
    total_income = Transaction.objects.get_total_income()
    assert total_income == sum(total.amount for total in transactions if total.type == "income")


@pytest.mark.django_db
def test_queryset_get_total_expenses(transactions):
    total_expenses = Transaction.objects.get_total_expenses()
    assert total_expenses == sum(expense.amount for expense in transactions if expense.type == "income")
