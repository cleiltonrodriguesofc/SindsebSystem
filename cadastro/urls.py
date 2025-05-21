from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


app_name = 'cadastro'

urlpatterns = [
    # path("", views.index, name="index"),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('cadastrar_socio/', views.cadastrar_socio, name='cadastrar_socio'),
    path('listar_socios/', views.listar_socios, name='listar_socios'),

    path('socio/<int:socio_id>/', views.ver_socio, name='ver_socio'),
    path('editar/<int:socio_id>/', views.editar_socio, name='editar_socio'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('documents/', views.documents, name='documents'),
    # path('reports/', views.reports, name='reports'),
    # path('settings/', views.settings, name='settings'),


]