from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.decorators.http import require_http_methods
from django_htmx.http import retarget
from project import settings

from django_finance.tracker.forms import CreateTransactionForm

from .filters import TransactionFilter
from .models import Transaction


class IndexView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, "../templates/index.html")


@login_required()
def get_transactions(request):
    page = request.GET.get("page", 1)  # page=2
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related(
            "category",
        ),
    )
    paginator = Paginator(transaction_filter.qs, settings.PAGE_SIZE)
    context = {
        "transactions": paginator.page(page),
    }
    return render(
        request, "tracker/transactions_container.html#transaction_list", context
    )


@login_required()
def transactions_list(request):
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related(
            "category",
        ),
    )

    paginator = Paginator(transaction_filter.qs, settings.PAGE_SIZE)
    transactions_page = paginator.page(1)
    total_income = transaction_filter.qs.get_total_income()
    total_expenses = transaction_filter.qs.get_total_expenses()
    context = {
        "transactions": transactions_page,
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
