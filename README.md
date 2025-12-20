## ☸️ Jalankan di Kubernetes

1. Build Docker image dan push ke registry yang bisa diakses cluster (misal Docker Hub):
  ```bash
  docker build -t username/ids-ips-tool:latest .
  docker push username/ids-ips-tool:latest
  # Ganti 'username' sesuai akun Docker Hub Anda
  ```
2. Edit file `k8s-ids-ips.yaml`, ganti bagian `image: ids-ips-tool:latest` menjadi `image: username/ids-ips-tool:latest`
3. Deploy ke cluster:
  ```bash
  kubectl apply -f k8s-ids-ips.yaml
  kubectl get pods
  kubectl exec -it <nama-pod> -- bash
  # Jalankan IDS/IPS di dalam pod:
  ./ids_main.py config.json sample.log
  # atau
  python ids_main.py config.json sample.log
  ```
> **Troubleshooting Kubernetes**
> - Jika error permission: chmod +x ids_main.py sebelum build image
> - Untuk volume log: gunakan emptyDir untuk dev/testing, hostPath untuk production (pastikan path benar di node)
> - Jika modul tidak ditemukan: pastikan jalankan dari /app atau root project di dalam pod
4. Mount log hostPath sesuai kebutuhan (edit path di yaml)

---
---


## 🙏 Catatan Pengembang

Proyek ini sedang dalam proses refaktor besar, terutama pada bagian dashboard FastAPI (modularisasi, rate limit, dan kompatibilitas bcrypt/passlib di Python 3.13). Jika Anda menemukan solusi atau ingin membantu, kontribusi dan saran sangat diharapkan! Silakan buat issue, pull request, atau kontak langsung jika ingin berdiskusi atau membantu memperbaiki masalah.

<p align="left">
  <img src="https://img.shields.io/badge/python-3.7%2B-blue" alt="Python Version">
  <img src="https://img.shields.io/github/license/Bangkah/IDS-IPS-Tool" alt="License">
  <img src="https://github.com/Bangkah/IDS-IPS-Tool/actions/workflows/python-package.yml/badge.svg" alt="CI">
  <img src="https://codecov.io/gh/Bangkah/IDS-IPS-Tool/branch/main/graph/badge.svg" alt="Codecov"/>
  <img src="https://img.shields.io/badge/tested-passed-brightgreen" alt="Tested">
  <img src="https://img.shields.io/docker/pulls/bangkah/ids-ips-tool?style=flat-square" alt="Docker Pulls">
  <img src="https://img.shields.io/pypi/v/ids-ips-tool?color=blue" alt="PyPI">
</p>

<div align="left">
<b>IDS/IPS Tool</b> adalah sistem modular deteksi dan pencegahan serangan (Intrusion Detection & Prevention System) berbasis Python. Mendukung analisis file log, monitoring real-time, network sniffer (Suricata-like), serta firewall CLI. Cocok untuk pembelajaran, riset, dan penggunaan di lingkungan kecil hingga menengah.
</div>

---

> **[WIP] Dashboard**
> 
> Fitur dashboard web (FastAPI/Streamlit) sedang dalam pengembangan dan belum stabil. Dokumentasi dan instruksi dashboard untuk sementara disembunyikan agar fokus pada fitur CLI yang sudah stabil. Silakan cek milestone atau issue [WIP] Dashboard di repo untuk update progres.

---


## ✅ Diuji di
- Ubuntu 22.04 (nftables default)
- Debian 12 (iptables)
- Arch Linux (ufw)

## ⚠️ Belum diuji di
- CentOS/RHEL
- Alpine Linux
- Windows (WSL mungkin bekerja, tapi tidak didukung resmi)

---

## 🛡️ Overview

**IDS/IPS Tool** adalah sistem modular deteksi dan pencegahan serangan (Intrusion Detection & Prevention System) berbasis Python. Mendukung analisis file log, monitoring real-time, network sniffer (Suricata-like), serta firewall CLI. Proyek ini cocok untuk pembelajaran, riset, dan penggunaan di lingkungan kecil hingga menengah.

---


## 🛠️ Use Case Nyata

### 1. Lindungi Server Pribadi
- Jalankan `./ips_main.py config.json /var/log/auth.log`
- Atau: `python ips_main.py config.json /var/log/auth.log`
- Otomatis blokir brute-force SSH.


- Tambahkan pola regex untuk SQLi/XSS di `config.json`
- Jalankan IDS real-time di log Nginx/Apache:
  ```bash
  ./ids_main.py config.json /var/log/nginx/access.log --realtime
  # atau
  python ids_main.py config.json /var/log/nginx/access.log --realtime
  ```
- **Catatan:** Jika file log tidak ditemukan, gunakan file log lain yang tersedia, atau buat file dummy (misal: `touch sample.log`) untuk simulasi.

### 3. Edukasi Cybersecurity
- Gunakan di lab kampus untuk deteksi serangan simulasi.


- **IDS (Intrusion Detection System):** Deteksi serangan dari file log
- **IPS (Intrusion Prevention System):** Pencegahan otomatis, blokir IP via iptables, nftables, atau ufw (kompatibel dengan banyak distro Linux modern)
- **Real-time Monitoring:** Pantau file log secara langsung (dengan watchdog)
- **Network IDS:** Sniffer multi-interface, mirip Suricata
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

## ⚠️ Known Issues (Des 2025)

- **Dashboard FastAPI**: [WIP] Tidak stabil, fitur dashboard dinonaktifkan sementara dari dokumentasi utama.
- **bcrypt/passlib**: Pastikan gunakan bcrypt >=4.1.2. Jika error, uninstall bcrypt lalu install versi terbaru.
- **Limiter/rate limit**: Jika error `Limiter not defined`, pastikan slowapi sudah terinstall dan import Limiter di file yang tepat.
- **Modularisasi**: Semua folder dashboard/core, dashboard/routers, dashboard/services, dashboard/websocket wajib ada file __init__.py.
- **Struktur baru**: Dokumentasi dan instruksi masih dalam proses update agar sesuai arsitektur baru.

Jika menemukan error baru, silakan laporkan via GitHub Issue atau cek FAQ/Troubleshooting di bawah.
  - Validasi IP otomatis sebelum blokir
  - Tidak akan memblokir IP yang sudah diblokir (deteksi duplikat)
  - Unblock presisi (khusus nftables: by handle)
  - Output list rules lebih mudah dibaca
  - Error handling dan feedback ke user lebih jelas
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


## 🐳 Jalankan dengan Docker

docker run --rm -it --cap-add=NET_ADMIN -v $(pwd):/app ids-ips-tool
### Build & Run Manual
```bash
docker build -t ids-ips-tool .
docker run --rm -it --cap-add=NET_ADMIN -v $(pwd):/app ids-ips-tool
# Setelah masuk container, jalankan:
./ids_main.py config.json sample.log
# atau
python ids_main.py config.json sample.log
```

### Docker Compose (Rekomendasi)
```bash
docker compose up --build
# Container akan masuk bash, jalankan:
./ids_main.py config.json sample.log
# atau
python ids_main.py config.json sample.log
```
> **Troubleshooting Docker**
> - Jika permission denied: pastikan file sudah chmod +x sebelum build, atau gunakan python ...
> - Untuk log hostPath: pastikan path di -v sudah benar dan file log ada di dalam /app

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
./ids_main.py config.json sample.log
# atau
python ids_main.py config.json sample.log
```

### 2. IDS Real-time (Seperti Antivirus)
```bash
./ids_main.py config.json /var/log/auth.log --realtime
# atau
python ids_main.py config.json /var/log/auth.log --realtime
```
> **Catatan:** Pastikan file log yang dimonitor benar-benar ada. Jika file tidak ditemukan, gunakan file log lain yang tersedia, misal sample.log atau log lain yang ingin Anda monitor.

### 3. IPS (Blokir IP Otomatis, Multi-Firewall)
```bash
./ips_main.py config.json sample.log
# atau
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

> **[WIP] Dashboard**
> 
> Fitur dashboard web (FastAPI/Streamlit) sedang dalam pengembangan dan belum stabil. Dokumentasi dan instruksi dashboard untuk sementara disembunyikan agar fokus pada fitur CLI yang sudah stabil. Silakan cek milestone atau issue [WIP] Dashboard di repo untuk update progres.

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
- **Bagaimana menjalankan IDS/IPS langsung?**  
  Gunakan `./ids_main.py ...` atau `./ips_main.py ...` (pastikan sudah chmod +x). Alternatif: `python ids_main.py ...`.
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
- **Permission denied saat menjalankan Network IDS/IDS/IPS?**  
  Jalankan dengan sudo/root jika perlu akses firewall atau network interface. Jika permission denied pada ./ids_main.py, ./ips_main.py: pastikan sudah chmod +x, atau gunakan python ...
- **WebSocket live feed tidak muncul?**  
  Pastikan file log (`ids_ips.log`) ada dan terisi event.
- **Notifikasi desktop tidak muncul?**  
  Pastikan `notify2` terinstall dan desktop environment mendukung.
- **Blokir IP gagal?**  
  Pastikan Anda menjalankan dengan hak sudo/root dan backend firewall (iptables/nftables/ufw) tersedia di sistem. Cek log untuk pesan error backend.
  Jika error modul: pastikan jalankan dari root folder project.

---


## 📄 Lisensi

Proyek ini berlisensi MIT. Lihat file LICENSE untuk detail.

---


## 👨‍💻 Kontributor & Kredit

<div align="center">
  <b>Dikembangkan oleh: Bangkah</b><br>
  Kontribusi, saran, dan pull request sangat diterima!
</div>
