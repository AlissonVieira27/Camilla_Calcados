from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.db.models import Q

from django.contrib.sessions.models import Session

from django.utils import timezone

from django.views.decorators.http import require_POST

from .forms import (
    BibliotecaForm,
    ConfiguracoesForm
)

from .models import (
    Biblioteca,
    ConfiguracaoUsuario
)

def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com Sucesso! Faça seu login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    form.fields['username'].widget.attrs.update({'placeholder': 'Escolha um nome de usuário', 'autocomplete': 'username'})
    form.fields['password1'].widget.attrs.update({'placeholder': 'Crie uma senha', 'autocomplete': 'new-password'})
    form.fields['password2'].widget.attrs.update({'placeholder': 'Repita sua senha', 'autocomplete': 'new-password'})
    return render(request, 'registro.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def _ids_favoritos(request):
    return {int(item) for item in request.session.get('bibliotecas_favoritas', [])}

def listar_bibliotecas(request):
    busca = request.GET.get('q', '').strip()
    regiao = request.GET.get('regiao', '').strip()
    lista = Biblioteca.objects.all().order_by('nome')

    if busca:
        lista = lista.filter(
            Q(nome__icontains=busca) |
            Q(regiao_administrativa__icontains=busca) |
            Q(endereco__icontains=busca)
        )
    if regiao:
        lista = lista.filter(regiao_administrativa__iexact=regiao)

    regioes = Biblioteca.objects.order_by('regiao_administrativa').values_list(
        'regiao_administrativa', flat=True
    ).distinct()
    return render(request, "listar_biblioteca.html", {
        "bibliotecas": lista,
        "regioes": regioes,
        "busca": busca,
        "regiao": regiao,
        "favoritos": _ids_favoritos(request),
    })

def alternar_favorito(request, id):
    biblioteca = get_object_or_404(Biblioteca, id=id)
    favoritos = _ids_favoritos(request)
    if biblioteca.id in favoritos:
        favoritos.remove(biblioteca.id)
    else:
        favoritos.add(biblioteca.id)
    request.session['bibliotecas_favoritas'] = sorted(favoritos)
    destino = request.POST.get('next')
    if destino not in {'listar_bibliotecas', 'salvos'}:
        destino = 'listar_bibliotecas'
    return redirect(destino)

def salvos(request):
    bibliotecas = Biblioteca.objects.filter(id__in=_ids_favoritos(request)).order_by('nome')
    return render(request, 'salvos.html', {'bibliotecas': bibliotecas, 'favoritos': _ids_favoritos(request)})

@login_required
def perfil(request):
    return render(request, 'perfil.html')

@login_required
def configuracoes(request):

    configuracao, _ = (
        ConfiguracaoUsuario.objects.get_or_create(
            user=request.user,
            defaults={
                'display_name': (
                    request.user.first_name
                    or request.user.username
                )
            }
        )
    )

    if request.method == 'POST':

        form = ConfiguracoesForm(
            request.POST,
            request.FILES,
            instance=configuracao,
            user=request.user
        )

        if form.is_valid():

            configuracao = form.save(
                commit=False
            )

            nome_completo = (
                form.cleaned_data[
                    'nome_completo'
                ].strip()
            )

            partes = nome_completo.split()

            if partes:

                request.user.first_name = partes[0]

                request.user.last_name = (
                    ' '.join(partes[1:])
                )

            else:

                request.user.first_name = ''
                request.user.last_name = ''

            request.user.email = (
                form.cleaned_data['email']
            )

            request.user.save(
                update_fields=[
                    'first_name',
                    'last_name',
                    'email'
                ]
            )

            configuracao.user = request.user
            configuracao.save()

            messages.success(
                request,
                'Suas configurações foram salvas com sucesso.'
            )

            return redirect('configuracoes')

    else:

        form = ConfiguracoesForm(
            instance=configuracao,
            user=request.user
        )

    sessoes = _obter_sessoes_usuario(
        request.user,
        request.session.session_key
    )

    return render(
        request,
        'configuracoes.html',
        {
            'form': form,
            'perfil_config': configuracao,
            'sessoes': sessoes,
        }
    )


def _obter_sessoes_usuario(
    user,
    sessao_atual
):

    sessoes = []

    sessoes_django = Session.objects.filter(
        expire_date__gte=timezone.now()
    ).order_by('-expire_date')

    for sessao in sessoes_django:

        dados = sessao.get_decoded()

        if str(
            dados.get('_auth_user_id')
        ) != str(user.pk):
            continue

        sessoes.append({
            'key': sessao.session_key,

            'current':
                sessao.session_key == sessao_atual,

            'expires':
                sessao.expire_date,
        })

    return sessoes


@login_required
@require_POST
def encerrar_sessao(request):

    session_key = request.POST.get(
        'session_key'
    )

    if not session_key:
        return redirect('configuracoes')

    if session_key == request.session.session_key:

        messages.error(
            request,
            'A sessão atual não pode ser encerrada por aqui.'
        )

        return redirect('configuracoes')

    sessao = Session.objects.filter(
        session_key=session_key,
        expire_date__gte=timezone.now()
    ).first()

    if sessao:

        dados = sessao.get_decoded()

        if str(
            dados.get('_auth_user_id')
        ) == str(request.user.pk):

            sessao.delete()

    messages.success(
        request,
        'Sessão encerrada com sucesso.'
    )

    return redirect('configuracoes')


@login_required
@require_POST
def excluir_conta(request):

    usuario = request.user

    logout(request)

    usuario.delete()

    return redirect('home')

def ajuda(request):
    return render(request, 'ajuda.html')

def termos(request):
    return render(request, 'termos.html')

def privacidade(request):
    return render(request, 'privacidade.html')

@login_required
def criar_biblioteca(request):
    if request.method == "POST":
        form = BibliotecaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Biblioteca adicionada com sucesso!')
            return redirect('listar_bibliotecas')
    else:
        form = BibliotecaForm()
    return render(request, "criar_biblioteca.html", {"form": form})

@login_required
def editar_biblioteca(request, id):
    biblioteca = get_object_or_404(Biblioteca, id=id)
    if request.method == "POST":
        form = BibliotecaForm(request.POST, request.FILES, instance=biblioteca)
        if form.is_valid():
            form.save()
            messages.success(request, 'Biblioteca atualizada com sucesso!')
            return redirect('listar_bibliotecas')
    else:
        form = BibliotecaForm(instance=biblioteca)
    return render(request, "editar_biblioteca.html", {"form": form, "biblioteca": biblioteca})

@login_required
def deletar_biblioteca(request, id):
    biblioteca = get_object_or_404(Biblioteca, id=id)
    if request.method == 'POST':
        biblioteca.delete()
        messages.success(request, 'Biblioteca removida com sucesso!')
        return redirect('listar_bibliotecas')
    return render(request, "confirmar_delecao.html", {"biblioteca": biblioteca})
