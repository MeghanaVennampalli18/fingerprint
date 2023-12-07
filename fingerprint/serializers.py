from rest_framework import serializers
from .models import User_Details

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Details
        fields = '__all__'