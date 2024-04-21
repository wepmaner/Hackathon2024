from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
Team = get_user_model()

class TeamSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Team
        fields = ['id', 'login', 'password', 'email','team_name','photo']

class TeamSerializerWithoutPassword(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'login', 'email','team_name','photo']

class TeamSerializerChange(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id','team_name','photo']

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.UserInfo
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Question
        fields = '__all__'

class TeamRatingSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.TeamRating
        fields = '__all__'