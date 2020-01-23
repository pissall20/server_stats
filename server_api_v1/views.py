from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from server_api_v1.serializers import UserSerializer
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
