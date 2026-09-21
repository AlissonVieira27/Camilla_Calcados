from django import forms
from .models import Biblioteca

class BibliotecaForm(forms.ModelForm):
    class Meta:
        model = Biblioteca
        fields = ['nome', 'regiao_administrativa', 'endereco', 'descricao', 'imagem', 'possui_internet']
        
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
        
        labels = {
            'nome': 'Nome da Biblioteca',
            'regiao_administrativa': 'Região Administrativa',
            'endereco': 'Endereço',
            'descricao': 'Descrição',
            'imagem': 'Foto do Local',
            'possui_internet': 'Possui acesso à internet?'
        }