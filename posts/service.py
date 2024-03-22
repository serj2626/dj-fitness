from django.contrib import messages


def add_like(request, article):
    if request.user not in article.likes.all() and request.user not in article.dislikes.all():
        article.likes.add(request.user)
        messages.success(request, 'Вы поставили лайк')

    elif request.user in article.likes.all() and request.user not in article.dislikes.all():
        article.likes.remove(request.user)
        messages.success(request, 'Вы убрали лайк')

    elif request.user not in article.likes.all() and request.user in article.dislikes.all():
        article.likes.add(request.user)
        article.dislikes.remove(request.user)
        messages.success(request, 'Вы поставили лайк')

    else:
        article.likes.add(request.user)
        messages.success(request, 'Вы поставили лайк')


def add_dislike(request, article):

    if request.user not in article.dislikes.all() and request.user not in article.likes.all():
        article.dislikes.add(request.user)
        messages.success(request, 'Вы поставили дизлайк')

    elif request.user not in article.dislikes.all() and request.user in article.likes.all():
        article.likes.remove(request.user)
        article.dislikes.add(request.user)
        messages.success(request, 'Вы поставили дизлайк')

    elif request.user in article.dislikes.all() and request.user not in article.likes.all():
        article.dislikes.remove(request.user)
        messages.success(request, 'Вы поставили дизлайк')

    else:
        article.dislikes.add(request.user)
        messages.success(request, 'Вы поставили дизлайк')
