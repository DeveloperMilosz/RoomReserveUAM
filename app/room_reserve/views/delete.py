from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Meeting

def delete_meeting(request, meeting_id):
    # Ensure the user is authenticated or has the right permissions
    if request.method == "POST":
        meeting = get_object_or_404(Meeting, id=meeting_id)
        meeting.delete()
        return JsonResponse({'message': 'Meeting deleted successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)