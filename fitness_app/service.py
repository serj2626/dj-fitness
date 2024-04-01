def get_path_for_avatar_for_trainer(instance, filename):
    return f'trainers/{instance.pk}/{filename}'


def get_client_ip(self, request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_new_training_for_trainer(obj, user, trainer, start, end):
    calendar = obj(trainer=trainer, user=user, start=start, end=end)
    calendar.save()
