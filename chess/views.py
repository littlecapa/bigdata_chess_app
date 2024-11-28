from django.shortcuts import render
from django.http import JsonResponse

from .proxies.twic_proxy import TwicProxy

def display_twic_status(request):
    """
    Render the page with the numbers and buttons.
    """
    twic_proxy = TwicProxy()
    return render(request, "chess/twic_download.html", {
        "last_download_number": twic_proxy.last_issue,
        "available_number": twic_proxy.highest_issue,
        "can_download_new": twic_proxy.highest_issue > twic_proxy.last_issue,
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
