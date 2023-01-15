from rest_framework.views import APIView
from .models import DataStore
from .serializers import DataStoreSerializer
from home.pagination import CustomPagination
from datetime import datetime


class DataStoreApiView(APIView):
    # pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        requested_date = datetime.strptime(self.request.GET['date'], '%d-%m-%Y')
        datastore = DataStore.objects.filter(
            last_updated__date=requested_date
        ).order_by('-cdate')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(datastore, request)
        serializer = DataStoreSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)