# ReDashboard Releases

Repository publik khusus untuk distribusi installer dan manifest pembaruan (`version.json`) aplikasi **ReDashboard** (Windows 10/11). Source code utama tetap berada di repository privat.

## Cara Publikasi Pertama Kali ke GitHub

Jalankan perintah berikut dari dalam folder `release-repo` ini (atau salin folder ini ke lokasi terpisah sebelum `git init`):

```powershell
git init -b main
git add .
git commit -m "Initial release manifest v0.1.0"
git remote add origin https://github.com/IchwanNurDwiYoga/redashboard-releases.git
git push -u origin main
```

Pastikan repository `IchwanNurDwiYoga/redashboard-releases` di GitHub disetel **Public** agar ReDashboard dapat membaca:
- `https://raw.githubusercontent.com/IchwanNurDwiYoga/redashboard-releases/main/version.json`
- `https://api.github.com/repos/IchwanNurDwiYoga/redashboard-releases/releases/latest`

## Alur Rilis Versi Baru

1. Naikkan `__version__` di `redashboard/__init__.py` (misal ke `0.2.0`).
2. Build installer baru `ReDashboard-Setup-0.2.0.exe`.
3. Perbarui `version.json` secara otomatis (termasuk hash SHA-256) menggunakan helper script:
   ```powershell
   python scripts/generate_version_manifest.py --version 0.2.0 --installer "path\to\ReDashboard-Setup-0.2.0.exe" --note "Perbaikan performa" --note "Fitur baru"
   ```
4. Buat GitHub Release baru dengan tag `v0.2.0` dan unggah `ReDashboard-Setup-0.2.0.exe` sebagai asset release.
5. Commit dan push `version.json` ke branch `main`.
