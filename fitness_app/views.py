import stripe

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import messages
from .models import OrderTraining, Trainer, Abonement, OrderAbonement, Reviews
from .forms import OrderAbonementForm, RatingForm, ReviewForm, OrderTrainingForm
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
    title = 'Тренер'
    context_object_name = 'trainer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context


class OrderAbonementCreateView(TitleMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    ''' Оформление абонемента '''

    model =  OrderAbonement
    template_name = 'fitness_app/order_abonement_create.html'
    form_class = OrderAbonementForm
    success_url = reverse_lazy('home')
    title = 'Оформление абонемента'
    success_message = 'Вы успешно оформили абонемент!'

    def post(self, request, *args, **kwargs):
        super(OrderAbonementCreateView, self).post(request, *args, **kwargs)
        # checkout_session = stripe.checkout.Session.create(
        #     line_items=[
        #         {
        #             # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
        #             'price': '{{PRICE_ID}}',
        #             'quantity': 1,
        #         },
        #     ],
        #     mode='payment',
        #     success_url=settings.DOMAIN_NAME + '/success.html',
        #     cancel_url=settings.DOMAIN_NAME + '/cancel.html',
        # )

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.abonement = form.cleaned_data['abonement']
        form.instance.end = timezone.now(
        ) + timedelta(days=form.instance.abonement.number_of_months * 30)
        return super().form_valid(form)


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        trainer = Trainer.objects.get(id=pk)
        if form.is_valid():
            if request.POST.get('parent', None):
                form.parent = Reviews.objects.get(
                    id=int(request.POST.get('parent')))
            form = form.save(commit=False)
            form.trainer = trainer
            form.save()
            messages.success(request, 'Отзыв успешно отправлен')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class OrderTrainingCreateView(TitleMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    ''' Оформление занятия '''

    model = OrderTraining
    template_name = 'fitness_app/order_training_create.html'
    form_class = OrderTrainingForm
    success_url = reverse_lazy('home')
    title = 'Записаться на тренировку'
    success_message = 'Вы успешно записались на занятие!'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class MyAbonementListView(ListView):
    model = Abonement
    template_name = "my_abonement_list.html"
