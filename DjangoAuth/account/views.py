from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .renderers import UserRenderers


# Generates Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)

  return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderers]
  def post(self, request):
    serializer = UserRegistrationSerializer(data = request.data)

    if not serializer.is_valid():
      return Response({'status': 403, 'message': serializer.errors} )
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'status': 201,'Token':token , 'message':"Registration Successfully Added", "payload": serializer.data})

class UserLoginView(APIView):
  renderer_classes = [UserRenderers]

  def post(self, request):
    serializer = UserLoginSerializer(data = request.data)
    if not serializer.is_valid():
      return Response({'status': 403, 'message': serializer.errors} )
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email = email, password = password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'status': 200,  'Token': token ,'message':"Login Successfully Added", "payload": serializer.data})
    else:
      return Response({'status': 404, 'Error':"Username or Password is not valid", })



class UserProfileView(APIView):
  renderer_classes = [UserRenderers]
  permission_classes = [IsAuthenticated]
  
  def get(self, request):
    serializer = UserProfileSerializer(request.user)

    if not IsAuthenticated:
      return Response({'status': 404, 'MSG':"No Token Found", })

    
    return Response({'status': 200, 'MSG':serializer.data, })

    
class UserPasswordChangeView(APIView):
  renderer_classes = [UserRenderers]
  permission_classes = [IsAuthenticated]
  
  def post(self, request):
    serializer = UserChangePasswordSerializer(data = request.data, context= {'user':request.user})
    if not serializer.is_valid():
      return Response({'status': 403, 'message': serializer.errors} )
    return Response({'status': 200, 'MSG':"Password Changed Successfully", })
  
class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderers]

  def post(self, request):
    serializer = SendPasswordResetEmailSerializer(data = request.data)
    if not serializer.is_valid():
      return Response({'status': 403, 'message': serializer.errors} )
    return Response({'status': 200, 'MSG':"Password Reset email sent, Please check your email"})


class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderers]

  def post(self, request, uid, token):
    serializer = UserPasswordResetSerializer(data = request.data, context={"uid": uid, "token": token})
    if not serializer.is_valid():
      return Response({'status': 403, 'message': serializer.errors} )
    return Response({'status': 200, 'MSG':"Password Reset Successfully"})





  


