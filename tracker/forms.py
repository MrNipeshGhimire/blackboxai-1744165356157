from django import forms
from .models import Transaction, Budget, UserProfile
from django.core.validators import MinValueValidator
from django.utils import timezone

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'date', 'transaction_type', 'category', 'description', 'receipt']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'transaction_type': 'Type',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].validators.append(MinValueValidator(0.01))
        self.fields['date'].initial = timezone.now().date()

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'amount', 'period', 'start_date', 'end_date', 'category', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].validators.append(MinValueValidator(0.01))
        self.fields['start_date'].initial = timezone.now().date()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['initial_balance', 'weekly_limit', 'monthly_limit', 'dark_mode', 'currency']
        widgets = {
            'initial_balance': forms.NumberInput(attrs={'step': '0.01'}),
            'weekly_limit': forms.NumberInput(attrs={'step': '0.01'}),
            'monthly_limit': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['weekly_limit'].required = False
        self.fields['monthly_limit'].required = False
