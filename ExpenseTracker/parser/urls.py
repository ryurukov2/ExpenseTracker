from django.urls import path

from ExpenseTracker.parser.views import import_card_csv, show_transactions, analytics, import_app_csv

urlpatterns = (
    path('', show_transactions, name='index'),
    path('upload_card/', import_card_csv, name='upload card csv'),
    path('upload_app/', import_app_csv, name='upload app csv'),
    path('transactions/', show_transactions, name='transactions'),
    path('analytics/', analytics, name='analytics'),
)