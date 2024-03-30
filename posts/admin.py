from django.contrib import admin
from .models import Article, Comment, Category

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    '''Admin View for Article)'''

    list_display = ('title', 'category', 'created_at',)
    filter_horizontal = ('likes', 'dislikes', )
    save_on_top = True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    '''Admin View for Comment)'''

    list_display = ('id', 'parent', 'article', 'user',
                    'created_at', 'updated_at', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for Category)'''

    list_display = ('name', 'created_at', 'updated_at', 'slug', )
    prepopulated_fields = {'slug': ('name', )}


