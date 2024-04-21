from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login),#Вход
    path('signup', views.signup),#Регистрация
    path('emailconfirm', views.auth_mail),#Подтверждение почты
    path('user/<int:user_id>/questions', views.get_questionByUserId),#Получить вопросы по id учатника
    path('team/<int:team_id>/questions', views.get_questionByTeamId),#Получить вопросы всех участников по id группы
    path('user/<int:user_id>/sendquestion', views.send_question),# Отправить вопрос пользователю по id
    path('user/<int:question_id>/send_answer', views.send_answer),# Ответить на вопрос пользователя по id вопроса
    path('teams/', views.get_teams), #Список всех групп
    path('team/<int:team_id>/users', views.get_users), #Получить участников по id группы
    path('team/<int:team_id>', views.teamControl), #Получить/изменить/удалить группу по id
    path('user/<int:user_id>', views.userControl), #Получить/изменить/удалить участника по id
    path('rating/send',views.send_rating),
    path('rating/<int:team_id>',views.get_rating)
    
    
]

