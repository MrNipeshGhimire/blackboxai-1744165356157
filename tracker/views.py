from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Budget, Transaction, UserProfile
from .forms import BudgetForm, TransactionForm, UserProfileForm
from django.utils import timezone

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user, is_active=True)
    return render(request, 'tracker/budget_list.html', {'budgets': budgets})

@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget created successfully!')
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'tracker/budget_form.html', {'form': form})

@login_required
def budget_update(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated successfully!')
            return redirect('budget_list')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'tracker/budget_form.html', {'form': form})

@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.is_active = False
        budget.save()
        messages.success(request, 'Budget deactivated successfully!')
        return redirect('budget_list')
    return render(request, 'tracker/budget_confirm_delete.html', {'budget': budget})

@login_required
def dashboard(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:5]
    
    # Calculate totals
    income = sum(t.amount for t in Transaction.objects.filter(
        user=request.user, 
        transaction_type='IN'
    ))
    expenses = sum(t.amount for t in Transaction.objects.filter(
        user=request.user, 
        transaction_type='EX'
    ))
    balance = profile.initial_balance + income - expenses
    
    context = {
        'profile': profile,
        'transactions': transactions,
        'income': income,
        'expenses': expenses,
        'balance': balance,
    }
    return render(request, 'tracker/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})

@login_required
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'tracker/profile.html', {'form': form})

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'tracker/transaction_list.html', {'transactions': transactions})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'tracker/transaction_form.html', {'form': form})

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('transaction_list')
    return render(request, 'tracker/transaction_confirm_delete.html', {'transaction': transaction})
