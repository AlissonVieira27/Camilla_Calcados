from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Biblioteca


class CadastroForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nome",
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "given-name",
            }
        ),
    )

    last_name = forms.CharField(
        label="Sobrenome",
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "family-name",
            }
        ),
    )

    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
            }
        ),
    )

    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirmar senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Já existe uma conta cadastrada com este e-mail."
            )

        return email

    def save(self, commit=True):
        usuario = super().save(commit=False)

        usuario.first_name = self.cleaned_data["first_name"]
        usuario.last_name = self.cleaned_data["last_name"]
        usuario.email = self.cleaned_data["email"]

        if commit:
            usuario.save()

        return usuario


class BibliotecaForm(forms.ModelForm):
    class Meta:
        model = Biblioteca

        fields = [
            "nome",
            "regiao_administrativa",
            "endereco",
            "descricao",
            "imagem",
            "possui_internet",
        ]

        widgets = {
            "descricao": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Descreva o espaço e sua estrutura",
                }
            ),
        }

        labels = {
            "nome": "Nome da Biblioteca",
            "regiao_administrativa": "Região Administrativa",
            "endereco": "Endereço",
            "descricao": "Descrição",
            "imagem": "Foto do Local",
            "possui_internet": "Possui acesso à internet?",
        }