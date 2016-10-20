from django.conf import settings

ERROR_FAIL = getattr(settings, 'ERROR_FAIL', 'login_fail')
ONE_PAGE_OF_DATA = getattr(settings, 'ONE_PAGE_OF_DATA', 2)
