from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    # will show items list
    return HttpResponse('List of items')

def vendor(requets):
    # will show vendors list
    return HttpResponse('List of vendors')

def purchaseorder(request):
    # will show purchase orders
    return HttpResponse('List of purchase orders')

def salesinvoice(request):
    # will show sales invoices
    return HttpResponse('List of sales invoices')
