from django import forms
from .models import FeedBack, NewsLetter


class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ['name', 'email', 'subject', 'message']


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = ['email']

    def clean_email(self):
        data = self.cleaned_data["email"]
        qs = NewsLetter.objects.filter(email=data)
        if qs.exists():
            raise forms.ValidationError("Вы уже подписаны на рассылку")
        
        return data
    