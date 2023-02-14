import codecs
import datetime
import pytz as pytz
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect
from .forms import CsvImportForm
import csv
from .models import Transaction, AppTransaction
from ..auth_app.models import Profile


def import_card_csv(request):
    if request.method == 'POST':
        form = CsvImportForm(request.POST, request.FILES)
        if form.is_valid():
            # get the uploaded file
            csv_file = request.FILES['csv_file']

            # open the file in Unicode-compatible mode
            csv_reader = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))

            # skip the header row
            next(csv_reader)
            txnowner = Profile.objects.get(user_id=request.user.id)
            # print(txn_str)
            existing_txns = set([
                ', '.join(str(getattr(field, name).strftime('%Y-%m-%d %H:%M:%S')) if name == 'timestamp' else str(getattr(field, name)) if getattr(field, name) is not None else ''
                          for name in ('timestamp', 'description', 'currency', 'amount', 'to_currency', 'to_amount', 'native_currency', 'native_amount')
                          ) for field in Transaction.objects.filter(owner=txnowner)
            ])

            # parse and save the data from the CSV file
            for row in csv_reader:
                row[3]="%.13f"%float(row[3])
                row[5]="%.13f"%float(row[5]) if row[5] else row[5]
                row[7]="%.13f"%float(row[7])
                row[8]="%.13f"%float(row[8])
                txn_data = ', '.join(row[:8])
                if txn_data in existing_txns:
                    continue
                else:
                    # parse the data from the row
                    date = row[0]
                    date_in_datetime = datetime.datetime.strptime(
                        date, '%Y-%m-%d %H:%M:%S')
                    aware_datetime = pytz.timezone('UTC')
                    timestamp = aware_datetime.localize(date_in_datetime)
                    description = row[1]
                    currency = row[2]
                    amount = float(row[3])
                    to_currency = row[4] if row[4] else None
                    to_amount = float(row[5]) if row[5] else None
                    native_currency = row[6]
                    native_amount = float(row[7])
                    native_amount_usd = float(row[8])

                    # create a new Transaction object and save it to the database
                    Transaction.objects.create(
                        owner=txnowner,
                        timestamp=timestamp,
                        description=description,
                        currency=currency,
                        amount=amount,
                        to_currency=to_currency,
                        to_amount=to_amount,
                        native_currency=native_currency,
                        native_amount=native_amount,
                        native_amount_usd=native_amount_usd
                    )
            return redirect('transactions')
    else:
        form = CsvImportForm()
    return render(request, 'parser/import_csv.html', {'form': form})


def import_app_csv(request):
    if request.method == 'POST':
        form = CsvImportForm(request.POST, request.FILES)
        if form.is_valid():
            # get the uploaded file
            txnowner = Profile.objects.get(user_id=request.user.id)
            existing_txns = set([
                ', '.join(str(getattr(field, name).strftime('%Y-%m-%d %H:%M:%S')) if name == 'timestamp' else str(getattr(field, name)) if getattr(field, name) is not None else ''
                          for name in ('timestamp', 'description', 'currency', 'amount', 'to_currency', 'to_amount', 'native_currency', 'native_amount', 'transaction_kind', 'transaction_hash')
                          ) for field in AppTransaction.objects.filter(owner=txnowner)
            ])

            csv_file = request.FILES['csv_file']

            # open the file in Unicode-compatible mode
            csv_reader = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))

            # skip the header row
            next(csv_reader)
            
            for row in csv_reader:
                row[3]="%.13f"%float(row[3])
                row[5]="%.13f"%float(row[5]) if row[5] else row[5]
                row[7]="%.13f"%float(row[7])
                row[8]="%.13f"%float(row[8])
                print(row[2])
                txn_data = ', '.join(row[:8]+row[9:])
                
                # print(txn_data)
                
                if txn_data in existing_txns:
                    continue
                else:
                    # parse the data from the row
                    date = row[0]
                    date_in_datetime = datetime.datetime.strptime(
                        date, '%Y-%m-%d %H:%M:%S')
                    aware_datetime = pytz.timezone('UTC')
                    timestamp = aware_datetime.localize(date_in_datetime)
                    description = row[1]
                    currency = row[2]
                    amount = float(row[3])
                    to_currency = row[4] if row[4] else None
                    to_amount = float(row[5]) if row[5] else None
                    native_currency = row[6]
                    native_amount = float(row[7])
                    native_amount_usd = float(row[8])
                    transaction_kind = row[9]
                    transaction_hash = row[10] if row[10] else None

                    # create a new AppTransaction object and save it to the database
                    AppTransaction.objects.create(
                        owner=txnowner,
                        timestamp=timestamp,
                        description=description,
                        currency=currency,
                        amount=amount,
                        to_currency=to_currency,
                        to_amount=to_amount,
                        native_currency=native_currency,
                        native_amount=native_amount,
                        native_amount_usd=native_amount_usd,
                        transaction_kind=transaction_kind,
                        transaction_hash=transaction_hash,
                    )
            return redirect('transactions')
    else:
        form = CsvImportForm()
    return render(request, 'parser/import_csv.html', {'form': form})


def show_transactions(request):
    transactions = Transaction.objects.all().filter(owner_id=request.user.id)
    return render(request, 'parser/transactions.html', {'transactions': transactions})


def analytics(request):
    # group the transactions by month and sum the native_amount field
    total_spent_by_month = Transaction.objects.filter(owner_id=request.user.id).filter(native_amount__lt=0).annotate(
        month=TruncMonth('timestamp')).values('month').annotate(total_spent=Sum('native_amount')).order_by('month')
    top_merchants = Transaction.objects.filter(owner_id=request.user.id).values('description').annotate(
        total_spent=Sum('native_amount')).order_by(
        'total_spent')[:20]
    total_spendings = Transaction.objects.all().filter(owner_id=request.user.id)
    total_sp, total_topup = 0, 0
    for obj in total_spendings:
        if obj.native_amount <= 0:
            total_sp = total_sp - obj.native_amount
        else:
            total_topup = total_topup + obj.native_amount
    total_cashback_received = AppTransaction.objects.filter(owner_id=request.user.id,
                                                            description='Card Cashback').aggregate(Sum('native_amount'),
                                                                                                   Sum('amount'))
    total_cashback_usd = total_cashback_received['native_amount__sum']
    total_cashback_cro = total_cashback_received['amount__sum']
    total_rebates_received = AppTransaction.objects.filter(owner_id=request.user.id,
                                                           description__startswith='Card Rebate:').aggregate(
        Sum('native_amount'), Sum('amount'))
    total_rebates_usd = total_rebates_received['native_amount__sum']
    total_rebates_cro = total_rebates_received['amount__sum']
    total_stake_rewards = AppTransaction.objects.filter(owner_id=request.user.id,
                                                        description='CRO Stake Rewards').aggregate(Sum('native_amount'),
                                                                                                   Sum('amount'))
    total_stake_usd = total_stake_rewards['native_amount__sum']
    total_stake_cro = total_stake_rewards['amount__sum']
    total_overall_usd, total_overall_cro = 0, 0
    if total_cashback_usd is not None and total_rebates_usd is not None and total_stake_usd is not None:
        total_overall_usd = total_cashback_usd + total_rebates_usd + total_stake_usd
    # render the template with the total_spent_by_month data
    if total_cashback_cro is not None and total_rebates_cro is not None and total_stake_cro is not None:
        total_overall_cro = total_cashback_cro + total_rebates_cro + total_stake_cro

    context = {'total_spent_by_month': total_spent_by_month,
               'top_merchants': top_merchants,
               'total_spent': total_sp,
               'total_topup': total_topup,
               'total_cashback_usd': total_cashback_usd,
               'total_cashback_cro': total_cashback_cro,
               'total_rebates_usd': total_rebates_usd,
               'total_rebates_cro': total_rebates_cro,
               'total_stake_usd': total_stake_usd,
               'total_stake_cro': total_stake_cro,
               'total_overall_cro': total_overall_cro,
               'total_overall_usd': total_overall_usd, }
    return render(request, 'parser/analytics.html', context)
