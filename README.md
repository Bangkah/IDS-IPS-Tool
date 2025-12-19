

# IDS/IPS Tool

![Python](https://img.shields.io/badge/python-3.7%2B-blue) ![License](https://img.shields.io/github/license/Bangkah/IDS-IPS-Tool) ![CI](https://github.com/Bangkah/IDS-IPS-Tool/actions/workflows/python-package.yml/badge.svg)

Sistem modular deteksi & pencegahan serangan (IDS/IPS) berbasis Python. Mendukung analisis file log, monitoring real-time, dan network sniffer (Suricata-like).



## Struktur Folder
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


## Fitur Utama
- Deteksi serangan dari file log (IDS)
- Pencegahan otomatis (IPS, blokir IP via iptables)
- Monitoring real-time file log
- Network IDS (sniffer, multi-interface)
- Statistik serangan otomatis
- Logging rotating, notifikasi desktop (opsional)
- Konfigurasi mudah via config.json


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
	python ids_main.py config.json sample.log

### IDS Real-time
	python ids_main.py config.json /var/log/auth.log --realtime

### IPS (Blokir IP Otomatis)
	python ips_main.py config.json sample.log

### Network IDS (Sniffer)
	sudo python netids_main.py config.json
	# Pilih interface: sudo python netids_main.py config.json --iface eth0


## Pengujian
	python -m unittest discover tests


## Kustomisasi & FAQ
- Tambahkan pola deteksi di `config.json`
- Ubah log file di `config.json`
- Kembangkan src/ids.py, src/ips.py, src/netids.py untuk fitur baru (notifikasi, integrasi SIEM, dsb)
- Tambahkan unit test di folder `tests/`

**FAQ:**
- Bagaimana menambah pola deteksi?  
  Edit `config.json` bagian `patterns` atau `net_patterns`.
- Apakah bisa menambah notifikasi lain?  
  Ya, modifikasi `src/alert.py`.
- Bagaimana menambah test?  
  Tambahkan file `test_*.py` di folder `tests/`.


## Catatan
- Untuk notifikasi desktop, pastikan `notify2` terinstall
- Untuk real-time, pastikan `watchdog` terinstall
- Untuk network IDS, butuh akses root/sudo
- Statistik serangan otomatis muncul saat Ctrl+C
- Logging otomatis rotating

---
Dikembangkan oleh: Bangkah & Tim Cyber Security

## Struktur Folder
```
ids_ips_tool/
├── src/
│   ├── config.py
│   ├── ids.py
│   ├── ips.py
│   ├── logger.py
│   └── alert.py
├── ids.py (legacy)
├── ips.py (legacy)
├── ids_main.py
├── ips_main.py
├── netids_main.py
├── config.json
├── sample.log
└── README.md
```

## Menjalankan IDS
```
python ids_main.py config.json sample.log
```

### Mode Real-time (Seperti Antivirus)
```
python ids_main.py config.json /var/log/auth.log --realtime
```

## Menjalankan IPS
```
python ips_main.py config.json sample.log
```

## Menjalankan Network IDS (Sniffer, Suricata-like)
```
sudo python netids_main.py config.json
```
Opsional: pilih interface tertentu dengan --iface (misal eth0, wlan0)
```
sudo python netids_main.py config.json --iface eth0
```

## Pengujian
```
python -m unittest discover tests
```

## Kustomisasi
- Tambahkan pola deteksi di `config.json`
- Ubah log file di `config.json`
- Kembangkan src/ids.py atau src/ips.py untuk fitur baru (notifikasi, integrasi IPS, dsb)

## Catatan
- File di src/ adalah kode utama (modular, siap dikembangkan).
- File legacy (ids.py, ips.py) bisa dihapus jika sudah tidak dipakai.
- Semua log dan blokir IP dicatat otomatis.
- Untuk notifikasi desktop, pastikan `notify2` terinstall (`pip install notify2`)
- Untuk real-time, pastikan `watchdog` terinstall (`pip install watchdog`)
- Untuk network IDS, butuh akses root/sudo.
- Statistik serangan otomatis muncul saat Anda menekan Ctrl+C.
- Logging otomatis rotating, log lama tidak hilang.

---
Dikembangkan oleh: Bangkah
