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
    path('metcode-panel/arsivle/<int:project_id>/', views.toggle_archive, name='toggle_archive'),
    
    # --- YENİ EKLENEN MESAJ KONTROL YOLLARI ---
    path('metcode-panel/mesaj-oku/<int:message_id>/', views.read_message, name='read_message'),
    path('metcode-panel/mesaj-sil/<int:message_id>/', views.delete_message, name='delete_message'),

    path('metcode-panel/lab-ekle/', views.add_lab_project, name='add_lab_project'),
    path('metcode-panel/lab-sil/<int:project_id>/', views.delete_lab_project, name='delete_lab_project'),
    path('metcode-panel/lab-duzenle/<int:project_id>/', views.edit_lab_project, name='edit_lab_project'), # BU SATIRI EKLE

    path('cikis/', views.custom_logout, name='custom_logout'),
     path('kvkk/', views.kvkk_view, name='kvkk'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)