from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.decorators.http import require_http_methods
from django_htmx.http import retarget

from django_finance.tracker.forms import CreateTransactionForm

from .filters import TransactionFilter
from .models import Transaction


class IndexView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, "../templates/index.html")


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


@login_required()
def create_transaction(request):
    if request.method == "POST":
        form = CreateTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            context = {"message": "Transaction was added successfully!"}
            return render(request, "tracker/transactions_create_success.html", context)
        else:
            context = {"form": form}
            response = render(request, "tracker/transactions_create.html", context)
            return retarget(response, "#transaction-block")

    context = {"form": CreateTransactionForm()}
    return render(request, "tracker/transactions_create.html", context)


@login_required()
def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        form = CreateTransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction.save()
            context = {"message": "Transaction was added successfully!"}
            return render(request, "tracker/transactions_create_success.html", context)
        else:
            context = {"form": form, "transaction": transaction}
            response = render(request, "tracker/transactions_update.html", context)
            return retarget(response, "#transaction-block")
    context = {
        "form": CreateTransactionForm(instance=transaction),
        "transaction": transaction,
    }
    return render(request, "tracker/transactions_update.html", context)


@login_required()
@require_http_methods(["DELETE"])
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()
    context = {"message": "Transaction was deleted successfully!"}
    return render(request, "tracker/transactions_create_success.html", context)