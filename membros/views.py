from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import BibliotecaForm, CadastroForm
from .models import Biblioteca

def cadastro(request):
    if request.user.is_authenticated:
        return redirect("listar_bibliotecas")

    if request.method == "POST":
        dados = request.POST.copy()

        # O e-mail também será usado internamente como nome de usuário.
        email = dados.get("email", "").strip().lower()
        dados["username"] = email

        form = CadastroForm(dados)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Cadastro realizado com sucesso! Agora faça seu login.",
            )

            return redirect("login")
    else:
        form = CadastroForm()

    return render(
        request,
        "registro.html",
        {
            "form": form,
        },
    )

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

def configuracoes(request):
    return render(request, 'configuracoes.html')

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
