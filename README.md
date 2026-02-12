# 🚀 AUTO TWITTER ACCOUNT CREATOR (ANDROID - APPIUM)

Tools automation untuk membuat akun Twitter/X secara otomatis menggunakan:

- ✅ Python
- ✅ Appium
- ✅ ADB
- ✅ Android Device (Real Device)
- ✅ Chrome
- ✅ Temporary Email (citayam.com)

---

# 📦 REQUIREMENTS (WAJIB INSTALL)

## 1️⃣ Install Python (Versi 3.10 – 3.11 Direkomendasikan)

Download:
https://www.python.org/downloads/

Cek versi:
python --version

---

## 2️⃣ Install NodeJS (Untuk Appium)

Download:
https://nodejs.org/

Cek versi:
node -v
npm -v

---

## 3️⃣ Install Appium

Install global:
npm install -g appium

Install driver UiAutomator2:
appium driver install uiautomator2

Cek driver:
appium driver list

---

## 4️⃣ Install Android Platform Tools (ADB)

Download:
https://developer.android.com/tools/releases/platform-tools

Tambahkan folder ke PATH.

Cek device:
adb devices

---

## 5️⃣ Install Dependencies Python

Buat file requirements.txt lalu isi:

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

Ubah di script bagian ini sesuai device kamu:

UDID_DEVICE = "ISI_DENGAN_UDID_KAMU"
DEVICE_NAME = "Nama Device Kamu"

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

# ⚙️ FITUR SCRIPT

✅ Auto Install Twitter jika belum ada  
✅ Auto Generate Email  
✅ Auto Isi Biodata  
✅ Auto Input OTP  
✅ Auto Set Password  
✅ Auto Skip Upload Foto  
✅ Auto Save Data ke TXT  
✅ Auto Detect Limit / Cloudflare  
✅ Auto Refresh IP (Mode Pesawat)  
✅ Loop Unlimited  

---

# 📁 OUTPUT FILE

File hasil tersimpan di:

data_akun1.txt

Format:

Username : exampleuser  
Email    : example@email.com  
Password : ********  
Tanggal  : 2026-02-12 10:22:33  
----------------------------------------

---

# 🔥 STRUKTUR PROJECT

AUTO-TWITTER/
│
├── 1.py
├── requirements.txt
└── README.md

---

# ⚠️ CATATAN PENTING

- Gunakan REAL DEVICE (lebih stabil dari emulator)
- Pastikan koneksi internet stabil
- Jika kena LIMIT → script auto refresh IP
- Jangan gunakan terlalu agresif

---

# 🛠 TROUBLESHOOT

## Device Tidak Terdeteksi

adb kill-server  
adb start-server  
adb devices  

---

## Appium Error

Pastikan:
appium driver list

Driver UiAutomator2 sudah terinstall.

---


