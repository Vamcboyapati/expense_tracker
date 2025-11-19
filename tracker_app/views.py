from django.shortcuts import render,redirect
from .models import *
from django.db.models import Sum 
from django.contrib import messages
# Create your views here.

def index(request):
  if request.method=="POST":
    description=request.POST.get('description')
    amount=request.POST.get('amount')
    crnt_balance,_=CurrentBalance.objects.get_or_create(id=1)
    expense_type="CREDIT"
    if float(amount)<0:
      expense_type="DEBIT"
    if float(amount)==0:
      messages.warning(request,'Be careful!')
      return redirect('/')
    traking_hist=TrackingHistory.objects.create(
      amount=amount,
      expense_type=expense_type,
      description=description,
      current_balance=crnt_balance,
    )
    crnt_balance.current_balance+=float(traking_hist.amount)
    crnt_balance.save()   
    print(description,amount)
    return redirect('/')
  crnt_balance,_=CurrentBalance.objects.get_or_create(id=1)
  income=0
  expense=0
  for i in TrackingHistory.objects.all():
    if i.expense_type=="CREDIT":
      income+=i.amount
    else:
      expense+=i.amount

  context={'transactions': TrackingHistory.objects.all().order_by('-id'),'current_balance':crnt_balance,"Income":income,"Expense":expense}
  return render(request,'index.html',context)

def delete_transaction(request, id):
  tracking_history=TrackingHistory.objects.get(id=id)
  if tracking_history:
    crnt_balance,_=CurrentBalance.objects.get_or_create(id=1)
    crnt_balance.current_balance-=tracking_history.amount
    crnt_balance.save()
  tracking_history.delete()
  return redirect('/')