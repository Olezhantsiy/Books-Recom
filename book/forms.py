from django import forms
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import PasswordInput, ModelForm
from django.core.validators import validate_email
# форма авторизации
class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Username')
    password = forms.CharField(required=True, label='Пароль')

# форма регистрации
class RegisterForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

    username = forms.CharField(min_length=3,
                               max_length=120,
                               required=True,
                               label='Никнейм',
                               validators=[RegexValidator(regex='^[a-zA-Z0-9]*$', message='Может содержать только латинские буквы и цифры', code='invalid_username'),],
                               error_messages={'min_length': 'Имя пользователя должен содержать не менее 3 символов'}
                               )

    email = forms.EmailField(required=True, label='Email', error_messages={'invalid': 'Введите корректный адрес электронной почты '})

    password = forms.CharField(widget=PasswordInput(), required=True, label='Пароль')
    password_confirm = forms.CharField(widget=PasswordInput(), required=True, label='Повторите пароль')

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        # валидация паролей
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError(
                {'password_confirm': "Пароли не совпадают", 'password': ''}
            )
        # валидация никнейма
        username = self.cleaned_data.get("username")

        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError({'username': "Пользователь с таким именем уже существует"})

        # валидация email
        email = self.cleaned_data.get("email")
        try:
            validate_email(email)
        except ValidationError as e:
            raise forms.ValidationError({'email': "Email не является валидным адресом"})

        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError({'email': "Пользователь с таким адресом электронной почты уже существует"})

        return cleaned_data