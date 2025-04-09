from django.contrib import admin
from .models import UserProfile, Transaction

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'initial_balance', 'weekly_limit', 'monthly_limit')
    search_fields = ('user__username',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'amount', 'date', 'transaction_type')
    list_filter = ('transaction_type', 'date')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'
