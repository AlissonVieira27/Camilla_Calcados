from .models import ConfiguracaoUsuario


def preferencias_usuario(request):
    if not request.user.is_authenticated:
        return {
            'perfil_config': None
        }

    try:
        configuracao = ConfiguracaoUsuario.objects.get(
            user=request.user
        )
    except ConfiguracaoUsuario.DoesNotExist:
        configuracao = None

    return {
        'perfil_config': configuracao
    }