from django.shortcuts import render,redirect
from django.views.generic import FormView
from django.contrib.auth import login,logout
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordChangeView

from django.urls import reverse_lazy
from django import forms
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from transactions.views import send_transaction_email

class UserRegistrationView(FormView):
    template_name='account/registration.html'
    form_class=UserRegistrationForm
    success_url='profile'

    def  form_valid(self, form):
        user=form.save()
        login(self.request,user)
        return super().form_valid(form)
    


class UserLoginView(LoginView):
    template_name='account/login.html'
    def get_success_url(self):
        return reverse_lazy('profile')
    


class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('homepage')        



class UserBankAccountUpdateView(View):
    template_name = 'account/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') 
        return render(request, self.template_name, {'form': form})
    
class PassChangeView(PasswordChangeView,LoginRequiredMixin):
    template_name = 'account/changepass.html'
    success_url = reverse_lazy('profile') 
    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        send_transaction_email(self.request.user, 0, "Password Change", "account/passchem.html")
        return super().form_valid(form)   