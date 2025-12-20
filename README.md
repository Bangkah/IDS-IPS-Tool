---

## 🙏 Catatan Pengembang

Saya mengalami beberapa kesulitan dalam proses refaktor besar dashboard FastAPI ini (terutama terkait modularisasi, rate limit, dan kompatibilitas bcrypt/passlib di Python 3.13). Jika Anda menemukan solusi atau ingin membantu, kontribusi dan saran sangat saya harapkan! Silakan buat issue, pull request, atau kontak langsung jika ingin berdiskusi atau membantu memperbaiki masalah.

# IDS/IPS Tool


![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/github/license/Bangkah/IDS-IPS-Tool)
![CI](https://github.com/Bangkah/IDS-IPS-Tool/actions/workflows/python-package.yml/badge.svg)
![Tested](https://img.shields.io/badge/tested-passed-brightgreen)

---


> **Status: SEDANG REFAKTOR BESAR DASHBOARD**
> - Struktur dashboard FastAPI sudah dipecah modular (core, routers, services, websocket).
> - Namun, masih ada beberapa masalah kompatibilitas dan error runtime (misal: Limiter not defined, bcrypt/passlib, dsb).
> - Jika Anda mencoba menjalankan dashboard dan mendapat error, cek bagian Troubleshooting di bawah.
> - Fitur IDS, IPS CLI, dan firewall tetap stabil. Dashboard web dalam proses stabilisasi.
---

## ⚠️ Known Issues (Des 2025)

- **Dashboard FastAPI**: Masih ada error Limiter not defined, error bcrypt/passlib di Python 3.13, dan beberapa import error jika struktur belum lengkap.
- **bcrypt/passlib**: Pastikan gunakan bcrypt >=4.1.2. Jika error, uninstall bcrypt lalu install versi terbaru.
- **Limiter/rate limit**: Jika error `Limiter not defined`, pastikan slowapi sudah terinstall dan import Limiter di file yang tepat.
- **Modularisasi**: Semua folder dashboard/core, dashboard/routers, dashboard/services, dashboard/websocket wajib ada file __init__.py.
- **Struktur baru**: Dokumentasi dan instruksi masih dalam proses update agar sesuai arsitektur baru.

Jika menemukan error baru, silakan laporkan via GitHub Issue atau cek FAQ/Troubleshooting di bawah.


---

## 🛡️ Overview

**IDS/IPS Tool** adalah sistem modular deteksi dan pencegahan serangan (Intrusion Detection & Prevention System) berbasis Python. Mendukung analisis file log, monitoring real-time, network sniffer (Suricata-like), serta dashboard web real-time untuk visualisasi dan kontrol.

---

## 🚀 Fitur Utama

- **IDS (Intrusion Detection System):** Deteksi serangan dari file log
- **IPS (Intrusion Prevention System):** Pencegahan otomatis, blokir IP via iptables, nftables, atau ufw (kompatibel dengan banyak distro Linux modern)
- **Real-time Monitoring:** Pantau file log secara langsung (dengan watchdog)
- **Network IDS:** Sniffer multi-interface, mirip Suricata
- **Statistik & Visualisasi:** Statistik otomatis, dashboard web real-time (FastAPI + Chart.js)
- **Rotating Logging:** Log otomatis bergulir
- **Notifikasi Desktop:** Opsional, via notify2
- **Konfigurasi Mudah:** Semua pola dan pengaturan di `config.json`
- **Unit Test:** Pengujian mudah dengan unittest
- **Firewall Tool (Terpisah):**
  - Manajemen blokir/unblock IP dan list rules untuk iptables, nftables, ufw melalui CLI terpisah (firewall/)
  - Validasi IP otomatis sebelum blokir
  - Tidak akan memblokir IP yang sudah diblokir (deteksi duplikat)
  - Unblock presisi (khusus nftables: by handle)
  - Output list rules lebih mudah dibaca
  - Error handling dan feedback ke user lebih jelas

---


## 🔎 Rule Engine Suricata-like (Signature, Whitelist, Severity)

Mulai versi terbaru, IDS/IPS mendukung rule engine ala Suricata:

- **Rule format:**
  - Field: `action`, `msg`, `regex`, `severity`, `src_ip`, `dst_ip`, `whitelist`
  - Contoh rule:
    ```json
    {
      "action": "alert",
      "msg": "SQL Injection attempt",
      "regex": "(SELECT|UNION|INSERT|UPDATE|DELETE|DROP|--|;|'|\")",
      "severity": "high",
      "src_ip": null,
      "dst_ip": null,
      "whitelist": ["127.0.0.1"]
    }
    ```
- **Whitelist:** IP yang diabaikan oleh rule tertentu.
- **Severity:** critical, high, medium, low, info (bisa dikustom).
- **Flexible:** Bisa deteksi serangan web, brute force, DDoS, dsb.

> Semua rule bisa didefinisikan di file JSON (misal `rules.json`) atau langsung di config.

### Contoh Rule File (rules.json)
```json
[
  {"action": "alert", "msg": "Failed password", "regex": "Failed password.*from ([\\d.]+)", "severity": "high"},
  {"action": "alert", "msg": "SQL Injection", "regex": "(SELECT|UNION|INSERT|UPDATE|DELETE|DROP|--|;|'|\")", "severity": "high", "whitelist": ["10.0.0.1"]}
]
```

### Integrasi ke IDS/IPS
- Tambahkan/muat rule dari file JSON
- Jalankan engine pada setiap log/alert
- Hanya alert yang lolos whitelist dan sesuai severity yang diproses

### Export Log ke ELK/Grafana
- Semua event/alert dapat diekspor ke file JSON/CSV
- Bisa di-push ke ELK Stack (Elasticsearch, Logstash, Kibana) atau Grafana (via filebeat, REST API, dsb)
- Contoh: `python export_log.py --elk` atau integrasi filebeat ke `ids_ips.log`

---

---

## 🗂️ Struktur Proyek

```
ids_ips_tool/
├── src/               # Kode utama modular (IDS, IPS, logger, dsb)
├── tests/             # Unit test
├── ids_main.py        # Entrypoint IDS
├── ips_main.py        # Entrypoint IPS
├── netids_main.py     # Entrypoint Network IDS
├── config.json        # Konfigurasi pola deteksi
├── requirements.txt   # Dependensi Python
├── dashboard/         # Dashboard web (FastAPI, HTML, JS, CSS)
├── firewall/          # Tool manajemen firewall (blokir, unblock, list IP)
├── README.md
```

---

## 🏗️ Arsitektur Singkat

- **src/**: Implementasi utama IDS, IPS, logger, alert, dsb
- **dashboard/**: Backend FastAPI, frontend HTML/JS/CSS, WebSocket live feed
- **firewall/**: Tool terpisah untuk manajemen firewall melalui CLI
- **config.json**: Pola deteksi, pengaturan log, dsb
- **Log File**: Semua event dicatat ke `ids_ips.log` (default)

---

## ⚙️ Instalasi


1. **Pastikan Python 3.7+ dan pip sudah terpasang**

2. **(Rekomendasi) Buat dan aktifkan virtual environment:**
  ```bash
  python3 -m venv .venv
  # Aktifkan venv (Linux/macOS)
  source .venv/bin/activate
  # atau jika menggunakan fish shell:
  source .venv/bin/activate.fish
  # Aktifkan venv (Windows)
  .venv\Scripts\activate
  ```

3. **Install dependensi:**
  ```bash
  pip install -r requirements.txt
  pip install uvicorn  # pastikan uvicorn terinstall di venv
  ```

4. **(Opsional) Install notifikasi desktop:**
  ```bash
  pip install notify2
  ```

5. **(Opsional) Untuk real-time monitoring:**
  ```bash
  pip install watchdog
  ```

### Instalasi langsung sebagai package dari GitHub

```bash
pip install git+https://github.com/Bangkah/IDS-IPS-Tool.git
```

Atau untuk versi tertentu:
```bash
pip install git+https://github.com/Bangkah/IDS-IPS-Tool.git@v1.0.1
```

---

## 📝 Konfigurasi

Edit `config.json` untuk menambah/mengubah pola deteksi, file log, dan backend firewall (untuk IPS). Contoh pola deteksi:

```json
  "patterns": [
    {"name": "Failed password", "regex": "Failed password.*from ([\\d.]+)", "severity": "high"},
    {"name": "SQL Injection", "regex": "(SELECT|UNION|INSERT|UPDATE|DELETE|DROP|--|;|'|\")", "severity": "high"},
    {"name": "XSS Attack", "regex": "(<script>|javascript:|onerror=|onload=)", "severity": "high"},
    {"name": "DDoS SYN Flood", "regex": "SYN flood|Possible SYN flooding|TCP SYN flood", "severity": "high"}
  ]
```

Setiap pola terdiri dari:
- `name`: Nama signature
- `regex`: Pola regex/keyword yang dicari pada log
- `severity`: Tingkat ancaman (low/medium/high)

Contoh konfigurasi lainnya:

```json
{
  "patterns": [
    {"name": "Failed password", "regex": "Failed password.*from ([\\d.]+)", "severity": "high"}
  ],
  "log_file": "ids_ips.log",
  "firewall": "auto",  // Pilihan: auto, iptables, nftables, ufw
  "net_patterns": [
    {"name": "TCP SYN Scan", "type": "tcp_syn"}
  ]
}
```

**Opsi `firewall` (khusus IPS):**
- `auto` (default): deteksi otomatis backend firewall (nftables > ufw > iptables)
- `iptables`: paksa gunakan iptables
- `nftables`: paksa gunakan nftables
- `ufw`: paksa gunakan ufw

Jika Anda menggunakan distro modern (Ubuntu 22.04+, Debian 12+, Fedora, dsb), backend default kemungkinan akan menggunakan nftables atau ufw. Untuk sistem lama, biasanya iptables.

---

## ▶️ Cara Menjalankan

### 1. IDS (Analisis File Log)
```bash
python ids_main.py config.json sample.log
```

### 2. IDS Real-time (Seperti Antivirus)
```bash
python ids_main.py config.json /var/log/auth.log --realtime
```
> **Catatan:** Pastikan file log yang dimonitor benar-benar ada. Jika file tidak ditemukan, gunakan file log lain yang tersedia, misal sample.log atau log lain yang ingin Anda monitor.

### 3. IPS (Blokir IP Otomatis, Multi-Firewall)
```bash
python ips_main.py config.json sample.log
```
Ganti `sample.log` dengan file log yang ingin Anda analisis.

> **Catatan:** IPS kini mendukung iptables, nftables, dan ufw. Secara default akan memilih otomatis backend firewall yang tersedia di sistem Anda. Anda bisa memaksa backend tertentu lewat config.json (lihat bagian Konfigurasi).

### 4. Network IDS (Sniffer)
```bash
sudo python netids_main.py config.json
# Untuk memonitor interface tertentu:
sudo python netids_main.py config.json --iface <nama_interface>
# Contoh: sudo python netids_main.py config.json --iface enp3s0
# Catatan: Pastikan nama interface (misal eth0, enp3s0, wlan0) sesuai dengan yang ada di sistem Anda.
# Untuk melihat daftar interface, gunakan perintah: ip link
```

### 5. Firewall CLI (Manajemen Firewall Terpisah)

Tool ini memungkinkan Anda memblokir, membuka blokir, dan melihat daftar IP yang diblokir secara langsung melalui command line, mendukung iptables, nftables, dan ufw.

Fitur unggulan:
- Validasi IP address sebelum blokir
- Tidak akan memblokir IP yang sudah diblokir
- Unblock otomatis mencari rule nftables secara presisi (by handle)
- Output list rules mudah dibaca
- Error handling dan feedback ke user lebih jelas

Contoh penggunaan:

Blokir IP:
```bash
python -m firewall.firewall_main --block 1.2.3.4
# atau
PYTHONPATH=. python firewall/firewall_main.py --block 1.2.3.4
```
Jika IP sudah diblokir, akan muncul pesan info.

Unblock IP:
```bash
python -m firewall.firewall_main --unblock 1.2.3.4
# atau
PYTHONPATH=. python firewall/firewall_main.py --unblock 1.2.3.4
```
Jika rule tidak ditemukan, akan muncul info.

List IP yang diblokir:
```bash
python -m firewall.firewall_main --list
# atau
PYTHONPATH=. python firewall/firewall_main.py --list
```
Output akan menampilkan rules yang aktif secara ringkas.

Pilih backend firewall secara eksplisit:
```bash
python -m firewall.firewall_main --block 1.2.3.4 --backend nftables
```

> **Catatan:** Jalankan dari root folder project agar import modul berhasil. Gunakan hak sudo/root untuk akses firewall.

---

## 🌐 Dashboard Web (Real-time)


### Menjalankan Dashboard
```bash
# Pastikan sudah mengaktifkan virtual environment (lihat bagian Instalasi di atas)
uvicorn dashboard.app:app --reload
# Buka browser ke http://127.0.0.1:8000
```

Jika muncul error `uvicorn: command not found`, pastikan Anda sudah mengaktifkan virtual environment dan sudah menjalankan `pip install uvicorn` di venv yang aktif.

Jika tetap error, coba jalankan dengan path lengkap:
```bash
.venv/bin/uvicorn dashboard.app:app --reload
atau
python -m uvicorn dashboard.app:app --reload
```

### Fitur Dashboard
- Statistik serangan (bar chart)
- Jenis serangan (pie chart)
- Top 5 IP penyerang
- Status IDS/IPS
- Live feed real-time (WebSocket)
- Kontrol panel: unblock IP, edit config.json

---

## 🧪 Pengujian

Jalankan semua unit test:
```bash
python -m unittest discover tests
```

---

## 🛠️ Kustomisasi & Pengembangan

- Tambahkan pola deteksi di `config.json`
- Ubah log file di `config.json`
- Kembangkan `src/ids.py`, `src/ips.py`, `src/netids.py` untuk fitur baru (notifikasi, integrasi SIEM, dsb)
- Tambahkan unit test di folder `tests/`
- Modifikasi dashboard (HTML/JS/CSS) sesuai kebutuhan

---

## ❓ FAQ

- **Bagaimana menambah pola deteksi?**  
  Edit `config.json` bagian `patterns` atau `net_patterns`.
- **Apakah bisa menambah notifikasi lain?**  
  Ya, modifikasi `src/alert.py`.
- **Bagaimana menambah test?**  
  Tambahkan file `test_*.py` di folder `tests/`.
- **Bagaimana mengubah port dashboard?**  
  Jalankan uvicorn dengan argumen `--port`, contoh: `uvicorn dashboard.app:app --reload --port 8080`
- **Bagaimana menambah/menghapus fitur dashboard?**  
  Edit file di `dashboard/` (app.py, templates, static)
- **Bagaimana cara memilih backend firewall?**  
  Edit `firewall` di config.json: `auto`, `iptables`, `nftables`, atau `ufw`.
- **Bagaimana tahu backend mana yang dipakai?**  
  IPS akan menampilkan backend yang digunakan di log dan output saat blokir IP.

---

## 🐞 Troubleshooting

- **Favicon 404 di dashboard?**  
  Abaikan, atau tambahkan file `favicon.ico` ke `dashboard/static/`.
- **FileNotFoundError saat IDS real-time?**  
  Pastikan path file log benar dan file ada.
- **Permission denied saat menjalankan Network IDS?**  
  Jalankan dengan sudo/root.
- **WebSocket live feed tidak muncul?**  
  Pastikan file log (`ids_ips.log`) ada dan terisi event.
- **Notifikasi desktop tidak muncul?**  
  Pastikan `notify2` terinstall dan desktop environment mendukung.
- **Blokir IP gagal?**  
  Pastikan Anda menjalankan dengan hak sudo/root dan backend firewall (iptables/nftables/ufw) tersedia di sistem. Cek log untuk pesan error backend.

---

## 📄 Lisensi

Proyek ini berlisensi MIT. Lihat file LICENSE untuk detail.

---

## 👨‍💻 Kontributor & Kredit

<div align="center">
  <b>Dikembangkan oleh: Bangkah</b><br>
  Kontribusi, saran, dan pull request sangat diterima!
</div>
