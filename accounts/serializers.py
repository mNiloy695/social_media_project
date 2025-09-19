from rest_framework import serializers
from django.contrib.auth import get_user_model
User=get_user_model()

class RegistrationModelSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['id','full_name','email','password','confirm_password','phone','profile']
    
    def validate(self,attrs):
        password=attrs.get('password',None)
        confirm_password=attrs.pop('confirm_password',None)
        email=attrs.get('email',None)
        if (password and confirm_password) and password !=confirm_password:
            raise serializers.ValidationError({"error":"Password and ConfirmPassword not matched !"})
        if email  and  User.objects.filter(email=email).exclude(pk=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError({"error":"The email Already exists !"})
        return attrs
    
    def create(self,validated_data):
        password=validated_data.pop('password')
        user=User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password=validated_data.get('password')

        for attr,value in validated_data.items():
            setattr(instance,attr,value)

        if password:
            validated_data.pop('password')
            instance.set_password(password)
       
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField(max_length=6)
    new_password=serializers.CharField()
    confirm_password=serializers.CharField()


class PasswordChangeSerializer(serializers.Serializer):
     old_password=serializers.CharField(max_length=100)
     new_password=serializers.CharField(max_length=100)