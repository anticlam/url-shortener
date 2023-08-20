from rest_framework.serializers import ModelSerializer
from .models import Link

#serializer for the Link model. it includes all the fields of the model.
class LinkSerializer(ModelSerializer):
    class Meta:
        model=Link
        fields='__all__'