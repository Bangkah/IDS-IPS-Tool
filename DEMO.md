# DEMO: IDS/IPS Tool

Berikut adalah bukti nyata bahwa tools ini bekerja di lingkungan nyata.

---

## 1. Screenshot Output CLI

### Contoh: Blokir IP Sukses (IPS)

![Contoh Output CLI](assets/demo_block_ip.png)

```
[2025-12-21 00:00:01] [INFO] [IPS] Blokir IP 192.168.1.100 berhasil (backend: nftables)
```

### Contoh: Deteksi Serangan (IDS)

![Contoh Output CLI](assets/demo_ids_detect.png)

```
[2025-12-21 00:00:02] [ALERT] [IDS] Deteksi brute-force SSH dari 10.10.10.10
```

---

## 2. Contoh Log ids_ips.log

```
[2025-12-21 00:00:01] [INFO] [IPS] Blokir IP 192.168.1.100 berhasil (backend: nftables)
[2025-12-21 00:00:02] [ALERT] [IDS] Deteksi brute-force SSH dari 10.10.10.10
[2025-12-21 00:00:03] [INFO] [FIREWALL] Unblock IP 192.168.1.100 sukses
```

---

> Ingin menambah screenshot atau log lain? Kirimkan via pull request!
