from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from . import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
Team = get_user_model()

from django.shortcuts import get_object_or_404

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from django.conf import settings
from django.core.mail import send_mail

from .models import EmailConfirm, UserInfo,Question,TeamRating


from random import randint

def rand_key_auth_mail(team):
    key_auth = randint(1000000, 9999999)


    EmailConfirm.objects.create(team=team, code=key_auth)
    return key_auth

@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['login', 'password'],
        properties={
            'login': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING)
        }
    ), responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING),
            'user': openapi.Schema(type=openapi.TYPE_OBJECT)
        }
    )})
@api_view(['POST'])
def login(request):
    """Запрос на вход, возвращает токен и имя пользователя"""
    team = get_object_or_404(Team, login=request.data.get('login'))
    if not team.check_password(request.data.get('password')):
        return Response({'deatil':"Not found",'status':status.HTTP_404_NOT_FOUND})
    token, created = Token.objects.get_or_create(user=team)
    serializer = serializers.TeamSerializer(instance=team)
    return Response({'token':token.key, 'user': serializer.data})



@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def auth_mail(request):
    """Проверка подверждения почты"""
    email_confirm = EmailConfirm.objects.filter(team=request.user).first()
    if request.POST.get('code') == str(email_confirm.code):
        request.user.emailConfirm = 1
        request.user.save()
        email_confirm.delete()
        return Response({'return': 'ok', 'status':status.HTTP_200_OK})
    return Response({'return':'NO!','status':status.HTTP_400_BAD_REQUEST})
    
@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['login', 'password'],
        properties={
            'login': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING)
        }
    ), responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING),
            'user': openapi.Schema(type=openapi.TYPE_OBJECT)
        }
    )})
@api_view(['POST'])
def signup(request):
    """Регистрация, возвращает токен и имя пользователя"""
    serializer = serializers.TeamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = Team.objects.get(login=request.data.get('login'))
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        key_auth = rand_key_auth_mail(user)
        send_mail('Хакатон вебпрактик', f'Подтвердите вашу почту\nВаш код для подтврждения почты: {key_auth}', settings.EMAIL_HOST_USER, ['srezvan21@yandex.ru'])
        
        return Response({'token': token.key, 'user': serializer.data}) 
    return Response({'error': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST}) 


@swagger_auto_schema(
    method='get',
    responses={200: serializers.QuestionSerializer(many=True)})
@api_view(['GET'])
def get_questionByUserId(request,user_id):
    """Получение списка вопросов по идентификатору участника"""
    user = get_object_or_404(UserInfo,pk=user_id)
    questions = Question.objects.filter(user=user)
    serializer =serializers.QuestionSerializer(instance=questions,many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='get',
    responses={200: serializers.QuestionSerializer(many=True)})
@api_view(['GET'])
def get_questionByTeamId(request,team_id):
    """Получение списка вопросов по идентификатору команды"""
    team = get_object_or_404(Team,pk=team_id)
    questions = Question.objects.filter(user__team=team)
    serializer =serializers.QuestionSerializer(instance=questions,many=True)
    return Response(serializer.data)



@swagger_auto_schema(method='post', request_body=serializers.QuestionSerializer, responses={200: 'ok'})
@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_question(request,user_id):
    """Отправка вопроса на почту"""
    serializer = serializers.QuestionSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(UserInfo,pk=user_id)
        serializer.save(user=user)
        from_user = request.data['name']
        text = request.data['text']
        send_mail('Хакатон вебпрактик', f'Здраствуйте {user.name}! Вам задали вопрос.\nОт: {from_user}\nВопрос: {text}\nОтветить на вопрос может капитан команды через личный кабинет', settings.EMAIL_HOST_USER, [user.email])
        return Response(status.HTTP_200_OK)
    return Response({'error': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['answer'],
        properties={
            'answer': openapi.Schema(type=openapi.TYPE_STRING)
        }
    ), responses={200: 'status:200'})
#Отправка ответа на вопрос:
@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_answer(request,question_id):
    """Отправка ответа на почту"""
    question = get_object_or_404(Question,pk=question_id)
    answer = request.data['answer']
    question.answer = answer
    #serializers = serializers.QuestionSerializer(instance=question)
    send_mail('Хакатон вебпрактик', f'Здраствуйте {question.name}! На ваш вопрос ответили\n{question.user.name} с команды {question.user.team.name}\nОтвет: {answer}\nВаш вопрос: {question.text}', settings.EMAIL_HOST_USER, [question.email])
    return Response(status.HTTP_200_OK)
    




@swagger_auto_schema(
    method='get',
    responses={200: serializers.TeamSerializerWithoutPassword(many=True)})
@api_view(['GET'])
def get_teams(request):
    teams = Team.objects.all()
    serializer = serializers.TeamSerializerWithoutPassword(instance=teams,many=True)
    return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
# @permission_classes([IsAuthenticated])
def teamControl(request,team_id):
    if request.method == 'GET':
        team = get_object_or_404(Team,pk=team_id)
        serializer = serializers.TeamSerializerWithoutPassword(instance=team)
        return Response({'result':serializer.data})
    elif request.method == 'PUT':
        if request.user.is_authenticated and request.user.id == team_id:
            team = get_object_or_404(Team,pk=team_id)
            data = request.data.copy()
            if not data.get('login'):
                data['login'] = team.login
            elif not data.get('email'):
                data['email'] = team.email
            elif not data.get('team_name'):
                data['team_name'] = team.team_name
            serializer = serializers.TeamSerializerChange(instance=team, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'result': serializer.data, 'status': status.HTTP_200_OK})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'DELETE':
        if request.user.id == team_id:
            team = get_object_or_404(Team,pk=team_id)
            team.delete()
            return Response(status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
#Получение/редактирование/удаление участника
@api_view(['GET','POST','PUT','DELETE'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
# @permission_classes([IsAuthenticated])
def userControl(request,user_id):
    if request.method == 'GET':
        user = get_object_or_404(UserInfo,pk=user_id)
        serializer = serializers.UserSerializer(instance=user)
        return Response({'result': serializer.data, 'status':status.HTTP_200_OK})
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        data = request.data.copy()
        data['team'] = request.user.id
        serializer = serializers.UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            send_mail('Хакатон вебпрактик', f'{request.data["name"]}, вас зарегистрировали в качестве участника в команде {request.user.name}', settings.EMAIL_HOST_USER, [request.data["email"]])
            return Response({'user':serializer.data,'status': status.HTTP_200_OK})
        return Response({'error': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
    
    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        users = UserInfo.objects.filter(team_id=request.user.id)
        user_ids = [user.id for user in users]
        if user_id in user_ids:
            user = get_object_or_404(UserInfo,pk=user_id)
            data = request.data.copy()
            data['team'] = request.user.id
            serializer = serializers.UserSerializer(instance=user,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'result': serializer.data, 'status': status.HTTP_200_OK})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status':status.HTTP_403_FORBIDDEN})
    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        users = UserInfo.objects.filter(team_id=request.user.id)
        user_ids = [user.id for user in users]
        if user_id in user_ids:
            user = get_object_or_404(UserInfo,pk=user_id)
            user.delete()
            return Response(status.HTTP_200_OK)
        return Response({'status':status.HTTP_403_FORBIDDEN})

@api_view(['GET'])
def get_users(request,team_id):
    users = UserInfo.objects.filter(team_id=team_id)
    users_serializer = serializers.UserSerializer(instance=users,many=True)
    return Response(users_serializer.data)

@api_view(['GET'])
def get_rating(request,team_id):
    ratings = TeamRating.objects.filter(from_team=team_id)
    ratings_serializer = serializers.TeamRatingSerializer(instance=ratings,many=True)
    return Response(ratings_serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_rating(request):
    data = request.data.copy()
    data['from_team'] = request.user.id
    rating = serializers.TeamRatingSerializer(data=data)

    if rating.is_valid():
        rating.save()
        return Response({'result':rating.data})
    return Response({'error': rating.errors, 'status':status.HTTP_400_BAD_REQUEST})
