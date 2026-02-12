# 🚀 AUTO CREATE TWITTER (ANDROID - APPIUM)

Automation tools untuk membuat akun Twitter/X menggunakan:

- Python
- Appium
- ADB
- Android Real Device
- Chrome
- Temporary Email (citayam.com)

---

# 📦 REQUIREMENTS

## 1️⃣ Install Python (3.10 – 3.11 Recommended)

Download:
https://www.python.org/downloads/

Cek versi:
python --version

---

## 2️⃣ Install NodeJS

Download:
https://nodejs.org/

Cek:
node -v
npm -v

---

## 3️⃣ Install Appium

Install global:
npm install -g appium

Install driver:
appium driver install uiautomator2

Cek driver:
appium driver list

---

## 4️⃣ Install Android Platform Tools (ADB) ⚠️ WAJIB

Download:
https://developer.android.com/tools/releases/platform-tools

Ekstrak misalnya ke:
C:\platform-tools

---

# ⚠️ PENTING — SET ENVIRONMENT VARIABLE ADB

Script menggunakan perintah:

adb shell cmd connectivity airplane-mode enable

Jika ADB tidak ada di PATH, akan error:

'adb' is not recognized as an internal or external command

## Cara Set PATH di Windows:

1. Tekan Windows + R
2. Ketik: sysdm.cpl
3. Masuk tab Advanced
4. Klik Environment Variables
5. Di System Variables cari: Path
6. Klik Edit
7. Klik New
8. Tambahkan:
   C:\platform-tools
9. Klik OK semua

Restart CMD / VS Code setelah itu.

Tes:

adb devices

Jika device muncul → berhasil.

---

# 🔄 ALTERNATIF TANPA SET PATH (OPSIONAL)

Jika tidak ingin set PATH, ubah script menjadi:

Tambahkan:

ADB_PATH = r"C:\platform-tools\adb.exe"

Lalu ubah perintah menjadi:

cmd_on = f'"{ADB_PATH}" -s {UDID_DEVICE} shell cmd connectivity airplane-mode enable'

---

## 5️⃣ Install Python Dependencies

Buat file requirements.txt:

pyfiglet
colorama
Appium-Python-Client
selenium

Install:

pip install -r requirements.txt

---

# 📱 SETTING ANDROID

Aktifkan:
- Developer Options
- USB Debugging
- Install via USB

Cek UDID:
adb devices

Ubah di script:

UDID_DEVICE = "ISI_UDID_KAMU"
DEVICE_NAME = "NAMA_DEVICE_KAMU"

---

# ▶️ CARA MENJALANKAN

## 1️⃣ Jalankan Appium Server

appium

Pastikan berjalan di:
http://127.0.0.1:4723

---

## 2️⃣ Jalankan Script

python 1.py

---

# ⚙️ FITUR

- Auto Install Twitter
- Auto Generate Email
- Auto Isi Biodata
- Auto Ambil OTP
- Auto Set Password
- Auto Skip Upload Foto
- Auto Save TXT
- Auto Detect Limit / Cloudflare
- Auto Refresh IP (Mode Pesawat)
- Loop Unlimited

---

# 📁 OUTPUT

File:
data_akun1.txt

Format:

Username : exampleuser
Email    : example@email.com
Password : ********
Tanggal  : 2026-02-12 10:22:33


----------------------------------------

---

# 📂 STRUKTUR PROJECT

AUTO-TWITTER/
│
├── 1.py
├── requirements.txt
└── README.md

---

# 🛠 TROUBLESHOOT

## Device Tidak Terdeteksi

adb kill-server
adb start-server
adb devices

---

## Appium Error

Cek:
appium driver list

Pastikan UiAutomator2 terinstall.

---
