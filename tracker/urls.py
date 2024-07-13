from django.urls import path

from tracker.views import IndexView, create_transaction, TransactionsListView

urlpatterns: list = [
    path("", view=IndexView.as_view(), name="index"),
    path("transactions/", view=TransactionsListView.as_view(), name="transactions_list"),
    path("transactions/create/", view=create_transaction, name="transactions_create"),
]
