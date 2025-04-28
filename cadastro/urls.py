from django.urls import path
from . import views

app_name = 'cadastro'

urlpatterns = [
    # path("", views.index, name="index"),
    path('cadastrar_socio/', views.cadastrar_socio, name='cadastrar_socio')
]