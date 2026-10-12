from django.urls import path

from app import views

urlpatterns = [
    path("", views.home, name="home"),
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
