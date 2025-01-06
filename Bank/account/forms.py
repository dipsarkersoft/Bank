from django.contrib.auth.forms import UserCreationForm
from django import forms
from .constant import AccountType,GenderType
from django.contrib.auth.models import User
from .models import UserAddress,UserBankAccount




class UserRegistrationForm(UserCreationForm):
    accountType=forms.ChoiceField(choices=AccountType)
    birthDate=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender=forms.ChoiceField(choices=GenderType)
    street_address=forms.CharField(max_length=100)
    city=forms.CharField(max_length=100)
    postalCode=forms.IntegerField()
    country=forms.CharField(max_length=100)

    class Meta:
        model=User
        fields=['username','password1','password2','first_name','last_name','email','accountType','birthDate','gender','city','postalCode','country','street_address' ]



    def save(self, commit = True):
        user=super().save(commit=False)
        if commit:
            user.save()
            accountType=self.cleaned_data.get('accountType')
            birthDate=self.cleaned_data.get('birthDate')
            gender=self.cleaned_data.get('gender')
            street_address=self.cleaned_data.get('street_address')
            city=self.cleaned_data.get('city')
            postalCode=self.cleaned_data.get('postalCode')
            country=self.cleaned_data.get('country')


            UserAddress.objects.create(
                user=user,
                postalCode=postalCode,
                city=city,
                country=country,
                street_address=street_address

            )
            UserBankAccount.objects.create(
                user=user,
                accountType=accountType,
                gender=gender,
                birthDate=birthDate,
                accountNo=10000+user.id
            )
        return user
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })    


    
class UserUpdateForm(forms.ModelForm):
    accountType=forms.ChoiceField(choices=AccountType)
    birthDate=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender=forms.ChoiceField(choices=GenderType)
    street_address=forms.CharField(max_length=100)
    city=forms.CharField(max_length=100)
    postalCode=forms.IntegerField()
    country=forms.CharField(max_length=100)

    class Meta:
        model=User
        fields=['first_name','last_name','email' ]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            }) 
        if self.instance:
            try:
                userAccount=self.instance.account
                userAddress=self.instance.address
            except UserBankAccount.DoesNotExist:

                userAccount=None
                userAccount=None
            if userAccount:
                self.fields['accountType'].initial=userAccount.accountType
                self.fields['birthDate'].initial=userAccount.birthDate
                self.fields['gender'].initial=userAccount.gender
                self.fields['street_address'].initial=userAddress.street_address
                self.fields['city'].initial=userAddress.city
                self.fields['postalCode'].initial=userAddress.postalCode
                self.fields['country'].initial=userAddress.country


        def save(self, commit = True):
            user=super().save(commit=False)
            if commit:
                user.save()

                userAccount,created=UserBankAccount.objects.get_or_create(user=user)
                userAddress,created=UserAddress.objects.get_or_create(user=user)

                userAccount.accountType=self.cleaned_data.get('accountType')
                userAccount.birthDate=self.cleaned_data.get('birthDate')
                userAccount.gender=self.cleaned_data.get('gender')
                userAccount.save()



                userAddress.street_address=self.cleaned_data.get('street_address')
                userAddress.city=self.cleaned_data.get('city')
                userAddress.postalCode=self.cleaned_data.get('postalCode')
                userAddress.country=self.cleaned_data.get('country')
                userAddress.save()


               
            return user       







    