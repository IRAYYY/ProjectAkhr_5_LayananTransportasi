from datetime import datetime, timedelta

akun = {}
rute_pesawat = {}
pesanan = {}
id_terakhir = 0

# login loket dan admin
login_loket = ("loket123", "loket1234")
login_admin = ("admin123", "admin1234")

# Kode diskon
kode_diskon = {
    "DISKON10": 10,
    "DISKON20": 20
}

# ==============================
# ADMIN
# ==============================
def create_rute():
    print("\n===== TAMBAH RUTE =====")
    key_rute = input("Masukkan Nama Rute: ").upper()

    if key_rute in rute_pesawat:
        print("Nama rute sudah digunakan!\n")
        return

    rute = input("Masukkan Bandara Keberangkatan dan Tujuan: ")
    while True:
        harga = input("Masukkan harga tiket: ")
        if not harga.isdigit():
            print("Harga harus berupa angka!\n")
        else:
            harga = int(harga)
            break

    rute_pesawat[key_rute] = {"rute": rute, "harga": harga}
    print("Rute berhasil ditambahkan!\n")


def edit_rute():

    if not rute_pesawat:
        print("Belum ada rute untuk diedit.\n")
        return

    for key, data in rute_pesawat.items():
        print(f"Nama Rute: {key}")
        print(f"Keberangkatan: {data['rute']}")
        print(f"Harga: {data['harga']}")
        print("------------------------")

    key = input("Masukkan Nama rute: ").upper()

    if key not in rute_pesawat:
        print("Rute tidak ditemukan!\n")
        return

    print("Rute ditemukan! Silakan masukkan data baru.")
    rute_baru = input("Masukkan keberangkatan baru: ")
    while True:
        harga_baru = input("Masukkan harga baru: ")
        if not harga_baru.isdigit():
            print("Harga harus berupa angka!\n")
        else:
            harga_baru = int(harga_baru)
            break

    rute_pesawat[key]["rute"] = rute_baru
    rute_pesawat[key]["harga"] = harga_baru

    print("Data rute berhasil diperbarui!\n")


def tampil_rute():
    print("\n===== DAFTAR SEMUA RUTE =====")
    if not rute_pesawat:
        print("Belum ada data rute.\n")
        return

    for key, data in rute_pesawat.items():
        print(f"Nama Rute: {key}")
        print(f"Keberangkatan: {data['rute']}")
        print(f"Harga: {data['harga']}")
        print("------------------------")


def hapus_rute():
    if not rute_pesawat:
        print("Belum ada rute untuk dihapus.\n")
        return

    for key, data in rute_pesawat.items():
        print(f"Nama Rute: {key}")
        print(f"Keberangkatan: {data['rute']}")
        print(f"Harga: {data['harga']}")
        print("------------------------")

    key = input("Masukkan nama rute yang ingin dihapus: ").upper()

    if key not in rute_pesawat:
        print("Nama rute tidak ditemukan!\n")
        return

    del rute_pesawat[key]
    print("Rute berhasil dihapus!\n")


def menu_admin():
    while True:
        print("\n===== MENU ADMIN =====")
        print("1. Tambah Rute")
        print("2. Edit Rute")
        print("3. Tampilkan Semua Rute")
        print("4. Hapus Rute")
        print("5. Kembali")

        pilih = input("Pilih menu: ")

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
    nama = input("Masukkan nama lengkap: ")

    while True:
        email = input("Masukkan email: ").lower()
        if email in akun:
            print("Email sudah digunakan!")
        elif "@" not in email:
            print("Email harus mengandung @")
        else:
            break

    while True:
        password = input("Buat password: ")
        if len(password) < 8:
            print("Password harus minimal 8 karakter!")
        else:
            break

    while True:
        telepon = input("Masukkan nomor telepon: ")
        if not telepon.isdigit():
            print("Nomor telepon harus berupa angka!")
        else:
            break

    id_terakhir += 1
    akun[email] = {"id": id_terakhir, "nama": nama, "password": password, "telepon": telepon}

    print(f"Akun berhasil dibuat! ID Anda: {id_terakhir}")


def lupa_password(email):
    print("\n===== LUPA PASSWORD =====")
    no_input = input("Masukkan nomor telepon terkait akun: ")

    if no_input == akun[email]["telepon"]:
        pw_baru = input("Masukkan password baru: ")
        akun[email]["password"] = pw_baru
        print("Password berhasil direset! Silakan login ulang.\n")
    else:
        print("Nomor telepon salah!\n")


def login():
    print("\n===== LOGIN =====")
    email = input("Masukkan email: ").lower()

    if email not in akun:
        print("Akun tidak terdaftar!\n")
        return None

    percobaan = 0
    while percobaan < 3:
        pw = input("Masukkan password: ")

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
    print("\n===== RUTE TERSEDIA =====")
    if not rute_pesawat:
        print("Belum ada rute tersedia.\n")
        return

    for key, data in rute_pesawat.items():
        print("------------------------")
        print(f"Nama Rute: {key}")
        print(f"Rute  : {data['rute']}")
        print(f"Harga : {data['harga']}")
        print("------------------------")


def auto_delete_expired(id_user):
    if id_user not in pesanan:
        return

    now = datetime.now()
    to_delete = []

    for key_tiket, info in pesanan[id_user].items():
        expired_time = datetime.strptime(info["expired"], "%Y-%m-%d %H:%M:%S")
        if now >= expired_time:
            to_delete.append(key_tiket)

    for x in to_delete:
        del pesanan[id_user][x]


def pesan_tiket(id_user):
    if not rute_pesawat:
        print("Belum ada rute untuk dipesan.\n")
        return

    print("\n===== PESAN TIKET =====")

    for key, data in rute_pesawat.items():
        print(f"Kode Rute      : {key}")
        print(f"Rute           : {data['rute']}")
        print(f"Harga          : {data['harga']}")
        print("---------------------------")

    while True:
        key_rute = input("Masukkan KODE RUTE (atau 'b' untuk batal): ").upper()
        if key_rute == "B":
            print("Batal memesan.\n")
            return

        if key_rute not in rute_pesawat:
            print("Kode rute tidak ditemukan.\n")
        else:
            data_rute = rute_pesawat[key_rute]
            break

    while True:
        jml = input("Masukkan jumlah tiket: ")
        if not jml.isdigit():
            print("Jumlah tiket harus angka.")
        else:
            jml = int(jml)
            if jml < 1:
                print("Minimal pesan 1 tiket.")
            else:
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

    if input("Konfirmasi pesan? (y/n): ").lower() != "y":
        print("Pemesanan dibatalkan.\n")
        return

    expired = datetime.now() + timedelta(days=7)

    item = {
        "key": key_rute,
        "rute": data_rute["rute"],
        "harga": data_rute["harga"],
        "jumlah": jml,
        "total": total,
        "expired": expired.strftime("%Y-%m-%d %H:%M:%S")
    }

    if id_user not in pesanan:
        pesanan[id_user] = {}

    id_tiket = f"T{len(pesanan[id_user])}"
    pesanan[id_user][id_tiket] = item

    print(f"Tiket berhasil dipesan! ID Tiket Anda: {id_tiket}\n")


def tampil_tiket_user(id_user):
    print("\n===== TIKET SAYA =====")

    auto_delete_expired(id_user)

    data = pesanan.get(id_user, {})
    if not data:
        print("Anda belum memiliki tiket.\n")
        return

    for key_tiket, info in data.items():

        expired_time = datetime.strptime(info["expired"], "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        sisa = expired_time - now

        if sisa.total_seconds() <= 0:
            status = "KEDALUWARSA"
            sisa_waktu = "0 hari 0 jam 0 menit"
        else:
            status = "AKTIF"
            hari = sisa.days
            jam = sisa.seconds // 3600
            menit = (sisa.seconds % 3600) // 60
            sisa_waktu = f"{hari} hari, {jam} jam, {menit} menit"

        print(f"ID Tiket      : {key_tiket}")
        print(f"Kode Rute     : {info['key']}")
        print(f"Nama Rute     : {info['rute']}")
        print(f"Harga Satuan  : {info['harga']}")
        print(f"Jumlah Tiket  : {info['jumlah']}")
        print(f"Total Harga   : {info['total']}")
        print(f"Status        : {status}")
        print(f"Sisa Waktu    : {sisa_waktu}")
        print(f"Expired Pada  : {info['expired']}")
        print("---------------------------")


def batalkan_tiket(id_user):
    auto_delete_expired(id_user)

    if id_user not in pesanan or not pesanan[id_user]:
        print("Anda belum memiliki tiket.\n")
        return

    tampil_tiket_user(id_user)

    while True:
        pilih = input("Masukkan ID tiket yang ingin dibatalkan atau 'b': ").upper()

        if pilih == "B":
            print("Batal membatalkan.\n")
            return

        if pilih not in pesanan[id_user]:
            print("ID tiket tidak ditemukan.")
        else:
            del pesanan[id_user][pilih]
            print("Tiket berhasil dibatalkan!\n")
            return


def user_login(email):
    id_user = akun[email]["id"]

    while True:
        print("\n===== MENU USER =====")
        print("1. Tampilkan Rute")
        print("2. Pesan Tiket")
        print("3. Tiket Saya")
        print("4. Batalkan Tiket")
        print("5. Logout")

        pilih = input("Pilih menu: ")

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

        pilih = input("Pilih menu: ")

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
    username = input("Masukkan username loket: ")
    password = input("Masukkan password: ")

    if username == login_loket[0] and password == login_loket[1]:
        print("Login loket berhasil!\n")
        loket_menu()
    else:
        print("Login gagal!\n")


def login_admin_form():
    print("\n===== LOGIN ADMIN =====")
    username = input("Masukkan username admin: ")
    password = input("Masukkan password: ")

    if username == login_admin[0] and password == login_admin[1]:
        print("Login admin berhasil!\n")
        menu_admin()
    else:
        print("Login gagal!\n")


def loket_menu():
    while True:
        print("\n===== MENU LOKET =====")
        print("1. Gunakan Tiket")
        print("2. Logout")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            loket_proses_tiket()
        elif pilih == "2":
            print("Logout...\n")
            break
        else:
            print("Pilihan tidak valid!\n")


def loket_proses_tiket():
    print("\n===== PENGGUNAAN TIKET =====")

    id_tiket = input("Masukkan ID Tiket: ").upper()

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
        print("Tiket tidak ditemukan!")
        return

    print("\n===== DATA TIKET =====")
    for k, v in data_tiket.items():
        print(f"{k.capitalize()} : {v}")

    konfirmasi = input("Apakah data benar? (y/n): ").lower()
    if konfirmasi == "y":
        del pesanan[uid][id_tiket]
        print("\nTiket berhasil digunakan!\n")
    else:
        print("Pembatalan proses.\n")

# ==============================
# MAIN MENU
# ==============================
while True:
    print("\n====== APLIKASI TIKET PESAWAT ======")
    print("1. Admin")
    print("2. User")
    print("3. Loket")
    print("4. Keluar")

    pilih = input("Pilih menu: ")

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