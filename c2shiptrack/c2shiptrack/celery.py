import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'c2shiptrack.settings')

app = Celery('c2shiptrack')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

#
# @app.on_init
# def setup_periodic_tasks(sender):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#
#
# @app.task
# def test(arg):
#     print(arg)
#     from api.tasks import test
#     test(arg)
