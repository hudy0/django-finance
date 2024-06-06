from django.urls import path

from tracker.views import (IndexView, TransactionsCreateView,
                           TransactionsListView)

urlpatterns: list = [
    path("", view=IndexView.as_view(), name="index"),
    path(
        "transactions/", view=TransactionsListView.as_view(), name="transactions_list"
    ),
    path(
        "transactions/create/",
        view=TransactionsCreateView.as_view(),
        name="transactions_create",
    ),
]
