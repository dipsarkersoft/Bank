from django.urls import path,include
from .views import LoanListView,PayLoanView,SendMoneyView,TransactionReportView,DepositMoneyView,LoanRequestView,WithdrawMoneyView



urlpatterns = [
    path('deposit/',DepositMoneyView.as_view(),name="deposit_money"),
    path('withdraw/',WithdrawMoneyView.as_view(), name="withdraw_money"),
    path('report/',TransactionReportView.as_view(),name="transaction_report"),
    path('loan_request/',LoanRequestView.as_view(),name="loan_request"),
    path('send_money/',SendMoneyView.as_view(),name="send_money"),
    path('loans/',LoanListView.as_view(),name="loan_list"),
    path('loans/<int:loan_id>',PayLoanView.as_view(),name="pay"),
    
   
   
]