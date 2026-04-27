#!/usr/bin/env python3
"""
nmap-tool - Interactive Nmap Command Builder
by erdmoks | https://github.com/erdmoks
"""

import os
import sys
import subprocess
from typing import Optional

# ── ANSI Colors ──────────────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    GREEN   = "\033[92m"
    CYAN    = "\033[96m"
    AMBER   = "\033[93m"
    RED     = "\033[91m"
    MUTED   = "\033[90m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    BLUE    = "\033[94m"

# ── Scan Definitions ─────────────────────────────────────────────────────────
CATEGORIES = {
    "1": {
        "name": "Host Discovery",
        "icon": "◈",
        "scans": [
            ("Ping Scan",         "-sn",                  "Port taraması yapmadan canlı hostları tespit et",          "LOW"),
            ("ARP Ping",          "-PR",                  "LAN'da ARP ile host tespiti, firewall bypass",             "LOW"),
            ("TCP SYN Ping",      "-PS80,443",            "SYN paketi ile host tespiti",                              "MED"),
            ("ICMP Echo",         "-PE",                  "Klasik ICMP ping",                                         "LOW"),
            ("No Ping (Skip)",    "-Pn",                  "Host discovery atla, tüm hostları up say",                 "MED"),
            ("List Scan",         "-sL",                  "Hedefleri listele, paket gönderme",                        "LOW"),
        ]
    },
    "2": {
        "name": "Port Tarama",
        "icon": "◈",
        "scans": [
            ("SYN Scan (Stealth)", "-sS",    "En popüler, hızlı ve görece gizli. Root gerekir.",         "MED"),
            ("TCP Connect",        "-sT",    "Full TCP bağlantısı. Root gerekmez ama loglanır.",          "MED"),
            ("UDP Scan",           "-sU",    "UDP portları için. Yavaş ama DNS/SNMP/DHCP için şart.",     "MED"),
            ("ACK Scan",           "-sA",    "Firewall kural tespiti.",                                   "MED"),
            ("Null Scan",          "-sN",    "Hiçbir flag yok. Bazı firewall'ları geçer.",                "HIGH"),
            ("FIN Scan",           "-sF",    "Sadece FIN flag. RFC uyumlu sistemlere karşı.",             "HIGH"),
            ("Xmas Scan",          "-sX",    "FIN+PSH+URG. IDS tarafından tespit edilir.",               "HIGH"),
            ("Top 1000 Ports",     "",       "(Varsayılan) En yaygın 1000 port",                          "LOW"),
            ("Tüm Portlar",        "-p-",    "65535 port. Yavaş ama kapsamlı.",                           "MED"),
            ("Top 100",            "-F",     "En hızlı tarama, sadece top 100 port.",                     "LOW"),
        ]
    },
    "3": {
        "name": "Servis & Versiyon",
        "icon": "◈",
        "scans": [
            ("Versiyon Tespiti",       "-sV",                       "Servis adı ve versiyonu tespit et.",       "MED"),
            ("Yoğun Versiyon",         "-sV --version-intensity 9", "Maksimum probe. Yavaş ama kapsamlı.",      "HIGH"),
            ("Hafif Versiyon",         "-sV --version-intensity 2", "Hızlı, az gürültülü versiyon tespiti.",    "LOW"),
            ("Agresif (Tümü)",         "-A",                        "OS + Versiyon + Script + Traceroute.",      "HIGH"),
            ("Default Scripts",        "-sC",                       "Varsayılan NSE script seti.",               "MED"),
        ]
    },
    "4": {
        "name": "OS Detection",
        "icon": "◈",
        "scans": [
            ("OS Detection",         "-O",                   "TCP/IP fingerprinting ile OS tahmini.",             "MED"),
            ("Agresif OS Tahmini",   "-O --osscan-guess",    "Düşük güvenle de olsa en yakın OS'u göster.",      "MED"),
            ("OS + Servis",          "-O -sV",               "OS tespiti + servis versiyonları.",                 "MED"),
            ("OS Limit",             "-O --osscan-limit",    "Sadece kesin host'larda OS tespiti.",               "LOW"),
        ]
    },
    "5": {
        "name": "Stealth & Evasion",
        "icon": "◈",
        "scans": [
            ("Decoy Scan",         "-D RND:10",         "10 sahte IP ile gerçek kaynağı gizle.",               "HIGH"),
            ("Source Port Spoof",  "--source-port 53",  "DNS portu gibi davran, firewall bypass.",             "HIGH"),
            ("Fragment Packets",   "-f",                "Paketleri 8 byte'a böl, IDS bypass.",                 "HIGH"),
            ("Spoof MAC",          "--spoof-mac 0",     "Rastgele MAC adresi kullan.",                         "HIGH"),
            ("Data Length",        "--data-length 25",  "Paketlere rastgele veri ekle.",                       "MED"),
            ("Randomize Hosts",    "--randomize-hosts", "Hedefleri rastgele sırayla tara.",                    "MED"),
            ("Bad Checksum",       "--badsum",          "Hatalı checksum ile IDS'i yanılt.",                   "HIGH"),
        ]
    },
    "6": {
        "name": "Vulnerability & NSE",
        "icon": "◈",
        "scans": [
            ("Vuln Tarama",       "--script=vuln",         "Bilinen açıkları tara.",                          "HIGH"),
            ("Auth Test",         "--script=auth",         "Kimlik doğrulama açıkları.",                      "HIGH"),
            ("SMB Açıkları",      "--script=smb-vuln-*",   "EternalBlue, MS17-010 vb.",                       "HIGH"),
            ("HTTP Scripts",      "--script=http-*",       "Web sunucusu bilgi toplama.",                     "MED"),
            ("SSL/TLS Check",     "--script=ssl-*",        "SSL sertifika ve cipher analizi.",                "MED"),
            ("Brute Force",       "--script=brute",        "Servis brute-force (DİKKAT!).",                   "HIGH"),
            ("Discovery Scripts", "--script=discovery",    "Agresif olmayan bilgi toplama.",                  "MED"),
            ("Backdoor Check",    "--script=backdoor",     "Backdoor servis tespiti.",                        "HIGH"),
        ]
    },
    "7": {
        "name": "Timing & Performance",
        "icon": "◈",
        "scans": [
            ("T0 - Paranoid",  "-T0",              "5 dk arayla paket. IDS geçer, çok yavaş.",             "LOW"),
            ("T1 - Sneaky",    "-T1",              "15 sn arayla. IDS geçer ama saatler alır.",            "LOW"),
            ("T2 - Polite",    "-T2",              "Bant genişliği dostu, yavaş.",                         "LOW"),
            ("T3 - Normal",    "-T3",              "Varsayılan. Dengeli.",                                  "MED"),
            ("T4 - Aggressive","-T4",              "Hızlı ağlar için önerilen.",                           "MED"),
            ("T5 - Insane",    "-T5",              "Maksimum hız. LAN'da kullan.",                         "HIGH"),
            ("Min Rate 1000",  "--min-rate 1000",  "Saniyede min 1000 paket.",                             "MED"),
            ("Max Retries 1",  "--max-retries 1",  "Sadece 1 tekrar deneme. Hızlandırır.",                 "MED"),
        ]
    },
    "8": {
        "name": "Output & Format",
        "icon": "◈",
        "scans": [
            ("Normal Çıktı",      "-oN scan.txt",      "Okunabilir format.",                                "LOW"),
            ("XML Çıktı",         "-oX scan.xml",      "Metasploit import için ideal.",                    "LOW"),
            ("Grepable",          "-oG scan.gnmap",    "Shell script'ler için.",                           "LOW"),
            ("Tüm Formatlar",     "-oA scan_results",  "3 formatı aynı anda kaydet. ÖNERİLEN!",            "LOW"),
            ("Verbose",           "-v",                "Gerçek zamanlı ilerleme.",                         "LOW"),
            ("Double Verbose",    "-vv",               "Daha fazla detay.",                                "LOW"),
            ("Reason",            "--reason",          "Port durumunun nedenini göster.",                  "LOW"),
            ("Packet Trace",      "--packet-trace",    "Tüm paketleri göster. Debug.",                    "LOW"),
        ]
    },
}

RISK_COLORS = {
    "LOW":  f"{C.GREEN}[DÜŞÜK]{C.RESET}",
    "MED":  f"{C.AMBER}[ORTA ]{C.RESET}",
    "HIGH": f"{C.RED}[YÜKSEK]{C.RESET}",
}

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"""
{C.GREEN}{C.BOLD}
  ███╗   ██╗███╗   ███╗ █████╗ ██████╗       ████████╗ ██████╗  ██████╗ ██╗
  ████╗  ██║████╗ ████║██╔══██╗██╔══██╗      ╚══██╔══╝██╔═══██╗██╔═══██╗██║
  ██╔██╗ ██║██╔████╔██║███████║██████╔╝         ██║   ██║   ██║██║   ██║██║
  ██║╚██╗██║██║╚██╔╝██║██╔══██║██╔═══╝          ██║   ██║   ██║██║   ██║██║
  ██║ ╚████║██║ ╚═╝ ██║██║  ██║██║              ██║   ╚██████╔╝╚██████╔╝███████╗
  ╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝              ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
{C.RESET}
{C.MUTED}  by erdmoks | Interactive Nmap Command Builder | github.com/erdmoks/nmap-tool{C.RESET}
{C.GREEN}  {'─'*70}{C.RESET}
""")

def show_categories():
    print(f"  {C.CYAN}{C.BOLD}TARAMA KATEGORİLERİ{C.RESET}\n")
    for key, cat in CATEGORIES.items():
        print(f"  {C.GREEN}[{key}]{C.RESET} {cat['icon']} {cat['name']}")
    print(f"\n  {C.GREEN}[0]{C.RESET} {C.MUTED}Çıkış{C.RESET}")
    print()

def show_scans(cat_key: str) -> Optional[list]:
    cat = CATEGORIES.get(cat_key)
    if not cat:
        return None

    print(f"\n  {C.GREEN}{C.BOLD}◈ {cat['name'].upper()}{C.RESET}\n")
    scans = cat["scans"]
    for i, (name, flag, desc, risk) in enumerate(scans, 1):
        flag_display = f"{C.AMBER}{flag}{C.RESET}" if flag else f"{C.MUTED}(varsayılan){C.RESET}"
        print(f"  {C.GREEN}[{i:2d}]{C.RESET} {name:<25} {flag_display:<35} {RISK_COLORS[risk]}")
        print(f"        {C.DIM}{desc}{C.RESET}")
        print()

    return scans

def get_target() -> str:
    print(f"\n  {C.CYAN}Hedef IP / Domain / CIDR:{C.RESET}", end=" ")
    target = input().strip()
    return target if target else "<HEDEF>"

def get_ports() -> str:
    print(f"\n  {C.CYAN}Port (boş = varsayılan | örn: 80,443 | 1-1000 | -):{C.RESET}", end=" ")
    ports = input().strip()
    if ports == "-":
        return "-p-"
    elif ports:
        return f"-p {ports}"
    return ""

def build_command(flags: list, target: str, extra_port: str) -> str:
    parts = ["nmap"] + [f for f in flags if f] + ([extra_port] if extra_port else []) + [target]
    return " ".join(parts)

def run_command(cmd: str):
    print(f"\n  {C.AMBER}[*] Nmap çalıştırılıyor...{C.RESET}\n")
    print(f"  {C.MUTED}{'─'*60}{C.RESET}\n")
    try:
        result = subprocess.run(cmd, shell=True, text=True)
        return result.returncode
    except KeyboardInterrupt:
        print(f"\n\n  {C.AMBER}[!] Tarama durduruldu.{C.RESET}")
        return -1

def save_command(cmd: str):
    fname = "last_scan.sh"
    with open(fname, "w") as f:
        f.write(f"#!/bin/bash\n# nmap-tool tarafından oluşturuldu\n{cmd}\n")
    os.chmod(fname, 0o755)
    print(f"\n  {C.GREEN}[+] Komut '{fname}' dosyasına kaydedildi.{C.RESET}")

def main():
    clear()
    banner()

    while True:
        show_categories()
        print(f"  {C.CYAN}Kategori seç:{C.RESET}", end=" ")
        cat_choice = input().strip()

        if cat_choice == "0":
            print(f"\n  {C.MUTED}İyi hacklemeler! 🔍{C.RESET}\n")
            sys.exit(0)

        if cat_choice not in CATEGORIES:
            print(f"  {C.RED}[!] Geçersiz seçim.{C.RESET}\n")
            continue

        clear()
        banner()
        scans = show_scans(cat_choice)
        if not scans:
            continue

        print(f"  {C.CYAN}Tarama seç (birden fazla: 1,3,5 | hepsi: a | geri: q):{C.RESET}", end=" ")
        scan_input = input().strip().lower()

        if scan_input == "q":
            clear()
            banner()
            continue

        selected_flags = []
        if scan_input == "a":
            selected_flags = [s[1] for s in scans if s[1]]
        else:
            for idx in scan_input.split(","):
                idx = idx.strip()
                if idx.isdigit():
                    i = int(idx) - 1
                    if 0 <= i < len(scans):
                        flag = scans[i][1]
                        if flag:
                            selected_flags.append(flag)

        if not selected_flags:
            print(f"  {C.RED}[!] Geçerli tarama seçilmedi.{C.RESET}")
            input(f"\n  {C.MUTED}Devam için Enter...{C.RESET}")
            clear()
            banner()
            continue

        target  = get_target()
        portarg = get_ports()
        cmd     = build_command(selected_flags, target, portarg)

        print(f"\n  {C.GREEN}{'─'*70}{C.RESET}")
        print(f"  {C.BOLD}{C.GREEN}OLUŞTURULAN KOMUT:{C.RESET}")
        print(f"\n  {C.MUTED}${C.RESET} {C.GREEN}{cmd}{C.RESET}")
        print(f"  {C.GREEN}{'─'*70}{C.RESET}")

        print(f"""
  {C.CYAN}Ne yapmak istersin?{C.RESET}
  {C.GREEN}[1]{C.RESET} Komutu çalıştır (nmap kurulu olmalı)
  {C.GREEN}[2]{C.RESET} Komutu kaydet (last_scan.sh)
  {C.GREEN}[3]{C.RESET} Panoya kopyala (xclip/pbcopy)
  {C.GREEN}[4]{C.RESET} Ana menüye dön
""")
        print(f"  {C.CYAN}Seçim:{C.RESET}", end=" ")
        action = input().strip()

        if action == "1":
            yn = input(f"\n  {C.RED}[!] Sadece izinli sistemlerde kullan! Devam? (e/h):{C.RESET} ").strip().lower()
            if yn == "e":
                run_command(cmd)
                input(f"\n  {C.MUTED}Devam için Enter...{C.RESET}")
        elif action == "2":
            save_command(cmd)
            input(f"\n  {C.MUTED}Devam için Enter...{C.RESET}")
        elif action == "3":
            if sys.platform == "darwin":
                subprocess.run(f"echo '{cmd}' | pbcopy", shell=True)
            else:
                subprocess.run(f"echo '{cmd}' | xclip -selection clipboard", shell=True)
            print(f"  {C.GREEN}[+] Panoya kopyalandı!{C.RESET}")
            input(f"\n  {C.MUTED}Devam için Enter...{C.RESET}")

        clear()
        banner()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {C.MUTED}Çıkılıyor...{C.RESET}\n")
        sys.exit(0)
