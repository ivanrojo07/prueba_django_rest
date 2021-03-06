from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status,authentication

from profiles_api.serializers import HelloSerializers, RegisterSerializers,LoginSerializer

from rest_framework.decorators import  api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
import json
# function para obtener token

@api_view(["POST"])
@permission_classes((AllowAny,))
def get_token(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({
            'error':'Please provide both username and password fields'
        },status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username,password=password)
    if not user:
        return Response({
            'error': 'Invalid credentials'
        },
        status=HTTP_404_NOT_FOUND)
    token, obj = Token.objects.get_or_create(user=user)
    print(token)
    print(obj)
    return Response({
        'token':token.key
    },
    status=HTTP_200_OK)


class RegisterView(APIView):

    serializer_class =  RegisterSerializers
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        if request.user.is_authenticated:
            return Response({"message":"You are not authenticated"}, status=HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                serializer= self.serializer_class(user)
                return Response({
                    "message":"User created",
                    "user": serializer.data
                },status=201)

            else:

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return

class LoginView(APIView):
    permission_classes =(AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({'message':"success",'user':RegisterSerializers(user).data},status=HTTP_200_OK)
        
class LogoutView(APIView):
    def post(self,request):
        logout(request)
        return Response({'message':"Logout successfully"},status=HTTP_200_OK)

class UserView(CreateAPIView):
    serializer_class=RegisterSerializers
    lookup_field='pk'

    def get_object(self,*args,**kwargs):
        return self.request.user

class HelloApiView(APIView):
    # HOLA MUNDO

    serializer_class = HelloSerializers
    def get(self, request, format=None):
        # Retornar lista de caracteristicas apiview

        an_apiview= [
            "usamos metodos HTTP como funciones(get,post,patch, put, delete)",
            "es similiar a una vista tradicional de django",
            "No da el mayor control sobre la logica de nuestra aplicación",
            "esta mapeado manualmente a los URLs"
            
        ]
        return Response({"message":"Hola", 'an_apiview': an_apiview},status=200)

    def post(self, request):
        """Crear un mensaje con nuestro nombre"""
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f'Hello {name}'
            return Response({"message":message},status=200)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self,request, pk=None):
        """Maneja actualizar un objeto"""
        return Response({
            "method":"PUT"
        })

    def patch(self, request, pk=None):
        """Maneja actualizacion parcial de un objeto"""
        return Response({
            "method":"PATCH"
        })

    def delete(self, request, pk=None):
        """Maneja Eliminación de un objeto"""
        return Response({
            "method":"DELETE"
        })