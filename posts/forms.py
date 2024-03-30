from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(label='', widget=forms.Textarea(
        attrs={'rows': 2, 'class': 'form-control',
               'placeholder': 'Напишите ваш комментарий', 'id': 'comment'}))

    class Meta:
        model = Comment
        fields = ('text',)
