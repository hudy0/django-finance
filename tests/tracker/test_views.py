import pytest
from django.urls import reverse


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
