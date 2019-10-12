from django.urls import path

from CreditManagement.views import MoneyObtainmentView, TransactionAddView, TransactionFinalisationView, \
    TransactionListView

app_name = 'credits'

urlpatterns = [
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('transactions/add', TransactionAddView.as_view(), name='transaction_add'),
    path('finalise_transactions/', TransactionFinalisationView.as_view(), name='transactions_finalise'),
    path('dining_money/', MoneyObtainmentView.as_view(), name='dining_money')
]
