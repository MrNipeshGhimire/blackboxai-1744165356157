from django import forms
from .models import Transaction, UserProfile

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'date', 'transaction_type', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'transaction_type': 'Type',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].required = False

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['initial_balance', 'weekly_limit', 'monthly_limit']
        widgets = {
            'initial_balance': forms.NumberInput(attrs={'step': '0.01'}),
            'weekly_limit': forms.NumberInput(attrs={'step': '0.01'}),
            'monthly_limit': forms.NumberInput(attrs={'step': '0.01'}),
        }
