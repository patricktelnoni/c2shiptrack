from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from c2shiptrack.models import LoggedInUser


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    print("Some one is logging in")
    LoggedInUser.objects.get_or_create(user=kwargs.get('user'))


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    print("Some one is logging out")
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()


