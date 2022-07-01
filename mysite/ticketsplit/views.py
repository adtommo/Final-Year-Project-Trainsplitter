from django.shortcuts import render
from django.http import HttpResponse, request
from .py.split.work import run
from .py.map.map import create_map
from .py.split.data_compile import data

# Create your views here.

def index(response):
	context = {}
	if response.method == 'POST':
		fro = response.POST.get('fro')
		to = response.POST.get('to')
		fro.upper()
		to.upper()
		try:
			output = run(fro,to)
			create_map(output[1])
			context = {'original_price':output[0],'route':output[1],'split_cost':output[2], 
						'each_point':output[3], 'origin':output[4], 'dest': output[5]}
		except:
			message = """
			Error: Either ',fro,' or ',to,' is invalid.
			Or the data is missing/out of date.
			"""
			context = {'message':message}
		#print(context)

	return render(response, "ticketsplit/index.html", context)

def whataresplit(response):
	return render(response, "ticketsplit/whataresplit.html", {})

def howtousesplit(response):
	return render(response, "ticketsplit/howtousesplit.html", {})

