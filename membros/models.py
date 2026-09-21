from django.db import models

class Biblioteca(models.Model):
    nome = models.CharField(max_length=255)
    regiao_administrativa = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255, blank=True)
    descricao = models.TextField(max_length=500, blank=True)
    imagem = models.ImageField(upload_to='bibliotecas/', blank=True, null=True)
    possui_internet = models.BooleanField(default=False)

    def __str__(self):
        return self.nome