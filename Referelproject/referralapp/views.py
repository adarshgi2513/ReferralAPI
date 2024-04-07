from django.shortcuts import render, redirect
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer,LoginSerializer,UserDetailsSerializer,ReferralUserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
# Create your views here.



#this is the user registration API
#User Registration Endpoint:
class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            referral_code = serializer.validated_data.get('referral_code')
            referred_by_user = None
            if referral_code:
                referred_by_user = User.objects.filter(referral_code=referral_code).first()
                if referred_by_user:
                    referred_by_user.referral_points += 1
                    referred_by_user.save()
            user = serializer.save()
            return Response({"user_id": user.id, "message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#login API
class LoginAPI(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        _data=request.data
        serializer=LoginSerializer(data=_data)
        if not serializer.is_valid():
            return Response({'message':serializer.errors},status=status.HTTP_404_NOT_FOUND)
        user=authenticate(name=serializer.data['name'],password=serializer.data['password'])
        
        if not user:
            return Response({'message':"invalid"},status=status.HTTP_404_NOT_FOUND)
        
        token, _ =Token.objects.get_or_create(user=user)

        return Response({'message':'login successfull','token':str(token)},status=status.HTTP_201_CREATED)
     #user detail API
    #User Details Endpoint:
class UserDetails(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        # Retrieve the authenticated user
        user = request.user
        # Serialize user details
        serializer = UserDetailsSerializer(user)
        # Return serialized user details in the response
        return Response(serializer.data)

#Referrals Endpoint
class ReferralsEndpoint(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        referral_code = user.referral_code
        if referral_code:
            referred_users = User.objects.filter(referral_code=referral_code)
            paginator = PageNumberPagination()
            paginated_referred_users = paginator.paginate_queryset(referred_users, request)
            serializer = ReferralUserSerializer(paginated_referred_users, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response({'message': 'No referrals found'}, status=status.HTTP_404_NOT_FOUND)