from django.urls import path
from . import views

app_name = 'perfil'

urlpatterns = [
    path('', views.Insert.as_view(), name='insert'),
    # path('register/', views.Register.as_view(), name='register'),
    path('update/', views.Update.as_view(), name='update'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('delete/<int:pk>', views.PerfilDeleteView.as_view(), name='delete'),
]
