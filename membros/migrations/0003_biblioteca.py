from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('membros', '0002_anime_delete_membros')]

    operations = [
        migrations.DeleteModel(name='Anime'),
        migrations.CreateModel(
            name='Biblioteca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('regiao_administrativa', models.CharField(max_length=100)),
                ('endereco', models.CharField(blank=True, max_length=255)),
                ('descricao', models.TextField(blank=True, max_length=500)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='bibliotecas/')),
                ('possui_internet', models.BooleanField(default=False)),
            ],
        ),
    ]
