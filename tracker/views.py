from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .filters import TransactionFilter
from .models import Transaction


class IndexView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, "tracker/index.html")


class TransactionsListView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, *args, **kwargs):
        transaction_filter = TransactionFilter(
            request.GET,
            queryset=Transaction.objects.filter(user=request.user).select_related(
                "category"
            ),
        )
        context = {"filter": transaction_filter}
        if request.htmx:
            return render(
                request,
                template_name="tracker/transactions_container.html",
                context=context,
            )
        return render(
            request, template_name="tracker/transactions_list.html", context=context
        )
