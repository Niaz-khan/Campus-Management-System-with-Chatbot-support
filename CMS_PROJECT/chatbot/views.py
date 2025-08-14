from django.shortcuts import render
from .llm import handle_real_data
from .forms import ChatForm

def chatbot_view(request):
    answer = None
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            answer = handle_real_data(question, request.user)
    else:
        form = ChatForm()

    return render(request, 'chatbot/chatbot.html', {'form': form, 'answer': answer})
