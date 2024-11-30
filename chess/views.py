from django.shortcuts import render, redirect
from django.http import JsonResponse
import logging
import json

from .proxies.twic_proxy import TwicProxy

logger = logging.getLogger(__name__)

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
    if request.method == "POST":
        try:
            twic_proxy = TwicProxy()
            twic_proxy.get_next_twic()
            return JsonResponse({
                "status": "success", 
                "message": "Download done!", 
                "updated_last_download_number": twic_proxy.last_issue
            }, status=200)
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            logger.error(f"Error during download: {str(e)}")
            return JsonResponse({"status": "error", "message": "Unable to Download TWIC"}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({"status": "error", "message": "Unexpected error during download"}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid TWIC download request method"}, status=405)

def main_page(request):
    print("Main")
    return render(request, "chess/main_page.html")
