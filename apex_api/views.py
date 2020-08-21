# from django.shortcuts import render
#from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from .models import UserSignUp
from .serializers import UserRegisterSerializer


class UserRegistration(APIView):
    def post(self, request):
        if request.method == "POST":
            serializer = UserRegisterSerializer(data=request.data, instance=request.user)
            serializer.is_valid(raise_exception=True)
            # serializer.validated_data.get("referral_code")
            # serializer.validated_data.get("full_name")
            # serializer.validated_data.get("email")
            # serializer.validated_data.get("password")
            serializer.save()
            return Response(
                {'data': 'Created Successfully!'}, status=status.HTTP_201_CREATED
            )

# {
#     "referral_code": "foo_b",
#     "full_name": "Foo bar",
#     "email": "f@example.com",
#     "password": "foob2345"
# }