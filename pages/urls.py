from django.contrib import admin
from django.urls import path
from pages import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.index, name='index'),
    path('arsiv/', views.archive, name='archive'),
    path('proje/<int:project_id>/', views.project_detail, name='project_detail'),
    
    path('patron-girisi/', views.custom_login, name='custom_login'),
    path('metcode-panel/', views.custom_dashboard, name='custom_dashboard'),
    path('metcode-panel/ekle/', views.add_project, name='add_project'),
    path('metcode-panel/duzenle/<int:project_id>/', views.edit_project, name='edit_project'),
    path('metcode-panel/sil/<int:project_id>/', views.delete_project, name='delete_project'),
    
    path('cikis/', views.custom_logout, name='custom_logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

