# exportdata/views.py

from django.http import JsonResponse
from notes.models import Notes  # Replace 'yourapp' with your actual app name

def export_data_to_json(request):
    data_to_export = Notes.objects.all()
    print("data_to_export: ", data_to_export)
    serialized_data = []

    for item in data_to_export:
        serialized_data.append({
            "title": item.title,
            "text": item.text,
        })
    print(serialized_data)

    return JsonResponse(serialized_data, safe=False)
