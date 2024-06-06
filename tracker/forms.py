from django import forms
from tracker.models import Transaction, Category


class CreateTransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.RadioSelect())
    # type = forms.ChoiceField(choices=Transaction.TRANSACTION_TYPE_CHOICES)

    class Meta:
        model = Transaction
        fields = ["category", "type", "amount", "date"]
        widgets = {
            "date": forms.DateInput(
                attrs={"type": "date"},
            ),
        }
