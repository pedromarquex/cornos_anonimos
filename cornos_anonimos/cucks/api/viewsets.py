from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from cucks.models import Cuck
from .serializers import CuckSerializer


class CuckSignUpViewSet(ModelViewSet):
    queryset = Cuck.objects.all()
    serializer_class = CuckSerializer
    # http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    http_method_names = ['post']

    # def create(self, request, *args, **kwargs):
    # return super(CuckViewSet, self).create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        erro_signup = {}
        # validating fields username and email which should be unique
        # verifying if already exists a user with this email
        try:
            email = request.data['user.email']
            User.objects.get(email=email)
            erro_signup['email_error'] = 'já existe uma conta com este email'
        except:
            pass
        # verifying if already exists a user with this username
        try:
            username = request.data['user.username']
            User.objects.get(username=username)
            erro_signup['username_error'] = 'este username já está sendo utilizado'
        except:
            pass

        # caso tenha erro, retornar o erro
        if len(erro_signup) > 0:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=erro_signup)
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=request.data['password'])
                cuck = Cuck.objects.create(nick=request.data['nick'], user=user)
                serializer = self.get_serializer(cuck)
                a = 2
                return Response(status=status.HTTP_201_CREATED, data=serializer.data)
            except:
                user = User.objects.get(username=username)
                user.delete()


class CuckLoginViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CuckSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        erro_login = {}
        try:
            User.objects.get(username=request.data['username'])
        except:
            erro_login['user_error'] = 'usuário não cadastrado'

        if len(erro_login) > 0:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=erro_login)
        else:
            try:
                user = authenticate(username=request.data['username'], password=request.data['password'])
                if user is not None:
                    login(request, user)
                    return Response(status=status.HTTP_200_OK, data={'ok': 'usuário logado'})
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={'erro': 'senha inválida'})
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'erro': 'login error'})
