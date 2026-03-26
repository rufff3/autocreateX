import pyfiglet
from colorama import Fore, Style, init
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import random
import re
import subprocess
import sys
import os
import requests
import string

init(autoreset=True)

BANNER_JUDUL = "AUTO   TWITTER"
BANNER_NAMA  = "Tools By : Ruff"
ID_TWITTER = "com.twitter.android"
PASSWORD_AKUN = "CONTOH" #atur pasword tiap akun
NAMA_FILE_HASIL = "CONTOH.TXT" #nama file output akun berhasil 
BLACKLIST_OTP = ["2024", "2025", "2026", "2023", "123456", "000000"]
API_KEY = "" #ISI APIKEY DENGAN ANDA MENUJU LINK CITAYAM.COM DAN MEMINTA API KEY
UDID_DEVICE = ""  #UID DEVICE SETELAH MENJALANKAN PERINTAH ADB DEVICES
DEVICE_NAME = 'Redmi Note 14 Pro' #gapenting

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"

options = UiAutomator2Options()
options.platform_name = 'Android'
options.automation_name = 'UiAutomator2'
options.device_name = DEVICE_NAME
options.udid = UDID_DEVICE
options.no_reset = False 
options.auto_grant_permissions = False
options.set_capability("ignoreHiddenApiPolicyError", True)
options.set_capability("noSign", True)
options.set_capability("newCommandTimeout", 600)
options.set_capability("waitForIdleTimeout", 100)
options.set_capability("adbExecTimeout", 60000)
options.set_capability("uiautomator2ServerInstallTimeout", 60000)

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    font_judul = pyfiglet.figlet_format(BANNER_JUDUL, font="slant", width=100)
    print(Fore.CYAN + Style.BRIGHT + font_judul)
    font_nama = pyfiglet.figlet_format(BANNER_NAMA, font="slant", width=100)
    print(Fore.YELLOW + Style.BRIGHT + font_nama)
    print("\n")

def get_random_name():
    depan = ["Rudi", "Bayu", "Eko", "Dina", "Siti", "Reza", "Fajar", "Adit", "Gilang", "Putri", "Dewi", "Budi", "Sari", "Indra", "Maya", "saikul", "Rizky", "Nina", "Agus", "Lina", "Hendra", "Dian", "Yudi", "Rina", "Fauzi", "Siska", "Andi", "Wulan", "Eka", "Rama", "Sinta", "Doni", "Mira", "Hadi", "Rani", "Fikri", "Sari", "Ilham", "Nia", "Bambang", "Dina", "Rizal", "Sari", "Yanto", "Lina", "Hendra", "Dian", "Yudi", "Rina", "Fauzi", "Siska", "Andi", "Wulan"]
    belakang = ["Santoso", "Pratama", "Wijaya", "Kusuma", "Saputra", "Hidayat", "Siregar", "Utami", "Nugroho", "Wibowo", "Subagja", "Ramadhan", "pebrianto", "Putra", "Lestari", "Gunawan", "Sari", "Purnama", "Kurniawan", "Dewi", "Saputro", "Yuliana", "Fadhil", "Amelia", "Hidayah", "Prasetyo", "Sari", "Wahyudi", "Aulia"]
    return f"{random.choice(depan)} {random.choice(belakang)}"

def simpan_akun_ke_txt(username, email):
    user_clean = str(username).replace("\n", "").strip()
    if not user_clean or user_clean == "None" or user_clean == "Akun_Baru":
        user_clean = email.split('@')[0] + str(random.randint(10,99))
    print(f"\n{CYAN}>> 💾 MENYIMPAN DATA KE {NAMA_FILE_HASIL}...{RESET}")
    try:
        with open(NAMA_FILE_HASIL, "a", encoding='utf-8') as f:
            f.write(f"Username : {user_clean}\n")
            f.write(f"Email    : {email}\n")
            f.write(f"Password : {PASSWORD_AKUN}\n")
            f.write(f"Tanggal  : {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("----------------------------------------\n")
        print(f"{GREEN}>> ✅ DATA BERHASIL DISIMPAN! (User: {user_clean}){RESET}")
    except Exception as e:
        print(f"{RED}❌ Gagal Simpan File: {e}{RESET}")

def tutup_popup_google_smart_lock(driver):
    print(f"{YELLOW}>> 🔒 Cek Popup Google Smart Lock...{RESET}")
    try:
        tombol_x = driver.find_elements(AppiumBy.XPATH, "//*[contains(@content-desc, 'Close') or contains(@resource-id, 'cancel') or contains(@resource-id, 'close_button')]")
        if tombol_x:
            tombol_x[0].click()
            print(f"{GREEN}>> ✅ Popup Google Ditutup.{RESET}")
            time.sleep(1)
            return
        ada_popup = driver.find_elements(AppiumBy.XPATH, "//*[contains(@text, 'Pilih akun') or contains(@text, 'Choose an account') or contains(@resource-id, 'credential_picker_layout')]")
        if ada_popup:
            print(f"{YELLOW}>> ⚠️ Popup Smart Lock Asli terdeteksi! Tekan Back...{RESET}")
            driver.press_keycode(4)
            time.sleep(2)
            driver.activate_app(ID_TWITTER)
    except: pass

def tolak_perizinan(driver):
    print(f"{YELLOW}>> 🛡️ Menunggu Popup Perizinan (4 detik)...{RESET}")
    time.sleep(4) 
    try:
        xpath_tolak = "//*[contains(@resource-id, 'permission_deny_button') or contains(@resource-id, 'button2') or contains(@text, 'Jangan') or contains(@text, 'Tolak') or contains(@text, 'Deny') or contains(@text, 'Tidak')]"
        for i in range(3): 
            try:
                tombol_tolak = driver.find_elements(AppiumBy.XPATH, xpath_tolak)
                if tombol_tolak:
                    print(f"{RED}>> ⛔ Menolak Perizinan! (Percobaan {i+1}){RESET}")
                    tombol_tolak[0].click()
                    time.sleep(2)
                    return 
            except: pass
            time.sleep(1)    
    except Exception as e:
        print(f"{RED}❌ Gagal handle perizinan (Skip): {e}{RESET}")

def refresh_ip_mode_pesawat(driver):
    print(f"\n{RED}>> ✈️ TERDETEKSI ERROR/LIMIT/CLOUDFLARE! MEMULAI REFRESH IP (MODERN)...{RESET}")
    try:
        print(f"{YELLOW}>> ✈️ Mengaktifkan Mode Pesawat...{RESET}")
        cmd_on = f'adb -s {UDID_DEVICE} shell cmd connectivity airplane-mode enable'
        subprocess.run(cmd_on, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{YELLOW}>> ⏳ Tunggu 5 detik...{RESET}")
        time.sleep(5) 
        print(f"{GREEN}>> 📡 Mematikan Mode Pesawat (Reconnect)...{RESET}")
        cmd_off = f'adb -s {UDID_DEVICE} shell cmd connectivity airplane-mode disable'
        subprocess.run(cmd_off, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{YELLOW}>> ⏳ Menunggu sinyal 8 detik...{RESET}")
        time.sleep(8)
    except Exception as e:
        print(f"{RED}❌ Gagal Mode Pesawat: {e}{RESET}")

def pastikan_pindah_aplikasi(driver, package_id):
    print(f"{YELLOW}>> 🔄 Mengecek posisi aplikasi ({package_id})...{RESET}")
    for i in range(3):
        try:
            current = driver.current_package
            if current == package_id: return True
            driver.activate_app(package_id)
            time.sleep(2)
        except: pass
    return False

def cek_dan_install_twitter(driver, wait):
    print(f"\n{CYAN}[SYSTEM] Mengecek keberadaan Twitter/X...{RESET}")
    if driver.is_app_installed(ID_TWITTER):
        print(f"{GREEN}>> ✅ Twitter sudah terinstal. Lanjut...{RESET}")
        return True 
    print(f"{YELLOW}>> ⚠️ Twitter TIDAK ADA! (Auto Install via Play Store...).{RESET}")
    try:
        driver.execute_script("mobile: deepLink", {"url": "market://details?id=com.twitter.android", "package": "com.android.vending"})
    except: return False 
    time.sleep(5)
    try:
        tombol = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@text, 'Install') or contains(@text, 'Instal') or contains(@text, 'Update')]")))
        tombol.click()
        print(f"{YELLOW}>> ⬇️ Sedang Menginstall... (Tunggu maks 3 menit){RESET}")
    except: pass  
    for i in range(60):
        if driver.is_app_installed(ID_TWITTER):
            print(f"{GREEN}>> ✅ INSTALL SUKSES!{RESET}")
            time.sleep(3)
            return True
        time.sleep(3)
    return False

DOMAIN_TERLARANG = ["motormio.com", "wedansmail.com"]

def ambil_email_api():
    print(f"{YELLOW}>> ⏳ Meminta domain dari API Citayam...{RESET}")
    url_domain = f"https://citayam.com/api/domains/{API_KEY}"
    try:
        response = requests.get(url_domain, timeout=10)
        data_domain = response.json()
        domain_pilihan = "citayam.com" 
        if isinstance(data_domain, list) and len(data_domain) > 0:
            domain_aman = [d for d in data_domain if d not in DOMAIN_TERLARANG]
            if len(domain_aman) > 0:
                domain_pilihan = random.choice(domain_aman) 
            else:
                print(f"{YELLOW}>> ⚠️ Semua domain dari API dilarang! Memakai default.{RESET}")
        karakter_pilihan = string.ascii_lowercase + string.digits
        nama_acak = ''.join(random.choices(karakter_pilihan, k=10))
        email_baru = f"{nama_acak}@{domain_pilihan}"
        print(f"{GREEN}>> ✅ EMAIL BARU DIDAPAT (API): {email_baru}{RESET}")
        return email_baru
    except Exception as e:
        print(f"{RED}❌ Gagal mengambil domain via API: {e}{RESET}")
        return None

def ambil_otp_api(email_target):
    print(f"\n{CYAN}>> 🚀 MENUNGGU OTP VIA API UNTUK: {email_target}...{RESET}")
    url_pesan = f"https://citayam.com/api/messages/{email_target}/{API_KEY}"
    start_time = time.time()
    pesan_dibaca = []
    while time.time() - start_time < 60: 
        try:
            response = requests.get(url_pesan, timeout=10)
            data_pesan = response.json()
            if isinstance(data_pesan, list) and len(data_pesan) > 0:
                for pesan in data_pesan:
                    pesan_id = pesan.get('id')
                    if pesan_id not in pesan_dibaca:
                        isi_teks = str(pesan.get('subject', '')) + " " + str(pesan.get('body', ''))
                        match = re.search(r'\b\d{6}\b', isi_teks)
                        if match:
                            kode = match.group(0)
                            if kode not in BLACKLIST_OTP and not kode.startswith("100"):
                                print(f"{GREEN}>> ✅ OTP DITEMUKAN (API): {kode}{RESET}")
                                return kode
                        pesan_dibaca.append(pesan_id)
        except Exception as e:
            pass 
        time.sleep(5) 
    print(f"{RED}❌ OTP tidak kunjung masuk via API (Timeout).{RESET}")
    return None

def cek_limit_jumlah_akun_dan_uninstall(driver):
    print(f"{YELLOW}>> 🔍 Cek Limit / Cloudflare...{RESET}")
    time.sleep(1.5)
    try:
        xpath_limit = "//*[contains(@text, 'melampaui batas') or contains(@text, 'exceeded') or contains(@text, 'mencapai batas') or contains(@text, 'kesalahan teknis') or contains(@text, 'coba lagi nanti') or contains(@text, 'Buktikan bahwa Anda adalah manusia') or contains(@text, 'Verify you are human')]"
        limit_msgs = driver.find_elements(AppiumBy.XPATH, xpath_limit)
        for msg in limit_msgs:
            try:
                if msg.is_displayed():
                    print(f"\n{RED}>> ⛔ LIMIT / CLOUDFLARE TERDETEKSI (VALID)!{RESET}")
                    print(f"{RED}>> 🗑️ UNINSTALL TWITTER...{RESET}")
                    try: driver.remove_app(ID_TWITTER)
                    except: pass
                    time.sleep(5)
                    return True
            except: pass   
    except: pass
    return False

def klik_tombol_buat_akun_seperti_hp_kosong(driver, wait):
    print(f"{CYAN}>> [HP KOSONG] Mencari tombol 'Buat Akun'...{RESET}")
    try:
        driver.find_element(AppiumBy.XPATH, "//*[contains(@text, 'Create account') or contains(@text, 'Buat akun')]").click()
        print(f"{GREEN}>> ✅ Sukses Klik Tombol Depan{RESET}")
    except:
        try:
            uk = driver.get_window_size()
            driver.tap([(int(uk['width']*0.5), int(uk['height']*0.85))])
        except Exception as e: return False
    time.sleep(2)
    return cek_limit_jumlah_akun_dan_uninstall(driver)

def buka_form_pendaftaran(driver, wait):
    if not cek_dan_install_twitter(driver, wait): return False
    print(f"\n{CYAN}[APP] Membuka Aplikasi Twitter...{RESET}")
    driver.activate_app(ID_TWITTER)
    time.sleep(10)
    tutup_popup_google_smart_lock(driver) 
    tolak_perizinan(driver) 
    print(f"{YELLOW}>> 🔍 Mengecek apakah ini Halaman Awal (Fresh Install)?{RESET}")
    try:
        tombol_buat_akun_awal = driver.find_elements(AppiumBy.XPATH, "//*[contains(@text, 'Create account') or contains(@text, 'Buat akun') or contains(@text, 'See what') or contains(@text, 'Lihat apa')]")
        if tombol_buat_akun_awal:
            print(f"{GREEN}>> 🆕 Terdeteksi Halaman Awal! (Aman){RESET}")
        else:
            print(f"{YELLOW}>> 🏠 Halaman Awal TIDAK ADA. Asumsi sedang LOGIN...{RESET}")
            print(f"{YELLOW}>> 👊 Force Click HOME (Anti-Grok)...{RESET}")
            try:
                tombol_home = driver.find_elements(AppiumBy.XPATH, "//android.widget.FrameLayout[@content-desc='Home' or @content-desc='Beranda'] | //*[contains(@resource-id, 'home_tab')]")
                if tombol_home:
                    tombol_home[0].click()
                    print(f"{GREEN}>> ✅ Sukses Klik Home. Posisi Netral.{RESET}")
                    time.sleep(3)
            except: pass
    except: pass
    sudah_login = False
    try:
        indicators = [
            "Show navigation drawer", 
            "//android.widget.FrameLayout[@content-desc='Home']", 
            "//android.widget.FrameLayout[@content-desc='Beranda']",
            "//*[contains(@resource-id, 'composer_write')]",
            "//*[contains(@text, 'Untuk Anda')]",
            "//*[contains(@text, 'For You')]"
        ]
        for ind in indicators:
            if "Slash" in ind or "//" in ind:
                if driver.find_elements(AppiumBy.XPATH, ind):
                    sudah_login = True; break
            else:
                if driver.find_elements(AppiumBy.ACCESSIBILITY_ID, ind):
                    sudah_login = True; break
    except Exception as e:
        if "instrumentation" in str(e).lower(): return False 
    if sudah_login:
        print(f"{YELLOW}>> [NAVIGASI] Status: SUDAH LOGIN (Di Menu Home). OTW Tambah Akun...{RESET}")
        try:            
            print(f"{CYAN}>> Klik Profil (Kiri Atas)...{RESET}")
            try:
                try: 
                    driver.find_element(AppiumBy.XPATH, "//*[contains(@content-desc, 'Tampilkan penarik navigasi') or contains(@content-desc, 'Show navigation drawer')]").click()
                except: 
                    uk = driver.get_window_size()
                    driver.tap([(int(uk['width']*0.09), int(uk['height']*0.09))])
            except: pass
            time.sleep(2)
            tutup_popup_google_smart_lock(driver)
            print(f"{CYAN}>> Klik Menu Switcher (Titik Tiga)...{RESET}")
            try:
                wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[contains(@content-desc, 'Pindah akun') or contains(@resource-id, 'user_switcher')]"))).click()
            except:
                uk = driver.get_window_size()
                driver.tap([(int(uk['width']*0.72), int(uk['height']*0.11))])
            time.sleep(2)
            print(f"{CYAN}>> Klik 'Buat akun baru' (Menu Bawah)...{RESET}")
            try:
                wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[contains(@text, 'Buat akun baru') or contains(@text, 'Create a new account')]"))).click()
            except:
                uk = driver.get_window_size()
                driver.tap([(int(uk['width']*0.5), int(uk['height']*0.78))])
            time.sleep(5)
            if cek_limit_jumlah_akun_dan_uninstall(driver): return "LIMIT"
            if klik_tombol_buat_akun_seperti_hp_kosong(driver, wait): return "LIMIT"
        except Exception as e: 
            print(f"{RED}❌ Gagal Navigasi Login: {e}{RESET}")
            return False         
    else:
        print(f"{YELLOW}>> [NAVIGASI] Status: BELUM LOGIN. Klik tombol depan...{RESET}")
        if klik_tombol_buat_akun_seperti_hp_kosong(driver, wait): return "LIMIT"
    print(f"{YELLOW}>> ⏳ Menunggu Form...{RESET}")
    try:
        wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))
        print(f"{GREEN}>> ✅ FORM SIAP DIISI!{RESET}")
        return True
    except: return False

def tekan_tombol_lanjut_pendaftaran(driver, wait):
    print(f"{CYAN}>> [LIVE] Cari tombol Lanjut...{RESET}")
    try: driver.hide_keyboard()
    except: pass
    time.sleep(2)
    for text in ["Next", "Berikutnya", "Lanjut", "Sign up", "Daftar"]:
        try:
            driver.find_element(AppiumBy.XPATH, f"//*[contains(@text, '{text}')]").click()
            print(f"{GREEN}>> ✅ Klik: {text}{RESET}"); return True
        except: continue
    try: driver.press_keycode(66)
    except: pass
    return True

def atur_tanggal_lahir_scroll_bawah(driver):
    print(f"{CYAN}>> 📅 Mengatur Tanggal Lahir...{RESET}")
    try: driver.hide_keyboard()
    except: pass
    time.sleep(2) 
    try:
        try: driver.find_element(AppiumBy.ID, "com.twitter.android:id/birthday_edit_text").click()
        except: driver.find_element(AppiumBy.XPATH, "//*[contains(@text, 'Date') or contains(@text, 'Tanggal')]").click()
        time.sleep(2)
        try: driver.find_element(AppiumBy.ID, "android:id/date_picker_header_year").click()
        except: pass
        time.sleep(1)
        uk = driver.get_window_size()
        driver.swipe(int(uk['width'] * 0.5), int(uk['height'] * 0.4), int(uk['width'] * 0.5), int(uk['height'] * 0.8), 250)
        time.sleep(2)
        target_tahun = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008"]
        berhasil_pilih = False
        for th in target_tahun:
            try:
                driver.find_element(AppiumBy.XPATH, f"//*[contains(@text, '{th}')]").click()
                print(f"{GREEN}>> ✅ Tahun {th} terpilih!{RESET}")
                berhasil_pilih = True; break
            except: pass
        if not berhasil_pilih:
            driver.tap([(int(uk['width']*0.5), int(uk['height']*0.55))])
        time.sleep(1)
        try: driver.find_element(AppiumBy.ID, "android:id/button1").click()
        except: driver.tap([(int(uk['width']*0.85), int(uk['height']*0.7))])
        print(f"{GREEN}>> ✅ Tanggal Lahir Selesai.{RESET}")
        return True 
    except Exception as e: 
        print(f"{RED}⚠️ Gagal atur tanggal: {e}{RESET}")
        return False

def isi_biodata_pintar(driver, wait, name_text, email_text):
    print(f"{CYAN}>> [FORM] Memulai pengisian cerdas...{RESET}")
    try:
        tombol_email = driver.find_elements(AppiumBy.XPATH, "//*[contains(@text, 'email')]")
        if tombol_email:
            print(f"{YELLOW}>> ⚠️ Terdeteksi mode HP, ganti ke Email...{RESET}")
            tombol_email[0].click(); time.sleep(2)
    except: pass
    try:
        kolom_isian = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        if len(kolom_isian) >= 2:
            print(f"{CYAN}>> 📝 Mengisi Nama & Email...{RESET}")
            kolom_isian[0].click(); time.sleep(1); kolom_isian[0].send_keys(name_text)
            try: driver.hide_keyboard()
            except: pass
            kolom_isian[1].click(); time.sleep(1); kolom_isian[1].send_keys(email_text)
            try: driver.hide_keyboard()
            except: pass
        else:
            driver.find_element(AppiumBy.XPATH, "(//android.widget.EditText)[1]").send_keys(name_text)
            driver.find_element(AppiumBy.XPATH, "(//android.widget.EditText)[2]").send_keys(email_text)
    except: pass
    time.sleep(1)
    if not atur_tanggal_lahir_scroll_bawah(driver):
        return False 
    return True 

def main():
    print_banner()
    counter = 1
    fail_count = 0  
    while True:
        print(f"\n\n{CYAN}=== MEMBUAT AKUN KE - {counter} ==={RESET}")
        driver = None
        try:
            if fail_count >= 3:
                print(f"\n{RED}>> ⚠️ TERDETEKSI 3x GAGAL BERTURUT-TURUT! UNINSTALL & RESET...{RESET}")
                try:
                    temp_driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
                    try:
                        temp_driver.remove_app(ID_TWITTER)
                        print(f"{GREEN}>> ✅ Twitter Berhasil Di-uninstall.{RESET}")
                    except Exception as e:
                        print(f"{RED}❌ Gagal Uninstall: {e}{RESET}")
                    finally:
                        temp_driver.quit()
                except Exception as e:
                    print(f"{RED}❌ Gagal Init Driver untuk Uninstall: {e}{RESET}")
                fail_count = 0
                time.sleep(5)
            print(f"{YELLOW}>> 🔄 Memulai Driver Baru...{RESET}")
            driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
            wait = WebDriverWait(driver, 60)
            email = ambil_email_api()
            if not email: 
                if driver: driver.quit()
                fail_count += 1 
                print(f"{RED}>> ⚠️ KEGAGALAN KE-{fail_count} DARI 3{RESET}")
                continue
            status_nav = buka_form_pendaftaran(driver, wait)
            if status_nav == "LIMIT":
                print(f"{RED}⚠️ LIMIT TERDETEKSI (AWAL) - MODPES & RESTART...{RESET}")
                refresh_ip_mode_pesawat(driver) 
                if driver: driver.quit()
                fail_count += 1 
                print(f"{RED}>> ⚠️ KEGAGALAN KE-{fail_count} DARI 3{RESET}")
                continue 
            if not status_nav: 
                print(f"{RED}❌ Navigasi gagal.{RESET}")
                refresh_ip_mode_pesawat(driver)
                if driver: driver.quit()
                fail_count += 1 
                print(f"{RED}>> ⚠️ KEGAGALAN KE-{fail_count} DARI 3{RESET}")
                continue
            print(f"\n{CYAN}>> [TWITTER] Mengisi form...{RESET}")
            pastikan_pindah_aplikasi(driver, ID_TWITTER)
            if not isi_biodata_pintar(driver, wait, get_random_name(), email):
                print(f"{RED}❌ Gagal Mengisi Biodata / Tanggal.{RESET}")
                refresh_ip_mode_pesawat(driver)
                if driver: driver.terminate_app(ID_TWITTER)
                fail_count += 1 
                print(f"{RED}>> ⚠️ KEGAGALAN KE-{fail_count} DARI 3{RESET}")
                continue
            time.sleep(2)
            tekan_tombol_lanjut_pendaftaran(driver, wait)
            if cek_limit_jumlah_akun_dan_uninstall(driver):
                print(f"{RED}⚠️ LIMIT/CLOUDFLARE TERDETEKSI (BIODATA) - MODPES & RESTART...{RESET}")
                refresh_ip_mode_pesawat(driver)
                if driver: driver.quit()
                fail_count += 1 
                continue
            print(f"\n{RED}>> 🛑 TAHAN! Menunggu Loading Layar Hitam (10 detik)...{RESET}")
            time.sleep(10)
            print(f"{YELLOW}>> 🔍 Mengecek halaman OTP...{RESET}")
            otp_page = False
            for _ in range(5):
                try:
                    if driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText"): 
                        otp_page = True; break
                except: pass
                time.sleep(2)
            if not otp_page:
                print(f"{YELLOW}⚠️ Belum masuk OTP, tekan Lanjut sekali lagi...{RESET}")
                tekan_tombol_lanjut_pendaftaran(driver, wait)
                time.sleep(5)
            otp = ambil_otp_api(email)
            if otp:
                print(f"\n{GREEN}>> [TWITTER] Menginput Kode: {otp}{RESET}")
                time.sleep(2)
                try:
                    kode_box = wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))
                    kode_box.click(); kode_box.send_keys(otp)
                    try: driver.hide_keyboard()
                    except: pass
                    time.sleep(2)
                    tekan_tombol_lanjut_pendaftaran(driver, wait)
                    print(f"{YELLOW}>> ⏳ Tunggu loading halaman Password (5 detik)...{RESET}")
                    time.sleep(5)
                    print(f"{CYAN}>> Mengisi Password...{RESET}")
                    pass_box = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((AppiumBy.CLASS_NAME, "android.widget.EditText")))
                    pass_box.click()
                    pass_box.send_keys(PASSWORD_AKUN)
                    time.sleep(1)
                    tekan_tombol_lanjut_pendaftaran(driver, wait)
                    print(f"{YELLOW}>> ⏳ Finishing (Upload Foto)...{RESET}")
                    WebDriverWait(driver, 30).until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@text, 'upload') or contains(@text, 'foto') or contains(@text, 'username') or contains(@text, 'lewati') or contains(@text, 'skip')]")))
                    print(f"\n{GREEN}>> ✅ SUKSES! Lewati Foto...{RESET}")
                    try: driver.find_element(AppiumBy.XPATH, "//*[contains(@text, 'Lewati') or contains(@text, 'Skip') or contains(@text, 'Jangan')]").click()
                    except: pass
                    print(f"{RED}>> 🛑 TAHAN 8 DETIK: Tunggu Username Muncul...{RESET}")
                    time.sleep(8)
                    username_final = ""
                    try:
                        inputs = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
                        for inp in inputs:
                            txt = inp.text
                            if txt and len(txt) > 3:
                                username_final = txt
                                print(f"{GREEN}>> ✅ Username Terdeteksi: {username_final}{RESET}")
                                break
                    except: pass
                    simpan_akun_ke_txt(username_final, email)
                    print(f"{GREEN}>> ⚡ SELESAI! Langsung tutup aplikasi...{RESET}")
                    driver.terminate_app(ID_TWITTER)
                    counter += 1
                    fail_count = 0 
                except Exception as e:
                    print(f"{RED}❌ Error Finishing: {e}{RESET}")
                    refresh_ip_mode_pesawat(driver)
                    driver.terminate_app(ID_TWITTER)
                    fail_count += 1 
                    print(f"{RED}>> ⚠️ KEGAGALAN KE-{fail_count} DARI 3{RESET}")
            else:
                print(f"{RED}❌ Gagal OTP.{RESET}")
                refresh_ip_mode_pesawat(driver)
                driver.terminate_app(ID_TWITTER)      
                fail_count += 1 
                print(f"{RED}>> ⚠️ KEGAGALAN KE-{fail_count} DARI 3{RESET}")
            time.sleep(3)
        except Exception as e:
            print(f"{RED}⚠️ TERJADI CRASH/ERROR UTAMA: {e}{RESET}")
            if driver:
                refresh_ip_mode_pesawat(driver)
            fail_count += 1 
            print(f"{RED}>> ⚠️ KEGAGALAN KE-{fail_count} DARI 3{RESET}")
            time.sleep(5) 
        finally:
            if driver:
                print(f"{YELLOW}>> Menutup Sesi Driver...{RESET}")
                try: driver.quit()
                except: pass
            print(f"\n{YELLOW}>> 💤 Memulai ulang loop HP Fresh...{RESET}")
            time.sleep(5)

if __name__ == "__main__":
    main()
