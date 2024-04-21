from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth import get_user_model
Team = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Team
        fields = ("login",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Team
        fields = ("login",)