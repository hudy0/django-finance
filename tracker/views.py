from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from tracker.forms import CreateTransactionForm

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
                "category",
            ),
        )
        total_income = transaction_filter.qs.get_total_income()
        total_expenses = transaction_filter.qs.get_total_expenses()
        context = {
            "filter": transaction_filter,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": total_income - total_expenses,  # net_income
        }
        if request.htmx:
            return render(
                request,
                template_name="tracker/transactions_container.html",
                context=context,
            )
        return render(
            request,
            template_name="tracker/transactions_list.html",
            context=context,
        )


class TransactionsCreateView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, *args, **kwargs):
        context = {"form": CreateTransactionForm()}
        return render(request, "tracker/transactions_create.html", context=context)

    @staticmethod
    def post(request, *args, **kwargs):
        form = CreateTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            context = {"message": "Transaction was added successfully!"}
            return render(
                request,
                template_name="tracker/transactions_create_success.html",
                context=context,
            )
        context = {"form": form}
        return render(request, "tracker/transactions_create.html", context=context)
