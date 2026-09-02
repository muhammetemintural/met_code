# met.code | Professional Portfolio & Agency Architecture

Bu proje, modern web teknolojileri kullanılarak geliştirilmiş, performans ve güvenlik odaklı kurumsal bir portfolyo ve yazılım ajansı mimarisidir. İlerleyen aşamalarda özel bir siber güvenlik (Pentest) laboratuvarı olarak kullanılmak üzere izole bir altyapıya uygun tasarlanmıştır.

## 🚀 Kullanılan Teknolojiler (Tech Stack)
* **Backend:** Python, Django 5.x
* **Frontend:** HTML5, Tailwind CSS, Vanilla JS
* **Veritabanı:** SQLite (Geliştirme) / PostgreSQL (Canlı Ortam Planı)
* **Performans & Optimizasyon:** Pillow (Görsel Sıkıştırma - WebP), WhiteNoise (Statik Dosya Yönetimi)
* **Güvenlik:** python-dotenv (Çevre Değişkenleri Yönetimi)

## 📂 Proje Yapısı
* `met_code/` : Ana Django konfigürasyonları, `settings.py` ve URL yönlendirmeleri.
* `pages/` : Sayfa görünümleri (views), veritabanı modelleri (models) ve form işleme mantığı.
* `templates/` : Özel 404 ekranı, ana sayfa ve diğer HTML bileşenleri.
* `staticfiles/` : WhiteNoise tarafından derlenmiş ve canlı ortama hazır CSS/JS dosyaları.
* `media/` : Kullanıcı tarafından yüklenen ve Pillow ile optimize edilen dinamik görseller (Git'e dahil edilmez).

## ⚙️ Kurulum ve Çalıştırma (Lokal)
Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

1. Gerekli kütüphaneleri kurun:
   ```bash
   pip install -r requirements.txt