import psutil
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


class MemoryViewSet(APIView):

    def get(self, request):
        values_dict = {
            "virtual": [
                {"label": "Used", "value": psutil.virtual_memory()._asdict()['percent']},
                {"label": "Free", "value": 100 - psutil.virtual_memory()._asdict()['percent']},
            ],
            "swap": [
                {"label": "Used", "value": psutil.swap_memory()._asdict()['percent']},
                {"label": "Free", "value": 100 - psutil.swap_memory()._asdict()['percent']},
            ]
        }

        return Response(values_dict, status=status.HTTP_200_OK)


class ProcessViewSet(APIView):

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

    def get(self, request):
        process_list = self.get_process_sorted_by_memory(30)
        return Response(process_list, status=status.HTTP_200_OK)


class DiskViewSet(APIView):

    @staticmethod
    def get_storage_stats():
        disk_usage = list()
        for k, v in psutil.disk_usage("/")._asdict().items():
            if k == "percent":
                disk_usage.append({"label": "Used", "value": v})
                disk_usage.append({"label": "Free", "value": 100 - v})

        disk_io = list()
        for k, v in psutil.disk_io_counters()._asdict().items():
            if "bytes" in k:
                disk_io.append({"label": k, "value": (v / (1024 * 1024))})
            elif "time":
                disk_io.append({"label": k, "value": (v / 1000)})

        return {
            "disk_usage": disk_usage,
            "disk_io": disk_io
        }

    def get(self, request):
        return Response(self.get_storage_stats(), status=status.HTTP_200_OK)
