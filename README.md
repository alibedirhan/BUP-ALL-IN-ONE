# 🐓 Bupiliç Yönetim Sistemi (BUP-ALL-IN-ONE)

<div align="center">

![Version](https://img.shields.io/github/v/release/alibedirhan/BUP-ALL-IN-ONE?style=for-the-badge)
![Downloads](https://img.shields.io/github/downloads/alibedirhan/BUP-ALL-IN-ONE/total?style=for-the-badge)
![License](https://img.shields.io/github/license/alibedirhan/BUP-ALL-IN-ONE?style=for-the-badge)
![Last Commit](https://img.shields.io/github/last-commit/alibedirhan/BUP-ALL-IN-ONE?style=for-the-badge)

**Tavukçuluk sektörü için geliştirilmiş kapsamlı işletme yönetim sistemi**

[📥 Son Sürümü İndir](https://github.com/alibedirhan/BUP-ALL-IN-ONE/releases/latest/download/Bupilic_Yonetim_Sistemi.exe) • [📖 Dokümantasyon](#kullanım-kılavuzu) • [🐛 Hata Bildirimi](https://github.com/alibedirhan/BUP-ALL-IN-ONE/issues) • [💬 Destek](#destek)

</div>

---

## 🎯 Proje Hakkında

Bupiliç Yönetim Sistemi, tavukçuluk sektöründeki işletmelerin karmaşık süreçlerini kolaylaştırmak ve verimliliği artırmak için geliştirilmiş modern bir yönetim uygulamasıdır. Küçük ölçekli çiftliklerden büyük endüstriyel tesislere kadar her büyüklükteki işletmeye hitap eden kapsamlı çözümler sunar.

### ✨ Temel Özellikler

| 🔧 Özellik | 📝 Açıklama |
|-----------|-------------|
| 💰 **İskonto Hesaplama** | Otomatik iskonto hesaplamaları ve fiyatlandırma yönetimi |
| 📊 **Karlılık Analizi** | Detaylı maliyet analizi ve kar-zarar raporları |
| 🔍 **Müşteri Kayıp/Kaçak Takibi** | Müşteri davranış analizi ve kayıp önleme sistemleri |
| 📈 **Yaşlandırma Raporları** | Alacak yaşlandırma ve risk değerlendirme raporları |
| 🛡️ **Güvenli Erişim** | Şifre korumalı kullanıcı yönetimi |
| 🎨 **Modern Arayüz** | Kullanıcı dostu ve sezgisel tasarım |

---

## 🚀 Hızlı Başlangıç

### 📋 Sistem Gereksinimleri

- **İşletim Sistemi:** Windows 10 veya üzeri
- **Framework:** .NET Framework 4.7.2 veya üzeri
- **RAM:** Minimum 4 GB (8 GB önerilir)
- **Depolama:** 500 MB boş alan
- **Ekran Çözünürlüğü:** Minimum 1024x768

### 📥 Kurulum

#### Yöntem 1: Hızlı Kurulum (Önerilen)

1. **Doğrudan İndir**: [Bupiliç_Yonetim_Sistemi.exe](https://github.com/alibedirhan/BUP-ALL-IN-ONE/releases/latest/download/Bupilic_Yonetim_Sistemi.exe)
2. **Çalıştır**: İndirilen dosyayı çift tıklayın
3. **Giriş**: Varsayılan şifre ile sisteme girin

#### Yöntem 2: GitHub Releases

1. [Releases](https://github.com/alibedirhan/BUP-ALL-IN-ONE/releases) sayfasına gidin
2. En son sürümü seçin
3. `.exe` dosyasını indirin ve çalıştırın

### 🔐 İlk Giriş

```
Varsayılan Şifre: cal93
```

> ⚠️ **Güvenlik Uyarısı**: İlk girişten sonra şifrenizi değiştirmeniz önerilir.

---

## 📚 Kullanım Kılavuzu

### 🏠 Ana Ekran

Ana ekran, tüm modüllere hızlı erişim sağlayan merkezi kontrol panelidir. Buradan:

- Günlük raporları görüntüleyebilirsiniz
- Hızlı işlemler yapabilirsiniz
- Sistem durumunu takip edebilirsiniz

### 💰 İskonto Yönetimi

**İskonto Hesaplama Modülü** ile:

1. **Otomatik Hesaplamalar**: Müşteri kategorisine göre otomatik iskonto uygulama
2. **Esnek Oranlar**: Ürün bazlı veya genel iskonto tanımlama
3. **Tarihsel Takip**: Geçmiş iskonto uygulamalarını görüntüleme

### 📊 Karlılık Analizi

**Analiz Modülü** özellikleri:

- **Maliyet Takibi**: Detaylı maliyet kırılımları
- **Kar Marjı Hesaplama**: Ürün ve kategori bazlı karlılık
- **Trend Analizi**: Zaman içindeki karlılık değişimleri
- **Görsel Raporlar**: Grafikler ve çizelgeler

### 🔍 Müşteri Takip Sistemi

**Kayıp/Kaçak Takip Modülü**:

- Müşteri satın alma desenlerini analiz eder
- Risk altındaki müşterileri önceden tespit eder
- Müşteri sadakat programları önerir
- Otomatik uyarı sistemi

### 📈 Yaşlandırma Raporları

**Yaşlandırma Analizi**:

- 0-30, 31-60, 61-90, 90+ gün kategorileri
- Müşteri bazlı risk değerlendirmesi
- Tahsilat öncelik sıralaması
- Excel export özelliği

---

## 🛠️ Geliştiriciler İçin

### 🏗️ Proje Yapısı

```
BUP-ALL-IN-ONE/
├── src/
│   ├── Core/                 # Ana uygulama mantığı
│   ├── UI/                   # Kullanıcı arayüzü
│   ├── Data/                 # Veri erişim katmanı
│   ├── Services/             # İş mantığı servisleri
│   └── Utils/                # Yardımcı sınıflar
├── Resources/                # Kaynaklar ve görseller
├── Documentation/            # Proje dokümantasyonu
└── Tests/                    # Test dosyaları
```

### 🔨 Geliştirme Ortamı Kurulumu

1. **Gereksinimler**:
   ```
   - Visual Studio 2019 veya üzeri
   - .NET Framework 4.7.2 SDK
   - SQL Server LocalDB (isteğe bağlı)
   ```

2. **Proje Klonlama**:
   ```bash
   git clone https://github.com/alibedirhan/BUP-ALL-IN-ONE.git
   cd BUP-ALL-IN-ONE
   ```

3. **Build ve Çalıştırma**:
   ```bash
   dotnet restore
   dotnet build
   dotnet run
   ```

### 🧪 Test Etme

```bash
# Unit testleri çalıştır
dotnet test

# Test coverage raporu
dotnet test --collect:"XPlat Code Coverage"
```

---

## 📈 Sürüm Geçmişi

| Sürüm | Tarih | Önemli Değişiklikler |
|-------|-------|---------------------|
| v2.1.0 | 2024-09 | Yaşlandırma raporları eklendi |
| v2.0.0 | 2024-08 | UI yenilendi, performans iyileştirmeleri |
| v1.5.0 | 2024-07 | Müşteri takip sistemi |
| v1.0.0 | 2024-06 | İlk stabil sürüm |

Detaylı değişiklik listesi için [CHANGELOG.md](CHANGELOG.md) dosyasını inceleyin.

---

## 🤝 Katkıda Bulunma

Projeye katkıda bulunmaktan memnuniyet duyarız! 

### 🐛 Hata Bildirimi

Hata bulduğunuzda:

1. [Issues](https://github.com/alibedirhan/BUP-ALL-IN-ONE/issues) sayfasını kontrol edin
2. Benzer bir hata yoksa yeni issue açın
3. Aşağıdaki bilgileri ekleyin:
   - Hatanın detaylı açıklaması
   - Adım adım tekrar etme yöntemi
   - Ekran görüntüleri (varsa)
   - Sistem bilgileri

### 💡 Özellik Önerisi

Yeni özellik önerileri için:

1. [Issues](https://github.com/alibedirhan/BUP-ALL-IN-ONE/issues) sayfasında "Feature Request" etiketi ile açın
2. Özelliğin detaylı açıklamasını yapın
3. Use case'leri belirtin

---

## 📞 Destek

### 🆘 Teknik Destek

- **Issues**: [GitHub Issues](https://github.com/alibedirhan/BUP-ALL-IN-ONE/issues)
- **Wiki**: [Proje Wiki](https://github.com/alibedirhan/BUP-ALL-IN-ONE/wiki)
- **Email**: Teknik sorular için issue açmanızı öneririz

### 📖 Dokümantasyon

- [Kullanıcı Kılavuzu](docs/user-guide.md)
- [API Dokümantasyonu](docs/api.md)
- [Geliştirici Rehberi](docs/developer-guide.md)

### ❓ Sık Sorulan Sorular

<details>
<summary><strong>Program açılmıyor, ne yapmalıyım?</strong></summary>

1. .NET Framework 4.7.2 veya üzerinin yüklü olduğunu kontrol edin
2. Windows Update'i çalıştırın
3. Antivirus yazılımınızı geçici olarak devre dışı bırakın
4. Yönetici olarak çalıştırmayı deneyin

</details>

<details>
<summary><strong>Şifremi unuttumsam ne yapmalıyım?</strong></summary>

Varsayılan şifre: `bupilic2024`
Eğer değiştirdiyseniz, veri klasöründeki config dosyasını silebilir veya teknik destek ile iletişime geçebilirsiniz.

</details>

<details>
<summary><strong>Verileri nasıl yedeklerim?</strong></summary>

Program klasöründeki `Data` klasörünü düzenli olarak yedekleyin. Gelecek sürümlerde otomatik yedekleme özelliği eklenecektir.

</details>

---

## 🏆 Teşekkürler

Bu projeyi kullandığınız ve desteklediğiniz için teşekkür ederiz! 

### 🌟 Özel Teşekkürler

- Tüm beta test kullanıcılarımıza
- Geri bildirimde bulunan sektör uzmanlarına
- Açık kaynak topluluğuna

---

## 📄 Lisans

Bu proje [MIT License](LICENSE) altında lisanslanmıştır. Detaylar için lisans dosyasını inceleyebilirsiniz.

---

## 📊 İstatistikler

![GitHub stats](https://github-readme-stats.vercel.app/api?username=alibedirhan&show_icons=true&theme=vue)

---

<div align="center">

**⭐ Beğendiyseniz yıldız vermeyi unutmayın! ⭐**

Geliştirici: [Ali Bedirhan](https://github.com/alibedirhan)

📧 İletişim: [GitHub Profile](https://github.com/alibedirhan)

---

*Son güncelleme: Aralık 2024*

</div>
