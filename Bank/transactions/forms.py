# from django import forms
# from .models import Transactions



# class TransactionForm(forms.ModelForm):

#     class Meta:
#         model=Transactions
#         fields=['amount','transactionsType']

#     def __init__(self,*args,**kwargs):
#         self.userAccount=kwargs.pop('account')
#         super().__init__(*args,**kwargs)
#         self.fields['transactionsType'].disabled=True
#         self.fields['transactionsType'].widget=forms.HiddenInput

    
    
#     def save(self, commit=True):
#         self.instance.account = self.account
#         self.instance.balance_after_transaction = self.account.balance
#         return super().save()



# class DepositForm(TransactionForm):
#     def clean_amount(self):
#         minDepositamount=100
#         amount=self.cleaned_data.get('amount')
#         if amount<minDepositamount:
#             raise forms.ValidationError(
#                 f'You need to deposit at least {minDepositamount} $'
#             )
#         return amount
    

# class WithDrawForm(TransactionForm):
#     def clean_amount(self):
#         account=self.account
#         minWithdrawamount=500
#         maxWithdrawamount=10000
#         balance=account.balance
#         amount=self.cleaned_data.get('amount')
#         if amount<minWithdrawamount:
#             raise forms.ValidationError(
#                 f'You Can Withdraw At Least {minWithdrawamount}'
#             )
#         if amount>minWithdrawamount:
#             raise forms.ValidationError(
#                 f'You Can Withdraw At Most {maxWithdrawamount}'

#             )
        
#         if amount>balance:
#             raise forms.ValidationError(
#                 f'You Have {balance} TK In Your Account'
#                 'You Can Withdraw At Most {maxWithdrawamount}'
                
#             )
        
#         return amount
    



# class LoanRequestForm(TransactionForm):
#     def clea_amount(self):
#         amount=self.cleaned_data.get('amount')
#         return amount



from django import forms
from .models import Transaction
from account.models import UserBankAccount



class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type'
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account') # account value ke pop kore anlam
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True # ei field disable thakbe
        self.fields['transaction_type'].widget = forms.HiddenInput() # user er theke hide kora thakbe

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()


class DepositForm(TransactionForm):
    def clean_amount(self): # amount field ke filter korbo
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount') # user er fill up kora form theke amra amount field er value ke niye aslam, 50
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )

        return amount


class WithdrawForm(TransactionForm):

    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 20000
        balance = account.balance # 1000
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount} $'
            )

        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount} $'
            )

        if amount > balance: # amount = 5000, tar balance ache 200
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You can not withdraw more than your account balance'
            )

        return amount



class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')

        return amount
    


class SendMoneyForm(TransactionForm):
    class Meta:
        model=Transaction
        fields=[
            'amount',
            'transaction_type',
            'recever_id'
        ]

    def clean_recever_id (self):
         recever_id = self.cleaned_data.get('recever_id')
         if not UserBankAccount.objects.filter(accountNo=recever_id).exists():
            raise forms.ValidationError(" account  not found ")
         return recever_id
    
    
    def clean_amount(self):

        amount = self.cleaned_data.get('amount')
        if not self.account:
            raise forms.ValidationError("Account doesnot Exists")
        if self.account.balance < amount:
            raise forms.ValidationError("Not enough balance ")
        return amount
    

    
    
    