


# IDS/IPS Tool

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/github/license/Bangkah/IDS-IPS-Tool)
![CI](https://github.com/Bangkah/IDS-IPS-Tool/actions/workflows/python-package.yml/badge.svg)


Sistem modular untuk deteksi dan pencegahan serangan (IDS/IPS) berbasis Python. Mendukung analisis file log, monitoring real-time, dan network sniffer ala Suricata.

---

## Struktur Folder
```
ids_ips_tool/
├── src/                # Kode utama modular (IDS, IPS, logger, dsb)
│   ├── __init__.py
│   ├── alert.py
│   ├── config.py
│   ├── ids.py
│   ├── ips.py
│   ├── logger.py
├── tests/              # Unit test (unittest)
│   └── test_ids.py
├── ids_main.py         # Entrypoint IDS
├── ips_main.py         # Entrypoint IPS
├── netids_main.py      # Entrypoint Network IDS ala Suricata
├── config.json         # Konfigurasi pola deteksi
├── sample.log          # Contoh file log
└── README.md
```

## Fitur Utama
- Deteksi serangan dari file log (IDS)
- Pencegahan otomatis (IPS, blokir IP via iptables)
- Monitoring real-time file log (seperti antivirus)
- Network IDS (sniffer, Suricata-like, multi-interface)
- Statistik serangan otomatis
- Logging rotating, notifikasi desktop (opsional)
- Konfigurasi mudah via config.json
- Kode modular, siap dikembangkan

## Instalasi
## Membuat Release/Tag
Untuk menandai versi rilis:
```
git tag v1.0.0
git push origin v1.0.0
```
Atau gunakan fitur Release di GitHub.

1. Pastikan Python 3.7+ dan pip sudah terpasang
2. Install dependensi:
	 ```
	 pip install -r requirements.txt
	 ```
	 Atau manual:
	 ```
	 pip install scapy watchdog notify2
	 ```

## Konfigurasi
Edit `config.json` untuk menambah/mengubah pola deteksi:
```json
{
	"patterns": [
		{"name": "Failed password", "regex": "Failed password.*from ([\\d.]+)", "severity": "high"},
		{"name": "Invalid user", "regex": "Invalid user.*from ([\\d.]+)", "severity": "medium"},
		{"name": "Port scan", "regex": "Possible port scan.*from ([\\d.]+)", "severity": "low"}
	],
	"log_file": "ids_ips.log",
	"net_patterns": [
		{"name": "TCP SYN Scan", "type": "tcp_syn"},
		{"name": "ICMP Echo", "type": "icmp_echo"}
	]
}
```

## Cara Menjalankan

### IDS (Analisis File Log)
```
python ids_main.py config.json sample.log
```

### IDS Real-time (Seperti Antivirus)
```
python ids_main.py config.json /var/log/auth.log --realtime
```

### IPS (Blokir IP Otomatis)
```
python ips_main.py config.json sample.log
```

### Network IDS (Sniffer, Suricata-like)
```
sudo python netids_main.py config.json
```
Opsional: pilih interface tertentu dengan --iface (misal eth0, wlan0)
```
sudo python netids_main.py config.json --iface eth0
```

## Pengujian
Semua kode utama sudah dilengkapi unit test:
```
python -m unittest discover tests
```
CI/CD otomatis menjalankan test di setiap push/PR (lihat badge di atas).
```
python -m unittest discover tests
```

## Kustomisasi & Pengembangan
## Dokumentasi Lanjutan
- **FAQ:**
	- Q: Bagaimana menambah pola deteksi?  
		A: Edit `config.json` bagian `patterns` atau `net_patterns`.
	- Q: Apakah bisa menambah notifikasi lain?  
		A: Ya, modifikasi `src/alert.py`.
	- Q: Bagaimana menambah test?  
		A: Tambahkan file `test_*.py` di folder `tests/`.
- **Panduan Kontribusi:** Lihat CONTRIBUTING.md
- **Lisensi:** MIT (lihat LICENSE)
- Tambahkan pola deteksi di `config.json`
- Ubah log file di `config.json`
- Kembangkan src/ids.py, src/ips.py, src/netids.py untuk fitur baru (notifikasi, integrasi SIEM, dsb)
- Tambahkan unit test di folder `tests/`

## Catatan
- Untuk notifikasi desktop, pastikan `notify2` terinstall (`pip install notify2`)
- Untuk real-time, pastikan `watchdog` terinstall (`pip install watchdog`)
- Untuk network IDS, butuh akses root/sudo.
- Statistik serangan otomatis muncul saat Anda menekan Ctrl+C.
- Logging otomatis rotating, log lama tidak hilang.

---
Dikembangkan oleh: Tim Cyber Security & Bangkah

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
