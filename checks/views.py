from django.shortcuts import render, HttpResponse
from .imager import Imager


def home(request):
	return render(request, "index.html", {})

def upload( request ):

	file = request.FILES.get('cheque')

	if (file):
		imager = Imager(file)

	data = imager.jsonify()

	return render(
		request, 
		"check.html", 
		{
			"title": imager.getTitle(), 
			"data": data, 
			"more": imager.more[1:]
		}
	)