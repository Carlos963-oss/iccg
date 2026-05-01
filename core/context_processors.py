from .models import Ministerio

def ministerios(request):
    return {
        'ministerios': Ministerio.objects.all()
    }