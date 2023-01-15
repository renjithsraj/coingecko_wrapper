from django.urls import path
from .views import (
    DataStoreApiView,
)

urlpatterns = [
    path('prices/btc', DataStoreApiView.as_view()),
]