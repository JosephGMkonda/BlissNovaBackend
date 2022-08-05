from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions



# Registration serializer

class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(max_length=150,write_only=True)
    
    class Meta:
        model = User
        fields = ("username","email","password")

    def ValidateUser(self,request):
        username = request.get("username",None)
        email = request.get('email',None)
        

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email':('email already exists')})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username':('username already exists')})

    

        return super().validate(request)

    def validatePassword(self,request):
        user = User(**request)
        password = request.get('password')

        try:
            validate_password(password,user)
        
        except exceptions.ValidationError as e:
            serializer_errors = serializers.as_serializer_error(e)
            raise exceptions.ValidationError(
                {'password':serializer_errors['none_field_errors']}
            )
        return request


    def create(self,validated_data):
        return User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']

        )

        
