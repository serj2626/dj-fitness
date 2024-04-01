from urllib import request
from django.shortcuts import get_object_or_404, redirect
import stripe
from http import HTTPStatus
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.contrib import messages
from .models import RatingTrainer, Trainer, Abonement, OrderAbonement, Reviews, OrderTraining, CalendarTrainer
from .forms import OrderAbonementForm, RatingForm, ReviewForm, OrderTrainingForm
from .service import get_client_ip, add_new_training_for_trainer
from common.mixins import TitleMixin
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class HomeView(TitleMixin, TemplateView):
    ''' Главная страница '''

    template_name = 'fitness_app/home.html'
    title = 'Главная'


class TrainerListView(TitleMixin, ListView):
    ''' Список тренеров '''

    model = Trainer
    template_name = 'fitness_app/trainer_list.html'
    title = 'Тренеры'
    context_object_name = 'trainers'


class AbonementListView(TitleMixin, ListView):
    ''' Список сезонных абонементов '''

    queryset = Abonement.objects.order_by('pk')
    template_name = 'fitness_app/abonement_list.html'
    title = 'Сезонные билеты'
    context_object_name = 'tickets'


class TrainerDetailView(TitleMixin, DetailView):
    ''' Детальная информация о тренере '''

    model = Trainer
    template_name = 'fitness_app/trainer_detail.html'

    context_object_name = 'trainer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        context["title"] = self.get_object()
        context['form'] = ReviewForm()
        context['reviews'] = Reviews.objects.filter(
            trainer=self.get_object(), parent__isnull=True)
        return context


class AddReview(View):
    """Отзывы к тренеру"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        trainer = Trainer.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent = Reviews.objects.get(
                    id=int(request.POST.get('parent')))
            form.trainer = trainer
            form.save()
            messages.success(request, 'Отзыв успешно отправлен')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SuccessTemplateView(TitleMixin, TemplateView):
    ''' Страница успешного оформления '''

    template_name = 'fitness_app/success.html'
    title = 'Спасибо!'


class CancelTemplateView(TitleMixin, TemplateView):
    ''' Страница отмены '''

    template_name = 'fitness_app/cancel.html'
    title = 'Отмена'


class OrderAbonementCreateView(TitleMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    ''' Оформление абонемента '''

    model = OrderAbonement
    template_name = 'fitness_app/order_abonement_create.html'
    form_class = OrderAbonementForm
    success_url = reverse_lazy('my_abonements')
    title = 'Оформление абонемента'
    success_message = 'Вы успешно оформили абонемент!'

    def post(self, request, *args, **kwargs):
        super(OrderAbonementCreateView, self).post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1OxCk22NWu5rst1qs5XNvq5E',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='{}{}'.format(
                settings.DOMAIN_NAME, reverse('order_success')),
            cancel_url='{}{}'.format(
                settings.DOMAIN_NAME, reverse('order_cancel')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.abonement = form.cleaned_data['abonement']
        form.instance.end = timezone.now(
        ) + timedelta(days=form.instance.abonement.number_of_months * 30)
        return super().form_valid(form)


class DeleteAbonementView(TitleMixin, LoginRequiredMixin, View):

    def get(self, request, pk):
        abonement = get_object_or_404(OrderAbonement, pk=pk)
        abonement.delete()
        return HttpResponseRedirect(reverse('my_abonements'))


class OrderTrainingCreateView(TitleMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    ''' Оформление персональной тренировки '''

    model = OrderTraining
    template_name = 'fitness_app/order_training_create.html'
    form_class = OrderTrainingForm
    success_url = reverse_lazy('my_trainings')
    title = 'Записаться на тренировку'
    success_message = 'Вы успешно записались на занятие!'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.end = form.instance.start + \
            timedelta(minutes=form.instance.rate.count_minutes)
        add_new_training_for_trainer(CalendarTrainer, self.request.user,
                                     form.instance.trainer, form.instance.start, form.instance.end)
        return super().form_valid(form)


class DeleteTrainingView(TitleMixin, LoginRequiredMixin, View):

    def get(self, request, pk):
        training = get_object_or_404(OrderTraining, pk=pk)
        training.delete()
        return HttpResponseRedirect(reverse('my_trainings'))


class MyAbonementListView(TitleMixin, LoginRequiredMixin, ListView):
    template_name = "fitness_app/my_abonement_list.html"
    title = 'Мои абонементы'
    context_object_name = 'abonements'

    def get_queryset(self):
        return OrderAbonement.objects.filter(user=self.request.user)


class MyTrainingListView(TitleMixin, LoginRequiredMixin, ListView):
    template_name = "fitness_app/my_training_list.html"
    title = 'Мои тренировки'
    context_object_name = 'trainings'

    def get_queryset(self):
        return OrderTraining.objects.filter(user=self.request.user)


class AddStarRating(View):
    """Добавление рейтинга тренеру"""

    def post(self, request, pk):
        print(get_client_ip(self, request))
        rate = int(request.POST.get("rate"))
        RatingTrainer.objects.update_or_create(
            ip=get_client_ip(self, request),
            trainer_id=pk,
            defaults={"star_id": rate},
        )

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CalendarTrainerView(TitleMixin, LoginRequiredMixin, ListView):
    ''' Расписание тренеров '''

    model = CalendarTrainer
    template_name = "fitness_app/calendar.html"
    title = 'Расписание тренеров'
    context_object_name = 'trainings'
