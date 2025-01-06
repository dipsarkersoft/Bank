from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from .constant import DEPOSIT,SEND_MONEY, WITHDRAWAL,LOAN, LOAN_PAID
from datetime import datetime
from django.db.models import Sum
from transactions.forms import (
    DepositForm,
    WithdrawForm,
    LoanRequestForm,
    SendMoneyForm
)
from transactions.models import Transaction
from account.models import UserBankAccount
from core.models import BankRuft



def send_transaction_email(user,amount,subject,template):
    message=render_to_string(template,{
        'user':user,
        'amount':amount,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()



def send_transaction_email_sender(sender,recever,amount,subject,template):
    message=render_to_string(template,{
        'sender':sender,
        'recever':recever,
        'amount':amount,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[sender.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


def send_transaction_email_recever(sender,recever,amount,subject,template):
    message=render_to_string(template,{
        'sender':sender,
        'recever':recever,
        'amount':amount,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[recever.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

def Cheak_Bank_ruft():
    isBankRuft=BankRuft.objects.first()
    return isBankRuft.bankruft
        




class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transactions_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account

        
       
        account.balance += amount 
        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        send_transaction_email(self.request.user, amount, "Deposite Message", "transactions/deposite_email.html")

        return super().form_valid(form)


class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw Money'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial

    def form_valid(self, form):

        amount = form.cleaned_data.get('amount')
        
        usr=self.request.user.account
        if Cheak_Bank_ruft():
            messages.error(self.request, "The bank is bankrupt, no withdrawals are allowed.")
            return redirect('withdraw_money')
        
        usr.balance -= amount
        usr.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'Successfully withdrawn {"{:,.2f}".format(float(amount))}$ from your account'
        )
        send_transaction_email(self.request.user, amount, "WithDraw Message", "transactions/withdraw_email.html")

        return super().form_valid(form)

class LoanRequestView(TransactionCreateMixin):
    form_class = LoanRequestForm
    title = 'Request For Loan'

    def get_initial(self):
        initial = {'transaction_type': LOAN}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        if Cheak_Bank_ruft():
            messages.error(self.request, "The bank is bankrupt, no Loan are allowed.")
            return redirect('loan_request')
        current_loan_count = Transaction.objects.filter(
            account=self.request.user.account,transaction_type=3,loan_approve=True).count()
        if current_loan_count >= 3:
            return HttpResponse("You have cross the loan limits")
        messages.success(
            self.request,
            f'Loan request for {"{:,.2f}".format(float(amount))}$ submitted successfully'
        )
        send_transaction_email(self.request.user, amount, "Loan Request Message", "transactions/loan.html")

        return super().form_valid(form)
    
class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transactions_report.html'
    model = Transaction
    balance = 0 
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance = Transaction.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
       
        return queryset.distinct() 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })

        return context
    
        
class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(Transaction, id=loan_id)
        print(loan)
        if loan.loan_approve:
            user_account = loan.account
               
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transaction = user_account.balance
                user_account.save()
                loan.loan_approved = True
                loan.transaction_type = LOAN_PAID
                loan.save()
                return redirect('loan_list')
            else:
                messages.error(
            self.request,
            f'Loan amount is greater than available balance'
        )

        return redirect('loan_list')


class LoanListView(LoginRequiredMixin,ListView):
    model = Transaction
    template_name = 'transactions/loan_request.html'
    context_object_name = 'loans' 
    
    def get_queryset(self):
        user_account = self.request.user.account
        queryset = Transaction.objects.filter(account=user_account,transaction_type=3)
        print(queryset)
        return queryset



class SendMoneyView(TransactionCreateMixin,LoginRequiredMixin):
    title='Send Money'
    form_class=SendMoneyForm

    def get_initial(self):
        initial = {
            'transaction_type':SEND_MONEY,
        }
        return initial
    
    def form_valid(self, form):
        recever_acc=form.cleaned_data.get('recever_id')
        amount=form.cleaned_data.get('amount')
        sender_acc=self.request.user.account

        if Cheak_Bank_ruft():
            messages.error(self.request, "The bank is bankrupt, no Money Transfer are allowed.")
            return redirect('send_money')

        rcver_isEx=UserBankAccount.objects.get(accountNo=recever_acc)
        sender_acc.balance-=amount
        rcver_isEx.balance+=amount
        sender=self.request.user
        reciver=rcver_isEx.user

        
        


        sender_acc.save(update_fields=['balance'])
        rcver_isEx.save(update_fields=['balance'])

        

        messages.success(
            self.request,
            f'Successfully Transfer {"{:,.2f}".format(float(amount))}$ from {sender_acc.accountNo} to {rcver_isEx.accountNo}'

            )
        
        

        send_transaction_email_sender(sender,reciver,amount, "Send Money", "transactions/sender.html")
        send_transaction_email_recever(sender, reciver, amount, "Receved Money", "transactions/recever.html")


        return super().form_valid(form)
    



