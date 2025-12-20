
# Panduan Kontribusi
## Good First Issue
- Tambahkan support untuk Alpine Linux
- Perbaiki deteksi backend firewall otomatis
- Tambahkan notifikasi via Telegram/Slack
- Tambahkan contoh serangan di DEMO.md
## Setup Dev Environment
1. Clone repo: `git clone https://github.com/Bangkah/IDS-IPS-Tool.git`
2. Buat virtualenv: `python3 -m venv .venv && source .venv/bin/activate`
3. Install dep: `pip install -r requirements.txt`
4. Jalankan test: `python -m unittest discover tests`
## Template Issue

**Deskripsi masalah/fitur:**

**Langkah reproduksi:**
1. ...
2. ...

**Log/error:**

**Lingkungan:**
- OS: ...
- Python: ...
## Template Pull Request

**Ringkasan perubahan:**

- [ ] Sudah lulus unit test
- [ ] Sudah update dokumentasi jika perlu
- [ ] Tidak ada merge conflict

Terima kasih ingin berkontribusi pada proyek IDS/IPS Tool!

## Cara Kontribusi
1. Fork repository ini
2. Buat branch baru untuk fitur/bugfix Anda
3. Commit perubahan dengan pesan yang jelas
4. Push branch ke fork Anda
5. Buat Pull Request ke repository utama

## Standar Kode
- Ikuti PEP8 untuk Python
- Tambahkan/memperbarui unit test di `tests/`
- Pastikan semua test lulus sebelum PR

## Laporan Bug & Fitur
- Gunakan tab Issues untuk melaporkan bug/fitur
- Sertakan langkah reproduksi dan log jika ada

## Komunikasi
- Bahasa: Indonesia/English
- Sopan dan profesional

Selamat berkontribusi!
