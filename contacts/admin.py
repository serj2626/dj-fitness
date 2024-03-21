from django.contrib import admin
from .models import NewsLetter, FeedBack


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    '''Admin View for NewsLetter)'''

    list_display = ('email',)


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    '''Admin View for FeedBack)'''

    list_display = ('name', 'email', 'subject', )
