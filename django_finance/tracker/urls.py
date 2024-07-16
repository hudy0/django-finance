from django.urls import path

from django_finance.tracker.views import (
    IndexView,
    create_transaction,
    TransactionsListView,
    update_transaction,
    delete_transaction,
)

urlpatterns: list = [
    path("", view=IndexView.as_view(), name="index"),
    path("transactions/", view=TransactionsListView.as_view(), name="transactions_list"),
    path("transactions/create/", view=create_transaction, name="transactions_create"),
    path("transactions/<int:pk>/update/", view=update_transaction, name="transactions_update"),
    path("transactions/<int:pk>/delete/", view=delete_transaction, name="transactions_delete"),
]
