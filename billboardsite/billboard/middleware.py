from datetime import datetime, timedelta
import pytz
from django.contrib.auth import logout
from django.utils import timezone
from django.conf import settings


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')  # пытаемся забрать часовой пояс из сессии
        #  Если он есть в сессии, то выставляем такой часовой пояс.
        #  Если же его нет - часовой пояс выставить по умолчанию (на время сервера)
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)


class TimeoutLogout:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ttl = settings.LOGOUT_TIMEOUT

    def __call__(self, request):
        user = request.user
        tz_0 = pytz.timezone('UTC')
        if user.is_authenticated \
                and user.last_login < tz_0.localize(datetime.utcnow()) - timedelta(seconds=self.ttl):
            logout(request)

        response = self.get_response(request)

        return response
