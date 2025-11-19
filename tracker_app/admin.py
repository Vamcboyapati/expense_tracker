from django.contrib import admin
from tracker_app.models import *

admin.site.site_title="Expense Tracker"
admin.site.site_header="Expense Tracker"
admin.site.site_url="Expense Tracker"


@admin.action(description="Mark selected extense type as credit")
def make_credit(modeladmin, request, queryset):
    for q in queryset:
      if q.amount<0:
         q.amount=q.amount*-1
         q.save()
    queryset.update(expense_type="CREDIT")

@admin.action(description="Mark selected extense type as debit")
def mark_debit(modeladmin,request,queryset):
   for q in queryset:
      if q.amount>0:
         q.amount=q.amount*-1
         q.save()
   queryset.update(expense_type="DEBIT")
admin.site.register(CurrentBalance)
class TrackingHistoryAdmin(admin.ModelAdmin):
  list_display=[
    'amount',
    'current_balance',
  'expense_type',
  'description',
  'created_at',
  'display',
  ]

  def display(self,obj):
    if obj.amount>0:
      return "Positive"
    return "negative"
  actions=[make_credit,mark_debit]
  list_filter=['expense_type']
  search_fields=['expense_type','description']
  ordering=['created_at']
admin.site.register(TrackingHistory,TrackingHistoryAdmin)
