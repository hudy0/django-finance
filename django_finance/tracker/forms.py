from django import forms

from django_finance.tracker.models import Category, Transaction


class CreateTransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.RadioSelect(),
    )
    # type = forms.ChoiceField(choices=Transaction.TRANSACTION_TYPE_CHOICES)

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Amount cannot be negative")
        return amount

    class Meta:
        model = Transaction
        fields = ["category", "type", "amount", "date"]
        widgets = {
            "date": forms.DateInput(
                attrs={"type": "date"},
            ),
        }
