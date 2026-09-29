from django.utils import timezone
from django.utils import translation

from .models import ConfiguracaoUsuario


class PreferenciasUsuarioMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:

            try:
                configuracao = request.user.configuracao

            except ConfiguracaoUsuario.DoesNotExist:
                configuracao = None

            if configuracao:

                if configuracao.timezone:
                    timezone.activate(
                        configuracao.timezone
                    )
                else:
                    timezone.deactivate()

                if configuracao.language:
                    translation.activate(
                        configuracao.language
                    )
                else:
                    translation.deactivate()

            else:
                timezone.deactivate()
                translation.deactivate()

        else:
            timezone.deactivate()
            translation.deactivate()

        response = self.get_response(request)

        return response