from django.shortcuts import redirect, render
from .models import NewsLetter
from django.contrib import messages
from .forms import FeedBackForm, NewsletterForm


def feedback_view(request):
    if request.method == "POST":
        form = FeedBackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Спасибо за обратную связь")
        return redirect('home')



def newsletter_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form  = form.save(commit=False)
            form.email = email
            form.save()
            messages.success(request, "Вы подписались на рассылку")
        return redirect('home')
