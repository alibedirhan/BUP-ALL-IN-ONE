🏢 BupiliÇ İşletme Yönetim Sistemi
Show Image
Show Image
Show Image
Show Image
Modern ve kullanıcı dostu işletme yönetim sistemi. CustomTkinter tabanlı arayüz ile İskonto Hesaplama, Karlılık Analizi, Müşteri Kayıp/Kaçak ve Yaşlandırma modüllerini içerir.
✨ Özellikler
🔥 Ana Modüller

💰 İskonto Hesaplama: Otomatik iskonto hesaplamaları ve raporlama
📈 Karlılık Analizi: Şube bazlı karlılık analizleri ve grafikler
👥 Müşteri Kayıp/Kaçak: Müşteri hareketleri takibi ve analizi
📊 Yaşlandırma: Detaylı yaşlandırma raporları ve visualizasyonlar

🎨 Kullanıcı Arayüzü

✅ Modern CustomTkinter tasarımı
✅ Light/Dark tema desteği
✅ Türkçe tam destek
✅ Responsive tasarım
✅ Kullanıcı dostu navigasyon

🔧 Teknik

Python 3.10 desteği
CustomTkinter 5.2.2 entegrasyonu
PyInstaller ile tek dosya executable
UPX sıkıştırması ile optimizasyon
GitHub Actions otomatik build sistemi
Comprehensive error handling
Modüler kod yapısı
Cross-module communication
Automatic dependency management

🏗️ Infrastructure

GitHub Actions CI/CD pipeline
Otomatik versiyonlama sistemi
Multi-architecture builds (x64, x86)
Automated testing
Release management
Artifact compression ve distribution

[0.9.0] - 2024-12-XX (Beta)
✨ Yeni Özellikler

Beta sürüm ana framework'ü
Temel modül yapıları
İlk GUI tasarımı

🐛 Düzeltilen Hatalar

İlk beta sürümü - known issues var

🔧 Teknik

İlk PyInstaller konfigürasyonu
Temel build sistemi

[0.1.0] - 2024-11-XX (Alpha)
✨ Yeni Özellikler

İlk prototip sürümü
Temel modül yapısı
Konsept proof

📝 Notlar

İlk geliştirme sürümü
Sadece geliştirici testleri için


🏷️ Tag Format
Bu projede aşağıdaki tag formatı kullanılır:
vMAJOR.MINOR.PATCH[-PRERELEASE]

Örnekler:
- v1.0.0        (Stable release)
- v1.1.0        (Minor update)
- v1.0.1        (Bug fix)
- v2.0.0-beta.1 (Beta release)
- v1.2.0-rc.1   (Release candidate)
📊 Release Types
Major Release (v1.0.0 → v2.0.0)

Breaking changes
Büyük yeni özellikler
Architecture değişiklikleri
API değişiklikleri

Minor Release (v1.0.0 → v1.1.0)

Yeni özellikler (backward compatible)
Performance iyileştirmeleri
Yeni modüller

Patch Release (v1.0.0 → v1.0.1)

Bug fixes
Security patches
Küçük iyileştirmeler
Documentation updates

Pre-release

Alpha: İlk geliştirme sürümleri
Beta: Feature-complete ama test aşamasında
RC (Release Candidate): Son test aşaması

🔄 Release Process

Development: develop branch'de geliştirme
Feature Freeze: Yeni özellikler durdurulur
Testing: Comprehensive testing
Release Branch: release/vX.X.X branch oluşturulur
Final Testing: Son testler
Tag: Version tag'i oluşturulur
Build: GitHub Actions otomatik build
Release: GitHub Releases'da yayınlanır
Merge: main branch'e merge edilir

📈 Version History
VersionRelease DateDownloadsNotable Featuresv1.0.02025-01-XX-İlk stable releasev0.9.02024-12-XX-Beta releasev0.1.02024-11-XX-Initial alpha

📅 Son güncelleme: Bu CHANGELOG otomatik olarak her release'de güncellenir. Özellikler

✅ Python 3.10+ desteği
✅ Portable tek dosya (kurulum gerektirmez)
✅ Windows 7/8/10/11 uyumluluğu
✅ Excel dosyaları desteği
✅ PDF export özelliği
✅ Loglama ve hata takibi

🚀 Hızlı Başlangıç
📥 İndirme (Tavsiye Edilen)

Releases sayfasından en son sürümü indirin
BupiliC-vX.X.X-windows-x64.exe dosyasını çalıştırın
Varsayılan şifre: bupilic2024

💻 Kaynak Koddan Çalıştırma
bash# Repository'yi klonlayın
git clone https://github.com/alibedirhan/BUP-ALL-IN-ONE.git
cd BUP-ALL-IN-ONE

# Virtual environment oluşturun (tavsiye edilir)
python -m venv venv
venv\Scripts\activate  # Windows

# Gereksinimler yükleyin
pip install -r requirements.txt

# Uygulamayı başlatın
python bupilic_ana_program.py
🛠️ Geliştirici Kılavuzu
📋 Gereksinimler

Python 3.10 veya üzeri
Windows 7/8/10/11
4GB RAM (minimum)
500MB disk alanı

🔨 Local Build
bash# Build ortamını hazırlayın
scripts\setup_env.bat

# Test build'i çalıştırın
scripts\test_build.bat

# Release build'i oluşturun
python build\build.py --version v1.0.0
🚀 GitHub Actions ile Otomatik Build
Repository'ye tag push ettiğinizde otomatik build başlar:
bashgit tag v1.0.0
git push origin v1.0.0
Build sonrası otomatik olarak:

Windows x64/x86 executable'ları oluşturulur
UPX ile sıkıştırılır
GitHub Releases'da yayınlanır

📁 Proje Yapısı
BUP-ALL-IN-ONE/
├── .github/workflows/          # GitHub Actions
├── build/                      # Build scripts & configs
├── scripts/                    # Helper scripts
├── bupilic_ana_program.py      # Ana program
├── ISKONTO_HESABI/            # İskonto modülü
├── KARLILIK_ANALIZI/          # Karlılık modülü
├── MUSTERI_SAYISI_KONTROLU/   # Müşteri modülü
├── YASLANDIRMA/               # Yaşlandırma modülü
├── icon/                      # Uygulama ikonları
├── requirements.txt           # Python gereksinimleri
└── README.md                  # Bu dosya
🔧 Konfigürasyon
👤 Kullanıcı Ayarları

Şifre değiştirme: Ayarlar menüsünden
Tema seçimi: Header'daki tema butonundan
Kullanıcı bilgileri: JSON formatında config/user_settings.json'da saklanır

📊 Modül Ayarları
Her modül kendi konfigürasyon dosyalarını yönetir:

data/input/: Giriş dosyaları
data/output/: Çıktı dosyaları
logs/: Log dosyaları
config/: Konfigürasyon dosyaları

🚨 Sorun Giderme
❓ Sık Karşılaşılan Sorunlar
Q: Antivirus uyarı veriyor
A: Bu normaldir. PyInstaller ile oluşturulan exe dosyaları bazı antivirus programları tarafından false positive olarak algılanabilir.
Q: Program yavaş açılıyor
A: İlk açılış biraz yavaş olabilir (özellikle Windows Defender taraması). Sonraki açılışlar daha hızlı olacaktır.
Q: Excel dosyası açılmıyor
A: Excel dosyanızın doğru formatta olduğundan ve başka bir program tarafından kullanılmadığından emin olun.
Q: Şifremi unuttum
A: config/user_settings.json dosyasını silin. Varsayılan şifre bupilic2024 olarak sıfırlanacak.
📝 Log Dosyaları
Sorunları tespit etmek için log dosyalarını kontrol edin:

logs/app_YYYYMMDD_HHMMSS.log

🤝 Katkıda Bulunma

Fork edin
Feature branch oluşturun (git checkout -b feature/amazing-feature)
Commit edin (git commit -m 'Add amazing feature')
Push edin (git push origin feature/amazing-feature)
Pull Request oluşturun

📄 Lisans
Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için LICENSE dosyasına bakın.
📞 Destek

🐛 Bug Reports: GitHub Issues
💡 Feature Requests: GitHub Discussions
📧 Email: alibedirhan@example.com

🏆 Teşekkürler

CustomTkinter - Modern UI framework
PyInstaller - Executable packaging
Pandas - Data processing
Matplotlib - Data visualization


⭐ Bu projeyi beğendiyseniz star vermeyi unutmayın!
