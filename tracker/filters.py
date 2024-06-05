from django import forms
from django_filters import ChoiceFilter, FilterSet, DateFilter

from tracker.models import Transaction


class TransactionFilter(FilterSet):
    transaction_type = ChoiceFilter(
        choices=Transaction.TRANSACTION_TYPE_CHOICES,
        field_name="type",
        lookup_expr="iexact",
        empty_label="Any",
    )
    start_date = DateFilter(
        field_name="date",
        lookup_expr="gte",
        label="Start Date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    end_date = DateFilter(
        field_name="date",
        lookup_expr="lte",
        label="End Date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = Transaction
        fields = ["transaction_type", "start_date", "end_date"]
