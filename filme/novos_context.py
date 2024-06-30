from .models import Filme

def lista_filmes_recentes(request):
    lista_filmes = Filme.objects.all().order_by('-data_criacao')[0:8]
    return {"lista_filmes_recentes": lista_filmes}

def lista_filmes_em_alta(request):
    lista_filmes = Filme.objects.all().order_by('-visualizacoes')[0:8]
    return {"lista_filmes_em_alta": lista_filmes}

def filme_destaque(request):
    try:
        filme = Filme.objects.order_by('-data_criacao')[0]
        return {"filme_destaque": filme}
    except:
        return {"filme_destaque": None}
