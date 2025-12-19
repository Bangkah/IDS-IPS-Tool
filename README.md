



# IDS/IPS Tool

![Python](https://img.shields.io/badge/python-3.7%2B-blue) ![License](https://img.shields.io/github/license/Bangkah/IDS-IPS-Tool) ![CI](https://github.com/Bangkah/IDS-IPS-Tool/actions/workflows/python-package.yml/badge.svg)

---

## 🛡️ Overview

**IDS/IPS Tool** adalah sistem modular deteksi dan pencegahan serangan (Intrusion Detection & Prevention System) berbasis Python. Mendukung analisis file log, monitoring real-time, network sniffer (Suricata-like), serta dashboard web real-time untuk visualisasi dan kontrol.

---

## 🚀 Fitur Utama

- **IDS (Intrusion Detection System):** Deteksi serangan dari file log
- **IPS (Intrusion Prevention System):** Pencegahan otomatis, blokir IP via iptables
- **Real-time Monitoring:** Pantau file log secara langsung (dengan watchdog)
- **Network IDS:** Sniffer multi-interface, mirip Suricata
- **Statistik & Visualisasi:** Statistik otomatis, dashboard web real-time (FastAPI + Chart.js)
- **Rotating Logging:** Log otomatis bergulir
- **Notifikasi Desktop:** Opsional, via notify2
- **Konfigurasi Mudah:** Semua pola dan pengaturan di `config.json`
- **Unit Test:** Pengujian mudah dengan unittest

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
├── README.md
```

---

## 🏗️ Arsitektur Singkat

- **src/**: Implementasi utama IDS, IPS, logger, alert, dsb
- **dashboard/**: Backend FastAPI, frontend HTML/JS/CSS, WebSocket live feed
- **config.json**: Pola deteksi, pengaturan log, dsb
- **Log File**: Semua event dicatat ke `ids_ips.log` (default)

---

## ⚙️ Instalasi

1. **Pastikan Python 3.7+ dan pip sudah terpasang**
2. **Install dependensi:**
   ```bash
   pip install -r requirements.txt
   ```
3. **(Opsional) Install notifikasi desktop:**
   ```bash
   pip install notify2
   ```
4. **(Opsional) Untuk real-time monitoring:**
   ```bash
   pip install watchdog
   ```

---

## 📝 Konfigurasi

Edit `config.json` untuk menambah/mengubah pola deteksi, file log, dsb. Contoh:

```json
{
  "patterns": [
    {"name": "Failed password", "regex": "Failed password.*from ([\\d.]+)", "severity": "high"}
  ],
  "log_file": "ids_ips.log",
  "net_patterns": [
    {"name": "TCP SYN Scan", "type": "tcp_syn"}
  ]
}
```

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

### 3. IPS (Blokir IP Otomatis)
```bash
python ips_main.py config.json sample.log
```
Ganti `sample.log` dengan file log yang ingin Anda analisis.

### 4. Network IDS (Sniffer)
```bash
sudo python netids_main.py config.json
# Untuk memonitor interface tertentu:
sudo python netids_main.py config.json --iface <nama_interface>
# Contoh: sudo python netids_main.py config.json --iface enp3s0
# Catatan: Pastikan nama interface (misal eth0, enp3s0, wlan0) sesuai dengan yang ada di sistem Anda.
# Untuk melihat daftar interface, gunakan perintah: ip link
```

---

## 🌐 Dashboard Web (Real-time)

### Menjalankan Dashboard
```bash
uvicorn dashboard.app:app --reload
# Buka browser ke http://127.0.0.1:8000
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

---

## 📄 Lisensi

Proyek ini berlisensi MIT. Lihat file LICENSE untuk detail.

---

## 👨‍💻 Kontributor & Kredit

<div align="center">
  <b>Dikembangkan oleh: Bangkah</b><br>
  Kontribusi, saran, dan pull request sangat diterima!
</div>
