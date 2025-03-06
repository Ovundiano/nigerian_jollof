from django.shortcuts import render
from django.http import HttpResponse


def test_cloudinary(request):
    return HttpResponse(
        "Media storage system is now using standard Django FileSystemStorage"
    )
