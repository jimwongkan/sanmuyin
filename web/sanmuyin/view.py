# -*- coding: utf-8 -*-
 
#from django.http import HttpResponse
from django.shortcuts import render
from . import ProductService
 
def queryProducts(request):
	context={}
	context['productList']=ProductService.queryProductList()
	return render(request, 'productList.html', context)

def addProduct(request):
	context={}
	context['temp']=[{'id':'344','name':'fdsfew'},{'id':'222','name':'fdsfew'},{'id':'333','name':'fdsfew'},{'id':'444','name':'fdsfew'},{'id':'555','name':'fdsfew'},{'id':'666','name':'fdsfew'}]
	return render(request, 'productList.html', context)

def deleteProduct(request):
	context={}
	context['temp']=[{'id':'344','name':'fdsfew'},{'id':'222','name':'fdsfew'},{'id':'333','name':'fdsfew'},{'id':'444','name':'fdsfew'},{'id':'555','name':'fdsfew'},{'id':'666','name':'fdsfew'}]
	return render(request, 'productList.html', context)