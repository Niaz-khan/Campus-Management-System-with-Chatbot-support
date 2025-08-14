from django import forms

class ChatForm(forms.Form):
    question = forms.CharField(
        label='Ask a Question',
        max_length=500,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your question...'})
    )
    # Add any additional fields if needed
    