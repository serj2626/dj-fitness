from django.shortcuts import redirect, render
from django.views.generic import CreateView
from common.mixins import TitleMixin
from .models import NewsLetter
from django.contrib import messages
from .forms import FeedBackForm, NewsletterForm
from .service import send_email_for_newsletter, send_email_for_feedback
from .tasks import send_feedback, send_newsletter


def feedback_view(request):
    if request.method == "POST":
        form = FeedBackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Спасибо за обратную связь")
            send_feedback.delay(form.cleaned_data.get('email'), form.cleaned_data.get('name'))
        return redirect('home')


def newsletter_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.email = email
            form.save()
            messages.success(request, "Вы подписались на рассылку")
            send_newsletter.delay(email=email)
        return redirect('home')

