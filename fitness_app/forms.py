from tkinter import Label
from django import forms
from .models import (OrderAbonement, Rate, RatingTrainer, Abonement,
                     Reviews, RatingStar, OrderTraining, Trainer)


class OrderAbonementForm(forms.ModelForm):
    abonement = forms.ModelChoiceField(
        label='Выберите абонемент', empty_label='Не выбран', queryset=Abonement.objects.all())

    class Meta:
        model = OrderAbonement
        fields = ['abonement']
        widgets = {

            # 'start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'abonement': forms.Select(attrs={'class': ' form-select w-100'}),
            # 'end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class ReviewForm(forms.ModelForm):
    """Форма отзывов"""
    name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={'class': 'form-control shadow-sm', 'placeholder': 'Ваше имя', 'id': 'nameID'}),
    )
    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={'class': 'form-control shadow-sm', 'placeholder': 'Ваша почта'}))
    text = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={
                              "rows": 2, "cols": 10,  'class': 'form-control shadow-sm', 
                              'placeholder': 'Напишите ваш отзыв', 'id': 'textID'}),
    )

    class Meta:
        model = Reviews
        fields = ("name", "email", "text")


class RatingForm(forms.ModelForm):
    """Форма рейтинга"""

    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = RatingTrainer
        fields = ("star",)


class OrderTrainingForm(forms.ModelForm):
    """Форма забронирования занятия"""
    trainer = forms.ModelChoiceField(
        label='Тренер', queryset=Trainer.objects.all(), empty_label='Выберите тренера')
    rate = forms.ModelChoiceField(
        label='Тариф', queryset=Rate.objects.all(), empty_label='Выберите тариф')
    start = forms.DateTimeField(label='Дата начала занятия', widget=forms.DateTimeInput(
        attrs={'class': 'form-control', 'type': 'datetime-local'}))

    class Meta:
        model = OrderTraining
        fields = ('trainer', 'rate', 'start', )
