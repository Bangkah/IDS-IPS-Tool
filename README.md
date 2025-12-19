


# IDS/IPS Tool

![Python](https://img.shields.io/badge/python-3.7%2B-blue) ![License](https://img.shields.io/github/license/Bangkah/IDS-IPS-Tool) ![CI](https://github.com/Bangkah/IDS-IPS-Tool/actions/workflows/python-package.yml/badge.svg)

Sistem modular deteksi & pencegahan serangan (IDS/IPS) berbasis Python. Mendukung analisis file log, monitoring real-time, dan network sniffer (Suricata-like).

---

## Fitur Utama
- Deteksi serangan dari file log (IDS)
- Pencegahan otomatis (IPS, blokir IP via iptables)
- Monitoring real-time file log
- Network IDS (sniffer, multi-interface)
- Statistik serangan otomatis
- Logging rotating, notifikasi desktop (opsional)
- Konfigurasi mudah via config.json

## Struktur Proyek
```
ids_ips_tool/
├── src/           # Kode utama modular (IDS, IPS, logger, dsb)
├── tests/         # Unit test
├── ids_main.py    # Entrypoint IDS
├── ips_main.py    # Entrypoint IPS
├── netids_main.py # Entrypoint Network IDS
├── config.json    # Konfigurasi pola deteksi
├── README.md
```

## Instalasi
1. Pastikan Python 3.7+ dan pip sudah terpasang
2. Install dependensi:
   ```
   pip install -r requirements.txt
   ```

## Konfigurasi
Edit `config.json` untuk menambah/mengubah pola deteksi. Contoh:
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

## Cara Menjalankan

### IDS (Analisis File Log)
```bash
python ids_main.py config.json sample.log
```


### IDS Real-time (Seperti Antivirus)
```bash
python ids_main.py config.json /var/log/auth.log --realtime
```
> **Catatan:** Pastikan file log yang dimonitor benar-benar ada. Jika file tidak ditemukan, gunakan file log lain yang tersedia, misal sample.log atau log lain yang ingin Anda monitor.

### IPS (Blokir IP Otomatis)
```bash
python ips_main.py config.json sample.log
```
Ganti `sample.log` dengan file log yang ingin Anda analisis.

### Network IDS (Sniffer)
```bash
sudo python netids_main.py config.json
# Untuk memonitor interface tertentu:
sudo python netids_main.py config.json --iface <nama_interface>
# Contoh: sudo python netids_main.py config.json --iface enp3s0
# Catatan: Pastikan nama interface (misal eth0, enp3s0, wlan0) sesuai dengan yang ada di sistem Anda.
# Untuk melihat daftar interface, gunakan perintah: ip link
```

## Pengujian
```bash
python -m unittest discover tests
```

## Kustomisasi
- Tambahkan pola deteksi di `config.json`
- Ubah log file di `config.json`
- Kembangkan src/ids.py, src/ips.py, src/netids.py untuk fitur baru (notifikasi, integrasi SIEM, dsb)
- Tambahkan unit test di folder `tests/`

## FAQ
- **Bagaimana menambah pola deteksi?**  
  Edit `config.json` bagian `patterns` atau `net_patterns`.
- **Apakah bisa menambah notifikasi lain?**  
  Ya, modifikasi `src/alert.py`.
- **Bagaimana menambah test?**  
  Tambahkan file `test_*.py` di folder `tests/`.

## Catatan
- Untuk notifikasi desktop, pastikan `notify2` terinstall (`pip install notify2`)
- Untuk real-time, pastikan `watchdog` terinstall (`pip install watchdog`)
- Untuk network IDS, butuh akses root/sudo
- Statistik serangan otomatis muncul saat Ctrl+C
- Logging otomatis rotating

---

---

<div align="center">
  <b>Dikembangkan oleh: Bangkah</b>
</div>
