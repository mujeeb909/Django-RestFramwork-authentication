from rest_framework import serializers
from .models import CustomUser
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import *

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'password', 'password2', 'tc')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Validations
    def validate(self, data):
        password = data['password']
        password2 = data['password2']

        if password != password2:
            raise serializers.ValidationError({'Error': "Password mismatch"})

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2', None)  # Exclude 'password2' from the dictionary

        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
    
    def validate(self, data):
        email = data['email']
        password = data['password']

        if not email or not password :
            raise serializers.ValidationError({'Error': "Plz fill all input fields"})

        return data
    

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['id','name', 'email']


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField( max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField( max_length=255, style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['password', 'password2']
    
    def validate(self, data):
        password = data['password']
        password2 = data['password2']
        user = self.context.get('user')

        if password != password2:
            raise serializers.ValidationError({'Error': "Password mismatch"})
        user.set_password(password)
        user.save()

        return data
    

class SendPasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ['email']
    
    def validate(self, data):
        email = data['email']
        if CustomUser.objects.filter(email = email).exists():
            user = CustomUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print( "Encoded ID",uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("Token", token)
            link = "http://localhost:8000/api/user/reset/"+uid+"/"+token
            print(link)
            # Send Email
            body = "Click following link to reset " + link
            data_email = {
                "subject":"Email Reset",
                "body": body,
                "to_email": user.email
            }
            Util.send_mail(data_email)
            return data

            
        else:
            raise serializers.ValidationError({'Error': "Email Does not exist"})


class UserPasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField( max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField( max_length=255, style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['password', 'password2']
    
    def validate(self, data):
        try:
            password = data['password']
            password2 = data['password2']
            uid = self.context.get('uid')
            token = self.context.get('token')

            if password != password2:
                raise serializers.ValidationError({'Error': "Password mismatch"})
        
            id = smart_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError({'Error': "Invalid Token or Expired"})
            user.set_password(password)
            user.save()
        
            return data
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError({'Error': "Invalid Token or expired"}) 

        