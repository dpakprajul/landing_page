# chartapp/views.py

from django.shortcuts import render
import requests  # To make HTTP requests

def chart_view(request):
    # Replace 'http://localhost:8000' with the URL of your Django REST API
    api_url = 'http://localhost:8001/api/notes/'  # Example API URL
    response = requests.get(api_url)
    data = response.json()
    context ={
        'data': data
    } 

    # Pass the data to the template
    return render(request, 'chartapp/chart.html', context)


