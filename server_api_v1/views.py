import psutil
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response

from server_api_v1.serializers import UserSerializer


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class MemoryViewSet(viewsets.ViewSet):

    def get(self):
        values_dict = {
            "virtual": [
                {"label": "Used", "value": psutil.virtual_memory()._asdict()['used'] / (1024 * 1024)},
                {"label": "Free", "value": psutil.virtual_memory()._asdict()['free'] / (1024 * 1024)}
            ],
            "swap": [
                {"label": "Used", "value": psutil.swap_memory()._asdict()['used'] / (1024 * 1024)},
                {"label": "Free", "value": psutil.swap_memory()._asdict()['free'] / (1024 * 1024)}
            ]
        }

        return Response(values_dict, status=status.HTTP_200_OK)


class ProcessViewSet(viewsets.ViewSet):

    @staticmethod
    def get_process_sorted_by_memory(top_n):
        """
        Get list of running processes sorted by Memory Usage
        """
        list_of_processes = []
        # Iterate over the list
        for proc in psutil.process_iter():
            try:
                # Fetch process details as dict
                pinfo = proc.as_dict(attrs=['pid', 'name'])
                pinfo['memory used'] = round(proc.memory_info().rss / (1024 * 1024), 3)
                # pinfo['virtual_memory_size'] = round(proc.memory_info().vms / (1024 * 1024), 3)
                # Append dict to list
                list_of_processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Sort list of dict by key vms i.e. memory usage
        list_of_process_objs = sorted(list_of_processes, key=lambda process: process['memory used'], reverse=True)
        if top_n:
            list_of_process_objs = list_of_process_objs[:top_n]
        return list_of_process_objs

    def get(self):
        process_list = self.get_process_sorted_by_memory(30)
        return Response(process_list, status=status.HTTP_200_OK)
