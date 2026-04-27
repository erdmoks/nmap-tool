# nmap-tool 🔍

Interactive, terminal-based Nmap command builder. Nmap parametrelerini ezberlemeden, kategori bazlı menülerle tarama komutları oluştur.

```
  ███╗   ██╗███╗   ███╗ █████╗ ██████╗       ████████╗ ██████╗  ██████╗ ██╗
  ████╗  ██║████╗ ████║██╔══██╗██╔══██╗      ╚══██╔══╝██╔═══██╗██╔═══██╗██║
  ██╔██╗ ██║██╔████╔██║███████║██████╔╝         ██║   ██║   ██║██║   ██║██║
  ██║╚██╗██║██║╚██╔╝██║██╔══██║██╔═══╝          ██║   ██║   ██║██║   ██║██║
  ██║ ╚████║██║ ╚═╝ ██║██║  ██║██║              ██║   ╚██████╔╝╚██████╔╝███████╗
  ╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝              ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
```

---

## Özellikler

- 8 tarama kategorisi, 60+ hazır profil
- Risk seviyesi göstergeleri (LOW / ORTA / YÜKSEK)
- Hedef IP, domain veya CIDR gir
- Port aralığı özelleştirme
- Oluşturulan komutu çalıştır, kaydet veya panoya kopyala
- Sıfır bağımlılık — sadece Python 3

---

## Kurulum

```bash
git clone https://github.com/erdmoks/nmap-tool
cd nmap-tool
chmod +x nmap_tool.py
```

### Nmap kurulu değilse

```bash
# Debian/Ubuntu
sudo apt install nmap

# Arch
sudo pacman -S nmap

# macOS
brew install nmap
```

---

## Kullanım

```bash
python3 nmap_tool.py
# veya
./nmap_tool.py
```

### Akış

1. Kategori seç (1-8)
2. Tarama türlerini seç (`1,3` veya `a` için hepsi)
3. Hedef IP/domain gir
4. Port aralığı belirle (opsiyonel)
5. Komutu çalıştır / kaydet / kopyala

---

## Kategoriler

| # | Kategori | Ne İşe Yarar |
|---|----------|-------------|
| 1 | **Host Discovery** | Ağdaki canlı hostları tespit |
| 2 | **Port Tarama** | Açık portları bul |
| 3 | **Servis & Versiyon** | Çalışan servislerin versiyonları |
| 4 | **OS Detection** | İşletim sistemi tahmini |
| 5 | **Stealth & Evasion** | IDS/IPS bypass teknikleri |
| 6 | **Vulnerability & NSE** | Güvenlik açığı tarama scriptleri |
| 7 | **Timing & Performance** | Tarama hızı ayarları |
| 8 | **Output & Format** | Sonuç kaydetme formatları |

---

## Örnekler

```bash
# Hızlı ağ taraması
nmap -sn 192.168.1.0/24

# Stealth SYN + versiyon + T4
nmap -sS -sV -T4 -p 1-1000 192.168.1.1

# Vulnerability scan
nmap --script=vuln -sV 10.0.0.1

# Tüm çıktıları kaydet
nmap -sS -oA scan_results 192.168.1.1
```

---

## Uyarı

> Bu araç **yalnızca sahip olduğunuz veya yazılı izin aldığınız sistemlerde** kullanılmalıdır.  
> İzinsiz port taraması birçok ülkede **yasadışıdır**.  
> Yazar hiçbir sorumluluk kabul etmez.

---

## Diğer Araçlar

- [recon-tool](https://github.com/erdmoks/recon-tool) — Pasif keşif aracı

---

