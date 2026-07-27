from django.contrib import admin
from django.urls import path
from pages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # İşte en kritik satır:
    path('proje/<int:project_id>/', views.project_detail, name='project_detail'),
]