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
init(autoreset=True)
BANNER_JUDUL = "AUTO  TWITTER"
BANNER_NAMA  = "Tools By : Ruff"
ID_TWITTER = "com.twitter.android"
ID_CHROME = "com.android.chrome"
URL_CITAYAM = "https://citayam.com/" 
PASSWORD_AKUN = "kontol87"
NAMA_FILE_HASIL = "data_akun1.txt"
BLACKLIST_OTP = ["2024", "2025", "2026", "2023", "123456", "000000"]
UDID_DEVICE = "cfe0fe2" 
DEVICE_NAME = 'Redmi Note 13 Pro'
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
    depan = ["Rudi", "Bayu", "Eko", "Dina", "Siti", "Reza", "Fajar", "Adit", "Gilang", "Putri", "Dewi", "Budi", "Sari", "Indra", "Maya", "saikul"]
    belakang = ["Santoso", "Pratama", "Wijaya", "Kusuma", "Saputra", "Hidayat", "Siregar", "Utami", "Nugroho", "Wibowo", "Subagja", "Ramadhan", "pebrianto"]
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
def buka_url_browser_utama(driver, url):
    pastikan_pindah_aplikasi(driver, ID_CHROME)
    print(f"\n{CYAN}[BROWSER] Mengakses: {url} (Mode User 0)...{RESET}")
    try:
        cmd = f'adb -s {UDID_DEVICE} shell am start --user 0 -a android.intent.action.VIEW -d "{url}" -n com.android.chrome/com.google.android.apps.chrome.Main'
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    except Exception as e:
        try: driver.get(url)
        except: return False
    time.sleep(5)
    return True
def lewati_welcome_chrome(driver):
    try:
        if driver.find_elements(AppiumBy.ID, "com.android.chrome:id/terms_accept_btn"):
            driver.find_element(AppiumBy.ID, "com.android.chrome:id/terms_accept_btn").click()
        if driver.find_elements(AppiumBy.ID, "com.android.chrome:id/negative_button"):
            driver.find_element(AppiumBy.ID, "com.android.chrome:id/negative_button").click()
    except: pass
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
def ambil_email_fresh(driver, wait):
    buka_url_browser_utama(driver, URL_CITAYAM)
    lewati_welcome_chrome(driver)
    time.sleep(3)
    email_lama = ""
    try:
        src = driver.page_source
        found = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', src)
        if found: email_lama = found[0]
    except: pass
    print(f"{YELLOW}>> 🧹 Menghapus email lama...{RESET}")
    try:
        driver.find_element(AppiumBy.XPATH, "//*[contains(@text, 'Hapus') or contains(@text, 'Delete')]").click()
        time.sleep(2)
    except: pass
    print(f"{YELLOW}>> ⏳ Menunggu generate email BARU...{RESET}")
    start_time = time.time()
    while time.time() - start_time < 30:
        try:
            src = driver.page_source
            found_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', src)
            if found_emails:
                email_kandidat = found_emails[0]
                if "motormio.com" in email_kandidat or "wedansmail.com" in email_kandidat:
                    driver.find_element(AppiumBy.XPATH, "//*[contains(@text, 'Hapus') or contains(@text, 'Delete')]").click()
                    time.sleep(5); continue
                if email_kandidat != email_lama:
                    print(f"{GREEN}>> ✅ EMAIL BARU DIDAPAT: {email_kandidat}{RESET}")
                    return email_kandidat
            try: driver.find_element(AppiumBy.XPATH, "//*[contains(@text, 'Segarkan')]").click()
            except: pass
        except: pass
        time.sleep(3)
    return None
def ambil_otp_fresh(driver, wait):
    print(f"\n{CYAN}>> 🚀 PINDAH KE CHROME UNTUK AMBIL OTP...{RESET}")
    buka_url_browser_utama(driver, URL_CITAYAM)
    time.sleep(5)
    start_time = time.time()
    print(f"{YELLOW}>> ⏳ Mencari Kode (Maks 45 detik)...{RESET}")
    try:
        driver.find_element(AppiumBy.XPATH, "//*[contains(@text, 'Segarkan')]").click(); time.sleep(3)
    except: pass
    while time.time() - start_time < 45:
        try:
            msgs = driver.find_elements(AppiumBy.XPATH, "//*[contains(@text, 'Twitter') or contains(@text, 'X') or contains(@text, 'verify')]")
            if msgs:
                print(f"{GREEN}>> 📩 Pesan ketemu! Klik...{RESET}")
                msgs[0].click(); time.sleep(5)
                try: visible_text = driver.find_element(AppiumBy.TAG_NAME, "body").text
                except: visible_text = driver.page_source
                otp_list = re.findall(r'\b\d{6}\b', visible_text)
                for o in otp_list:
                    if o not in BLACKLIST_OTP:
                        print(f"{GREEN}>> ✅ OTP DITEMUKAN: {o}{RESET}")
                        return o
            else:
                try: driver.find_element(AppiumBy.XPATH, "//*[contains(@text, 'Segarkan')]").click()
                except: pass
        except: pass
        time.sleep(3)
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
    sudah_login = False
    try:
        if driver.find_elements(AppiumBy.ACCESSIBILITY_ID, "Show navigation drawer"): sudah_login = True
        elif driver.find_elements(AppiumBy.XPATH, "//*[contains(@text, 'Untuk Anda') or contains(@text, 'For You')]"): sudah_login = True
        elif driver.find_elements(AppiumBy.XPATH, "//*[contains(@text, 'Mengikuti') or contains(@text, 'Following')]"): sudah_login = True
    except: pass
    if sudah_login:
        print(f"{YELLOW}>> [NAVIGASI] Status: SUDAH LOGIN. OTW Tambah Akun...{RESET}")
        try:
            print(f"{CYAN}>> Klik Profil...{RESET}")
            try: driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Show navigation drawer").click()
            except: 
                uk = driver.get_window_size()
                driver.tap([(int(uk['width']*0.09), int(uk['height']*0.09))])
            time.sleep(3)
            print(f"{CYAN}>> Klik Menu Switcher...{RESET}")
            try: driver.find_element(AppiumBy.ID, "com.twitter.android:id/user_switcher").click()
            except:
                uk = driver.get_window_size()
                driver.tap([(int(uk['width']*0.72), int(uk['height']*0.11))])
            time.sleep(3)
            print(f"{CYAN}>> Klik 'Buat akun baru'...{RESET}")
            try: driver.find_element(AppiumBy.XPATH, "//*[@text='Buat akun baru' or @text='Create a new account']").click()
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
    except Exception as e: print(f"{RED}⚠️ Gagal atur tanggal: {e}{RESET}")
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
    atur_tanggal_lahir_scroll_bawah(driver)
def main():
    print_banner()
    counter = 1
    while True:
        print(f"\n\n{CYAN}=== MEMBUAT AKUN KE - {counter} ==={RESET}")
        driver = None
        try:
            print(f"{YELLOW}>> 🔄 Memulai Driver Baru...{RESET}")
            driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
            wait = WebDriverWait(driver, 60)
            status_nav = buka_form_pendaftaran(driver, wait)
            if status_nav == "LIMIT":
                print(f"{RED}⚠️ LIMIT TERDETEKSI (AWAL) - MODPES & RESTART...{RESET}")
                refresh_ip_mode_pesawat(driver) 
                if driver: driver.quit()
                continue 
            if not status_nav: 
                print(f"{RED}❌ Navigasi gagal.{RESET}")
                refresh_ip_mode_pesawat(driver)
                if driver: driver.quit()
                continue
            email = ambil_email_fresh(driver, wait)
            if not email: 
                if driver: driver.quit()
                continue
            print(f"\n{CYAN}>> [TWITTER] Mengisi form...{RESET}")
            pastikan_pindah_aplikasi(driver, ID_TWITTER)
            isi_biodata_pintar(driver, wait, get_random_name(), email)
            time.sleep(2)
            tekan_tombol_lanjut_pendaftaran(driver, wait)
            if cek_limit_jumlah_akun_dan_uninstall(driver):
                print(f"{RED}⚠️ LIMIT/CLOUDFLARE TERDETEKSI (BIODATA) - MODPES & RESTART...{RESET}")
                refresh_ip_mode_pesawat(driver)
                if driver: driver.quit()
                continue
            time.sleep(2)
            tekan_tombol_lanjut_pendaftaran(driver, wait)
            if cek_limit_jumlah_akun_dan_uninstall(driver):
                refresh_ip_mode_pesawat(driver)
                if driver: driver.quit()
                continue
            print(f"{CYAN}>> Klik Daftar...{RESET}")
            time.sleep(2)
            tekan_tombol_lanjut_pendaftaran(driver, wait)
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
            print(f"{YELLOW}>> ⏳ Memberi waktu notifikasi masuk (8 detik)...{RESET}")
            time.sleep(8)
            otp = ambil_otp_fresh(driver, wait)
            if otp:
                print(f"\n{GREEN}>> [TWITTER] Menginput Kode: {otp}{RESET}")
                pastikan_pindah_aplikasi(driver, ID_TWITTER)
                time.sleep(4)
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
                except Exception as e:
                    print(f"{RED}❌ Error Finishing: {e}{RESET}")
                    refresh_ip_mode_pesawat(driver)
                    driver.terminate_app(ID_TWITTER)
            else:
                print(f"{RED}❌ Gagal OTP.{RESET}")
                refresh_ip_mode_pesawat(driver)
                driver.terminate_app(ID_TWITTER)      
            time.sleep(3)
        except Exception as e:
            print(f"{RED}⚠️ TERJADI CRASH/ERROR UTAMA: {e}{RESET}")
            if driver:
                refresh_ip_mode_pesawat(driver)
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