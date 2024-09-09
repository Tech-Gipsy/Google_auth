# auth_app/views.py
from allauth.account.views import login
from allauth.socialaccount.models import SocialAccount
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth
from .serializers import UserSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = auth.create_user(
                    email=email,
                    password=password
                )
                return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = auth.get_user_by_email(email)
                # Normally you would validate the password, but Firebase does this via the sign-in process

                # Sign in with email and password using Firebase
                custom_token = auth.create_custom_token(user.uid)
                return Response({"status":"Login Successfull","token":custom_token},status=status.HTTP_200_OK,)
                return Response({"token": custom_token}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def google_sign_in(request):
    user = request.user
    if user.is_authenticated:
        social_account = SocialAccount.objects.get(user=user, provider='google')
        id_token = social_account.extra_data['id_token']
        try:
            # Verify the ID token with Firebase
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            # You can now create a session or further authenticate
            login(request, user)
            return redirect('/')
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return redirect('/accounts/login/')

