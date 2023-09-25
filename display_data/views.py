from django.shortcuts import render
import requests
#import Notes
from notes.models import Notes
from django.db.models import Q

from datetime import datetime, timedelta, timezone

def display_data(request):
    # Replace 'API_URL' with the actual API URL
    api_url = 'http://localhost:8001/api/notes/'
    
    # Fetch data from the API
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        current_time = datetime.now(timezone.utc)
        extracted_data = []

        for item in data:
            created_date_str = item.get('created', '')
            created_date = datetime.strptime(created_date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
            timestamp = created_date.timestamp()

            # Check if the row is older than 60 seconds
            if (current_time - created_date) < timedelta(seconds=60):
                extracted_item = {
                    'title': item.get('title', ''),
                    'created': created_date,
                    'timestamp': timestamp,
                    'number': item.get('number', 0),
                }
                extracted_data.append(extracted_item)

        filtered_data_asc = sorted(extracted_data, key=lambda x: x['number'], reverse=True)
        # Filter data to include items with 'number' greater than 900
        filtered_data = [item for item in filtered_data_asc if item.get('number', 0) > 900]

        if filtered_data:  # Check if filtered_data is not empty
            highest_item = max(filtered_data, key=lambda item: item.get('number', 0))
        else:
            highest_item = None  # Set highest_item to None if there are no items in filtered_data

        context = {'filtered_data': filtered_data, 'highest_item': highest_item}

        return render(request, 'display_data.html', context)
    else:
        error_message = 'Failed to fetch data from the API'
        return render(request, 'error.html', {'error_message': error_message})
    



    




def highest_data(request):
    # Replace 'API_URL' with the actual API URL
    api_url = 'http://localhost:8001/api/notes/'
    
    # Fetch data from the API
    response = requests.get(api_url)

    lorem_ipsum_content = """
        Loreum Ipsum placeholder content goes here.
        Loreum Ipsum placeholder content goes here.
        Loreum Ipsum placeholder content goes here.
        Loreum Ipsum placeholder content goes here.
        Loreum Ipsum placeholder content goes here.
        Loreum Ipsum placeholder content goes here.
        Loreum Ipsum placeholder content goes here.
        Loreum Ipsum placeholder content goes here.
        Loreum Ipsum placeholder content goes here.
        Loreum Ipsum placeholder content goes here.
        Loreum Ipsum placeholder content goes here.
        Loreum Ipsum placeholder content goes here.
    """
    
    if response.status_code == 200:
        data = response.json()
        current_time = datetime.now(timezone.utc)
        extracted_data = []

        for item in data:
            created_date_str = item.get('created', '')
            created_date = datetime.strptime(created_date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
            
            # Convert current_time to the same timezone as created_date
            current_time_in_timezone = current_time.astimezone(created_date.tzinfo)
            
            # Check if the row is older than 60 seconds
            if (current_time_in_timezone - created_date) < timedelta(seconds=60):
                extracted_item = {
                    'id': item.get('id', 0),  # Add 'id' to the extracted data
                    'title': item.get('title', ''),
                    'created': created_date,
                    'timestamp': created_date.timestamp(),
                    'number': item.get('number', 0),
                    'text': item.get('text', ''),
                }
                extracted_data.append(extracted_item)

        extracted_data = [{'title': item['title'], 'created': item['created'], 'number': item['number'], 'id': item['id'], 'text': item['text'] } for item in extracted_data]
        filtered_data = [item for item in extracted_data if item.get('number', 0) > 900]

        context = {'highest_item': filtered_data, 'lorem_ipsum_content': lorem_ipsum_content, 'extracted_data': extracted_data}
        
        return render(request, 'highest_data.html', context)
    else:
        error_message = 'Failed to fetch data from the API'
        return render(request, 'error.html', {'error_message': error_message})


def high_priority_notes(request):
    # Calculate the datetime 2 minutes ago
    two_minutes_ago = datetime.now() - timedelta(minutes=1)
    
    # Filter high-priority notes created or edited within the last 2 minutes
    high_priority_notes = Notes.objects.filter(
        Q(priority='High', created__gte=two_minutes_ago) |
        Q(priority='High', edited__gte=two_minutes_ago)
    )
    
    context = {'high_priority_notes': high_priority_notes}
    return render(request, 'high_priority_notes.html', context)