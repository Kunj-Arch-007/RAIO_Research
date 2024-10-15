import os
import mimetypes
import logging
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import pandas as pd

# Import your script logic modules here
from .chargesCountScripts.chargeCounts import ORG_chargesCounts, MorningStoneChargesCounts, EveningStoneChargesCounts

logger = logging.getLogger(__name__)




# Rendering the StoneCharges Counts Page 
def homePage(request):
    return render(request, "ChargeCounts.html")


# Rendering Morning File Template 
def StoneMorningCounts(request):
    # Retrieve counts from session
    morningCounts = request.session.get('morningCounts', {})
    
    # Log the retrieved counts
    logger.debug(f"Retrieved Morning Counts: {morningCounts}")
    
    # Clear the counts from the session after retrieving them
    request.session['morningCounts'] = {}
    
    return render(request, "StoneCharges_MorningCounts.html", {'morningCounts': morningCounts})


# Rendering Evening File Template 
def StoneEveningCounts(request):
    # Retrieve counts from session
    eveningCounts = request.session.get('eveningCounts', {})
    
    # Log the retrieved counts
    logger.debug(f"Retrieved Evening Counts: {eveningCounts}")
    
    # Clear the counts from the session after retrieving them
    request.session['eveningCounts'] = {}
    
    return render(request, "StoneCharges_EveningCounts.html", {'eveningCounts': eveningCounts})




@csrf_exempt
def generate_file_ChargesCounts(request):
    logger.debug(f"POST data: {request.POST}")
    logger.debug(f"Files data: {request.FILES}")    
    excel_file = request.FILES.get('excelFile')
    
    if not excel_file:
        logger.error("No file found in request")
        return JsonResponse({'error': 'No file found in request'}, status=400)
    
    if request.method == 'POST':
        try:
            saved_file_path = handle_uploaded_file(excel_file)
            if saved_file_path:
                result_path, morningCounts, eveningCounts = ORG_chargesCounts(saved_file_path) 
                
                # Store counts in session
                request.session['morningCounts'] = morningCounts
                request.session['eveningCounts'] = eveningCounts
                
                logger.debug(f"Stored Morning Counts: {morningCounts}")
                logger.debug(f"Stored Evening Counts: {eveningCounts}")
                
                # Instead of returning a file, return the counts as JSON
                return JsonResponse({
                    'morningCounts': morningCounts,
                    'eveningCounts': eveningCounts
                })
            else:
                logger.error('Failed to save file')
                return JsonResponse({'error': 'Failed to save file'}, status=500)
        except Exception as e:
            logger.exception("Error processing file in generate_file_ChargesCounts")
            return JsonResponse({'error': str(e)}, status=500)
    
    logger.error("Invalid request method or no file found")
    return JsonResponse({'error': 'Invalid request method or no file found'}, status=400)

def handle_uploaded_file(file):
    try:
        upload_dir = 'uploaded_files'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        file_path = os.path.join(upload_dir, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return file_path
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        return None

def serve_file_response(file_path):
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response