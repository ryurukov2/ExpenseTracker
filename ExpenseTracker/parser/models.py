from django.db import models

from ExpenseTracker.auth_app.models import Profile


class Transaction(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    description = models.CharField(max_length=255)
    currency = models.CharField(max_length=5)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    to_currency = models.CharField(max_length=5, null=True, blank=True)
    to_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    native_currency = models.CharField(max_length=5)
    native_amount = models.DecimalField(max_digits=10, decimal_places=2)
    native_amount_usd = models.DecimalField(max_digits=10, decimal_places=2)


class AppTransaction(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    description = models.CharField(max_length=255)
    currency = models.CharField(max_length=5)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    to_currency = models.CharField(max_length=5, null=True, blank=True)
    to_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    native_currency = models.CharField(max_length=5)
    native_amount = models.DecimalField(max_digits=10, decimal_places=2)
    native_amount_usd = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_kind = models.CharField(max_length=255)
    transaction_hash = models.CharField(max_length=255, null=True, blank=True)


# Category - description + choices=subcategories