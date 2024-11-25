# views.py
from django.shortcuts import render
from django.http import JsonResponse

# Mock values for demonstration
last_download_number = 10
available_number = 20

def display_twic_status(request):
    """
    Render the page with the numbers and buttons.
    """
    return render(request, "chess/twic_download.html", {
        "last_download_number": last_download_number,
        "available_number": available_number,
        "can_download_new": available_number > last_download_number,
    })

def download_twic(request):
    """
    Logic to handle the 'Download' button.
    """
    # Replace this with your actual download logic
    return JsonResponse({"status": "success", "message": "Download started!"})

def cancel_action(request):
    """
    Logic to handle the 'Cancel' button.
    """
    return JsonResponse({"status": "cancelled", "message": "Action cancelled!"})
