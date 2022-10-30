from drf_spectacular.utils import extend_schema_field, inline_serializer
from rest_framework import serializers
from freelancer.account.models import User, Profile
from freelancer.resume.models import CV, Education, WorkExperience, Contact
from freelancer.project.models import Project
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError(
                'A user with this email and password is not found.')
        return user


class RegisterUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username",
                  "email", "password", "confirm_password")

    def validate(self, data):
        if data.get("password", None) != data.get("confirm_password", None):
            raise serializers.ValidationError("Password not match")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create(**validated_data)


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ("cv",)


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        exclude = ("cv",)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("id", "image", "link")


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        exclude = ("user",)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("bio", "avatar", "approved")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username")


class UserInfoSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()

    @extend_schema_field(inline_serializer(
        name='User Data',
        fields={
            "user": UserSerializer(),
            "profile": ProfileSerializer(),
            "resume": ResumeSerializer(),
            "work-experience": WorkExperienceSerializer(many=True),
            "education": EducationSerializer(many=True),
            "contact": ContactSerializer(many=True),
        }
    ))
    def get_user(self, obj):
        user_data = UserSerializer(obj).data
        profile_data = ProfileSerializer(obj.profile).data
        resume_data = ResumeSerializer(obj.user_cv).data
        experience_data = WorkExperienceSerializer(obj.user_cv.cv_experience, many=True).data
        education_data = EducationSerializer(obj.user_cv.cv_education, many=True).data
        contact_data = ContactSerializer(obj.user_cv.cv_contact, many=True).data
        user_data.update({
            "profile": profile_data,
            "resume": {
                **resume_data,
                "work-experience": experience_data,
                "education": education_data,
                "contact": contact_data
            }
        })
        return user_data
