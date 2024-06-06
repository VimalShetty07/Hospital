from rest_framework.response import Response
from rest_framework import authentication
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework_simplejwt.backends import TokenBackend
from .models import User
import datetime
from rest_framework.exceptions import ValidationError



class CustomAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        try:
            if 'Authorization' not in request.headers:
                response = Response({'error': 'Please Login'}, status=status.HTTP_403_FORBIDDEN)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                return response

            elif request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1] == None:
                response = Response({'error': 'Please Login'}, status=status.HTTP_403_FORBIDDEN)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                return response
            

            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            # print(type(token))
            data = {'token': token}
            # print(data)
            valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
            user_id = valid_data['user_id']
            user = User.objects.get(id=user_id)
            request.user = user
            user.last_login = datetime.datetime.now()
            user.save()
            return (user, None)

        except:
            raise ValidationError({"error": ["Please Login"]})