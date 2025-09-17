from django.shortcuts import render
from .serializers import RegistrationModelSerializer,LoginSerializer,ForgotPasswordSerializer,ResetPasswordSerializer,PasswordChangeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework import status
import random
from .models import ForgotPasswordModel
from .email import send_email
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from  rest_framework import permissions
User=get_user_model()
# Create your views here.


def otp_generator():
    otp=random.randint(100000,999999)
    return otp


class RegistrationView(APIView):
    def post(self,request):
        serializer=RegistrationModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detal":"Your Account Succesfully Created"},status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PATCH','PUT'])
def UserDetailView(request,pk):
#    if request.method =='GET':
   
   try:
        user_detail = User.objects.get(pk=pk)
        serializer=RegistrationModelSerializer(user_detail)
   except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
   
   if request.method=='GET':
         id=serializer.data.get('id')
         full_name=serializer.data.get('full_name')
         email=serializer.data.get('email')
         phone=serializer.data.get('phone')
         return Response({
             'id':id,
             "email":email,
             "phone":phone,
             "full_name":full_name
         })
     
   if not request.user.is_authenticated:
      return Response("Only Authenticated user Can update")
   
   if request.method in ['PUT','PATCH']:
      
      if not (user_detail==request.user):
         return Response("Only Owner can update his data or profile")
      serializer=RegistrationModelSerializer(user_detail,data=request.data,partial=True)
      if serializer.is_valid():
         user=serializer.save()
         return Response("your data updated")
    
   return Response(serializer.errors)
    
#LOGIN SECTION

class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data.get('email')
            password=serializer.validated_data.get('password')

            try:
                user=User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail":"No User Exists On This Email"},status=status.HTTP_404_NOT_FOUND)
            
            if not user.check_password(password):
                 return Response({"detail":"Incorrect Password"}, status=status.HTTP_401_UNAUTHORIZED)
            
            refresh=RefreshToken.for_user(user)
            return Response({
                'refresh':str(refresh),
                'access':str(refresh.access_token),
                'user':{
                    'id':user.id,
                    'role':user.role,
                    'email':user.email,
                    'phone':user.phone,
                    "is_active":user.is_active,
                    "is_staff":user.is_staff,
                    "is_superuser":user.is_superuser
                     
                }
            })
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    def  post(self,request):
        serializer=ForgotPasswordSerializer(data=request.data)

        if serializer.is_valid():
            email=serializer.validated_data.get('email')

            try:
                user=User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail":"User Doesnot Exist's On This Email"})
            
            
            otp=otp_generator()
            subject="Rest Your Password"
            message=f"Your One Time OTP code Is {otp}.It's valid for 5 min"
            receiver=user.email
            ForgotPasswordModel.objects.create(
                user=user,
                otp=otp
            )
            send_email(subject,message,receiver)
            
            return Response({
            "message":"OTP Send To Your email Check it",
            "password_reset_url":"http://127.0.0.1:8000/account/reset_password/"
         })
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

                  



class ResetPasswordView(APIView):
    def post(self,request):
        serializer=ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data.get('email')
            new_password=serializer.validated_data.get('new_password')
            confirm_password=serializer.validated_data.get('confirm_password')
            otp=serializer.validated_data.get('otp')
            if new_password and new_password!=confirm_password:
                return Response({"detail":"password and confirm password not matched!"},status=status.HTTP_400_BAD_REQUEST)
            try:
             user=User.objects.get(email=email)
            except User.DoesNotExist:
              return Response({"detail":"User Doesn't exists"},status=status.HTTP_400_BAD_REQUEST)

            try:
                forgot_pass_model=ForgotPasswordModel.objects.filter(user=user,otp=otp).latest('created_at')
            except ForgotPasswordModel.DoesNotExist:
                return Response({"detail":"Invalid OTP"},status=status.HTTP_400_BAD_REQUEST)
            
            if forgot_pass_model.is_used:
                return Response("The otp already used")
            if forgot_pass_model.is_expire_otp():
                return Response("OTP expired")
            
            user.set_password(new_password)
            user.save()
            forgot_pass_model.is_used=True
            forgot_pass_model.save()
            return Response({"detail":"Password Reseted succesfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
          
            
        
class PasswordChangeView(APIView):
   def post(self,request,pk):
      try:
         user=User.objects.get(pk=pk)
      except User.DoesNotExist:
         return Response("user doesn't exitst")
      if user != request.user:
         return Response("You can not Change This Password only Owner can change it")
      serializer=PasswordChangeSerializer(data=request.data)
      if serializer.is_valid():
         old_password=serializer.validated_data.get('old_password',None)
         new_password=serializer.validated_data.get('new_password',None)
         if not user.check_password(old_password):
            return Response("Old Password not matched")
         user.set_password(new_password)
         user.save()
         return Response("your password changed")
      return Response(serializer.errors)




class LogoutView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request):
        refresh=request.data.get('refresh')
        print(refresh)
        if not refresh:
            return Response({"detail":"refresh token is required"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token=RefreshToken(refresh)
            token.blacklist()
        except TokenError:
            return Response(
                {"error": "Invalid or expired refresh token"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {"message": "Logout successfully"},
            status=status.HTTP_200_OK
        )
