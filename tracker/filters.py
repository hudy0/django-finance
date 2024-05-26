from django_filters import ChoiceFilter, FilterSet

from tracker.models import Transaction


class TransactionFilter(FilterSet):
    transaction_type = ChoiceFilter(
        choices=Transaction.TRANSACTION_TYPE_CHOICES,
        field_name="type",
        lookup_expr="iexact",
        empty_label="Any",
    )

    class Meta:
        model = Transaction
        fields = ["transaction_type"]
