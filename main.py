from datetime import datetime
import time

akun = {}
rute_pesawat = {}   
pesanan = {}        
id_terakhir = 0

# login loket dan admin, tuple bang
login_loket = ("loket123", "loket1234")
login_admin = ("admin123", "admin1234")

# Kode diskon
kode_diskon = {
    "DISKON10": 10,
    "DISKON20": 20
}

def input_nonempty(prompt):
    while True:
        val = input(prompt)
        if val.strip() == "":
            print("Input tidak boleh kosong!\n")
        else:
            return val.strip()

def input_optional(prompt):
    val = input(prompt)
    return val  # bisa kosong

def input_harga(prompt):
    while True:
        v = input(prompt)
        if v.strip() == "":
            print("Input tidak boleh kosong!\n")
            continue
        if not v.isdigit():
            print("Harga harus berupa angka!\n")
            continue
        return int(v)

def input_telepon(prompt):
    while True:
        v = input(prompt)
        if v.strip() == "":
            print("Input tidak boleh kosong!\n")
            continue
        if not v.isdigit():
            print("Nomor telepon harus berupa angka!\n")
            continue
        return v

def input_jadwal_not_past(prompt):
    while True:
        jadwal = input(prompt).strip()
        if jadwal == "":
            print("Jadwal tidak boleh kosong!\n")
            continue
        try:
            dt = datetime.strptime(jadwal, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Format jadwal tidak valid! Gunakan format YYYY-MM-DD HH:MM\n")
            continue

        if dt < datetime.now():
            print("Jadwal tidak boleh kurang dari waktu sekarang!\n")
            continue

        return jadwal

def bersihkan_rute_kadaluarsa():
    """Hapus rute & semua tiket terkait jika jadwal sudah lewat."""
    now = datetime.now()
    rute_to_delete = []
    for key, data in rute_pesawat.items():
        try:
            dt = datetime.strptime(data["jadwal"], "%Y-%m-%d %H:%M")
        except Exception:
            # jika format jadwal rusak, skip
            continue
        if dt < now:
            rute_to_delete.append(key)

    for key in rute_to_delete:
        del rute_pesawat[key]
        # Hapus semua pesanan yang punya key_rute = key
        for uid, tiket_dict in pesanan.items():
            to_remove = []
            for tiket_id, info in tiket_dict.items():
                if info.get("key") == key:
                    to_remove.append(tiket_id)
            for tid in to_remove:
                del tiket_dict[tid]
        print(f"Rute '{key}' dan semua pesanan terkait telah kadaluarsa dan dihapus.")

# ==============================
# ADMIN
# ==============================
def create_rute():
    print("\n===== TAMBAH RUTE =====")
    while True:
        key_rute = input_nonempty("Masukkan Nama Rute: ").upper()
        if key_rute in rute_pesawat:
            print("Nama rute sudah digunakan!\n")
            continue
        break

    rute = input_nonempty("Masukkan Bandara Keberangkatan dan Tujuan: ")

    harga = input_harga("Masukkan harga tiket: ")

    jadwal = input_jadwal_not_past("Masukkan jadwal keberangkatan (YYYY-MM-DD HH:MM): ")

    rute_pesawat[key_rute] = {
        "rute": rute,
        "harga": harga,
        "jadwal": jadwal
    }
    print("Rute berhasil ditambahkan!\n")

def edit_rute():
    if not rute_pesawat:
        print("Belum ada rute untuk diedit.\n")
        return

    print("\n===== EDIT RUTE =====")
    for key, data in rute_pesawat.items():
        print(f"Nama Rute: {key}")
        print(f"Keberangkatan: {data['rute']}")
        print(f"Harga: {data['harga']}")
        print(f"Jadwal: {data['jadwal']}")
        print("------------------------")

    key = input_nonempty("Masukkan Nama rute yang ingin diedit: ").upper()
    if key not in rute_pesawat:
        print("Rute tidak ditemukan!\n")
        return

    lama = rute_pesawat[key]
    print("Tekan ENTER jika tidak ingin mengubah data.")

    rute_baru = input_optional(f"Masukkan keberangkatan baru (kosongkan jika tidak diubah) [{lama['rute']}]: ").strip()
    if rute_baru == "":
        rute_baru = lama["rute"]

    # Harga
    while True:
        harga_baru_raw = input_optional(f"Masukkan harga baru (kosongkan jika tidak diubah) [{lama['harga']}]: ").strip()
        if harga_baru_raw == "":
            harga_baru = lama["harga"]
            break
        if not harga_baru_raw.isdigit():
            print("Harga harus berupa angka!\n")
            continue
        harga_baru = int(harga_baru_raw)
        break

    # Jadwal
    while True:
        jadwal_baru_raw = input_optional(f"Masukkan jadwal baru (YYYY-MM-DD HH:MM) (kosongkan jika tidak diubah) [{lama['jadwal']}]: ").strip()
        if jadwal_baru_raw == "":
            jadwal_baru = lama["jadwal"]
            break
        try:
            dt = datetime.strptime(jadwal_baru_raw, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Format jadwal tidak valid! Gunakan format YYYY-MM-DD HH:MM\n")
            continue
        if dt < datetime.now():
            print("Jadwal tidak boleh kurang dari waktu sekarang!\n")
            continue
        jadwal_baru = jadwal_baru_raw
        break

    rute_pesawat[key] = {
        "rute": rute_baru,
        "harga": harga_baru,
        "jadwal": jadwal_baru
    }
    print("Data rute berhasil diperbarui!\n")

def tampil_rute():
    bersihkan_rute_kadaluarsa()
    print("\n===== DAFTAR SEMUA RUTE =====")
    if not rute_pesawat:
        print("Belum ada data rute.\n")
        return
    for key, data in rute_pesawat.items():
        print(f"Kode Rute : {key}")
        print(f"Rute      : {data['rute']}")
        print(f"Harga     : {data['harga']}")
        print(f"Jadwal    : {data['jadwal']}")
        print("------------------------")

def hapus_rute():
    if not rute_pesawat:
        print("Belum ada rute untuk dihapus.\n")
        return
    for key, data in rute_pesawat.items():
        print(f"Kode Rute : {key} | Rute: {data['rute']} | Jadwal: {data['jadwal']}")
    key = input_nonempty("Masukkan nama rute yang ingin dihapus: ").upper()
    if key not in rute_pesawat:
        print("Nama rute tidak ditemukan!\n")
        return
    del rute_pesawat[key]
    # Hapus pesanan juga
    for uid, tiket_dict in pesanan.items():
        to_remove = []
        for tid, info in tiket_dict.items():
            if info.get("key") == key:
                to_remove.append(tid)
        for tid in to_remove:
            del tiket_dict[tid]
    print("Rute dan tiket terkait berhasil dihapus!\n")

def menu_admin():
    while True:
        bersihkan_rute_kadaluarsa()
        print("\n===== MENU ADMIN =====")
        print("1. Tambah Rute")
        print("2. Edit Rute")
        print("3. Tampilkan Semua Rute")
        print("4. Hapus Rute")
        print("5. Kembali")

        pilih = input_nonempty("Pilih menu: ")

        if pilih == "1":
            create_rute()
        elif pilih == "2":
            edit_rute()
        elif pilih == "3":
            tampil_rute()
        elif pilih == "4":
            hapus_rute()
        elif pilih == "5":
            break
        else:
            print("Pilihan tidak valid!\n")

# ==============================
# USER MANAGEMENT
# ==============================
def buat_akun():
    global id_terakhir
    print("\n===== BUAT AKUN =====")
    nama = input_nonempty("Masukkan nama lengkap: ")

    while True:
        email = input("Masukkan email: ").lower().strip()
        if email == "":
            print("Email tidak boleh kosong!\n")
            continue
        if email in akun:
            print("Email sudah digunakan!")
            continue
        if "@" not in email:
            print("Email harus mengandung @")
            continue
        break

    while True:
        password = input("Buat password: ")
        if password.strip() == "":
            print("Password tidak boleh kosong!\n")
            continue
        if len(password) < 8:
            print("Password harus minimal 8 karakter!\n")
            continue
        break

    telepon = input_telepon("Masukkan nomor telepon: ")

    id_terakhir += 1
    akun[email] = {"id": id_terakhir, "nama": nama, "password": password, "telepon": telepon}

    print(f"Akun berhasil dibuat! ID Anda: {id_terakhir}")

def lupa_password(email):
    print("\n===== LUPA PASSWORD =====")
    no_input = input_nonempty("Masukkan nomor telepon terkait akun: ")

    if no_input == akun[email]["telepon"]:
        while True:
            pw_baru = input("Masukkan password baru: ")
            if pw_baru.strip() == "":
                print("Password tidak boleh kosong!\n")
                continue
            if len(pw_baru) < 8:
                print("Password harus minimal 8 karakter!\n")
                continue
            break
        akun[email]["password"] = pw_baru
        print("Password berhasil direset! Silakan login ulang.\n")
    else:
        print("Nomor telepon salah!\n")

def login():
    print("\n===== LOGIN =====")
    email = input_nonempty("Masukkan email: ").lower()

    if email not in akun:
        print("Akun tidak terdaftar!\n")
        return None

    percobaan = 0
    while percobaan < 3:
        pw = input("Masukkan password: ")
        if pw.strip() == "":
            print("Password tidak boleh kosong!\n")
            continue

        if pw == akun[email]["password"]:
            print(f"\nSelamat datang, {akun[email]['nama']}!")
            print("Login berhasil!\n")
            return email
        else:
            percobaan += 1
            print("Password salah!")

            if percobaan < 3:
                pilihan = input("Ketik (y) untuk lupa password, selain (y) untuk mencoba lagi: ").lower()
                if pilihan == "y":
                    lupa_password(email)
                    return None

    print("\nPassword salah 3 kali! Akun dihapus.\n")
    del akun[email]
    return None

# ==============================
# USER: PEMESANAN
# ==============================
def tampil_rute_user():
    bersihkan_rute_kadaluarsa()
    print("\n===== RUTE TERSEDIA =====")
    if not rute_pesawat:
        print("Belum ada rute tersedia.\n")
        return
    for key, data in rute_pesawat.items():
        print("------------------------")
        print(f"Kode Rute : {key}")
        print(f"Rute      : {data['rute']}")
        print(f"Harga     : {data['harga']}")
        print(f"Jadwal    : {data['jadwal']}")
        print("------------------------")

def pesan_tiket(id_user):
    bersihkan_rute_kadaluarsa()
    if not rute_pesawat:
        print("Belum ada rute untuk dipesan.\n")
        return

    print("\n===== PESAN TIKET =====")
    for key, data in rute_pesawat.items():
        print(f"Kode Rute      : {key}")
        print(f"Rute           : {data['rute']}")
        print(f"Harga          : {data['harga']}")
        print(f"Jadwal         : {data['jadwal']}")
        print("---------------------------")

    while True:
        key_rute = input("Masukkan KODE RUTE (atau 'b' untuk batal): ").upper().strip()
        if key_rute == "":
            print("Kode rute tidak boleh kosong!\n")
            continue
        if key_rute == "B":
            print("Batal memesan.\n")
            return
        if key_rute not in rute_pesawat:
            print("Kode rute tidak ditemukan.\n")
            continue
        data_rute = rute_pesawat[key_rute]
        break

    while True:
        jml = input("Masukkan jumlah tiket: ").strip()
        if jml == "":
            print("Jumlah tiket tidak boleh kosong!\n")
            continue
        if not jml.isdigit():
            print("Jumlah tiket harus angka!\n")
            continue
        jml = int(jml)
        if jml < 1:
            print("Minimal pesan 1 tiket!\n")
            continue
        break

    total = data_rute["harga"] * jml
    print(f"Total harga sebelum diskon: {total}")

    # ======= FITUR DISKON =======
    diskon_input = input("Masukkan kode diskon (jika ada): ").upper()
    if diskon_input in kode_diskon:
        persen = kode_diskon[diskon_input]
        potongan = total * persen // 100
        total -= potongan
        print(f"Diskon {persen}% diterapkan! Potongan: {potongan}")
    else:
        print("Tidak ada diskon.")

    print(f"Total harga akhir: {total}")

    print(f"Total harga akhir: {total}")
    print("\n===== DETAIL PEMESANAN =====")
    print(f"Rute      : {data_rute['rute']}")
    print(f"Jadwal    : {data_rute['jadwal']}")
    print(f"Jumlah    : {jml}")
    print(f"Total     : {total}")
    print("-----------------------------")
    

    while True:
        konf = input("Konfirmasi pembelian? (y/n): ").lower().strip()
        if konf == "":
            print("Input konfirmasi tidak boleh kosong!\n")
            continue
        if konf not in ("y", "n"):
            print("Silakan masukkan 'y' atau 'n'.\n")
            continue
        break

    if konf != "y":
        print("Pemesanan dibatalkan.\n")
        return

    item = {
        "key": key_rute,
        "rute": data_rute["rute"],
        "harga": data_rute["harga"],
        "jadwal": data_rute["jadwal"],
        "jumlah": jml,
        "total": total
    }

    if id_user not in pesanan:
        pesanan[id_user] = {}

    id_tiket = f"T{len(pesanan[id_user])}"
    pesanan[id_user][id_tiket] = item

    print(f"Tiket berhasil dipesan! ID Tiket Anda: {id_tiket}\n")

def tampil_tiket_user(id_user):
    bersihkan_rute_kadaluarsa()
    print("\n===== TIKET SAYA =====")
    data = pesanan.get(id_user, {})
    if not data:
        print("Anda belum memiliki tiket.\n")
        return
    for key_tiket, info in data.items():
        print(f"ID Tiket      : {key_tiket}")
        print(f"Kode Rute     : {info['key']}")
        print(f"Nama Rute     : {info['rute']}")
        print(f"Harga Satuan  : {info['harga']}")
        print(f"Jumlah Tiket  : {info['jumlah']}")
        print(f"Total Harga   : {info['total']}")
        print(f"Jadwal        : {info['jadwal']}")
        print("---------------------------")

def batalkan_tiket(id_user):
    bersihkan_rute_kadaluarsa()
    if id_user not in pesanan or not pesanan[id_user]:
        print("Anda belum memiliki tiket.\n")
        return

    tampil_tiket_user(id_user)

    while True:
        pilih = input("Masukkan ID tiket yang ingin dibatalkan atau 'b': ").upper().strip()
        if pilih == "":
            print("Input tidak boleh kosong!\n")
            continue
        if pilih == "B":
            print("Batal membatalkan.\n")
            return
        if pilih not in pesanan[id_user]:
            print("ID tiket tidak ditemukan!\n")
            continue
        del pesanan[id_user][pilih]
        print("Tiket berhasil dibatalkan!\n")
        return

def user_login(email):
    id_user = akun[email]["id"]
    while True:
        bersihkan_rute_kadaluarsa()
        print("\n===== MENU USER =====")
        print("1. Tampilkan Rute")
        print("2. Pesan Tiket")
        print("3. Tiket Saya")
        print("4. Batalkan Tiket")
        print("5. Logout")

        pilih = input_nonempty("Pilih menu: ")

        if pilih == "1":
            tampil_rute_user()
        elif pilih == "2":
            pesan_tiket(id_user)
        elif pilih == "3":
            tampil_tiket_user(id_user)
        elif pilih == "4":
            batalkan_tiket(id_user)
        elif pilih == "5":
            print("Logout...\n")
            break
        else:
            print("Pilihan tidak valid!\n")

def menu_user():
    while True:
        print("\n====== MENU USER ======")
        print("1. Login")
        print("2. Buat Akun")
        print("3. Kembali")

        pilih = input_nonempty("Pilih menu: ")

        if pilih == "1":
            email = login()
            if email:
                user_login(email)
        elif pilih == "2":
            buat_akun()
        elif pilih == "3":
            break
        else:
            print("Pilihan tidak valid!\n")

# ==============================
# LOKET
# ==============================
def login_loket_form():
    print("\n===== LOGIN LOKET =====")
    username = input_nonempty("Masukkan username loket: ")
    password = input_nonempty("Masukkan password: ")

    if username == login_loket[0] and password == login_loket[1]:
        print("Login loket berhasil!\n")
        loket_menu()
    else:
        print("Login gagal!\n")

def login_admin_form():
    print("\n===== LOGIN ADMIN =====")
    username = input_nonempty("Masukkan username admin: ")
    password = input_nonempty("Masukkan password: ")

    if username == login_admin[0] and password == login_admin[1]:
        print("Login admin berhasil!\n")
        menu_admin()
    else:
        print("Login gagal!\n")

def loket_menu():
    while True:
        bersihkan_rute_kadaluarsa()
        print("\n===== MENU LOKET =====")
        print("1. Gunakan Tiket")
        print("2. Logout")

        pilih = input_nonempty("Pilih menu: ")
        if pilih == "1":
            loket_proses_tiket()
        elif pilih == "2":
            print("Logout...\n")
            break
        else:
            print("Pilihan tidak valid!\n")

def loket_proses_tiket():
    print("\n===== PENGGUNAAN TIKET =====")
    id_tiket = input_nonempty("Masukkan ID Tiket: ").upper()

    ditemukan = False
    uid = None
    data_tiket = None

    for user_id, tiket_list in pesanan.items():
        if id_tiket in tiket_list:
            ditemukan = True
            uid = user_id
            data_tiket = tiket_list[id_tiket]
            break

    if not ditemukan:
        print("Tiket tidak ditemukan!\n")
        return

    print("\n===== DATA TIKET =====")
    for k, v in data_tiket.items():
        print(f"{k.capitalize()} : {v}")

    konfirmasi = input_nonempty("Apakah data benar? (y/n): ").lower()
    if konfirmasi == "y":
        del pesanan[uid][id_tiket]
        print("\nTiket berhasil digunakan!\n")
    else:
        print("Pembatalan proses.\n")

# ==============================
# MAIN MENU
# ==============================
while True:
    bersihkan_rute_kadaluarsa()
    print("\n====== APLIKASI TIKET PESAWAT ======")
    print("1. Admin")
    print("2. User")
    print("3. Loket")
    print("4. Keluar")

    pilih = input_nonempty("Pilih menu: ")

    if pilih == "1":
        login_admin_form()
    elif pilih == "2":
        menu_user()
    elif pilih == "3":
        login_loket_form()
    elif pilih == "4":
        print("Keluar dari program...")
        break
    else:
        print("Pilihan tidak valid!\n")
