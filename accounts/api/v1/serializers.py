from rest_framework import serializers
from accounts.models import User
from django.contrib.auth.password_validation import validate_password


class RegistrationSerialize(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password', 'password1']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError('Passwords do not match')
        try:
            validate_password(attrs.get('password'))
        except serializers.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password1',None)
        return User.objects.create_user(**validated_data)
