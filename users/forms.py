from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
User = get_user_model()


class CreationForm(UserCreationForm):
    """Форма регистрации пользователя"""

    email = forms.EmailField(required=True, label='Электронная почта')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name','username', 'email')
