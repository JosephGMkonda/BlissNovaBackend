from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .serializer import RegistrationSerializer
from rest_framework import serializers
import uuid



class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        

        if (serializer.is_valid()):
            serializer.save()
            return Response({
                "RequestId":str(uuid.uuid4()),
                "Message":"User created successfully",

                
                "user":serializer.data
                },status=status.HTTP_201_CREATED)

        return Response({"Errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


        
    
        

