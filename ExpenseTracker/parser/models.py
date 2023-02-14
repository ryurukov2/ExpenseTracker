from django.db import models

from ExpenseTracker.auth_app.models import Profile


class Transaction(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    description = models.CharField(max_length=255)
    currency = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=20, decimal_places=13)
    to_currency = models.CharField(max_length=10, null=True, blank=True)
    to_amount = models.DecimalField(max_digits=20, decimal_places=13, null=True, blank=True)
    native_currency = models.CharField(max_length=10)
    native_amount = models.DecimalField(max_digits=20, decimal_places=13)
    native_amount_usd = models.DecimalField(max_digits=20, decimal_places=13)


class AppTransaction(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    description = models.CharField(max_length=255)
    currency = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=20, decimal_places=13)
    to_currency = models.CharField(max_length=10, null=True, blank=True)
    to_amount = models.DecimalField(max_digits=20, decimal_places=13, null=True, blank=True)
    native_currency = models.CharField(max_length=10)
    native_amount = models.DecimalField(max_digits=20, decimal_places=13)
    native_amount_usd = models.DecimalField(max_digits=20, decimal_places=13)
    transaction_kind = models.CharField(max_length=255)
    transaction_hash = models.CharField(max_length=255, null=True, blank=True)


# Category - description + choices=subcategories