from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from account.api.serializers import RegistrationSerializer

from rest_framework.authtoken.models import Token


@api_view(['POST',])
def api_registration_view(request):
	if request.method == 'POST':
		serializer = RegistrationSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			account = serializer.save()
			data['success'] = True
			data['message'] = 'successfully registered'
			data['email'] = account.email

			token = Token.objects.get(user=account).key
			data['token'] = token
		else:
			data = serializer.errors
			data['success'] = False
		return Response(data)