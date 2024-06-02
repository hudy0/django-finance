from datetime import datetime

import factory

from accounts.models import User
from tracker.models import Category, Transaction


class UserFactoryClass(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ["username"]

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Sequence(lambda n: "user%d" % n)


class CategoryFactoryClass(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ["name"]

    name = factory.Iterator(
        [
            "Bills",
            "Food",
            "Clothes",
            "Medical",
            "Housing",
            "Salary",
            "Social",
            "Transport",
            "Vacation",
        ]
    )


class TransactionFactoryClass(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    user = factory.SubFactory(UserFactoryClass)
    category = factory.SubFactory(CategoryFactoryClass)
    amount = 5
    type = factory.Iterator([x[0] for x in Transaction.TRANSACTION_TYPE_CHOICES])
    date = factory.Faker(
        "date_between",
        start_date=datetime(year=2022, month=1, day=1).date(),
        end_date=datetime.now().date(),
    )
