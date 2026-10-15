from django import forms
from .models import Expense,Income,Limit

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'type', 'date']


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount','date']

class LimitForm(forms.ModelForm):
    class Meta:
        model = Limit
        fields = ['amount']
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']