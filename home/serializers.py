from rest_framework import serializers
from .models import DataStore




class DataStoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataStore
        fields = ["last_updated", "current_price", "coin_id"]

    def to_representation(self, instance):
        data = super(DataStoreSerializer, self).to_representation(instance)
        data['timestamp'] = data.pop('last_updated')
        data['price'] = data.pop('current_price')
        data['coin'] = data.pop('coin_id')
        return data