from django.contrib import admin
from .models import (
    Rate, Trainer, TrainerImages, Reviews, RatingTrainer,
    RatingStar, Reviews, Abonement, OrderAbonement, OrderTraining)


class ImageTrainer(admin.TabularInline):
    '''Фото тренера'''

    model = TrainerImages
    extra = 3


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    
    '''Тарифы тренеров'''

    list_display = ('title','count_minutes', 'price',)


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    '''Тренер'''

    list_display = ('position', 'first_name', 'last_name',
                    'email', 'phone', 'rate', )

    inlines = [ImageTrainer]


# @admin.register(TrainerImages)
# class TrainerImagesAdmin(admin.ModelAdmin):
#     '''Admin View for TrainerImages)'''

#     list_display = ('title',  'trainer', )

#     @admin.register(Reviews)
#     class ReviewsAdmin(admin.ModelAdmin):
#         '''Admin View for Reviews)'''

#         list_display = ('email', 'name', 'parent', 'trainer', )


@admin.register(RatingTrainer)
class RatingTrainerAdmin(admin.ModelAdmin):
    '''Рейтинг тренера'''

    list_display = ('star', 'trainer', 'ip', )


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    '''Количество звезд рейтинга'''

    list_display = ('value',)



@admin.register(Abonement)
class AbonementAdmin(admin.ModelAdmin):
    '''Абонементы'''

    list_display = ('title', 'description', 'price', 'number_of_months', )


@admin.register(OrderAbonement)
class OrderAbonementAdmin(admin.ModelAdmin):
    '''Забронированные абонемент'''

    list_display = ('user', 'abonement', 'start', 'end', 'status', )




admin.site.register(OrderTraining)