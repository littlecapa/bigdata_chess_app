from django.shortcuts import render, redirect
from django.http import JsonResponse
import logging
import json
import subprocess

from .proxies.twic_proxy import TwicProxy
from .proxies.li_proxy import LiProxy

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
    return render(request, "chess/main_page.html")

def lisplit(request):
    """
    Renders the lisplit page with input fields and buttons.
    """
    li_proxy = LiProxy()
    default_values = {
        "year": "2024",
        "month": "11",
        "source_folder": li_proxy.download_folder_path,
        "target_folder": li_proxy.unzip_folder_path,
    }

    if request.method == "POST":
        data = json.loads(request.body) 
        year = data.get("year")
        month = data.get("month")
        source_folder = data.get("source_folder")
        target_folder = data.get("target_folder")

        print(year, month, source_folder, target_folder)
        if year and month and source_folder and target_folder:
            try:
                # Run the shell script in the background
                subprocess.Popen([li_proxy.script_name_unzst, year, month, source_folder, target_folder])
                li_proxy.unzip_started(year, month)
                # Show a success message
                return JsonResponse({"status": "success", "message": "Split started successfully!"})
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)})
        else:
            return JsonResponse({"status": "error", "message": "All fields are required!"})

    return render(request, "chess/lisplit.html", default_values)

def execute_split(request):
    """
    After executing the split, redirect to the main page.
    """
    return redirect("main_page")


def liprocess(request):
    """
    Renders the lisplit page with input fields and buttons.
    """
    li_proxy = LiProxy()
    default_values = {
        "year": "2024",
        "month": "11",
    }

    if request.method == "POST":
        data = json.loads(request.body) 
        year = data.get("year")
        month = data.get("month")

        if year and month:
            try:
                print("Start Extract")
                li_proxy.extract(year, month)
                # Show a success message
                return JsonResponse({"status": "success", "message": "Process successfully!"})
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)})
        else:
            return JsonResponse({"status": "error", "message": "All fields are required!"})

    return render(request, "chess/liprocess.html", default_values)

def liconcat(request):
    """
    Renders the lisplit page with input fields and buttons.
    """
    li_proxy = LiProxy()
    default_values = {
        "source_folder": li_proxy.eco_split_folder_path,
        "target_folder": li_proxy.eco_complete_folder_path,
        "source_folder_eval": li_proxy.evaluated_folder_path,
        "target_folder_eval": li_proxy.evaluated_complete_folder_path,
    }

    if request.method == "POST":
        data = json.loads(request.body) 
        source_folder = data.get("source_folder")
        target_folder = data.get("target_folder")
        source_folder_eval = data.get("source_folder_eval")
        target_folder_eval = data.get("target_folder_eval")

        print(source_folder, target_folder, source_folder_eval, target_folder_eval)
        if source_folder and target_folder and source_folder_eval and target_folder_eval:
            try:
                # Run the shell script in the background
                print(li_proxy.script_name_concat, source_folder, target_folder)
                subprocess.Popen([li_proxy.script_name_concat, source_folder, target_folder])
                print(li_proxy.script_name_concat, source_folder_eval, target_folder_eval)
                subprocess.Popen([li_proxy.script_name_concat, source_folder_eval, target_folder_eval])
                # Show a success message
                return JsonResponse({"status": "success", "message": "Concat started successfully!"})
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)})
        else:
            return JsonResponse({"status": "error", "message": "All fields are required!"})

    return render(request, "chess/liconcat.html", default_values)

def execute_concat(request):
    return redirect("main_page")