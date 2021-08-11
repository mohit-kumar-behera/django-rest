from django.urls import include, path

from account.api.views import (
	api_registration_view,
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'account-api'

urlpatterns = [
	path('register', api_registration_view, name="register"),
	path('login', obtain_auth_token, name='login'),
]