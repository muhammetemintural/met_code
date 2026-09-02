from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, ContactMessage, LabProject # Bütün modelleri çağırdık

# 1. ANA SAYFA (Form Yakalama ve Lab Projeleri Eklendi)
def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Veritabanına kaydet
        ContactMessage.objects.create(name=name, email=email, message=message)
        
        # Mail Bildirimi
        try:
            konu = f"YENİ TALEP: met.code - {name}"
            icerik = f"Sistemden yeni bir mesaj aldın!\n\nMüşteri: {name}\nE-Posta: {email}\n\nMesaj Detayı:\n{message}\n\nKontrol paneline girerek yanıtlayabilirsin."
            send_mail(
                subject=konu,
                message=icerik,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=True,
            )
        except:
            pass
            
        return redirect('/#iletisim')

    projeler = Project.objects.filter(is_active=True).order_by('-created_at')[:6]
    lab_projeler = LabProject.objects.all().order_by('-created_at')[:4]
    return render(request, 'index.html', {'projeler': projeler, 'lab_projeler': lab_projeler})

# 2. TÜM PROJELER ARŞİV SAYFASI
def archive(request):
    projeler = Project.objects.all().order_by('-created_at')
    return render(request, 'arsiv.html', {'projeler': projeler})

# 3. PROJE DETAY SAYFASI
def project_detail(request, project_id):
    proje = get_object_or_404(Project, id=project_id)
    return render(request, 'project_detail.html', {'proje': proje})

# 4. GİZLİ GİRİŞ EKRANI
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('custom_dashboard')
        
    if request.method == 'POST':
        kullanici = request.POST.get('username')
        sifre = request.POST.get('password')
        
        user = authenticate(request, username=kullanici, password=sifre)
        if user is not None:
            login(request, user)
            return redirect('custom_dashboard')
        else:
            return render(request, 'panel_login.html', {'hata': 'Hatalı şifre veya kullanıcı adı!'})
            
    return render(request, 'panel_login.html')

# 5. PATRON PANELİ
@login_required(login_url='custom_login')
def custom_dashboard(request):
    projeler = Project.objects.all().order_by('-created_at')
    mesajlar = ContactMessage.objects.all().order_by('-created_at')
    lab_projeler = LabProject.objects.all().order_by('-created_at')
    
    stats = {
        'total_projects': projeler.count(),
        'vitrin_count': projeler.filter(is_active=True).count(),
        'arsiv_count': projeler.filter(is_active=False).count(),
        'unread_messages': mesajlar.filter(is_read=False).count(),
    }
    
    return render(request, 'panel_dashboard.html', {
        'projeler': projeler, 
        'mesajlar': mesajlar, 
        'lab_projeler': lab_projeler,
        'stats': stats
    })

# 6. YENİ PROJE EKLE
@login_required(login_url='custom_login')
def add_project(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category', 'web')
        description = request.POST.get('description')
        icon = request.POST.get('icon', 'fa-solid fa-code')
        live_link = request.POST.get('live_link', '')
        github_link = request.POST.get('github_link', '')
        image = request.FILES.get('image') 
        
        tech_list = request.POST.getlist('tech_choices')
        technology = ", ".join(tech_list)
        
        placement = request.POST.get('placement')
        is_active = True if placement == 'vitrin' else False
        
        Project.objects.create(
            title=title, category=category, technology=technology,
            description=description, icon=icon, image=image,
            live_link=live_link, github_link=github_link, is_active=is_active
        )
        return redirect('custom_dashboard')
        
    return render(request, 'panel_add_project.html')

# 7. PROJE DÜZENLE
@login_required(login_url='custom_login')
def edit_project(request, project_id):
    proje = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        proje.title = request.POST.get('title')
        proje.technology = request.POST.get('technology')
        proje.description = request.POST.get('description')
        proje.icon = request.POST.get('icon', 'fa-solid fa-code')
        proje.live_link = request.POST.get('live_link', '')
        proje.github_link = request.POST.get('github_link', '')
        
        if 'image' in request.FILES:
            proje.image = request.FILES['image']
            
        proje.is_active = True if request.POST.get('is_active') == 'on' else False
        proje.save()
        return redirect('custom_dashboard')
        
    return render(request, 'panel_edit_project.html', {'proje': proje})

# 8. PROJE SİL
@login_required(login_url='custom_login')
def delete_project(request, project_id):
    proje = get_object_or_404(Project, id=project_id)
    proje.delete()
    return redirect('custom_dashboard')

# 9. ÇIKIŞ YAP
def custom_logout(request):
    logout(request)
    return redirect('index')

# 10. HIZLI ARŞİVLE / VİTRİNE AL
@login_required(login_url='custom_login')
def toggle_archive(request, project_id):
    proje = get_object_or_404(Project, id=project_id)
    proje.is_active = not proje.is_active
    proje.save()
    return redirect('custom_dashboard')

# 11. MESAJ OKUNDU İŞARETLE
@login_required(login_url='custom_login')
def read_message(request, message_id):
    mesaj = get_object_or_404(ContactMessage, id=message_id)
    mesaj.is_read = True
    mesaj.save()
    return redirect('custom_dashboard')

# 12. MESAJ SİL
@login_required(login_url='custom_login')
def delete_message(request, message_id):
    mesaj = get_object_or_404(ContactMessage, id=message_id)
    mesaj.delete()
    return redirect('custom_dashboard')

# 13. LABORATUVAR PROJESİ EKLE (İŞTE EKSİK OLAN KISIM)
@login_required(login_url='custom_login')
def add_lab_project(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        progress = request.POST.get('progress')
        color = request.POST.get('color')
        
        LabProject.objects.create(
            title=title, description=description, progress=progress, color=color
        )
        return redirect('custom_dashboard')
    return render(request, 'panel_add_lab.html')

# 14. LABORATUVAR PROJESİ SİL
@login_required(login_url='custom_login')
def delete_lab_project(request, project_id):
    proje = get_object_or_404(LabProject, id=project_id)
    proje.delete()
    return redirect('custom_dashboard')

# 15. LABORATUVAR PROJESİ DÜZENLE (YENİ)
@login_required(login_url='custom_login')
def edit_lab_project(request, project_id):
    proje = get_object_or_404(LabProject, id=project_id)
    if request.method == 'POST':
        proje.title = request.POST.get('title')
        proje.description = request.POST.get('description')
        proje.progress = request.POST.get('progress')
        proje.color = request.POST.get('color')
        proje.save()
        return redirect('custom_dashboard')
        
    return render(request, 'panel_edit_lab.html', {'proje': proje})