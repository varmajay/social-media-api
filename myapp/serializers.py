from rest_framework import serializers
from .models import *
from django import forms
from django.contrib.auth.password_validation import validate_password
# from django.conf import settings
# from django.core.mail import send_mail


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['name','email','password','confirm_password']


    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        # subject = 'welcome to Social Media '
        # message = f"""Hi {validated_data['name']}, thank you for registering in Social Media ."""
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [validated_data['email']]
        # send_mail( subject, message, email_from, recipient_list )
        user = User.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user





class LoginSerializer(serializers.ModelSerializer):
    email =serializers.EmailField(max_length = 225)
    class Meta:
        model = User
        fields = ['email','password']


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance



class ViewProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['name','email','profile','bio']


class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['name','phone','gender','address','profile','bio']




class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['image','caption']


class ViewPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['image','caption','created_at','likes']



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']

class ViewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user','post','comment','date']