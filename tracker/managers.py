from django.db import models


class TransactionQuerySetAPI(models.QuerySet):
    def get_expanse(self):
        return self.filter(type="expense")

    def get_income(self):
        return self.filter(type="income")

    def get_total_expenses(self):
        var = self.get_expanse().aggregate(total=models.Sum("amount"))["total"] or 0
        return var

    def get_total_income(self):
        var = self.get_income().aggregate(total=models.Sum("amount"))["total"] or 0
        return var
