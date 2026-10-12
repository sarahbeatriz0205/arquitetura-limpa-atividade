from django.urls import path

from app import views

urlpatterns = [
    path("", views.home, name="home"),
    # ===========================================================================
    # Rotas de cada CRUD (exemplo com "trabalhos"; as demais seguem o mesmo padrão)
    #   - trabalhos/              : exibe página de listagem
    #   - trabalhos/incluir/      : exibe a página de inclusão de registro
    #   - trabalhos/alterar/<id>/ : exibe a página de alteração de registro
    #   - trabalhos/excluir/<id>/ : exibe a página de exclusão de registro
    #   - trabalhos/salvar/       : insere, altera ou exclui um registro do BD
    # ===========================================================================
    path("trabalhos/", views.trabalhos, name="trabalhos"),
    path("trabalhos/<str:acao>/", views.trabalhos, name="trabalhos"),
    path("trabalhos/<str:acao>/<int:id>/", views.trabalhos, name="trabalhos"),
    path("servicos/", views.servicos, name="servicos"),
    path("servicos/<str:acao>/", views.servicos, name="servicos"),
    path("servicos/<str:acao>/<int:id>/", views.servicos, name="servicos"),
    path("demandas/", views.demandas, name="demandas"),
    path("demandas/<str:acao>/", views.demandas, name="demandas"),
    path("demandas/<str:acao>/<int:id>/", views.demandas, name="demandas"),
    path("propostas/", views.propostas, name="propostas"),
    path("propostas/<str:acao>/", views.propostas, name="propostas"),
    path("propostas/<str:acao>/<int:id>/", views.propostas, name="propostas"),
]
