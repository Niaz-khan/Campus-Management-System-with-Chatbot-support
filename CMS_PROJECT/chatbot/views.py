from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .llm import handle_real_data

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            answer = handle_real_data(question, request.user)
            return HttpResponse(answer)
    return HttpResponse('')

