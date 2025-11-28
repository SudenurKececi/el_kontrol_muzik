## • Proje adı

El Hareketleri ile Kontrol Edilebilen Müzik Çalar Uygulaması

## • Projenin amacı

Bu projenin amacı, bilgisayar kamerası ve yapay zeka tabanlı el takibi kullanarak müzik çaları dokunmadan, sadece el hareketleriyle kontrol edebilmektir.
Kullanıcı sağ ve sol el parmaklarını kullanarak sesi artırıp azaltabilir, sonraki veya önceki şarkıya geçebilir.

## • Kullanılan teknolojiler

Python: Projenin geliştirildiği programlama dili.

OpenCV: Kameradan görüntü almak ve görüntü üzerinde çizim yapmak için kullanılan kütüphane.

MediaPipe Hands: Google tarafından geliştirilmiş, eldeki 21 ana noktayı (landmark) tespit eden hazır model. Bu sayede kendimiz model eğitmek zorunda kalmıyoruz.

pyautogui: Klavye ve medya tuşlarını yazılımdan kontrol etmek için kullanılıyor (volume up/down, next/prev track).

## • Çalışma prensibi

Kameradan görüntü alınır.
OpenCV ile sürekli olarak webcam’den frame (görüntü) okunur.

MediaPipe ile el tespiti yapılır.
Her kare, MediaPipe Hands modeline gönderilir. Model:

El(ler)in konumunu,

Her el için 21 adet landmark (eklem noktası),

Ve elin sağ mı sol mu olduğunu (Right / Left) verir.

Parmak durumu hesaplanır.
Landmark koordinatları kullanılarak:

İşaret parmağı ucu (8) ile alt boğum (6) karşılaştırılır. Uç daha yukarıdaysa → işaret parmağı havada (True) kabul edilir.

Başparmak ucu (4) ile alt boğum (2) karşılaştırılır. Sağ elde başparmak sağ tarafa doğru açıldığında, sol elde sol tarafa doğru açıldığında → başparmak havada (True) kabul edilir.

Jest → Komut eşleştirme yapılır.

### - Kurallar:

• Sağ el işaret parmağı havada → SES ARTTIR

• Sağ el baş parmak havada → SES AZALT

• Sol el işaret parmağı havada → SONRAKI ŞARKI

• Sol el baş parmak havada → ÖNCEKİ ŞARKI

Kodda bu mantık finger_states fonksiyonu ile parmak durumu hesabı,
trigger_action fonksiyonu ile jestin gerçek komuta dönüştürülmesi şeklinde uygulanmıştır.

pyautogui ile işletim sistemine komut gönderilir.
pyautogui.press("volumeup"), pyautogui.press("nexttrack") gibi fonksiyonlarla işletim sisteminin medya tuşları tetiklenir.
Böylece arka planda çalışan müzik çalar uygulaması (Spotify vb.) jestlere göre kontrol edilir.

Görsel geri bildirim verilir (ayna modu).

El üzerindeki landmark noktaları ve iskelet yapısı ekranda gösterilir.

Son yapılan komut (“SES ARTTIR”, “SONRAKI SARKI” vb.) ekranda kısa süre kırmızı yazıyla gösterilir.

Kameradan gelen görüntü cv2.flip(..., 1) ile yatay çevrilerek ayna görüntüsü elde edilir. Böylece kullanıcı kendini aynaya bakar gibi görür.

## • Avantajlar ve sınırlamalar

### - Avantajlar:

Dokunmadan kontrol → özellikle eller meşgulken veya uzaktan kullanımda pratik.

Hazır modeller (MediaPipe) sayesinde yeni başlayan biri için bile uygulanabilir.

Sadece web kamera ile ekstra donanıma gerek yok.

### - Sınırlamalar:

Işık koşulları çok kötü olduğunda el tespiti zorlaşabilir.

Arka plan çok kalabalık olduğunda parmakların doğru algılanması zorlaşabilir.

Jestlerin çalışması için elin kameraya belirli bir uzaklıkta ve açıda olması gerekiyor.

### - Geliştirilebilir yönler:

Daha fazla jest eklemek (oynat/duraklat, sesi tamamen kapat vs.).

Kullanıcı arayüzü eklemek (başlangıç ekranında hangi jest ne yapıyor gösterilebilir).

Medya tuşları yerine doğrudan belirli bir müzik uygulamasının API’sini kullanmak.
