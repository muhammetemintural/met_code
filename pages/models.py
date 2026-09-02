from django.db import models
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image

class Project(models.Model):
    # Kategori Seçenekleri (İleride filtreleme için kullanılacak)
    KATEGORILER = (
        ('web', 'Web Geliştirme'),
        ('mobil', 'Mobil Uygulama'),
        ('otomasyon', 'Otomasyon & Bot'),
        ('sistem', 'Sistem & Mimari'),
        ('ai', 'Yapay Zeka & Veri'),
    )

    title = models.CharField(max_length=200, verbose_name="Proje Başlığı")
    category = models.CharField(max_length=50, choices=KATEGORILER, default='web', verbose_name="Kategori")
    description = models.TextField(verbose_name="Proje Açıklaması")
    technology = models.CharField(max_length=200, verbose_name="Kullanılan Teknolojiler")
    icon = models.CharField(max_length=100, default="fa-solid fa-code", verbose_name="FontAwesome İkonu")
    
    image = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name="Proje Fotoğrafı")
    live_link = models.URLField(blank=True, null=True, verbose_name="Canlı Site Linki")
    github_link = models.URLField(blank=True, null=True, verbose_name="GitHub Linki")
    
    is_active = models.BooleanField(default=True, verbose_name="Sitede Göster")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    def save(self, *args, **kwargs):
        # Eğer bir resim yüklendiyse ve zaten optimize edilmemişse (.webp değilse)
        if self.image and not self.image.name.endswith('.webp'):
            img = Image.open(self.image)
            
            # Şeffaf resimleri (PNG) RGB'ye çevir ki WEBP yaparken bozulmasın
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Resim çok büyükse genişliğini 1200px'e sabitle (orantılı küçült)
            if img.width > 1200:
                output_size = (1200, int(img.height * (1200 / img.width)))
                img = img.resize(output_size, Image.Resampling.LANCZOS)
            
            # Remi bellekte WEBP formatında ve %85 kaliteyle sıkıştır
            output = BytesIO()
            img.save(output, format='WEBP', quality=85)
            output.seek(0)
            
            # Eski resmi yeni optimize edilmiş resimle değiştir
            dosya_adi = self.image.name.split('.')[0] + '.webp'
            self.image = ContentFile(output.read(), name=dosya_adi)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Proje"
        verbose_name_plural = "Projeler"
        ordering = ['-created_at']

class ContactMessage(models.Model):
    name = models.CharField(max_length=150, verbose_name="Kurum / Kişi Adı")
    email = models.EmailField(verbose_name="E-Posta Adresi")
    message = models.TextField(verbose_name="İhtiyaç / Mesaj")
    is_read = models.BooleanField(default=False, verbose_name="Okundu mu?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Gönderilme Tarihi")

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = "İletişim Mesajı"
        verbose_name_plural = "İletişim Mesajları"
        ordering = ['-created_at']

class LabProject(models.Model):
    COLOR_CHOICES = (
        ('primary', 'Mor (Primary)'),
        ('secondary', 'Pembe (Secondary)'),
    )
    title = models.CharField(max_length=200, verbose_name="Proje Başlığı")
    description = models.TextField(verbose_name="Kısa Açıklama")
    progress = models.IntegerField(default=50, verbose_name="İlerleme Yüzdesi")
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='primary', verbose_name="Tema Rengi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Laboratuvar Projesi"
        verbose_name_plural = "Laboratuvar Projeleri"
        ordering = ['-created_at']