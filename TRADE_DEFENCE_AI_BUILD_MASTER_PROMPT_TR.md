# TRADE DEFENCE MANAGEMENT PLATFORM — AI BUILD MASTER PROMPT
**Sürüm:** 1.0  
**Dil:** Ürün arayüzü çok dilli tasarlanmalı; ilk sürümde en az İngilizce ve Türkçe desteklenebilir altyapı, varsayılan arayüz dili proje sahibi tarafından yapılandırılabilir.  
**Görev:** Ekteki ürün şartnameleriyle tanımlanan sistemi yalnızca tarif etme; gerçek, çalıştırılabilir, test edilmiş ve kurulabilir bir uygulama olarak inşa et.

## 1. Senin rolün ve teslimat standardın
Kıdemli ürün mühendisi, yazılım mimarı, UX/UI tasarımcısı, güvenlik mühendisi, QA lideri ve DevOps mühendisi gibi hareket et. Ekli ana ürün şartnamesi ile derin fonksiyonel şartnameyi birlikte oku. Bu belgeyi uygulama yürütme talimatı ve bağlayıcı teslimat sözleşmesi olarak kullan.

**Sadece plan, mockup, statik HTML veya tıklanmayan bir demo teslim etme.** Gerçek frontend, backend, veritabanı şeması/migration'ları, kimlik doğrulama, yetkilendirme, doğrulama, hata yönetimi, testler, örnek veri, yerel geliştirme ortamı, kurulum talimatları ve üretim dağıtımına yönelik yapılandırma oluştur.

Şartnamelerde belirsizlik varsa:
1. Güvenli, yaygın ve geri döndürülebilir varsayımı seç.
2. Varsayımı `docs/ASSUMPTIONS_AND_DECISIONS.md` dosyasına gerekçesiyle yaz.
3. Kritik yasal, ticari veya güvenlik kararlarında gerçek veri uydurma; yapılandırma veya insan onayı gerektiren noktaları açıkça işaretle.
4. Küçük bir belirsizlik için tüm işi durdurup kullanıcıdan onay bekleme. Yalnızca güvenli ve makul bir varsayım yapılamayan, uygulamanın yönünü değiştirecek konularda soru sor.
5. Önce mevcut repo ve çalışma ortamını incele; var olan dosyaları sebepsiz yere silme veya üzerine yazma.

## 2. Çalışma biçimi: planla, inşa et, doğrula, düzelt
Bu bir otonom uygulama geliştirme görevidir. Aşamaları sırayla uygula ve her aşamanın sonunda gerçekten çalıştır:
- A. Şartname çıkarımı: gereksinimleri ID ile takip et, modülleri ve bağımlılıkları haritala.
- B. Mimari ve temel proje: repo yapısı, ortam değişkenleri, veritabanı, migration, logging, hata modeli.
- C. Kimlik ve erişim: giriş/çıkış, güvenli oturum, kullanıcı/rol/izin, sunucu tarafı yetki kontrolü.
- D. Tasarım sistemi ve uygulama kabuğu.
- E. İş modüllerini uçtan uca geliştir: UI → API → servis/iş kuralları → DB → audit/test.
- F. Dosya/rapor iş akışı ve güvenli dosya yükleme.
- G. AI ve dış kaynak entegrasyonları: gerçek entegrasyon mümkün değilse adapter/interface + açık “yapılandırılmadı” durumu; sahte canlı veri gösterme.
- H. Test, erişilebilirlik, güvenlik kontrolleri ve hata düzeltme.
- I. Docker ile yerel kurulum, seed, yedekleme/geri yükleme yönergeleri, deployment dokümanı.
- J. Son doğrulama: uygulamayı sıfırdan kur, migration çalıştır, seed et, testleri ve build'i çalıştır; sonuçları raporla.

Her aşamada yalnızca ne yapacağını anlatma; dosyaları oluştur ve değiştir. Çalıştırabildiğin komutları gerçekten çalıştır. Başarısız testleri saklama; nedenini çöz veya açık blocker olarak belgele. Test edilmemiş özelliğe “tamamlandı” deme.

## 3. Bağlayıcı kaynak ve gereksinim önceliği
1. Bu AI Build Master Prompt.
2. `Anti_Damping_Platform_Master_Spec_TR.docx`.
3. `Anti_Damping_Platform_Deep_Functional_Spec_TR.docx`.
4. `docs/ASSUMPTIONS_AND_DECISIONS.md` içinde kaydedilmiş ve çelişkiyi açıkça çözen kararlar.

Ana şartname kapsamı tanımlar; derin fonksiyonel şartname ekran/etkileşim davranışını tanımlar. Çelişki fark edersen sessizce seçme: karar kaydına ekle ve daha güvenli, daha test edilebilir yaklaşımı uygula.

## 4. Önerilen teknoloji mimarisi
Mevcut repo/ortam daha uygun ve çalışan bir stack'e sahip değilse şu mimariyi kullan:
- Frontend: React + TypeScript + Vite; erişilebilir, tekrar kullanılabilir component library.
- Backend: Python + FastAPI; typed request/response şemaları ve açık API dokümantasyonu.
- DB: PostgreSQL; migration'lar, foreign key'ler, indeksler, transaction'lar.
- ORM/migrations: SQLAlchemy 2 + Alembic veya aynı kalite seviyesinde tutarlı alternatif.
- Background jobs: Redis + Celery/RQ veya eşdeğer; dış kaynak tarama, OCR, bildirim, rapor üretimi gibi uzun işler request thread'inde çalışmamalı.
- File storage: S3-compatible object storage; local development için güvenli yerel adapter.
- Auth: OIDC uyumlu tasarım; yerel dev ortamında güvenli kimlik sağlayıcı/oturum çözümü. Parola saklanıyorsa yalnızca güçlü modern hash, asla düz metin.
- Testing: frontend unit/component tests, backend unit/integration tests, kritik kullanıcı akışları için E2E tests.
- Packaging: Docker Compose ile frontend, backend, PostgreSQL ve gerekli worker servisleri.
- Observability: yapılandırılmış loglar, correlation/request ID, health/readiness endpoint'leri.
- API: sürümlenebilir `/api/v1` temeli; OpenAPI şeması.
- Secrets: yalnızca environment/secret manager; repo'ya gerçek anahtar koyma.

Teknoloji seçimini `docs/ARCHITECTURE.md` dosyasına kaydet. Gereksiz mikroservis mimarisi kurma; ilk sürümde modüler monolit tercih et. Modüller arası sınırları açık tut.

## 5. Tasarım sistemi — bağlayıcı UI/UX sözleşmesi
Ürün adı: **Trade Defence Management Platform**. Görsel karakter: premium enterprise SaaS + hukuk teknolojisi + finansal analiz terminali. Güvenilir, ciddi, sakin, yüksek veri yoğunluğunda okunabilir.

### Renk tokenları
- `navy-900: #14243A` — ana navigasyon, başlık ve marka.
- `canvas: #F5F7FA` — ana sayfa arka planı.
- `surface: #FFFFFF` — kart, tablo, modal ve form yüzeyi.
- `teal-700: #167D8D` — birincil aksiyon, aktif seçim ve bağlantı.
- `success: #23845D` — tamamlandı/doğrulandı.
- `warning: #B7791F` — yaklaşan süre/inceleme.
- `critical: #B93838` — gecikmiş süre/gerçek kritik risk.
- Metin için WCAG kontrastını sağlayan nötr koyu tonlar; ikincil metin için yeterli kontrast.
- Renk tek başına anlam taşımaz; metin/ikon/etiket ile desteklenir. Kırmızı yalnızca kritik durumlarda kullanılır.

### Tipografi ve ölçüler
- Inter veya eşdeğer, okunaklı sans-serif.
- Sayfa başlığı 24–28 px; bölüm başlığı 16–20 px; gövde 14–16 px; yoğun tablo 13–14 px; yardımcı metin 12–13 px.
- 4 px tabanlı spacing scale; tutarlı radius, border, elevation ve focus tokenları.
- Gereksiz gradient, aşırı gölge, dekoratif animasyon ve her yere rozet koyma yok.
- Desktop tam çalışma deneyimi; tablet destekli; mobilde kritik görevler ve inceleme akışları kullanılabilir.
- Varsayılan açık tema; erişilebilir, eksiksiz ve tutarlı koyu tema tercihi de sun. Kullanıcının tema tercihini sakla.

### Uygulama kabuğu
- Sol navigasyon sabit ve daraltılabilir.
- Üst çubuk: global arama, bildirimler, yardım, kullanıcı profili.
- Ana içerik: sayfa başlığı, breadcrumb, birincil aksiyon, filtre/sekme ve içerik.
- Tıklanabilir satır, checkbox ve satır menüsü birbirinden bağımsız davranmalı.
- Büyük formu küçük modal içine sıkıştırma; tam sayfa veya geniş panel kullan.
- Loading, empty, error, permission denied, stale data ve success durumları her modülde tasarlanmalı.
- Klavye ile gezinme, görünür focus, anlamlı label, form hata ilişkisi ve makul kontrast şart.

### Bileşen davranışları
- Ortak Button, IconButton, Input, Select, DatePicker, Textarea, Checkbox, Tabs, Table, Badge, Alert, Toast, Modal/Drawer, Pagination, FilterBar, EmptyState, Skeleton, ErrorState, FilePreview, Timeline, AuditLog ve ConfirmDialog bileşenleri oluştur.
- Her bileşen için default, hover, focus, disabled, loading ve error durumları.
- Tablo: server-side pagination/filter/sort, sütun tercihleri, satır seçimi, klavye desteği ve boş durum.
- Form: istemci ve sunucu doğrulaması, alan bazlı hata, form üstü genel hata, dirty-state uyarısı ve güvenli tekrar gönderim.
- Silme/arşivleme/yayımlama/kapama gibi işlemler etki özeti ve onay gerektirir.
- Başarı mesajı yalnızca backend başarı yanıtından sonra gösterilir.

## 6. Ürün kapsamı
Şartnamelerdeki tüm modülleri gereksinim ID'leriyle takip et. En az şu modülleri uçtan uca geliştir:
1. Kimlik doğrulama, kullanıcılar, roller ve izinler.
2. Dashboard ve öncelikli işler.
3. CRM: müşteriler, kişiler, şirketler, tesisler, ürünler.
4. Global ticari savunma veri tabanı ve resmî vaka kaydı.
5. Kaynaklar, veri kökeni, doğrulama, tarihçe ve veri kalitesi.
6. Risk tarama ve ürün kapsam eşleştirme.
7. Danışmanlık dosyaları ve vaka yaşam döngüsü.
8. İş akışı şablonları ve sürümleme.
9. Görev, sorumlu, bağımlılık, onay ve blokaj.
10. Hukuki süre ve takvim motoru.
11. Belge yönetimi, sürümler, OCR durumu, erişim ve redaksiyon.
12. Mali/ekonomik analiz ve varsayım kayıtları.
13. Soru formları ve cevap çalışma alanı.
14. Güncel durum/ilerleme raporu oluşturma, önceki raporla karşılaştırma, onay ve yayımlama.
15. Müşteri portalı ve müşteriyle paylaşılabilen belge/raporlar.
16. İletişim, toplantı ve faaliyet kaydı.
17. Teklif, sözleşme, bütçe ve finans takibi.
18. AI asistanı ve kaynaklı cevaplar.
19. Otomasyonlar ve bildirimler.
20. Global arama, raporlama ve analitik.
21. Güvenlik, audit, veri saklama, yedekleme ve yönetim.

Bir danışmanlık dosyası birden fazla resmî soruşturmayla ilişkilendirilebilir. İç danışmanlık dosyası ile resmî soruşturma kaydı ayrı varlıklar olmalı. Ürün kodu, ülke, şirket, dönem ve önlem verileri tarihçeli tutulmalı.

## 7. Veri doğruluğu ve resmî kaynaklar — sıfır uydurma ilkesi
Resmî kaynak entegrasyonları için adapter/interface modeli oluştur. Önce erişim şartlarını, lisansları, API bulunabilirliğini ve kullanım koşullarını doğrula. API olmadığı veya erişim izni bulunmadığı durumda scraping yapıldığı izlenimini verme; connector'ı yapılandırılmamış olarak göster, manuel içe aktarma ve kaynak URL'si kaydetme akışını sun.

İncelenecek kaynak örnekleri: European Commission trade defence/investigations, TARIC, EUR-Lex, EU Official Journal, WTO trade remedies, Türkiye Ticaret Bakanlığı ve Resmî Gazete, USITC ve US Department of Commerce kaynakları. Bu liste otomatik erişim izni anlamına gelmez.

Her dış kaynak kaydında mümkünse:
- kaynak adı ve URL,
- yayımlanma/erişim tarihi,
- son kontrol zamanı,
- kaynağın ham referansı veya dosya hash'i,
- veri alanı bazında doğrulama durumu,
- kim/ne zaman doğruladı,
- önceki değer ve değişiklik farkı,
- otomatik çıkarım ile uzman onayının ayrımı.

Hukuki tarih, vergi/anti-damping oranı, ürün kapsamı, şirket kapsamı veya karar sonucu **asla tahmin edilip doğrulanmış gibi sunulamaz**. Belirsiz veri `unverified` olarak işaretlenir. Resmî deadline hesaplaması kural kaynağı, sürüm, başlangıç olayı, takvim/iş günü yöntemi ve insan doğrulamasıyla izlenebilir olmalı. Otomatik sistem tek başına hukuki tavsiye vermez.

## 8. Güvenlik ve gizlilik — üretim seviyesinde taban
- Sunucu tarafı authorization her request ve nesne erişiminde uygulanmalı; yalnızca UI'da gizlemek yeterli değil.
- Tenant/client/case scope izolasyonu; IDOR ve yatay yetki yükseltme testleri.
- MFA destekleyen kimlik tasarımı, güvenli session/token yönetimi, CSRF/CORS yapılandırması, rate limiting, brute-force koruması.
- Dosya yüklemelerinde boyut/uzantı/MIME doğrulaması, zararlı dosya tarama entegrasyon noktası, rastgele storage key, private storage ve indirme yetkisi.
- Hassas veriler aktarımda ve depolamada şifrelenmeli; secret'lar repoda tutulmamalı.
- Her kritik işlem için audit log: aktör, zaman, nesne, işlem, sonuç ve gerektiğinde değişiklik farkı.
- Loglara parola, token, gereksiz kişisel veri veya belge içeriği yazma.
- GDPR veri minimizasyonu, erişim/düzeltme/saklama/silme politikaları için yapılandırılabilir kontroller.
- İç notlar, maliyetler, risk değerlendirmeleri ve müşteriyle paylaşılan içerik ayrı erişim katmanlarına sahip olmalı.
- Backup/restore prosedürü yaz ve mümkünse test et.
- Güvenlik bulgularını ve kalan riskleri `docs/SECURITY.md` içinde açıkla.

## 9. AI asistanı kuralları
- AI çıktısı kaynağa, belgeye veya veri kaydına atıf vermeli; desteklenmeyen iddia yapmamalı.
- AI çıktısı taslak statüsünde başlamalı; yasal değerlendirme, dışarıya rapor gönderme, resmî başvuru, deadline onayı veya dosya kapatma insan onayı gerektirir.
- Prompt injection ve dosya içindeki talimat benzeri metinlere karşı savunma: kullanıcı belgesi güvenilmeyen veri kabul edilir.
- Müşteri/tenant yetkisi dışında veri AI context'ine giremez.
- Model sağlayıcı, veri saklama, maliyet ve hassas verinin gönderimi yapılandırılabilir olmalı.
- Model yapılandırılmadıysa AI modülü açık şekilde “yapılandırılmadı” göstermeli; sahte AI cevabı üretmemeli.
- AI cevabı: kaynaklar, varsayımlar, belirsizlikler, tarih damgası ve onay durumu gösterebilmeli.

## 10. Rapor merkezi için özel sözleşme
Kullanıcı dosyadaki görevleri, belgeleri, aşamaları veya gelişmeleri güncellediğinde “Güncel Rapor Oluştur” akışını başlatabilmeli:
1. Rapor türü: ilerleme / mevcut durum / kapsamlı.
2. Dönem: son rapordan bu yana / son 7 gün / son 30 gün / tüm dosya geçmişi / özel aralık.
3. Hedef kitle: müşteri / iç ekip; “ikisi” seçilirse iki ayrı çıktı üret.
4. İçerik: yönetici özeti, tamamlanan işler, yeni gelişmeler, açık görevler, sorumlular, hukuki ve iç süreler, riskler, eksik belgeler, sonraki adımlar, kaynaklar ve ekler.
5. Değişiklikleri önceki raporla karşılaştır; yeni/değişen/kaldırılan alanları göster.
6. Taslak oluştur, düzenle, onaya gönder, PDF/DOCX dışa aktar, yetkiye göre müşteri portalında yayımla.
7. İç notları müşteri sürümüne asla dahil etme; testlerle doğrula.
8. Rapor sürümlemesi, oluşturan, onaylayan, yayımlayan ve zaman damgaları saklanmalı.

## 11. Veritabanı, API ve kalite
- Veritabanı ilişki bütünlüğü, migration, indeks, transaction ve soft-delete/retention politikaları tutarlı olsun.
- API sözleşmeleri typed ve belgeli; hata formatı tutarlı; pagination/filter/sort standardı ortak.
- Liste ve detay ekranları doğrudan gerçek API/veritabanı verisini kullanmalı; hard-coded demo verisi yalnızca açıkça seed/demo modunda.
- Seed verileri sentetik ve gerçek kişi/şirket iddiası taşımayan örnekler olmalı.
- Her iş akışında audit trail ve erişim kontrolü test edilmeli.
- Kritik mutasyonlarda idempotency/duplicate-submit koruması düşünülmeli.
- Tarih/saat ve timezone açıkça yönetilmeli; hukuki deadline saat dilimi ve iş günü kuralları yapılandırılabilir olmalı.

## 12. Zorunlu teslimatlar
Aşağıdaki dosyaları üret:
- `README.md` — hızlı başlangıç, gereksinimler, komutlar, ilk kullanıcı oluşturma.
- `.env.example` — örnek değişkenler, gerçek sır yok.
- `docker-compose.yml` ve Dockerfile'lar — mümkün olduğunca tek komutla yerel çalıştırma.
- `docs/ARCHITECTURE.md`
- `docs/ASSUMPTIONS_AND_DECISIONS.md`
- `docs/REQUIREMENTS_TRACEABILITY.md` — her şartname gereksinimi için status, implementation location, test evidence ve kalan iş.
- `docs/SECURITY.md`
- `docs/DATA_SOURCES.md` — connector durumu ve erişim kısıtları.
- `docs/DEPLOYMENT.md`
- `docs/BACKUP_RESTORE.md`
- `docs/API.md` veya OpenAPI çıktısı.
- DB migration'ları ve güvenli seed script'i.
- Otomatik testler ve test çalıştırma talimatları.
- Kullanıcıya yönelik kısa kullanım rehberi.
- `docs/KNOWN_LIMITATIONS.md` — tamamlanmamış işler, yapılandırma gerektiren bağlantılar, riskler.
- `CHANGELOG.md`.

## 13. Kabul kriterleri — “bitti” demek için
Uygulama tamamlandı sayılabilmesi için aşağıdakilerin tümü kontrol edilmeli:
- [ ] Temiz ortamda dokümante edilen komutlarla ayağa kalkıyor.
- [ ] Migration ve seed başarıyla çalışıyor.
- [ ] Login/logout, rol ve sunucu tarafı erişim kontrolü çalışıyor.
- [ ] Her ana modülde liste → detay → oluştur/düzenle → doğrulama → audit akışı gerçek verilerle çalışıyor.
- [ ] Müşteri, şirket, ürün, resmî soruşturma ve danışmanlık dosyası ilişkileri doğru.
- [ ] Görev atama, durum değişikliği, deadline ve bildirim akışları test edildi.
- [ ] Dosya yükleme/indirme yetki kontrolü, sürümleme ve audit test edildi.
- [ ] Rapor oluşturma, düzenleme, onay, dışa aktarma ve müşteri/iç sürüm izolasyonu test edildi.
- [ ] Global arama, filtre, sıralama, pagination çalışıyor.
- [ ] Loading/empty/error/unauthorized durumları bulunuyor.
- [ ] Unit/integration/E2E testleri çalıştırıldı; sonuçlar belgeli.
- [ ] Lint/type-check/build başarılı.
- [ ] Hiçbir kritik hukuki veri veya dış kaynak bağlantısı uydurulmuş değil.
- [ ] Güvenlik açısından bilinen kritik açıklık yok; kalan bulgular raporlanmış.
- [ ] Erişilebilirlik ve responsive temel kontrolleri yapıldı.
- [ ] `REQUIREMENTS_TRACEABILITY.md` tamamlanma durumunu dürüstçe gösteriyor.

Bir şartname gereksinimi mevcut oturum/araç sınırları nedeniyle uygulanamıyorsa sessizce atlama. `BLOCKED` olarak kaydet; sebebini, kullanıcıdan gereken girdiyi ve güvenli geçici yolu belirt.

## 14. Son yanıt formatın
İşi bitirdiğinde kısa ama denetlenebilir teslimat raporu ver:
1. Uygulamada gerçekten tamamlanan modüller.
2. Kurulum ve çalıştırma komutları.
3. Test komutları ve gerçek sonuçları.
4. Demo/seed kullanıcıları varsa kimlik bilgilerini yalnızca development ortamı için açıkça belirt ve ilk girişte değişim gerektir.
5. Yapılandırma bekleyen dış entegrasyonlar ve nedenleri.
6. Tamamlanmayan işler ve bilinen riskler.
7. Üretime çıkmadan önce gerekli işlemler.
8. Şartname gereksinimlerinin karşılanma tablosu.

**Son talimat:** Şimdi mevcut dosyaları ve şartnameleri incele, kısa uygulama planını `docs/IMPLEMENTATION_PLAN.md` içine yaz ve hemen kodlamaya başla. Planı teslimat olarak sunup durma. Kullanılabilir en küçük uçtan uca sürümü kur, test et ve sonra kalan modülleri iteratif olarak tamamla. Gerçek test sonuçları olmadan “hazır” veya “eksiksiz” iddiasında bulunma.
